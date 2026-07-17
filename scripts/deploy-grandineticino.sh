#!/usr/bin/env bash
# Deploy funnel Grandineticino.ch su VPS Hostinger.
# Container e volume SEPARATI da kesi-site — non modifica il Docker KESI 2026.
#
# Uso (sul VPS):
#   ./scripts/deploy-grandineticino.sh
#
# Prerequisiti:
#   - Docker + Traefik già attivi (come per kesi-automotive.ch)
#   - DNS grandineticino.ch → IP del VPS (Infomaniak)
#   - EMAIL_HOST_PASSWORD da Infisical: KESI_FUNNEL_GRANDINETICINO_EMAIL_PASSWORD
#     (mittente/server sempre info@kesi.biz)

set -euo pipefail

DEPLOY_DIR="${DEPLOY_DIR:-/docker/funnel-grandineticino}"
REPO_URL="${REPO_URL:-https://github.com/PeterCatania721/funnel-grandineticino.git}"
BRANCH="${BRANCH:-main}"
COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.yaml}"
ENV_FILE="${ENV_FILE:-.env}"
KESI_DIR="${KESI_DIR:-/opt/sites/kesi-site}"
# Casella SMTP fissa
EMAIL_IDENTITY="${EMAIL_IDENTITY:-info@kesi.biz}"
INFISICAL_EMAIL_KEY="${INFISICAL_EMAIL_KEY:-KESI_FUNNEL_GRANDINETICINO_EMAIL_PASSWORD}"

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
  sudo mkdir -p "$DEPLOY_DIR"
  sudo chown "$(whoami):$(id -gn)" "$DEPLOY_DIR"
fi

cd "$DEPLOY_DIR"

if [[ ! -d .git ]]; then
  log "Clone repository…"
  git clone --branch "$BRANCH" "$REPO_URL" .
else
  log "Aggiorno repository (branch $BRANCH)…"
  git fetch origin "$BRANCH"
  git checkout "$BRANCH"
  git pull origin "$BRANCH"
fi

if [[ ! -f "$ENV_FILE" ]]; then
  if [[ -f .env.production.example ]]; then
    cp .env.production.example "$ENV_FILE"
    log "Creato $ENV_FILE da example — COMPILA SECRET_KEY e EMAIL_HOST_PASSWORD."
  else
    die "Manca $ENV_FILE. Copia .env.production.example e compila i valori."
  fi
fi

# Forza sempre mittente/SMTP user/destinatari su info@kesi.biz
set_env_kv() {
  local key="$1" val="$2"
  if grep -q "^${key}=" "$ENV_FILE" 2>/dev/null; then
    sed -i "s|^${key}=.*|${key}=${val}|" "$ENV_FILE"
  else
    echo "${key}=${val}" >> "$ENV_FILE"
  fi
}
set_env_kv EMAIL_HOST mail.infomaniak.com
set_env_kv EMAIL_PORT 587
set_env_kv EMAIL_USE_TLS True
set_env_kv EMAIL_HOST_USER "$EMAIL_IDENTITY"
set_env_kv DEFAULT_FROM_EMAIL "$EMAIL_IDENTITY"
set_env_kv LEAD_RECIPIENT_EMAIL "$EMAIL_IDENTITY"
set_env_kv FUNNEL_RECIPIENT_EMAIL "$EMAIL_IDENTITY"
log "Email SMTP impostata su $EMAIL_IDENTITY"

# Password: 1) Infisical key  2) env già presente  3) kesi-site .env (legacy)
resolve_email_password() {
  if [[ -n "${EMAIL_HOST_PASSWORD:-}" ]]; then
    echo "$EMAIL_HOST_PASSWORD"
    return 0
  fi
  if command -v infisical >/dev/null 2>&1 && [[ -f "${INFISICAL_ENV_FILE:-/root/.infisical-peter-agents.env}" || -n "${INFISICAL_TOKEN:-}" ]]; then
    :
  fi
  # Wrapper locale (Mac/agent) o secret già esportato
  if [[ -n "${KESI_FUNNEL_GRANDINETICINO_EMAIL_PASSWORD:-}" ]]; then
    echo "$KESI_FUNNEL_GRANDINETICINO_EMAIL_PASSWORD"
    return 0
  fi
  local get_script="${INFISICAL_GET:-}"
  if [[ -z "$get_script" && -x "$HOME/.grok/skills/infisical-vps/scripts/infisical-get.sh" ]]; then
    get_script="$HOME/.grok/skills/infisical-vps/scripts/infisical-get.sh"
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
  if grep -q '^EMAIL_HOST_PASSWORD=.\+' "$ENV_FILE" 2>/dev/null; then
    local existing
    existing=$(grep -E '^EMAIL_HOST_PASSWORD=' "$ENV_FILE" | cut -d= -f2- || true)
    case "$existing" in
      ''|INSERISCI*|GENERA*|REPLACE*|your-*|la-tua-*) ;;
      *) echo "$existing"; return 0 ;;
    esac
  fi
  if [[ -f "$KESI_DIR/.env" ]]; then
    local kesi_pass
    kesi_pass=$(grep -E '^EMAIL_HOST_PASSWORD=' "$KESI_DIR/.env" | cut -d= -f2- || true)
    if [[ -n "$kesi_pass" && "$kesi_pass" != "INSERISCI-PASSWORD-CASELLA" ]]; then
      log "EMAIL_HOST_PASSWORD da $KESI_DIR/.env (fallback legacy)."
      echo "$kesi_pass"
      return 0
    fi
  fi
  return 1
}

if email_pass=$(resolve_email_password); then
  set_env_kv EMAIL_HOST_PASSWORD "$email_pass"
  log "EMAIL_HOST_PASSWORD impostata (fonte: Infisical $INFISICAL_EMAIL_KEY o fallback)."
  unset email_pass
else
  die "Impossibile risolvere EMAIL_HOST_PASSWORD. Esporta $INFISICAL_EMAIL_KEY o imposta EMAIL_HOST_PASSWORD."
fi

PLACEHOLDER_PASSWORDS=(
  'GENERA-CON-python'
  'INSERISCI-PASSWORD'
  'REPLACE_WITH_YOUR_INFOMANIAK_APP_PASSWORD'
  'your-app-password'
  'la-tua-password-infomaniak'
)
for placeholder in "${PLACEHOLDER_PASSWORDS[@]}"; do
  if grep -q "$placeholder" "$ENV_FILE"; then
    die "EMAIL_HOST_PASSWORD è ancora un placeholder ($placeholder). Usa Infisical $INFISICAL_EMAIL_KEY."
  fi
done

if grep -q 'GENERA-CON-python' "$ENV_FILE"; then
  die "Compila SECRET_KEY in $DEPLOY_DIR/$ENV_FILE"
fi

log "Build e avvio funnel-grandineticino…"
docker compose -f "$COMPOSE_FILE" build --pull
docker compose -f "$COMPOSE_FILE" up -d

log "Attendo avvio container…"
sleep 5

if ! docker ps --format '{{.Names}}' | grep -qx 'funnel-grandineticino'; then
  docker compose -f "$COMPOSE_FILE" logs --tail=40
  die "funnel-grandineticino non è in esecuzione."
fi

log "Container attivo:"
docker ps --filter name=funnel-grandineticino --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'

SERVER_IP=$(curl -fsS --max-time 5 ifconfig.me 2>/dev/null || hostname -I | awk '{print $1}')
log ""
log "Deploy completato."
log "DNS Infomaniak (se non fatto):"
log "  A    grandineticino.ch     → $SERVER_IP"
log "  A    www.grandineticino.ch → $SERVER_IP"
log ""
log "Verifica: curl -sI https://grandineticino.ch/it/ | head -5"
log "Log:      docker compose -f $COMPOSE_FILE logs -f --tail=50"
