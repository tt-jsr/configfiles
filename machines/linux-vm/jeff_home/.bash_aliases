
alias ll='ls -lF'
alias la='ls -AF'
alias l='ls -CF'
alias ssh='ssh -o GSSAPIAuthentication=no'
alias cssh='chef_ssh'

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
alias pull='git pull origin'
alias push='git push origin'
alias delete='delete-branch'
alias branches='git branch'
alias gsu='git submodule update'
alias gfo='git fetch origin'
alias gss='git stash save'
alias gsp='git stash pop'
alias gsl='git stash list'


function git-checkout {
    git fetch origin
    git remote prune origin
    if [ -n "$1" ]
    then
        case $1 in
        master) 
            branch='master'
            ;;
        uat)
            branch='uat/current'
            ;;
        stage)
            branch='release/current'
            ;;
        dev)
            branch='develop'
            ;;
        *)
            branch=$1
            ;;
        esac
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
    echo "git submodule update"
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

function chef_ssh {
    if [ -z "$1" -o -z "$2" ]
    then 
        echo "Usage: chef-ssh env recipe"
        echo "Environments: dev, stage, sqe, devsim"
        echo "              uat, prod, prodsim"
        return
    fi

    knife=~/.chef/knife.rb

    case $1 in
    dev)
        env='int-dev-cert'
        ;;
    stage)
        env='int-stage-cert'
        ;;
    devsim)
        env='int-dev-sim'
        ;;
    sqe)
        env='int-sqe-cert'
        ;;
    uat)
        env='ext-uat-cert'
        knife=~/.chef/knife.external.rb
        ;;
    prod)
        env='ext-prod-live'
        knife=~/.chef/knife.external.rb
        ;;
    prodsim)
        env='ext-prod-sim'
        knife=~/.chef/knife.external.rb
        ;;
    esac

    oc=$2
    ips=`./run ./ttknife --config $knife search node "chef_environment:$env AND recipe:$oc" | grep IP | sed 's/IP:[ \t]*\([0-9.]*\)/\1/'`

    PS3="Machine: "
    select selection in $ips
    do
        ssh root@$selection
        break
    done
}

