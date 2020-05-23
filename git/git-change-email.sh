#!/bin/bash
# Replaces author name and email for all git history in all branches
# Requirement: Update WRONG_EMAIL, NEW_NAME, and NEW_EMAIL

git filter-branch --env-filter '
WRONG_EMAIL="wrong@email.com"
NEW_NAME="Newfirstname Newlastname"
NEW_EMAIL="new@email.com"

if [ "$GIT_COMMITTER_EMAIL" = "$WRONG_EMAIL" ]
then
    export GIT_COMMITTER_NAME="$NEW_NAME"
    export GIT_COMMITTER_EMAIL="$NEW_EMAIL"
fi
if [ "$GIT_AUTHOR_EMAIL" = "$WRONG_EMAIL" ]
then
    export GIT_AUTHOR_NAME="$NEW_NAME"
    export GIT_AUTHOR_EMAIL="$NEW_EMAIL"
fi
' --tag-name-filter cat -- --branches --tags
