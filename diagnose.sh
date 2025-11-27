cd /home/jose/Disposable/code/rpgsim

echo "=== GIT DIAGNOSIS ==="

which git
git --version

pwd
ls -la .git

git status
git remote -v

git config --get user.name
git config --get user.email

echo "=== TESTING GIT OPERATIONS ==="

git add --dry-run .
git status --porcelain | head -5