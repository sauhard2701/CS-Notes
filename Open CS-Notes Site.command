#!/bin/zsh

set -u

cd -- "$(dirname "$0")" || exit 1

export CS_NOTES_ROOT="$PWD"
URL="http://localhost:3000/#/"
HEALTH_URL="http://localhost:3000/"

if curl -fsS "$HEALTH_URL" >/dev/null 2>&1; then
  echo "CS-Notes already appears to be running."
  open "$URL"
  exit 0
fi

echo "Starting CS-Notes..."
echo "URL: $URL"
echo

/bin/zsh -lic 'cd "$CS_NOTES_ROOT" && npm run docs:serve' &
server_pid=$!

for _ in {1..60}; do
  if curl -fsS "$HEALTH_URL" >/dev/null 2>&1; then
    echo
    echo "CS-Notes is running at $URL"
    echo "Press Ctrl+C in this Terminal window to stop the server."
    open "$URL"
    wait "$server_pid"
    exit $?
  fi

  if ! kill -0 "$server_pid" >/dev/null 2>&1; then
    echo
    echo "Docsify exited before the site became available."
    wait "$server_pid"
    exit $?
  fi

  sleep 0.5
done

echo
echo "Timed out waiting for Docsify to start."
kill "$server_pid" >/dev/null 2>&1
exit 1
