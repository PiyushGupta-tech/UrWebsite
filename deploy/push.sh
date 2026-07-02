#!/usr/bin/env bash
# Sync local project to production (run from repo root).
# Requires: sshpass, SSH access to root@185.199.53.121:21761
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HOST="${DEPLOY_HOST:-185.199.53.121}"
PORT="${DEPLOY_PORT:-21761}"
USER="${DEPLOY_USER:-root}"
REMOTE="${DEPLOY_PATH:-/www/wwwroot/urbanrupeeHome}"
SSH_OPTS="-o StrictHostKeyChecking=no -p ${PORT}"

if [[ -z "${DEPLOY_SSH_PASS:-}" ]]; then
  echo "Set DEPLOY_SSH_PASS or configure SSH keys for ${USER}@${HOST}" >&2
  exit 1
fi

PWFILE="$(mktemp)"
chmod 600 "$PWFILE"
printf '%s' "$DEPLOY_SSH_PASS" > "$PWFILE"
cleanup() { rm -f "$PWFILE"; }
trap cleanup EXIT

RSYNC_SSH="sshpass -f $PWFILE ssh $SSH_OPTS"

echo "==> Build frontend"
(cd "$ROOT/frontend" && npm run build)

echo "==> Rsync to ${USER}@${HOST}:${REMOTE}"
rsync -avz --delete \
  --exclude '.git' \
  --exclude '.next' \
  --exclude 'frontend/node_modules' \
  --exclude '.venv' \
  --exclude 'backend/.venv' \
  --exclude 'backend/db.sqlite3' \
  --exclude 'backend/staticfiles' \
  --exclude 'backend/.env' \
  --exclude '.DS_Store' \
  -e "$RSYNC_SSH" \
  "$ROOT/" \
  "${USER}@${HOST}:${REMOTE}/"

echo "==> Backend static + restart"
sshpass -f "$PWFILE" ssh $SSH_OPTS "${USER}@${HOST}" bash -s <<REMOTE
set -e
cd ${REMOTE}
test -f backend/.env || { echo "Missing backend/.env — create from deploy/env.production.example" >&2; exit 1; }
source .venv/bin/activate
pip install -r backend/requirements.txt -q
# Stale SPA index in staticfiles breaks asset URLs after each frontend build.
rm -f backend/staticfiles/index.html
rm -rf backend/staticfiles/assets
cd backend && python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py createcachetable 2>/dev/null || true
chown www:www backend backend/db.sqlite3 2>/dev/null || true
chmod 775 backend 2>/dev/null || true
# rsync from macOS can leave dist/logos unreadable by gunicorn (www user).
chmod -R a+rX frontend/dist/logos frontend/dist/maps frontend/dist/videos 2>/dev/null || true
chown -R www:www frontend/dist/logos frontend/dist/maps frontend/dist/videos 2>/dev/null || true
systemctl restart urbanrupee-gunicorn
if systemctl list-unit-files urbanrupee-payout-refresh.service --no-legend 2>/dev/null | grep -q urbanrupee-payout-refresh; then
  systemctl restart urbanrupee-payout-refresh
fi
sleep 2
systemctl is-active urbanrupee-gunicorn
curl -s -o /dev/null -w "HTTP %{http_code}\n" -H "Host: urbanrupee.com" http://127.0.0.1:8005/
REMOTE

echo "==> Done"
