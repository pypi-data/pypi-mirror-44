#!/bin/sh

# Set up the path to python scripts
source ~/.bashrc

# Call the python script to revert all nodes
python ~/.local/lib/python2.7/site-packages/csr_ha/client_api/node_event.py -i all -e revert
