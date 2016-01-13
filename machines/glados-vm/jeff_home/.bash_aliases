
alias ll='ls -lhF'
alias la='ls -AF'
alias l='ls -CF'
alias ssh='ssh -o GSSAPIAuthentication=no'
alias cssh='chef_ssh'
alias cftp='chef_ftp'
alias cscp='chef-scp'
alias hd='od -A x -c '

#debesys
alias Make='make -rR -j4 --quiet show_progress=1 config=debug '
alias ttknife='./run ./ttknife'
alias spy='./run python ttex/unittests/spy.py'
alias ttrader='./run t_trader/tt/ttrader/t_trader.py -c ~/ttrader.conf'
alias pytrader='./run pytrader/src/pytrader.py -c ~/pytrader.conf'
alias scripttrader='./run t_trader/tt/ttrader/script_trader.py -c ~/ttrader.conf'
alias pytest='./run python ttex/pyTests/run_tests.py'
alias req-build='./run deploy/chef/scripts/request_build.py'
alias req-deploy='./run deploy/chef/scripts/request_deploy.py'
alias bump='./run deploy/chef/scripts/bump_cookbook_version.py'

#directories
alias cdlog='cd /var/log/debesys'
alias cddeb='cd ~/projects/debesys'
alias eris='cd ~/projects/debesys/orders/eris/include/eris/'
alias ice='cd ~/projects/debesys/orders/ice/include/ice/'
alias es='cd ~/projects/debesys/orders/espeed/include/espeed/'
alias cf='cd ~/projects/debesys/orders/cf/include/cf/'
alias kcg='cd ~/projects/debesys/orders/kcg/include/kcg'
alias ba='cd ~/projects/debesys/orders/bankalgo/include/bankalgo'
alias cme='cd ~/projects/debesys/orders/cme/include/cme'
alias deb='cd ~/projects/debesys'
alias om='cd ~/projects/debesys/all_messages/source/tt/messaging/order'
alias ttusm='cd ~/projects/debesys/all_messages/source/tt/messaging/ttus'
alias cfe='cd ~/projects/debesys/orders/cfe/include/cfe'
alias sfe='cd ~/projects/debesys/orders/sfe/include/sfe'
alias eurex='cd ~/projects/debesys/orders/eurex/include/eurex'
alias fixit='cd ~/projects/debesys/fixit/cpp/src/session'
alias otc='cd ~/projects/debesys/orders/eurex_otc/include/eurex_otc'
alias eotc='cd ~/projects/debesys/orders/eurex_otc/include/eurex_otc'
alias nfx='cd ~/projects/debesys/orders/nfx/include/nfx'

#git
alias status='git stash list;git status'
alias co='git-checkout'
alias ci='git commit'
alias pull='git pull origin'
alias push='git push origin'
alias delete='delete-branch'
alias gsu='git submodule update'
alias gfo='git fetch origin'
alias gss='git stash save'
alias gsp='git stash pop'
alias gsl='git stash list'
alias ebd='edit-branch-desc'
alias gnb='git-new-branch'

function ttlog {
    cd /home/jeff/projects/debesys
    ./run build/x86-64/release/bin/ttlog "$1"
    cd -
}

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
            if [ -e /home/jeff/gitbranches/$branch ]
            then
                rm /home/jeff/gitbranches/$branch
            fi
        fi
        break;
    done
}

function edit-branch-desc {
    vim "/home/jeff/gitbranches/$1"
}

function git-new-branch {
    git checkout -b $1
    edit-branch-desc $1
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
        cmd="ssh jrichards@"
        ;;
    stage)
        env='int-stage-cert'
        cmd="ssh jrichards@"
        ;;
    devsim)
        env='int-dev-sim'
        cmd="ssh jrichards@"
        ;;
    sqe)
        env='int-sqe-cert'
        cmd="ssh jrichards@"
        ;;
    uat)
        env='ext-uat-cert'
        knife=~/.chef/knife.external.rb
        cmd="ssh jrichards@"
        ;;
    prod)
        env='ext-prod-live'
        knife=~/.chef/knife.external.rb
        cmd="ssh jrichards@"
        ;;
    prodsim)
        env='ext-prod-sim'
        knife=~/.chef/knife.external.rb
        cmd="ssh jrichards@"
        ;;
    *)
        env=$1
        cmd="ssh jrichards@"
        ;;
    esac

    oc=$2
    ips=`./run ./ttknife --config $knife search node "chef_environment:$env AND recipe:$oc" | grep IP | sed 's/IP:[ \t]*\([0-9.]*\)/\1/'`

    PS3="Machine: "
    select selection in $ips
    do
        ${cmd}$selection
        break
    done
}

function chef_ftp {
    if [ -z "$1" -o -z "$2" ]
    then 
        echo "Usage: chef-ftp env recipe"
        echo "Environments: dev, stage, sqe, devsim"
        echo "              uat, prod, prodsim"
        return
    fi

    knife=~/.chef/knife.rb

    case $1 in
    dev)
        env='int-dev-cert'
        cmd="sftp jrichards@"
        ;;
    stage)
        env='int-stage-cert'
        cmd="sftp jrichards@"
        ;;
    devsim)
        env='int-dev-sim'
        cmd="sftp jrichards@"
        ;;
    sqe)
        env='int-sqe-cert'
        cmd="sftp jrichards@"
        ;;
    uat)
        env='ext-uat-cert'
        knife=~/.chef/knife.external.rb
        cmd="sftp jrichards@"
        ;;
    prod)
        env='ext-prod-live'
        knife=~/.chef/knife.external.rb
        cmd="sftp jrichards@"
        ;;
    prodsim)
        env='ext-prod-sim'
        knife=~/.chef/knife.external.rb
        cmd="sftp jrichards@"
        ;;
    *)
        env=$1
        cmd="sftp jrichards@"
        ;;
    esac

    oc=$2
    ips=`./run ./ttknife --config $knife search node "chef_environment:$env AND recipe:$oc" | grep IP | sed 's/IP:[ \t]*\([0-9.]*\)/\1/'`

    PS3="Machine: "
    select selection in $ips
    do
        ${cmd}$selection
        break
    done
}

csview () 
{ 
    local file="$1";
    cat "$file" | sed -e 's/,,/, ,/g' | column -s, -t | less -#5 -N -S
}

