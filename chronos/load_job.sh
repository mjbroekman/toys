#!/bin/bash

# HOST="zookeeper.domain.tld:8081/scheduler/iso8601"
# CURL="curl -L -H 'Content-Type: application/json' -X POST -d '`cat $1`' $HOST"

# echo $CURL
# $CURL

set -o noglob
IFS="
"
for j in `cat $1 | grep -v "PATH = " | grep -v ^\#`; do
    if [ "$j" != "${j//PATH = /}" ]; then
        continue
    fi
    omin=`echo $j | awk '{ print $1 }'`
    ohr=`echo $j | awk '{ print $2 }'`
    command=`echo $j | sed -e 's/\t/ /g' | sed -e 's/\t/ /g' | sed -e 's/  */ /g' | cut -d' ' -f6- | awk -F\> '{ print $1 }' | sed -e 's/2$//g'`
    interval=""
    if [ "$omin" != "${omin//,/}" ]; then
        firstmin=`echo $omin | awk -F, '{ print $1 }'`
        secmin=`echo $omin | awk -F, '{ print $2 }'`
        intmin=$(( $secmin - $firstmin ))
        interval="PT${intmin}M"
    elif [ "$omin" != "${omin//\//}" ]; then
        intmin=`echo $omin | awk -F/ '{ print $2 }'`
        interval="PT${intmin}M"
    fi

    if [ "$ohr" != "${ohr//\//}" ]; then
        intmin=`echo $ohr | awk -F/ '{ print $2 }'`
        interval="PT${intmin}H"
    fi

    minute=`echo $omin | awk -F, '{ print $1 }'`
    minute=`echo $minute | awk -F/ '$2 !~ /^$/ { print $2 } $2 ~ /^$/ { print $1 }'`
    hour=`echo $ohr | awk -F/ '$2 !~ /^$/ { print $2 } $2 ~ /^$/ { print $1 }'`

    if [ "$ohr" != "*" -a "$ohr" = "${ohr//\//}" ]; then
        hour=$(( $ohr + 4 ))
    fi

    if [ "$omin" = "*" -a -z "$interval" ]; then
        interval="PT1M"
    fi

    if [ "$omin" = "*" ]; then
        minute=$(( `date +%M` + 1 ))
    fi

    if [ "$ohr" = "*" -a -z "$interval" ]; then
        interval="PT1H"
    fi

    if [ "$ohr" = "*" ]; then
        hour=$(( `date -u +%H` + 1 ))
    fi

    if [ "$ohr" = "*" -a -z "$interval" ]; then
        interval="PT1H"
    fi

    if [ -z "$interval" ]; then
        interval="PT24H"
    fi
    
    dst=`date +R/%Y-%m-%dT`
    dyear=`date +%Y`
    dmon=`date +%m`
    dday=`date +%d`

    nhr=`date -u +%H`
    nmin=`date +%M`

    if [ $hour -lt 10 ]; then
        hour="0$hour"
    fi

    if [ $minute -lt 10 ]; then
        minute="0$minute"
    fi

    command=`echo $command | sed -e 's/ $//g'`
    name=`echo $command | awk -F/ '{ print $NF }' | sed -e 's/--//g' -e 's/=/-/g' | sed -e 's/.pl / /g' -e 's/.py / /g' -e 's/.sh / /g' | sed -e 's/.pl$//g' -e 's/.py$//g' -e 's/.sh$//g' | sed -e 's/ $//g'`
    name=`echo $name | sed -e 's/ / - /g'`

    echo "=============================================================="
    echo "Original : $j"
    echo "--------------------------------------------------------------"
    echo "curl -L -H 'Content-Type: application/json' -X POST -d '{\"schedule\": \"R/$dyear-$dmon-${dday}T$hour:$minute:00Z/$interval\",\"name\": \"$name\",\"command\": \"$command\",\"owner\": \"owner@domain.tld\",\"async\": false}' zookeeper.domain.tld:8081/scheduler/iso8601"
    echo "=============================================================="
done
