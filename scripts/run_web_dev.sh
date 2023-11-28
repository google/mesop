lsof -t -i:4200 | xargs kill && \
OPTIC_SERVER_HOST="http://localhost:8080" ibazel run //web/src/app/dev:server
