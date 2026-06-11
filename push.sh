#!/bin/bash

# Navigate to the script's directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$DIR"

# Check if git config user.email or user.name needs update
echo "🔍 Checking Git Configuration..."
CURRENT_NAME=$(git config user.name)
CURRENT_EMAIL=$(git config config user.email)

read -p "Enter your GitHub username (currently: $CURRENT_NAME): " username
if [ ! -z "$username" ]; then
    git config user.name "$username"
fi

read -p "Enter your GitHub email (currently: $CURRENT_EMAIL): " email
if [ ! -z "$email" ]; then
    git config user.email "$email"
fi

# Re-commit with updated details if configuration changed
git commit --amend --reset-author --no-edit

# Remote configuration
REMOTE_URL="git@github.com:$username/worldcup-dashboard.git"
echo "🌐 Setting remote origin to: $REMOTE_URL"
git remote add origin "$REMOTE_URL" 2>/dev/null || git remote set-url origin "$REMOTE_URL"

git branch -M main
echo "🚀 Pushing codebase to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo "=========================================================="
    echo "🎉 Pushed successfully!"
    echo "🌐 Live Page URL (after enabling GitHub Pages):"
    echo "   https://$username.github.io/worldcup-dashboard/index.html"
    echo "=========================================================="
else
    echo "❌ Push failed. Please check if:"
    echo "   1. You created the repository '$username/worldcup-dashboard' on GitHub."
    echo "   2. You added your SSH public key to your GitHub account Settings."
fi
