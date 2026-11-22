#!/usr/bin/env bash
# Start a local WordPress + Elementor + Supercraft stack in a project folder.
# Usage: setup-local-wp.sh <project-dir> <port>
# Plugin source folders can be overridden with env vars (see defaults below).
set -euo pipefail

PROJECT_DIR="${1:?project dir required}"
WP_PORT="${2:?port required}"
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"

SAAS="${SUPERCRAFT_SAAS_DIR:-/Volumes/T7/Lyness/SAAS}"
HARNESS="${SUPERCRAFT_HARNESS_DIR:-$SAAS/SuperDesign Harness}"
ELEMENTOR_DIR="${ELEMENTOR_DIR:-$HARNESS/local-plugins/elementor}"
PRO_ELEMENTS_DIR="${PRO_ELEMENTS_DIR:-$HARNESS/local-plugins/pro-elements}"
SUPERCOMPONENT_DIR="${SUPERCOMPONENT_DIR:-$SAAS/SuperComponent Studio}"
ANIMATION_DIR="${ANIMATION_DIR:-$SAAS/Supercraft Animation Plugin}"
MASTER_DIR="${MASTER_DIR:-$SAAS/Supercraft Master Plugin}"
NOVAMIRA_DIR="${NOVAMIRA_DIR:-$HARNESS/Novamira/novamira}"
NOVAMIRA_PRO_DIR="${NOVAMIRA_PRO_DIR:-$HARNESS/Novamira/novamira-pro}"
HELLO_THEME_DIR="${HELLO_THEME_DIR:-$ANIMATION_DIR/local-themes/hello-elementor}"

missing=0
for v in ELEMENTOR_DIR PRO_ELEMENTS_DIR SUPERCOMPONENT_DIR ANIMATION_DIR MASTER_DIR NOVAMIRA_DIR NOVAMIRA_PRO_DIR HELLO_THEME_DIR; do
  if [ ! -d "${!v}" ]; then echo "MISSING $v=${!v}"; missing=1; fi
done
[ "$missing" = 0 ] || { echo "Set the missing paths as env vars and re-run."; exit 2; }

if lsof -nP -iTCP:"$WP_PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "Port $WP_PORT is already in use. Pick another port."; exit 3
fi

docker info >/dev/null 2>&1 || { echo "Docker is not running. Start Docker Desktop first."; exit 4; }

cd "$PROJECT_DIR"
[ -e docker-compose.yml ] && { echo "docker-compose.yml already exists in $PROJECT_DIR; not overwriting."; exit 5; }

NAME="sc_$(basename "$PROJECT_DIR" | tr '[:upper:]' '[:lower:]' | tr -c 'a-z0-9\n' '_' | sed 's/__*/_/g;s/^_//;s/_$//')"
cp "$SKILL_DIR/templates/docker-compose.yml" docker-compose.yml
cp "$SKILL_DIR/templates/apache-limits.conf" apache-limits.conf
mkdir -p wp-uploads
cat > .env <<EOF
COMPOSE_PROJECT_NAME=$NAME
WP_PORT=$WP_PORT
ELEMENTOR_DIR=$ELEMENTOR_DIR
PRO_ELEMENTS_DIR=$PRO_ELEMENTS_DIR
SUPERCOMPONENT_DIR=$SUPERCOMPONENT_DIR
ANIMATION_DIR=$ANIMATION_DIR
MASTER_DIR=$MASTER_DIR
NOVAMIRA_DIR=$NOVAMIRA_DIR
NOVAMIRA_PRO_DIR=$NOVAMIRA_PRO_DIR
HELLO_THEME_DIR=$HELLO_THEME_DIR
EOF

for line in .env .wp-local-credentials wp-uploads/ .DS_Store; do
  grep -qxF "$line" .gitignore 2>/dev/null || echo "$line" >> .gitignore
done

docker compose up -d

for i in $(seq 1 60); do
  code=$(curl -s -o /dev/null -w '%{http_code}' "http://localhost:$WP_PORT/" || true)
  [ "$code" != "000" ] && break; sleep 2
done

PW=$(openssl rand -base64 18 | tr -d '/+=')
printf "WP_URL=http://localhost:%s\nWP_ADMIN_USER=admin\nWP_ADMIN_PASS=%s\n" "$WP_PORT" "$PW" > .wp-local-credentials
chmod 600 .wp-local-credentials

wp() {
  docker run --rm --user 33:33 --volumes-from "${NAME}_wordpress" --network "${NAME}_default" \
    -e WORDPRESS_DB_HOST=db:3306 -e WORDPRESS_DB_USER=wordpress \
    -e WORDPRESS_DB_PASSWORD=wordpress_password -e WORDPRESS_DB_NAME=wordpress \
    wordpress:cli wp "$@"
}

for i in $(seq 1 30); do wp db check >/dev/null 2>&1 && break; sleep 2; done

wp core install --url="http://localhost:$WP_PORT" --title="$(basename "$PROJECT_DIR")" \
  --admin_user=admin --admin_password="$PW" --admin_email=admin@example.test --skip-email
wp theme activate hello-elementor
wp plugin activate elementor pro-elements supercomponent-studio supercraft-animation-plugin \
  supercraft-master-plugin novamira novamira-pro
wp option update elementor_onboarded 1
wp plugin list --fields=name,status,version

echo "READY http://localhost:$WP_PORT (credentials in $PROJECT_DIR/.wp-local-credentials)"
