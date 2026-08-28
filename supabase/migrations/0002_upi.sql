-- =============================================================================
-- Direct UPI payment support
--
-- Adds a status for "customer says they paid, you have not checked yet" and a
-- place to keep the UPI reference they quote. Safe to run more than once.
-- =============================================================================

do $$ begin
  alter type order_status add value if not exists 'awaiting_verification' before 'paid';
exception when others then null; end $$;

alter table public.orders add column if not exists utr text;
alter table public.orders add column if not exists utr_submitted_at timestamptz;
alter table public.orders add column if not exists verified_at timestamptz;
alter table public.orders add column if not exists verified_by text;

-- One UPI reference can only ever belong to one order. Stops the same
-- screenshot being replayed against a second order.
create unique index if not exists orders_utr_unique
  on public.orders (utr) where utr is not null;

comment on column public.orders.utr is
  'UPI transaction reference quoted by the customer. UNVERIFIED until you have
   matched it against your own bank statement. Never fulfil on this alone.';
