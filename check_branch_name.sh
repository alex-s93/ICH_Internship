#!/bin/bash

BRANCH_NAME=$(git rev-parse --abbrev-ref HEAD)

if [[ ! $BRANCH_NAME =~ ^(feat|fix|docs|style|refactor|test|chore)/[a-zA-Z0-9_-]+$ ]]; then
    echo "Branch name '$BRANCH_NAME' does not match the naming convention."
    echo "Please use 'feat/', 'fix/', 'docs/', 'style/', 'refactor/', 'test/', or 'chore/' as prefixes followed by descriptive text (e.g., 'feat/my-feature')."
    exit 1
fi
