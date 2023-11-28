#!/bin/bash

lsof -t -i:4200 | xargs kill;
lsof -t -i:8080 | xargs kill;

# Define your commands
cmd1="scripts/run_web_dev.sh"
cmd2="scripts/run_py_dev.sh"

# Run both commands in subshells, redirect stderr to stdout, and prefix output
{ $cmd1 2>&1 >&3 | sed 's/^/[WEB] /' >&2; } 3>&1 &
{ $cmd2 2>&1 >&3 | sed 's/^/[PY] /' >&2; } 3>&1 &

# Wait for both background processes to finish
wait
