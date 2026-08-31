-- =============================================================================
-- RUN THIS ONE FILE. Nothing else.
--
-- Paste the whole thing into the Supabase SQL editor and press Run:
--   https://supabase.com/dashboard/project/jijnknqfampnmhyakxzz/sql/new
--
-- It is 0002_upi.sql and 0003_passengers.sql back to back. Every statement is
-- idempotent, so running it twice does nothing the second time. It does not
-- drop anything and it does not touch existing rows.
--
-- WHY IT IS URGENT: create-order inserts a `passengers` column that only
-- exists after this runs. Until then EVERY order fails with an unknown-column
-- error, the customer sees a generic failure, and no row is written.
--
-- Verify it worked with the SELECT at the bottom.
-- =============================================================================


-- ---------------------------------------------------------------- 0002 UPI --
-- A status for "customer says they paid, we have not checked yet". This value
-- has to be committed before anything can reference it, hence its own block.
do $$ begin
  alter type order_status add value if not exists 'awaiting_verification' before 'paid';
exception when others then null; end $$;

alter table public.orders add column if not exists utr text;
alter table public.orders add column if not exists utr_submitted_at timestamptz;
alter table public.orders add column if not exists verified_at timestamptz;
alter table public.orders add column if not exists verified_by text;

-- One UPI reference can only ever belong to one order. Stops the same payment
-- screenshot being replayed against a second order.
create unique index if not exists orders_utr_unique
  on public.orders (utr) where utr is not null;

comment on column public.orders.utr is
  'UPI transaction reference quoted by the customer. UNVERIFIED until you have
   matched it against your own bank statement. Never fulfil on this alone.';


-- --------------------------------------------------------- 0003 passengers --
-- Every traveller on an order, not just the lead:
--   [{ "surname": "...", "given_name": "...", "dob": "YYYY-MM-DD" }, ...]
-- The lead stays duplicated in the flat surname/given_name columns so the
-- notification email and any existing query keep working untouched.
alter table public.orders add column if not exists passengers jsonb not null default '[]'::jsonb;

comment on column public.orders.passengers is
  'All travellers in order, lead first. travellers column is the authoritative
   count and is derived from this array server-side, never from the browser.';

-- Count and array must not disagree, or the price would not match the number
-- of documents owed. Rows written before this column existed have an empty
-- array, so the check only bites once the array is actually populated.
alter table public.orders drop constraint if exists orders_pax_count_matches;
alter table public.orders add constraint orders_pax_count_matches
  check (jsonb_array_length(passengers) = 0 or jsonb_array_length(passengers) = travellers);


-- ------------------------------------------------------------------ verify --
-- Expect 5 rows: passengers, utr, utr_submitted_at, verified_at, verified_by.
-- Fewer than 5 means something above did not apply.
select column_name, data_type
from information_schema.columns
where table_schema = 'public'
  and table_name = 'orders'
  and column_name in ('passengers', 'utr', 'utr_submitted_at', 'verified_at', 'verified_by')
order by column_name;
