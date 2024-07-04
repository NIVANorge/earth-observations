""" 
Created on 20190920
@author: Dimitry Van der Zande
Download S2 or S3 files from CREODIAS
change your username/password in get_keycloak_token
modified by: Anna Birgitta Ledang (abl@niva.no) and Elizaveta Protsenko (elpa@niva.no)
"""
import wget
import json
import datetime
import requests
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--s2",
                    action = "store_true")
parser.add_argument("--s3",
                    action = "store_true")

parser.add_argument("--region", required=True) 
args = parser.parse_args()
region = args.region
# example of argument python downloadFromCreodias.py --s2 --region T32VNL

def URLread(fpath):
    TS = []
    with open(fpath) as file:
        for line in file:
            line = line.strip()
            TS.append(line)
    return TS

def get_keycloak_token():
    h = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    from userAccount import d
    resp = requests.post('https://auth.creodias.eu/auth/realms/dias/protocol/openid-connect/token', data=d, headers=h)
    return json.loads(resp.content.decode('utf-8'))['access_token']

'''
making the script more generic and taking arguments for which satellite sensor and region. 
'''
if args.s2: 
    sat_type = 's2'
    targetfolder = r'W:\Satellite\{}\L1\zip\{}'.format(sat_type,region)

elif args.s3:
    sat_type = 's3'
    #if args.ro1980:
    #    ro = '_1980'
    targetfolder = r'W:\Satellite\{}\L1\zip\{}'.format(sat_type,region)


fpathlinks = r'D:\Prosjekt\satelitt\dev_import_creodias\listOfUrls{}.txt'.format(sat_type)


#read URLfile
URLs = URLread(fpathlinks)

#get token (valid for 600 seconds, approx 25 files)
key = get_keycloak_token()
keytime = datetime.datetime.now()

#download URLfiles
URLsdownload = list.copy(URLs)
tries = 0
#while (len(URLsdownload) > 0 and tries < 10):
while (len(URLsdownload) > 0 and tries < 10):
    tries = tries + 1
    print('Number of tries: ' + str(tries))
    ndown = 1
    URLsfailed = []
    for url in URLsdownload:
        if len(url) > 0:
            print(' Downloading file ',ndown ,' of ',len(URLsdownload))
            print(key['properties']['title'])

            #cut key from URL
            url_short = url[0:79]
            url_pluskey = url_short + key

            #determine activity of key (600s activity)
            timecurr = datetime.datetime.now()
            timediff = (timecurr - keytime).seconds

            if timediff < 500:
                try:
                    time.sleep(15)
                    print(targetfolder)
                    #if not exists(targetfolder):
                    print(key['properties']['title'])
                    wget.download(url_pluskey, out=targetfolder)
                    
                    #elif exists(targetfolder):
                    #    print (url_pluskey + ' already exist in ' + targetfolder)
                except:
                    print('error')
                    URLsfailed.append(url_pluskey)
                ndown = ndown + 1
            else:
                key = get_keycloak_token()
                keytime = datetime.datetime.now()
                url_pluskey = url_short + key
                try:
                    time.sleep(15)
                    #if not exists(targetfolder):
                    wget.download(url_pluskey, out=targetfolder)
                    #elif exists(targetfolder):
                    #print (url_pluskey + ' already exist in ' + targetfolder)
                except:
                    print('error')
                    URLsfailed.append(url_pluskey)
                ndown = ndown + 1
    URLsdownload = list.copy(URLsfailed)
if len(URLsfailed) > 0:
    print('not all files have been downloaded')
    print(URLsfailed)
else:
    print('all files have been downloaded correctly')
# END -------------
