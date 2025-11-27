#!/bin/bash

echo "🔍 Diagnosing git environment..."
cd /home/jose/Disposable/code/rpgsim

# Check if git is available
echo "📋 Git version:"
which git
git --version || echo "❌ Git not found"

# Check current directory
echo "📁 Current directory:"
pwd

# Check if we're in right repo
echo "🔍 Repo status:"
git status || echo "❌ Not a git repository"

# Check remote
echo "🌐 Remote info:"
git remote -v

# Check git user config
echo "👤 Git user:"
git config --get user.name || echo "❌ No user.name configured"
git config --get user.email || echo "❌ No user.email configured"