#!/usr/bin/env bash
# Run on the server as a user that can write /www/wwwroot/urbanrupeeHome and restart gunicorn.
set -euo pipefail

APP_ROOT="${APP_ROOT:-/www/wwwroot/urbanrupeeHome}"
SERVICE="${GUNICORN_SERVICE:-urbanrupee-gunicorn}"

cd "$APP_ROOT"

echo "==> Pull latest code"
git fetch origin main
git reset --hard origin/main

echo "==> Frontend build"
cd frontend
npm ci
npm run build
cd ..

echo "==> Backend dependencies & static files"
source .venv/bin/activate
pip install -r backend/requirements.txt -q
cd backend
python manage.py collectstatic --noinput
cd ..

echo "==> Restart Gunicorn"
if command -v systemctl >/dev/null 2>&1; then
  sudo systemctl restart "$SERVICE"
  sudo systemctl status "$SERVICE" --no-pager -l | head -15
else
  echo "systemctl not found — restart $SERVICE manually"
fi

echo "==> Testimonial videos (not in git — copy once if missing)"
VIDEO_DIR="$APP_ROOT/frontend/public/videos/testimonials"
if [ ! -f "$VIDEO_DIR/finlix.mp4" ] || [ ! -f "$VIDEO_DIR/grootspay.mov" ]; then
  echo "    Upload finlix.mp4 and grootspay.mov to $VIDEO_DIR"
fi

echo "==> Done"
