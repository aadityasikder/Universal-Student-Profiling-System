#!/bin/bash

# Command to change permissions
command="sudo chmod 666 /dev/ttyACM0"

# Password
password="jetson"

# Sending the command along with the password
echo "$password" | sudo -S $command

# Exit with the status of the last executed command
exit $?

