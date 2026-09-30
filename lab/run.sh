#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export COMPOSE_PROJECT_NAME="${COMPOSE_PROJECT_NAME:-msquic-compat-vn}"

down() {
  echo "== docker compose down -v =="
  docker compose down -v --remove-orphans || true
}

echo "== docker compose down (clean) =="
down

echo "== docker compose up --build =="
up_ok=0
for attempt in $(seq 1 5); do
  if docker compose up --build -d; then
    up_ok=1
    break
  fi
  echo "IOC compose-up-retry attempt=${attempt}"
  sleep 15
  down
done
if [[ "${up_ok}" != 1 ]]; then
  echo "FAIL MSQUIC-COMPAT-VN-KEY-POISON compose up failed" | tee poc-last-run.txt
  down
  exit 1
fi

echo "== wait for container =="
ok=0
for i in $(seq 1 60); do
  if docker compose exec -T lab true >/dev/null 2>&1; then
    ok=1
    break
  fi
  sleep 2
done
if [[ "${ok}" != 1 ]]; then
  echo "FAIL MSQUIC-COMPAT-VN-KEY-POISON container not ready" | tee poc-last-run.txt
  docker compose logs --tail=80 || true
  down
  exit 1
fi

echo "== poc.py =="
set +e
docker compose exec -T lab python3 /lab/poc.py | tee poc-last-run.txt
rc=${PIPESTATUS[0]}
set -e
if [[ "${rc}" != 0 ]]; then
  if ! tail -n1 poc-last-run.txt 2>/dev/null | grep -q '^FAIL '; then
    echo "FAIL MSQUIC-COMPAT-VN-KEY-POISON poc exit=${rc}" >> poc-last-run.txt
  fi
fi
down
exit "${rc}"
