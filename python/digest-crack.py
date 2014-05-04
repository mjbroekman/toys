#!/usr/bin/env python
'''
A _very_ basic http digest cracker.  Like ridiculously basic.  Doesn't work well with large password character lists.

Mostly just to show theory than be an actual, effective, tool.

Written to solve the Cracking Digest Authentication challenge on Pentester Academy (http://www.pentesteracademy.com/video?id=173)

Author:  Maarten Broekman
'''
import os, sys, getopt, random, string, hashlib, itertools

# def passwd_combos(alpha,plen):
#     pass_list = []
#     idx = 0

#     while idx < plen:

#     for char in alpha:
#         return char + passwd_combos(alpha,(plen - 1))
#     # passwd = []
#     # idx = 0
#     # while idx < plen:
#     #     passwd.append(alpha)
#     #     idx += 1

#     # return passwd


try:
    opts, args = getopt.getopt(sys.argv[1:],"", ["alpha=","length=","cnonce=","nonce=","count=","user=","realm=","qop=","response=","method=","uri="])
except getopt.GetoptError:
    print 'digest-crack --alpha char --length passwd_length --cnonce client_nonce --nonce server_nonce --count request_count --user username --realm realm --qop qop --response response --method http_method --uri uri'
    sys.exit(2)

cnonce = nonce = cnt = user = realm = qop = resp = uri = meth = ""
alpha = ""
plen = 0

for opt,arg in opts:
    if opt == "--cnonce":
        cnonce = arg
    if opt == "--nonce":
        nonce = arg
    if opt == "--count":
        cnt = arg
    if opt == "--user":
        user = arg
    if opt == "--realm":
        realm = arg
    if opt == "--qop":
        qop = arg
    if opt == "--response":
        resp = arg
    if opt == "--uri":
        uri = arg
    if opt == "--method":
        meth = arg
    if opt == "--alpha":
        alpha += arg
    if opt == "--length":
        plen = int(arg)

if len(alpha) == 0:
    alpha = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation

if meth == "" or cnonce == "" or nonce == "" or cnt == "" or user == "" or realm == "" or resp == "" or uri == "":
    print 'Missing arguments.'
    print 'digest-crack --alpha char_string --length passwd_length --cnonce client_nonce --nonce server_nonce --count request_count --user username --realm realm --qop qop --response response --method http_method --uri uri'
    sys.exit(2)
if plen == 0:
    print 'Impossible password length'
    print 'digest-crack --alpha char --length passwd_length --cnonce client_nonce --nonce server_nonce --count request_count --user username --realm realm --qop qop --response response --method http_method --uri uri'
    sys.exit(2)

combs = len(alpha) ** plen
print "Traversing " + str(combs) + " combinations."

ha2 = hashlib.md5()
ha2.update(meth.upper() + ":" + uri)
ha2hex = ha2.hexdigest()
dot_out = int( combs / 100 )
pct = 0
for passwd in list(itertools.product(list(alpha),repeat=plen)):
    if pct % dot_out == 0:
        sys.stdout.write('.')

    pswd = "".join(passwd)
    ha1 = hashlib.md5()
    ha1.update(user + ':' + realm + ':' + pswd)
    ha3 = hashlib.md5()
    ha3.update(ha1.hexdigest() + ":" + nonce + ":" + cnt + ":" + cnonce + ":" + qop + ":" + ha2hex )
    if resp == ha3.hexdigest():
        print ''
        print "Password hit at",pct,"(",float((pct*100.0)/combs),"%)"
        print resp,'==',ha3.hexdigest()
        print 'Password='+pswd
        break

    pct = pct + 1


