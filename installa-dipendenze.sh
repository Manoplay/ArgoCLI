#!/usr/bin/env bash
if [ "$(which apt)" == "" ]; then
    sudo dnf install python-pip
else
    sudo apt install python-pip
fi
sudo pip install -g argoscuolanext prompt_toolkit requests