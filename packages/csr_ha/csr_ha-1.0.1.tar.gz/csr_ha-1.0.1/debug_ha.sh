#!/bin/sh

# Use this script to create a tar ball of debug information for the csr_ha package
directory=$(find ~/cloud/ -name HA)
ha_status="$directory/ha_status.log"
tar_file=""$directory/ha_debug.tar""
system_logs="$directory/gs_system.log"

# Write the status of each of the daemon processes running under guestshell
systemctl status csr_ha.service >> $ha_status
crontab -l >> $ha_status

echo "Current process information" >> $system_logs
ps -ef >> $system_logs

#Collecting the system logs for Guestshell
echo "Current system logs: " >> $system_logs
sudo cat /var/log/messages >> $system_logs

# Gather all the log files together in a tar ball
cd ~/


pip freeze >> $ha_status

# Need to add the logging ~/logs/ dir once the feature agnostic logging architecture is finalized
tar -c cloud/* --exclude=sock* --exclude=*revert_nodes.sh >> $tar_file

# Compress the file
gunzip -r $tar_file

# Copy the file to /bootflash
cp $directory/ha_debug.tar /bootflash

# Clean up
rm $ha_status
