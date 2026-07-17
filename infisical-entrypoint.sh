#!/bin/sh
# Avvio produzione: inietta secret da Infisical (path /), poi entrypoint Django.
# Password email: KESI_FUNNEL_GRANDINETICINO_EMAIL_PASSWORD → EMAIL_HOST_PASSWORD.
# Se l'identity manca, usa le variabili già presenti (es. .env) e prosegue.
set -e

EMAIL_IDENTITY="${EMAIL_IDENTITY:-info@kesi.biz}"
export EMAIL_HOST="${EMAIL_HOST:-mail.infomaniak.com}"
export EMAIL_PORT="${EMAIL_PORT:-587}"
export EMAIL_USE_TLS="${EMAIL_USE_TLS:-True}"
export EMAIL_HOST_USER="${EMAIL_HOST_USER:-$EMAIL_IDENTITY}"
export DEFAULT_FROM_EMAIL="${DEFAULT_FROM_EMAIL:-$EMAIL_IDENTITY}"
export LEAD_RECIPIENT_EMAIL="${LEAD_RECIPIENT_EMAIL:-$EMAIL_IDENTITY}"
export FUNNEL_RECIPIENT_EMAIL="${FUNNEL_RECIPIENT_EMAIL:-$EMAIL_IDENTITY}"

map_email_password() {
  if [ -z "${EMAIL_HOST_PASSWORD:-}" ] \
    && [ -n "${KESI_FUNNEL_GRANDINETICINO_EMAIL_PASSWORD:-}" ]; then
    export EMAIL_HOST_PASSWORD="$KESI_FUNNEL_GRANDINETICINO_EMAIL_PASSWORD"
  fi
}

run_app() {
  map_email_password
  if [ -z "${EMAIL_HOST_PASSWORD:-}" ]; then
    echo "funnel: WARNING — EMAIL_HOST_PASSWORD assente (né env né Infisical)" >&2
  else
    echo "funnel: SMTP ${EMAIL_HOST_USER} @ ${EMAIL_HOST}:${EMAIL_PORT} (password OK, len=${#EMAIL_HOST_PASSWORD})"
  fi
  exec /app/entrypoint.sh
}

if [ -z "${INFISICAL_MACHINE_CLIENT_ID:-}" ] \
  || [ -z "${INFISICAL_MACHINE_CLIENT_SECRET:-}" ] \
  || [ -z "${INFISICAL_PROJECT_ID:-}" ]; then
  echo "funnel: Infisical identity assente — avvio con env locale (.env)" >&2
  run_app
fi

if ! command -v infisical >/dev/null 2>&1; then
  echo "funnel: CLI Infisical assente nell'immagine — avvio con env locale" >&2
  run_app
fi

API_URL="${INFISICAL_API_URL:-https://agents-infisical.srv1663152.hstgr.cloud}"
SECRET_ENV="${INFISICAL_SECRET_ENV:-prod}"
# Secret del funnel stanno in path root del progetto Peter-Agents
SECRET_PATH="${INFISICAL_SECRET_PATH:-/}"

echo "funnel: login Infisical (${API_URL}, env=${SECRET_ENV}, path=${SECRET_PATH})"
LOGIN_OUT=$(infisical login \
  --method=universal-auth \
  --client-id="${INFISICAL_MACHINE_CLIENT_ID}" \
  --client-secret="${INFISICAL_MACHINE_CLIENT_SECRET}" \
  --domain="${API_URL}" \
  --plain --silent 2>&1) || {
  echo "funnel: login Infisical fallito — fallback env locale" >&2
  echo "$LOGIN_OUT" | sed 's/eyJ[^ ]*/[jwt]/g' >&2
  run_app
}

INFISICAL_TOKEN=$(printf '%s\n' "$LOGIN_OUT" | grep -o 'eyJ[^ ]*' | head -1)
if [ -z "$INFISICAL_TOKEN" ]; then
  # --plain may print only the token
  INFISICAL_TOKEN=$(printf '%s' "$LOGIN_OUT" | tr -d '\r\n' | grep -o 'eyJ[^ ]*' | head -1)
fi
if [ -z "$INFISICAL_TOKEN" ] && [ -n "$LOGIN_OUT" ]; then
  # last line often is the token when --plain
  INFISICAL_TOKEN=$(printf '%s\n' "$LOGIN_OUT" | tail -1 | tr -d '\r\n')
fi

if [ -z "$INFISICAL_TOKEN" ]; then
  echo "funnel: token Infisical vuoto — fallback env locale" >&2
  run_app
fi

export INFISICAL_TOKEN
echo "funnel: inject secrets da Infisical e avvio app"
exec infisical run \
  --token="${INFISICAL_TOKEN}" \
  --domain="${API_URL}" \
  --env="${SECRET_ENV}" \
  --path="${SECRET_PATH}" \
  --projectId="${INFISICAL_PROJECT_ID}" \
  -- /bin/sh -c '
    if [ -z "${EMAIL_HOST_PASSWORD:-}" ] \
      && [ -n "${KESI_FUNNEL_GRANDINETICINO_EMAIL_PASSWORD:-}" ]; then
      export EMAIL_HOST_PASSWORD="$KESI_FUNNEL_GRANDINETICINO_EMAIL_PASSWORD"
    fi
    EMAIL_IDENTITY="${EMAIL_IDENTITY:-info@kesi.biz}"
    export EMAIL_HOST_USER="${EMAIL_HOST_USER:-$EMAIL_IDENTITY}"
    export DEFAULT_FROM_EMAIL="${DEFAULT_FROM_EMAIL:-$EMAIL_IDENTITY}"
    export LEAD_RECIPIENT_EMAIL="${LEAD_RECIPIENT_EMAIL:-$EMAIL_IDENTITY}"
    export FUNNEL_RECIPIENT_EMAIL="${FUNNEL_RECIPIENT_EMAIL:-$EMAIL_IDENTITY}"
    if [ -n "${EMAIL_HOST_PASSWORD:-}" ]; then
      echo "funnel: SMTP ${EMAIL_HOST_USER} password from Infisical (len=${#EMAIL_HOST_PASSWORD})"
    else
      echo "funnel: WARNING — password email non trovata in Infisical" >&2
    fi
    exec /app/entrypoint.sh
  '
