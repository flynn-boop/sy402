#!/usr/bin/python3
import os
import hashlib
from datetime import datetime
import sys
import json
nohash=["/dev/","/proc/","/run/","/sys/", "/usr/bin/", "/usr/share/help/", "/var/lib/", "/var/run/", "/tmp/", "/lib/", "/sys/"]

d=dict()
file_list=[]

def get_files(path):
    entries=os.listdir(path)
    for f in entries:
        fl=path+f
        if (os.path.isdir(fl)):
            fl=fl+'/'
            if(fl not in nohash):
                get_files(fl)
        else:
            file_list.append(fl)

def get_hash():
    
    now=datetime.now()
    time=now.strftime("%m/%d/%Y %H:%M")
    for f in file_list:
        try:
            
            fh=open(f, 'rb')
            b=fh.read()
            h=hashlib.sha256(b).hexdigest()
            d[f]=(h,time)
        except:
#            print(f,"couldn't be hashed")
            pass


def main():
    if (len(sys.argv)==2):
        get_files("/")
        get_hash()
        fh_out=open(sys.argv[1], 'w')
        json.dump(d,fh_out)
                
    elif(len(sys.argv)==3):
        fh_in=open(sys.argv[2],'r')
        old=json.load(fh_in)
        get_files("/")
        get_hash()
        fh_out=open(sys.argv[1], 'w')
        json.dump(d,fh_out)

        old_files=list(old.keys())

        newfiles=[]
        
        
        changed=[]
        for k in d.keys():
            if( k in old_files):
                if (d[k][0]!=old[k][0]):
                    changed.append(k)
            else:
                newfiles.append(k)
        l_change=len(changed)
        print("\n______RESULTS")
        print(l_change, "files changed")
    
        old_hashes=[]
        old_time=[]
        moved=[] #moved to
        movedtime=[]
        movedfrom=[]
        for f in old_files:
            old_hashes.append(old[f][0])
        
        for f in newfiles:
            if d[f][0] in old_hashes:
                newfiles.remove(f)
                moved.append(f)
                h=d[f][0]
                ind=old_hashes.index(h)
                oldf=old_files[ind]
                movedfrom.append(oldf)
                movedtime.append(old[oldf][1])  

        del old_files
        del old_hashes
        removed=[]
        for k in old.keys():
            if(k not in d.keys()):
                removed.append(k)
                
        n_newfiles=len(newfiles)
        print(n_newfiles, "newfiles")

        n_mov=len(moved)
        print(n_mov, "moved")
        r_len=len(removed)
        print(r_len, "removed")
        
        
        print("\n\n____________Moved")
        print("FROM____________TO_________AFTER")
        for x in range(0, len( moved)):
            print(moved[x],"\t", movedfrom[x],'\t', movedtime[x] )
        print("\n\n ___________Changed")
        for f in changed:
            print(f)
        print("\n\n____________Removed")

        for f in removed:
            print(f)
        print("\n\n____________Newfiles")
        for f in newfiles:
            print(f)



    else:
        print("improper arguements. first arguement is filename to save hashes, second is optional and is a previous file of saved hashes")



main()
