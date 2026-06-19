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
#   - .env con EMAIL_HOST_PASSWORD compilata

set -euo pipefail

DEPLOY_DIR="${DEPLOY_DIR:-/opt/sites/funnel-grandineticino}"
REPO_URL="${REPO_URL:-https://github.com/PeterCatania721/funnel-grandineticino.git}"
BRANCH="${BRANCH:-main}"
COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.yaml}"
ENV_FILE="${ENV_FILE:-.env}"
KESI_DIR="${KESI_DIR:-/opt/sites/kesi-site}"

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

if ! grep -q '^EMAIL_HOST_PASSWORD=.\+' "$ENV_FILE" 2>/dev/null; then
  if [[ -f "$KESI_DIR/.env" ]]; then
    kesi_pass=$(grep -E '^EMAIL_HOST_PASSWORD=' "$KESI_DIR/.env" | cut -d= -f2- || true)
    if [[ -n "$kesi_pass" && "$kesi_pass" != "INSERISCI-PASSWORD-CASELLA" ]]; then
      if grep -q '^EMAIL_HOST_PASSWORD=' "$ENV_FILE"; then
        sed -i "s|^EMAIL_HOST_PASSWORD=.*|EMAIL_HOST_PASSWORD=$kesi_pass|" "$ENV_FILE"
      else
        echo "EMAIL_HOST_PASSWORD=$kesi_pass" >> "$ENV_FILE"
      fi
      log "EMAIL_HOST_PASSWORD copiata da $KESI_DIR/.env (solo lettura)."
    fi
  fi
fi

if grep -q 'GENERA-CON-python' "$ENV_FILE" || grep -q 'INSERISCI-PASSWORD' "$ENV_FILE"; then
  die "Compila SECRET_KEY e EMAIL_HOST_PASSWORD in $DEPLOY_DIR/$ENV_FILE"
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
