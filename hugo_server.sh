#!/bin/bash
WSL2_IPADDRESS=$(ip addr show eth0 | grep "inet\b" | awk '{print $2}' | cut -d/ -f1)
hugo server --bind $WSL2_IPADDRESS --baseURL=http://$WSL2_IPADDRESS -D -F --gc -w
