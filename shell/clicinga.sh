#!/bin/bash
#
# Description:
#   Command line tool to report on icinga alerts

IFS=$'\n'

icingaUser=$LOGNAME
icingaPw=`~/scripts/getpass.py icinga $icingaUser`
# icingaSSU="https://icinga.DOMAIN/icinga/cgi-bin/status.cgi?host=all&servicestatustypes=28&hoststatustypes=15&serviceprops=42&csvoutput"
icingaSSU="https://icinga.DOMAIN/icinga/cgi-bin/status.cgi?host=all&servicestatustypes=28&hostprops=42&hoststatustypes=15&serviceprops=42&csvoutput"
icingaHSU="https://icinga.DOMAIN/icinga/cgi-bin/status.cgi?hostgroup=all&style=hostdetail&hoststatustypes=12&hostprops=10282&csvoutput"
icingaHDU="https://icinga.DOMAIN/icinga/cgi-bin/extinfo.cgi?type=1&csvoutput&host="

curltmp="/tmp/tmpfile"
curlbin="/usr/bin/curl"
curlopts="-ks"

function svcreport {
    # Grab status info from cgi and store in var
    rm -f $curltmp
    touch $curltmp
    statusout=`$curlbin $curlopts --user $1:$2 $3 --output $curltmp`
    cat $curltmp | grep -v "SPACE FREE" | egrep '5/5|Attempt' | sed -e "s/'//g" -e "s/:$//g" >${curltmp}2
    statuslines=`wc -l ${curltmp}2 | awk '{ print $1 }'`
    statusout=`cat ${curltmp}2`

    statuslines=$(( $statuslines - 1 ))
    maxlines=$statuslines

    printf "\033[1;30;47m%s\033[0m\n" "$site ($statuslines service issues)"
    if [ $statuslines -gt 20 ]; then
        maxlines=20
    fi

    linecnt=0
    for i in $statusout; do
        echo $i | awk -F ";" '($3 == "CRITICAL") { printf "\033[1;37;41m"; }
                              ($2 ~ "DISK:") { $2="DISK"; }
                              /Status_Information/ { printf "\033[1;30;47m"; }
                              ($3 == "WARNING") { printf "\033[1;30;43m"; }
                              ($3 == "UNKNOWN") { printf "\033[1;37;45m"; }
                              END { printf ("%-15s %-13s %-8s %-15s %-0.80s", $1, $2, $3, $5, $7); print "\033[0m"; }'
    if [ $linecnt -gt $maxlines ]; then
        printf "\033[1;30;47m%s\033[0m\n" "$(( $statuslines - $linecnt )) more ..."
        break
    fi
    linecnt=$(( $linecnt + 1 ))
    done    
}

function svrreport {
    # Grab status info from cgi and store in var
    rm -f $curltmp
    touch $curltmp
    statusout=`$curlbin $curlopts --user $1:$2 $3 --output $curltmp`
    statuslines=`wc -l $curltmp | awk '{ print $1 }'`
    statusout=`cat $curltmp | sed -e "s/'//g" -e "s/:$//g"`
    statuslines=$(( $statuslines - 1 ))

    printf "\033[1;30;47m%s\033[0m\n" "$site ($statuslines host issues)"
    for i in $statusout; do
        echo $i | awk -F ";" '($2 == "DOWN") { printf "\033[1;37;41m"; }
        /Status_Information/ { printf "\033[1;30;47m"; }
        ($3 == "WARNING") { printf "\033[1;30;43m"; }
        ($3 == "UNKNOWN") { printf "\033[1;37;45m"; }
        END{ printf ("%-15s %-13s %-20s %-20s %-0.60s", $1, $2, $3, $4, $5); print "\033[0m"; }'
    done    
}

while /bin/true; do
    for u in domainA domainB
      do
        clear
        case $u in
            domainA*) site="locationA" ;;
            domainB*) site="locationB" ;;
        esac
        svrreport $icingaUser $icingaPw ${icingaHSU//DOMAIN/$u} $site
        echo
        svcreport $icingaUser $icingaPw ${icingaSSU//DOMAIN/$u} $site
        sleep 30
    done
    sleep 30
done
