#!/bin/bash

COMMIT_MSG= $(python3 src/generate_commit.py)

echo "Suggested Commit Message: $COMMIT_MSG"

echo

read -p "Do you want to keep this commit message( y/n )?" confirm

if [ "$confirm" == "y" ]; then
    echo "$COMMIT_MSG" > .git/COMMIT_EDITMSG
else
    echo "Commit message discarded."
    exit 1
fi
