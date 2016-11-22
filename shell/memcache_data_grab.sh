#!/bin/bash

DATE=`date +%s`

ps -aef     >./memcached.`hostname`.$DATE.ps-aef 2>&1
ps auxwww   >./memcached.`hostname`.$DATE.psauxwww 2>&1
netstat -an >./memcached.`hostname`.$DATE.netstat-an 2>&1
sysctl -a   >./memcached.`hostname`.$DATE.sysctl-a 2>&1
crm_mon -1  >./memcached.`hostname`.$DATE.crm_mon-1 2>&1
lsof        >./memcached.`hostname`.$DATE.lsof 2>&1

