
alias ll='ls -lF'
alias la='ls -AF'
alias l='ls -CF'

#debesys
alias Make='make -rR -j${CPU} --quiet show_progress=1 config=debug '
alias ttknife='./run ./ttknife'
alias spy='./run python ttex/unittests/spy.py'
alias ttrader='./run t_trader/tt/ttrader/t_trader.py -c ~/ttrader.conf'
alias pytrader='./run pytrader/src/pytrader.py -c ~/pytrader.conf'
alias scripttrader='./run t_trader/tt/ttrader/script_trader.py -c ~/ttrader.conf'
alias pytest='./run python ttex/pyTests/run_tests.py'
alias req-build='./run deploy/chef/scripts/request_build.py'
alias req-deploy='./run deploy/chef/scripts/request_deploy.py'
alias bump='./run deploy/chef/scripts/bump_cookbook_version.py'

#vim projects
alias ettex='gvim -c ":Project ~/ttex.proj"'
alias eachtung='gvim -c ":Project ~/achtung.proj"'
alias ecppactor='gvim -c ":Project ~/cppactor.proj"'
alias eoc='gvim -c ":Project ~/oc.proj"'
alias ettrader='gvim -c ":Project ~/ttrader.proj"'
alias epytrader='gvim -c ":Project ~/pytrader.proj"'

#directories
alias cdlog='cd /var/log/debesys'
alias cddeb='cd ~/projects/debesys'

#git
alias status='git stash list;git status'
alias co='git-checkout'
alias ci='git commit'
alias pull='git-pull'
alias push='git-push'
alias delete='delete-branch'
alias branches='git branch'

function git-pull {
    if [ -z "$1" ]
    then
        echo "Usage: git-pull repo"
        return
    fi
    git pull origin $*
}

function git-push {
    if [ -z "$1" ]
    then
        echo "Usage: git-push repo"
        return
    fi
    git push origin $*
}


function git-checkout {
    git fetch origin
    git remote prune origin
    if [ -n "$1" ]
    then
        branch=$1
    else
        echo
        PS3="Branch: "
        branches=`git for-each-ref --format='%(refname:short)' refs/heads`
        select b in $branches;
        do
            branch=$b
            break;
        done
    fi
    git checkout $branch
    git submodule update
    git stash list
}

function delete-branch {
    PS3="Branch: "
    branches=`git for-each-ref --format='%(refname:short)' refs/heads`
    select branch in $branches;
    do
        echo -n "Delete $branch (y/n)? "
        read yesno
        if [ "$yesno" = 'y' ]
        then
            git branch -d $branch
            git push origin :$branch
        fi
        break;
    done
}
