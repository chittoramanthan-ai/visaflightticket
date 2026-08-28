-- =============================================================================
-- Visa Flight Ticket - orders schema
-- Apply with:  supabase db push      (or paste into the SQL editor)
-- =============================================================================

create extension if not exists pgcrypto;

-- Human-facing order reference: VFT-000001, VFT-000002, ...
-- A sequence rather than a random id so you can read it out over the phone and
-- so the customer can quote it back to you without spelling a UUID.
create sequence if not exists order_ref_seq start 1000;

create type order_status as enum ('pending', 'paid', 'processing', 'delivered', 'refunded', 'failed');
create type service_kind as enum ('flight', 'hotel', 'both');
create type trip_kind    as enum ('oneway', 'round', 'multi');

create table if not exists public.orders (
  id                uuid primary key default gen_random_uuid(),
  ref               text unique not null default 'VFT-' || lpad(nextval('order_ref_seq')::text, 6, '0'),
  created_at        timestamptz not null default now(),
  updated_at        timestamptz not null default now(),

  -- what was ordered
  service           service_kind not null,
  trip              trip_kind    not null default 'oneway',
  travellers        smallint     not null default 1 check (travellers between 1 and 12),
  priority          boolean      not null default false,

  -- itinerary
  origin            text,
  destination       text,
  depart_date       date,
  return_date       date,
  legs              jsonb        not null default '[]'::jsonb,   -- multi-city extra legs
  visa_type         text,

  -- traveller / contact
  surname           text not null,
  given_name        text not null,
  dob               date,
  email             text not null,
  phone             text,
  notes             text,

  -- money. Amount is written by the server from its own price table; the
  -- browser never gets a say in what the customer is charged.
  currency          text        not null default 'INR',
  amount_minor      integer     not null check (amount_minor > 0),  -- paise
  status            order_status not null default 'pending',

  -- payment provider
  provider          text,
  provider_order_id text,
  provider_payment_id text,
  paid_at           timestamptz,

  -- fulfilment
  pnr               text,
  document_url      text,
  delivered_at      timestamptz,

  -- light abuse forensics
  user_agent        text,
  ip_hash           text
);

create index if not exists orders_created_idx  on public.orders (created_at desc);
create index if not exists orders_status_idx   on public.orders (status);
create index if not exists orders_email_idx    on public.orders (lower(email));
create index if not exists orders_provider_idx on public.orders (provider_order_id);

create or replace function public.touch_updated_at()
returns trigger language plpgsql as $$
begin
  new.updated_at = now();
  return new;
end $$;

drop trigger if exists orders_touch on public.orders;
create trigger orders_touch before update on public.orders
  for each row execute function public.touch_updated_at();

-- =============================================================================
-- Row Level Security
--
-- RLS is ON with no policies for anon or authenticated. That is deliberate:
-- nothing in the browser can read or write this table, not even to insert.
-- All writes go through Edge Functions using the service-role key, which
-- bypasses RLS and is never shipped to the client.
--
-- The alternative -- letting the browser insert directly with the anon key --
-- means anyone can POST an order with amount_minor = 100 and pay one rupee.
-- =============================================================================
alter table public.orders enable row level security;
revoke all on public.orders from anon, authenticated;

-- =============================================================================
-- Status lookup for the /login/ page.
-- Returns one row, only to someone who already knows BOTH the reference and
-- the email on the order. Exposes only fields safe to show, never the amount
-- or the provider ids.
-- =============================================================================
create or replace function public.order_status_lookup(p_ref text, p_email text)
returns table (ref text, status order_status, service service_kind,
               created_at timestamptz, delivered_at timestamptz)
language sql
security definer
set search_path = public
as $$
  select o.ref, o.status, o.service, o.created_at, o.delivered_at
  from public.orders o
  where upper(trim(o.ref)) = upper(trim(p_ref))
    and lower(trim(o.email)) = lower(trim(p_email))
  limit 1;
$$;

revoke all on function public.order_status_lookup(text, text) from public;
grant execute on function public.order_status_lookup(text, text) to anon;
