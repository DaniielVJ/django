for branch in $(git branch -r | grep -v HEAD); do
    git checkout ${branch#origin/}
    git pull --rebase origin ${branch#origin/}
done
