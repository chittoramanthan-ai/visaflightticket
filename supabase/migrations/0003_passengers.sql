-- =============================================================================
-- Every traveller on an order, not just the lead.
-- [{ "surname": "...", "given_name": "...", "dob": "YYYY-MM-DD" }, ...]
-- The lead is element 0 and is also kept in the flat surname/given_name/email
-- columns, so existing queries and the notification email keep working.
-- Safe to run more than once.
-- =============================================================================

alter table public.orders add column if not exists passengers jsonb not null default '[]'::jsonb;

comment on column public.orders.passengers is
  'All travellers in order, lead first. travellers column is the authoritative
   count and is derived from this array server-side, never from the browser.';

-- Count and array must not disagree, or the price would not match the document
-- count. Existing rows predate the column, so only enforce where it is filled.
alter table public.orders drop constraint if exists orders_pax_count_matches;
alter table public.orders add constraint orders_pax_count_matches
  check (jsonb_array_length(passengers) = 0 or jsonb_array_length(passengers) = travellers);
