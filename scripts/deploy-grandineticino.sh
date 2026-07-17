#!/usr/bin/env bash
# Deploy funnel Grandineticino.ch su VPS Hostinger.
# Container e volume SEPARATI da kesi-site — non modifica il Docker KESI 2026.
#
# Uso (sul VPS):
#   ./scripts/deploy-grandineticino.sh
#
# Email (regola fissa):
#   - mittente/SMTP user/destinatari = sempre info@kesi.biz
#   - password = SEMPRE da Infisical KESI_FUNNEL_GRANDINETICINO_EMAIL_PASSWORD
#     (a ogni deploy; non resta bloccata su un valore vecchio in .env)
#   - a runtime il container re-inietta da Infisical via infisical-entrypoint.sh

set -euo pipefail

DEPLOY_DIR="${DEPLOY_DIR:-/docker/funnel-grandineticino}"
REPO_URL="${REPO_URL:-https://github.com/PeterCatania721/funnel-grandineticino.git}"
BRANCH="${BRANCH:-main}"
COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.yaml}"
ENV_FILE="${ENV_FILE:-.env}"
IDENTITY_FILE="${IDENTITY_FILE:-.env.identity}"
EMAIL_IDENTITY="${EMAIL_IDENTITY:-info@kesi.biz}"
INFISICAL_EMAIL_KEY="${INFISICAL_EMAIL_KEY:-KESI_FUNNEL_GRANDINETICINO_EMAIL_PASSWORD}"
# Default: SEMPRE riscrivi password da Infisical (solo se FORCE_EMAIL_PASSWORD=0 si salta)
FORCE_EMAIL_PASSWORD="${FORCE_EMAIL_PASSWORD:-1}"

log() { echo "==> $*"; }
die() { echo "ERRORE: $*" >&2; exit 1; }

if docker ps -a --format '{{.Names}}' 2>/dev/null | grep -qx 'kesi-site'; then
  log "Container kesi-site rilevato — non verrà fermato né ricreato."
fi

for forbidden in "docker stop kesi-site" "docker rm kesi-site" "docker restart kesi-site"; do
  if [[ "${*:-}" == *"$forbidden"* ]]; then
    die "Comando non consentito su kesi-site."
  fi
done

if [[ ! -d "$DEPLOY_DIR" ]]; then
  log "Creo $DEPLOY_DIR"
  mkdir -p "$DEPLOY_DIR"
fi

cd "$DEPLOY_DIR"

# Preserve secrets across git update
preserve_secret_files() {
  local f
  for f in "$ENV_FILE" "$IDENTITY_FILE" config.env; do
    if [[ -f "$f" ]]; then
      cp -a "$f" "/tmp/funnel-preserve-${f//\//_}.$$"
    fi
  done
}
restore_secret_files() {
  local f src
  for f in "$ENV_FILE" "$IDENTITY_FILE" config.env; do
    src="/tmp/funnel-preserve-${f//\//_}.$$"
    if [[ -f "$src" ]]; then
      # config.env: prefer repo version if present (non-secret), but keep identity/.env
      if [[ "$f" == "config.env" && -f config.env ]]; then
        rm -f "$src"
        continue
      fi
      cp -a "$src" "$f"
      rm -f "$src"
      chmod 600 "$f" 2>/dev/null || true
    fi
  done
}

preserve_secret_files

if [[ ! -d .git ]]; then
  log "Clone repository…"
  git clone --branch "$BRANCH" "$REPO_URL" .
else
  log "Aggiorno repository (branch $BRANCH)…"
  git fetch origin "$BRANCH"
  # Discard local tracked drift (compose/Dockerfile) — secrets are outside git
  git checkout "$BRANCH"
  git reset --hard "origin/$BRANCH"
fi

restore_secret_files

if [[ ! -f "$ENV_FILE" ]]; then
  if [[ -f .env.production.example ]]; then
    cp .env.production.example "$ENV_FILE"
    chmod 600 "$ENV_FILE"
    log "Creato $ENV_FILE da example — SECRET_KEY verrà generato se placeholder."
  else
    die "Manca $ENV_FILE."
  fi
fi

# SECRET_KEY se ancora placeholder
if grep -q 'GENERA-CON-python' "$ENV_FILE" 2>/dev/null || ! grep -q '^SECRET_KEY=.\+' "$ENV_FILE" 2>/dev/null; then
  sk=$(python3 -c 'import secrets; print(secrets.token_urlsafe(50))')
  if grep -q '^SECRET_KEY=' "$ENV_FILE"; then
    sed -i "s|^SECRET_KEY=.*|SECRET_KEY=${sk}|" "$ENV_FILE"
  else
    echo "SECRET_KEY=${sk}" >> "$ENV_FILE"
  fi
  log "SECRET_KEY generata."
  unset sk
fi

set_env_kv() {
  local key="$1" val="$2" file="${3:-$ENV_FILE}"
  python3 - "$file" "$key" "$val" <<'PY'
import sys
from pathlib import Path
path, key, val = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
lines = path.read_text().splitlines() if path.exists() else []
out, found = [], False
for line in lines:
    if line.startswith(key + "="):
        out.append(f"{key}={val}")
        found = True
    else:
        out.append(line)
if not found:
    out.append(f"{key}={val}")
path.write_text("\n".join(out) + "\n")
PY
}

# Sempre identity email fissa
for f in "$ENV_FILE" config.env; do
  [[ -f "$f" ]] || continue
  set_env_kv EMAIL_HOST mail.infomaniak.com "$f"
  set_env_kv EMAIL_PORT 587 "$f"
  set_env_kv EMAIL_USE_TLS True "$f"
  set_env_kv EMAIL_HOST_USER "$EMAIL_IDENTITY" "$f"
  set_env_kv DEFAULT_FROM_EMAIL "$EMAIL_IDENTITY" "$f"
  set_env_kv LEAD_RECIPIENT_EMAIL "$EMAIL_IDENTITY" "$f"
  set_env_kv FUNNEL_RECIPIENT_EMAIL "$EMAIL_IDENTITY" "$f"
done
# config.env: path Infisical root (dove sta la password)
if [[ -f config.env ]]; then
  set_env_kv INFISICAL_SECRET_PATH / config.env
  set_env_kv INFISICAL_SECRET_ENV prod config.env
fi
log "Email SMTP impostata su $EMAIL_IDENTITY"

resolve_email_password_from_infisical() {
  # 1) già in env del processo (deploy da agent con infisical run)
  if [[ -n "${KESI_FUNNEL_GRANDINETICINO_EMAIL_PASSWORD:-}" ]]; then
    echo "$KESI_FUNNEL_GRANDINETICINO_EMAIL_PASSWORD"
    return 0
  fi
  if [[ -n "${EMAIL_HOST_PASSWORD:-}" && "${FORCE_EMAIL_PASSWORD}" != "1" ]]; then
    echo "$EMAIL_HOST_PASSWORD"
    return 0
  fi

  # 2) host wrapper Mac/agent
  local get_script="${INFISICAL_GET:-}"
  if [[ -z "$get_script" && -x "${HOME}/.grok/skills/infisical-vps/scripts/infisical-get.sh" ]]; then
    get_script="${HOME}/.grok/skills/infisical-vps/scripts/infisical-get.sh"
  fi
  if [[ -n "$get_script" && -x "$get_script" ]]; then
    local p
    p=$("$get_script" "$INFISICAL_EMAIL_KEY" 2>/dev/null || true)
    if [[ -n "$p" ]]; then
      echo "$p"
      return 0
    fi
  fi
  if [[ -x "${HOME}/.grok/infisical-peter.sh" ]]; then
    local line p
    line=$(~/.grok/infisical-peter.sh secrets get "$INFISICAL_EMAIL_KEY" --output=dotenv 2>/dev/null | grep "^${INFISICAL_EMAIL_KEY}=" || true)
    p="${line#${INFISICAL_EMAIL_KEY}=}"
    if [[ -n "$p" ]]; then
      echo "$p"
      return 0
    fi
  fi

  # 3) CLI Infisical sul VPS + identity file
  if command -v infisical >/dev/null 2>&1 && [[ -f "$IDENTITY_FILE" ]]; then
    # shellcheck disable=SC1090
    set -a
    # shellcheck source=/dev/null
    source "$IDENTITY_FILE"
    set +a
    if [[ -n "${INFISICAL_MACHINE_CLIENT_ID:-}" && -n "${INFISICAL_MACHINE_CLIENT_SECRET:-}" && -n "${INFISICAL_PROJECT_ID:-}" ]]; then
      local api env_name path token login_out p
      api="${INFISICAL_API_URL:-https://agents-infisical.srv1663152.hstgr.cloud}"
      env_name="${INFISICAL_SECRET_ENV:-prod}"
      path="${INFISICAL_SECRET_PATH:-/}"
      login_out=$(infisical login \
        --method=universal-auth \
        --client-id="$INFISICAL_MACHINE_CLIENT_ID" \
        --client-secret="$INFISICAL_MACHINE_CLIENT_SECRET" \
        --domain="$api" \
        --plain --silent 2>&1 || true)
      token=$(printf '%s\n' "$login_out" | grep -o 'eyJ[^ ]*' | head -1 || true)
      if [[ -z "$token" ]]; then
        token=$(printf '%s\n' "$login_out" | tail -1 | tr -d '\r\n')
      fi
      if [[ -n "$token" ]]; then
        p=$(infisical secrets get "$INFISICAL_EMAIL_KEY" \
          --token="$token" \
          --domain="$api" \
          --env="$env_name" \
          --path="$path" \
          --projectId="$INFISICAL_PROJECT_ID" \
          --plain 2>/dev/null | tr -d '\r' | tail -1 || true)
        if [[ -n "$p" && "$p" != *"error"* ]]; then
          echo "$p"
          return 0
        fi
      fi
    fi
  fi

  # 4) solo se non forziamo: password già in .env
  if [[ "${FORCE_EMAIL_PASSWORD}" != "1" ]] && grep -q '^EMAIL_HOST_PASSWORD=.\+' "$ENV_FILE" 2>/dev/null; then
    local existing
    existing=$(grep -E '^EMAIL_HOST_PASSWORD=' "$ENV_FILE" | cut -d= -f2- || true)
    case "$existing" in
      ''|INSERISCI*|GENERA*|REPLACE*|your-*|la-tua-*) ;;
      *) echo "$existing"; return 0 ;;
    esac
  fi
  return 1
}

if email_pass=$(resolve_email_password_from_infisical); then
  set_env_kv EMAIL_HOST_PASSWORD "$email_pass"
  log "EMAIL_HOST_PASSWORD aggiornata da Infisical ($INFISICAL_EMAIL_KEY, len=${#email_pass})."
  unset email_pass
else
  if [[ -f "$IDENTITY_FILE" ]]; then
    log "Password non letta a deploy-time — il container la prenderà da Infisical all'avvio."
  else
    die "Impossibile risolvere $INFISICAL_EMAIL_KEY. Installa $IDENTITY_FILE o esporta la secret."
  fi
fi

if [[ ! -f "$IDENTITY_FILE" ]]; then
  log "ATTENZIONE: manca $IDENTITY_FILE (machine identity Infisical). Runtime userà solo .env."
else
  # sanity: identity non vuota
  id_ok=$(python3 - <<PY
from pathlib import Path
p=Path("$IDENTITY_FILE")
vals={}
for line in p.read_text().splitlines():
    if "=" in line:
        k,v=line.split("=",1)
        vals[k]=v.strip()
need=["INFISICAL_PROJECT_ID","INFISICAL_MACHINE_CLIENT_ID","INFISICAL_MACHINE_CLIENT_SECRET"]
print("ok" if all(vals.get(k) for k in need) else "empty")
PY
)
  if [[ "$id_ok" != "ok" ]]; then
    die "$IDENTITY_FILE ha valori vuoti — popola la machine identity Infisical."
  fi
  chmod 600 "$IDENTITY_FILE"
  log "Infisical identity OK ($IDENTITY_FILE)."
fi

PLACEHOLDER_PASSWORDS=(
  'GENERA-CON-python'
  'INSERISCI-PASSWORD'
  'REPLACE_WITH_YOUR_INFOMANIAK_APP_PASSWORD'
  'your-app-password'
  'la-tua-password-infomaniak'
)
for placeholder in "${PLACEHOLDER_PASSWORDS[@]}"; do
  if grep -q "$placeholder" "$ENV_FILE" 2>/dev/null; then
    # SECRET_KEY placeholder already handled; password may be injected only at runtime
    if grep -q "EMAIL_HOST_PASSWORD=.*${placeholder}" "$ENV_FILE" 2>/dev/null; then
      if [[ ! -f "$IDENTITY_FILE" ]]; then
        die "EMAIL_HOST_PASSWORD placeholder e identity assente."
      fi
    fi
  fi
done

log "Build e avvio funnel-grandineticino…"
docker compose -f "$COMPOSE_FILE" build --pull
docker compose -f "$COMPOSE_FILE" up -d --force-recreate

log "Attendo avvio container…"
sleep 8

if ! docker ps --format '{{.Names}}' | grep -qx 'funnel-grandineticino'; then
  docker compose -f "$COMPOSE_FILE" logs --tail=50
  die "funnel-grandineticino non è in esecuzione."
fi

log "Verifica email runtime…"
docker exec funnel-grandineticino python - <<'PY'
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
from django.conf import settings
assert settings.EMAIL_HOST_USER == "info@kesi.biz", settings.EMAIL_HOST_USER
assert settings.DEFAULT_FROM_EMAIL == "info@kesi.biz"
assert settings.LEAD_RECIPIENT_EMAIL == "info@kesi.biz"
assert len(settings.EMAIL_HOST_PASSWORD or "") >= 8, "password missing"
print("OK", settings.EMAIL_HOST_USER, settings.EMAIL_HOST, "pass_len", len(settings.EMAIL_HOST_PASSWORD))
PY

log "Container attivo:"
docker ps --filter name=funnel-grandineticino --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'

SERVER_IP=$(curl -fsS --max-time 5 ifconfig.me 2>/dev/null || hostname -I | awk '{print $1}')
log ""
log "Deploy completato."
log "Verifica: curl -sI https://grandineticino.ch/it/ | head -5"
log "Log:      docker compose -f $COMPOSE_FILE logs -f --tail=50"
log "IP: $SERVER_IP"
