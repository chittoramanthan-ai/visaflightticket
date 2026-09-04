#!/usr/bin/env bash
# =============================================================================
# Take the payment path live. Run from the repo root:  bash supabase/deploy.sh
#
# Order matters. The SQL has to be applied FIRST: create-order inserts a
# `passengers` column that does not exist until then, so a function deployed
# ahead of the migration fails on every request.
#
# Nothing here is destructive. Re-running it just redeploys the same code.
# =============================================================================
set -euo pipefail

PROJECT_REF="jijnknqfampnmhyakxzz"   # must match SUPABASE_URL in src/build.py

say() { printf '\n\033[1;34m==> %s\033[0m\n' "$1"; }

# --- 0. sanity ---------------------------------------------------------------
command -v supabase >/dev/null || {
  echo "supabase CLI not found. https://supabase.com/docs/guides/cli"; exit 1; }

say "Checking which account the CLI is logged into"
if ! supabase projects list 2>/dev/null | grep -q "$PROJECT_REF"; then
  cat <<EOF

  STOP. The logged-in account cannot see project $PROJECT_REF.

  That is the project src/build.py points the website at, so deploying now
  would push this code to the WRONG database. Fix one of these first:

    - wrong account:  supabase logout && supabase login
    - wrong project:  update SUPABASE_URL / SUPABASE_ANON_KEY in src/build.py
                      to whichever project you actually mean to use

EOF
  exit 1
fi

say "Linking to $PROJECT_REF"
supabase link --project-ref "$PROJECT_REF"

# --- 1. schema ---------------------------------------------------------------
say "STEP 1 of 3: apply the schema"
cat <<EOF
  Open the SQL editor and run supabase/migrations/APPLY_ME.sql in full:
    https://supabase.com/dashboard/project/$PROJECT_REF/sql/new

  It should return 5 rows. Press Enter once it has.
EOF
read -r _

# --- 2. secrets --------------------------------------------------------------
say "STEP 2 of 3: set the secrets"
cat <<'EOF'
  Fill in your own values and run. Anything you leave out degrades gracefully:
  no Razorpay keys falls back to UPI, no Resend key means no notification email,
  but neither breaks order creation.

  supabase secrets set \
    ALLOWED_ORIGINS="https://visaflighttickets.com,https://www.visaflighttickets.com" \
    IP_SALT="$(openssl rand -hex 16)" \
    NOTIFY_EMAIL="you@yourdomain.com" \
    NOTIFY_FROM="support@visaflighttickets.com" \
    PAYMENT_MODE="upi" \
    UPI_VPA="yourvpa@bank" \
    UPI_PAYEE_NAME="Visa Flight Tickets" \
    RESEND_API_KEY="re_..." \
    RAZORPAY_KEY_ID="rzp_live_..." \
    RAZORPAY_KEY_SECRET="..." \
    RAZORPAY_WEBHOOK_SECRET="..."

  SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are injected automatically.
  Do NOT set them by hand.

  PAYMENT_MODE: "upi" costs you nothing per transaction but you reconcile by
  hand. "razorpay" is automatic and costs ~2%. "auto" picks UPI when no
  Razorpay key is present.

  Press Enter when the secrets are set.
EOF
read -r _

# --- 3. functions ------------------------------------------------------------
say "STEP 3 of 3: deploy the functions"
supabase functions deploy create-order
supabase functions deploy confirm-upi

# The webhook is called by Razorpay, which has no Supabase JWT to present. It
# authenticates itself with an HMAC signature instead, checked inside the
# function, so JWT verification has to be off or every callback 401s.
supabase functions deploy razorpay-webhook --no-verify-jwt

say "Deployed"
cat <<EOF

  If you are using Razorpay, point its webhook at:
    https://$PROJECT_REF.supabase.co/functions/v1/razorpay-webhook
  subscribe to payment.captured, and set the signing secret to the same value
  you gave RAZORPAY_WEBHOOK_SECRET above.

  Then place one real order and confirm a row appears in the orders table.
  A test that does not end in a row in the table is not a test.

EOF
