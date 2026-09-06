-- =============================================================================
-- Document the passport fields now carried in orders.passengers.
--
-- No schema change: passengers is jsonb, so the wider object shape needs no
-- migration. This exists so the column documents what it actually holds, which
-- now includes passport numbers - the reason the comment calls the sensitivity
-- out rather than just listing the keys.
--
-- Shape as of this migration:
--   [{ "title": "Mr", "surname": "...", "given_name": "...",
--      "dob": "YYYY-MM-DD",
--      "passport": "...", "passport_issue": "YYYY-MM-DD",
--      "passport_expiry": "YYYY-MM-DD" }, ...]
--
-- Safe to run more than once.
-- =============================================================================

comment on column public.orders.passengers is
  'All travellers in order, lead first. Keys: title, surname, given_name, dob,
   passport, passport_issue, passport_expiry. The travellers column is the
   authoritative count and is derived from this array server-side, never from
   the browser.
   Contains passport numbers: treat as sensitive. Reachable only through the
   service role, since RLS grants the anon key no policy on this table.';
