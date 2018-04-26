#!/bin/bash

# To run this script:

# 1. Create a directory to place the crash files. It does not need to be in /tmp 
#    if you would rather place it somewhere else. Name it something meaningful instead
#    of the ccpp-blah-blah the email says
#
# 2. Copy the first section of the crash dump email into 'email.dat' in the directory
#    created in #1.
#
#    The section we need extends from the "A crash has been detected..." to "Ext Version:..."
#
# 3. run gdblaunch.sh <the directory you created>
#
# The following will happen:
#    The script will retrieve the tarball from the shared directory, failing that, it will
#    try to scp it from the host machine. The tar file will be extracted
#
#    You will be asked if you want your repo to checkout the hash
#
#    You will be asked to create a back trace file. Unlike the backtrace_full.stack that comes
#    with the tarfile, this will include all stack frames (not limited to 4) and will include
#    function arguments and local variables.
#
#    The debugger will be launched

# Set REPO to the location of your repository
REPO=/home/jeff/projects/testrepo

# Set your username. scp will use this if we need to get the tarball from the host
USER=jrichards

if [[ -z $1 ]]
then
    DIR=`pwd`
    echo -n "Use current directory $DIR (y/n)? "
    read yno
    if [[ $yno != "y" ]]
    then
        exit
    fi
else
    DIR=$1
fi


# If the email.dat filedoesnot exist, assume it's on the clipboard
if [[ ! -f $DIR/email.dat ]]
then
    xclip -o > $DIR/email.dat
fi

# From the email, set the crash id
CRASHID=`cat $DIR/email.dat | sed -n -e 's/Crash ID: \([^ ]*\).*/\1/p'`
echo "CrashID: $CRASHID"
if [[ -z $CRASHID ]]
then
    echo "Crash id is not set"
    exit
fi

#From the email set the hash (Chef Version)
HASH=`cat $DIR/email.dat | sed -n -e 's/Chef Version: \([a-f0-9]*\).*/\1/p'`
echo "Hash: $HASH"
if [[ -z $HASH ]]
then
    echo "Hash is not set"
    exit
fi

# Set the name of executable
BINARY=`cat $DIR/email.dat | sed -n -e 's/^.* has been detected for \([^ ]*\).*/\1/p'`
echo "Binary: $BINARY"
if [[ -z $BINARY ]]
then
    echo "Binary is not set"
    exit
fi

# From the email, set the host and IP address
HOST=`cat $DIR/email.dat | sed -n -e 's/^.*has been detected for [a-zA-Z0-9_]* on \([a-zA-Z0-9]*\).*/\1/p'`
echo "Host: $HOST"
if [[ -z $HOST ]]
then
    echo "Host is not set"
    exit
fi

HOSTIP=`cat $DIR/email.dat | sed -n -e 's/^.*has been detected for [a-zA-Z0-9_]* on .*(\(.*\)).*/\1/p'`
echo "HostIP: $HOSTIP"
if [[ -z $HOSTIP ]]
then
    echo "HOSTIP is not set"
    exit
fi


RECIPE=`cat $DIR/email.dat | sed -n -e 's/^.*Chef Recipe Name: \([a-zA-Z0-9_]*\):.*/\1/p'`
echo "Recipe: $RECIPE"
if [[ -z $RECIPE ]]
then
    echo "Recipe is not set"
    exit
fi

#################################################################
EXT=$REPO/ext/linux/x86-64/release

CRASHNAME=`echo $CRASHID | sed s/:/_/g`

# Shared library path
SOPATH=$EXT/lib:$EXT/lib64:$EXT/opt/gcc-4.9.1/lib64/:/lib:/lib64:/usr/lib:/usr/lib64
TARBALL=${CRASHNAME}_${HOST}_crash_files.tar.gz
echo "Tarball: $TARBALL"

if [[ ! -f $TARBALL ]]
then
    if [[ -f /mnt/crashes/$BINARY/$TARBALL ]]
    then
        cp /mnt/crashes/$BINARY/$TARBALL $DIR
    else
        echo "Tarball not found on shared drive, trying from host..."
        scp ${USER}@$HOSTIP:/var/spool/abrt/$TARBALL $DIR
    fi
    if [[ ! -f $DIR/$TARBALL ]]
    then
        echo "Cannot get tarfile"
        exit
    fi
fi

# We use the 'var' directory to indicate if the tar file needs extraction
if [[ ! -d var ]]
then
    pushd $DIR
    echo -n "Extracting tarball..."
    tar xzf $TARBALL
    echo
    popd
fi


echo -n "Checkout $REPO to hash $HASH (y/n)? "
read yno
if [[ $yno == "y" ]]
then
    pushd $REPO
    git checkout $HASH
    git submodule update
    popd
fi

# Test for the existence of the corefile
if [[ ! -f $DIR/var/spool/abrt/$CRASHID/coredump ]]
then
    prompt='y'
    echo "Warning: 'coredump' does not exist"
fi

# Test for the existence of the executable
if [[ ! -f $DIR/var/debesys/cache/apps/${RECIPE}/debesys-${HASH}-ocs/bin/${BINARY} ]]
then
    prompt='y'
    echo "Warning: $BINARY not found"
fi

if [[ $prompt == 'y' ]]
then
    echo -n "Continue (y/n)? "
    read yno
    if [[ $yno != 'y' ]]
    then
        exit
    fi
fi

if [[ ! -f $BINARY.backtrace ]]
then
    echo -n "Generate backtrace file (y/n)? "
    read yno
    if [[ $yno == "y" ]]
    then
        gdb --batch --quiet -ex "set substitute-path /home/jenkins/fsroot/debrepo $REPO" -ex "set substitute-path /home/jenkins/debrepo $REPO" -ex "directory $REPO" -ex "set solib-search-path $SOPATH:$DIR" -ex "set solib-absolute-prefix $DIR" -ex "file $DIR/var/debesys/cache/apps/${RECIPE}/debesys-${HASH}-ocs/bin/${BINARY}" -ex "core-file $DIR/var/spool/abrt/$CRASHID/coredump"  --ex "thread apply all bt full" -ex "quit" > $BINARY.backtrace
        echo "$BINARY.backtrace written"
    fi
fi
 gdb -ex "set substitute-path /home/jenkins/fsroot/debrepo $REPO" -ex "set substitute-path /home/jenkins/debrepo $REPO" -ex "directory $REPO" -ex "set solib-search-path $SOPATH:$DIR" -ex "set solib-absolute-prefix $DIR" -ex "file $DIR/var/debesys/cache/apps/${RECIPE}/debesys-${HASH}-ocs/bin/${BINARY}" -ex "core-file $DIR/var/spool/abrt/$CRASHID/coredump" 
