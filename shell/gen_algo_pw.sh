#!/bin/bash
# 
# gen_algo_pw.sh - This is intended as an algorithmic way to generate initial passwords
#
# - mjbroekman
MYUSERNAME=$1
MYHOSTNAME=$2
MYHOSTADDR=$3
DATE=$4
MD5="md5"
SHA512="shasum -a 512"
PW1=`echo -n $MYUSERNAME$DATE | $MD5 | cut -c-5`
O1=`echo $MYHOSTADDR | awk -F\. '{ print $1 }'`
O2=`echo $MYHOSTADDR | awk -F\. '{ print $2 }'`
O3=`echo $MYHOSTADDR | awk -F\. '{ print $3 }'`
O4=`echo $MYHOSTADDR | awk -F\. '{ print $4 }'`
O1=$(( $O1 % 120 ))
O2=$(( $O2 % 120 ))
O3=$(( $O3 % 120 ))
O4=$(( $O4 % 120 ))
PW2=`echo -n $DATE$MYUSERNAME$MYHOSTNAME | $SHA512  | awk '{ print $1 }' | cut -c${O1}-$(( $O1 + 5 )),${O2}-$(( $O2 + 5 )),${O3}-$(( $O3 + 5 )),${O4}-$(( $O4 + 8 ))`

echo ${PW1}-${PW2}

unset MYUSERNAME MYHOSTNAME MYHOSTADDR PW1 O1 O2 O3 O4 PW2
