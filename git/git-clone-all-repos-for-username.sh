#!/bin/bash
# Clones all repositories for a given user
# Requirement: Update username and pages if more than 100

username=

pages=100

repositories=$(echo `curl --silent https://api.github.com/users/${username}/repos?per_page=${pages} | grep -A 1 "\"node_id\"" | grep -o "\"name\".*" | cut -d'"' -f 4 | sed "s/^/git@github.com:${username}\//g" | sed 's/$/\.git/g'`)

for i in ${repositories}; do git clone $i; done

