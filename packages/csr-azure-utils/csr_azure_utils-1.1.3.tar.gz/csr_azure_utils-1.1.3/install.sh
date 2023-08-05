#!/bin/sh
# Install tools and programs to run the CSR in the cloud
#

# Set up a directory tree for HA
if [ ! -d $HOME/cloud ]; then
    sudo mkdir $HOME/cloud
    sudo chown guestshell $HOME/cloud
fi

if [ ! -d $HOME/cloud/authMgr ]; then
    sudo mkdir $HOME/cloud/authMgr
    sudo chown guestshell $HOME/cloud/authMgr
fi

auth_dir="$HOME/cloud/authMgr/"

install_log="$auth_dir/install.log"

echo "Installing the Azure utilities package" >> $install_log

# Set up the path to python scripts
#echo 'export PYTHONPATH=$HOME/.local/lib/python2.7/site-packages/csr_cloud' >> $HOME/.bashrc
echo 'export PATH=$HOME/.local/bin:$HOME/.local/lib/python2.7/site-packages/csr_cloud:$PATH' >> $HOME/.bashrc
source $HOME/.bashrc

echo "Show the current PATH" >> $install_log
echo $PATH >> $install_log
echo "Show the current PYTHONPATH" >> $install_log
echo $PYTHONPATH >> $install_log
