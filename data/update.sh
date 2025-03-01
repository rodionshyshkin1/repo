#!/bin/bash

set -e

echo "Running dvc repro..."
dvc repro

echo "Adding changes to Git..."
git add raw.dvc dvc.lock

read -p "Enter commit message: " commit_msg
git commit -m "$commit_msg"

echo "Running git push to the current branch..."
git push origin $(git branch --show-current)

echo "Running dvc push..."
dvc push

echo "Dataset update was finished!"
