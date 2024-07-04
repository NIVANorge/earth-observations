'''
Created on 12. okt. 2018
Author: ABL
Updated: 19.08.2020
'''
# connect to the API
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
import datetime
from datetime import date, timedelta
from os import listdir
from userAccountColhub import d
from util import S2_settings_table, S3_settings_table
import argparse
#import datetime
from geojson import Polygon

import json

api = SentinelAPI(d['username'], d['password'],d['apiAddress'])


def download_data(producttype, region, trgDir):
    start = datetime.datetime.strptime("01-08-{}".format(year_of_download), "%d-%m-%Y")
    end = datetime.datetime.strptime("01-10-{}".format(year_of_download), "%d-%m-%Y")
    # all dates that need to be downloaded 
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

    track_month = 4 
    list_or_err = []

    print ('progress file in download data func', progress[str(year_of_download)][str(region)])

    for dato in date_generated:
        # Since there is a regulation by api on the dates that can be downloaded at once
        # We are looping over teh dates, one date per time is downloaded 
            #progress[str(year_of_download)][str(rregion)]
        year = dato.year
        startmonth = dato.month
        print ('before check', track_month, dato.month)
        #endmonth = dato.month
        startday = dato.day
        #endday = dato.day
        startdate = str(year) + str(startmonth) + str(startday)
        enddate = date(year, int(startmonth), int(startday)) + timedelta(days=1)
        '''if dato.month not in progress[str(year_of_download)][str(region)]:
            print(dato.strftime("%d-%m-%Y"))






            if dato.month > track_month: 
                print ('new month is', dato.month)
                #print (progress[str(year_of_download)][str(rregion)])
                if track_month not in progress[str(year_of_download)][str(region)]:
                    progress[str(year_of_download)][str(region)].append(track_month)
                    print ('Updated progress file', progress)
                    json_file.seek(0)
                    json.dump(progress_file, json_file,indent = 4)
            track_month = dato.month 

        '''
            
        # Query the data with products available for the chosen date 
        if platformname == 'Sentinel-2':
            print ('in sent 2')
            # here is where we actually query the data 
            products = api.query(date=(startdate, enddate),platformname=platformname, 
                            producttype=producttype, filename = r'*_{}_*'.format(region))

        elif platformname == 'Sentinel-3':
            footprint = geojson_to_wkt(read_geojson('southernNorway.geojson'))
            products = api.query(footprint, date=(startdate, enddate),platformname=platformname, 
                            producttype=producttype, filename = r'*_{}_*'.format(region))           

        nfiles = listdir(trgDir)
        print ('trgDir',trgDir)

        for key,val in products.items(): 
            #print(key)
            filnavn = val['filename'] 
            filnavn = filnavn[0:-4] + 'zip'
            # Check if the file is already downloaded 
            if filnavn in nfiles:
                print(filnavn, "already in folder")
            else:
                if 'DTERRENGDATA' not in filnavn: 
                    # filter out these files since they don't fit our needs 
                    print (filnavn, 'start downloading at:', datetime.datetime.now())
                    try:
                        api.download(key,directory_path=trgDir)
                    except: 
                        list_or_err.append(filnavn)
        '''else:
            print ('This month {} for region {} , year {} is already downloaded'.format(track_month, region,year_of_download))  

            if dato.month > track_month: 
                print ('new month is', dato.month)
                #print (progress[str(year_of_download)][str(rregion)])
                #progress[str(year_of_download)][str(region)].append(track_month)
                
                track_month = dato.month                
                #print ('Updated progress file', progress)
                #json_file.seek(0)
                #json.dump(progress_file, json_file,indent = 4)


        if track_month == 9 and track_month not in progress[str(year_of_download)][str(region)]:
            progress[str(year_of_download)][str(region)].append(track_month)
            json_file.seek(0)
            json.dump(progress_file, json_file,indent = 4)'''

    return list_or_err    


def download_data_svalbard(producttype, region, trgDir):
    start = datetime.datetime.strptime("01-08-{}".format(year_of_download), "%d-%m-%Y")
    end = datetime.datetime.strptime("01-10-{}".format(year_of_download), "%d-%m-%Y")
    # all dates that need to be downloaded 
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

    product_types = {
        'Sentinel-2':'S2MSI1C',
        'Sentinel-3':'OL_1_EFR___'
    } 

    track_month = 4 
    list_or_err = []

    print ('progress file in download data func', progress[str(year_of_download)][str(region)])

    for dato in date_generated:
        # Since there is a regulation by api on the dates that can be downloaded at once
        # We are looping over teh dates, one date per time is downloaded 
            #progress[str(year_of_download)][str(rregion)]
        year = dato.year
        startmonth = dato.month
        print ('before check', track_month, dato.month)

        startday = dato.day
        startdate = str(year) + str(startmonth) + str(startday)
        enddate = date(year, int(startmonth), int(startday)) + timedelta(days=1)

            
        # Query the data with products available for the chosen date 
        if platformname == 'Sentinel-2':
            print ('in sent 2')
            # here is where we actually query the data 
            products = api.query(date=(startdate, enddate),platformname=platformname, 
                            producttype=producttype, filename = r'*_{}_*'.format(region))

        elif platformname == 'Sentinel-3':
            footprint = geojson_to_wkt(read_geojson('SIOS_buoy.geojson'))

            products = api.query(footprint, date=(startdate, enddate),platformname=platformname, 
                            producttype=producttype, filename = r'*_{}_*'.format(region))           

        nfiles = listdir(trgDir)
        print ('trgDir',trgDir)

        for key,val in products.items(): 
            #print(key)
            filnavn = val['filename'] 
            filnavn = filnavn[0:-4] + 'zip'
            # Check if the file is already downloaded 
            if filnavn in nfiles:
                print(filnavn, "already in folder")
            else:
                if 'DTERRENGDATA' not in filnavn: 
                    # filter out these files since they don't fit our needs 
                    print (filnavn, 'start downloading at:', datetime.datetime.now())
                    try:
                        api.download(key,directory_path=trgDir)
                    except: 
                        list_or_err.append(filnavn)
        '''else:
            print ('This month {} for region {} , year {} is already downloaded'.format(track_month, region,year_of_download))  

            if dato.month > track_month: 
                print ('new month is', dato.month)
                #print (progress[str(year_of_download)][str(rregion)])
                #progress[str(year_of_download)][str(region)].append(track_month)
                
                track_month = dato.month                
                #print ('Updated progress file', progress)
                #json_file.seek(0)
                #json.dump(progress_file, json_file,indent = 4)


        if track_month == 9 and track_month not in progress[str(year_of_download)][str(region)]:
            progress[str(year_of_download)][str(region)].append(track_month)
            json_file.seek(0)
            json.dump(progress_file, json_file,indent = 4)'''

    return list_or_err  


def get_all_parameters():
    producttype = product_types[platformname] 
    if platformname == 'Sentinel-2':
        region = S2_settings_table[region_id]['tile']
        trgDir=r'W:\Satellite\S2/L1/zip/{}'.format(region)

    elif platformname == 'Sentinel-3': 
        region = S3_settings_table[region_id]['scene']
        
        trgDir=r'W:\Satellite\S3/L1/zip/_{}'.format(region)   
    
    return producttype, region, trgDir 

if __name__ == '__main__':
    case = None 




    startdate = '20200618'
    enddate = '20200926'
    import pandas as pd
    #date_range = pd.date_range(start='18/06/2020', end='26/09/2020')
    #print (date_range[0])
    footprint = geojson_to_wkt(read_geojson('SIOS_buoy.geojson')) 

    platformname = 'Sentinel-2'
    trgDir = f'W:\\Svlbrd\\{platformname}'

       # 1C is a level 1C
    product_types = {
        'Sentinel-2':'S2MSI1C',
        'Sentinel-3':'OL_1_EFR___',
        'Sentinel-3':'OL_1_LRR___'
    }    
    producttype =product_types[platformname] 
    # At least for Sentinel-3 querying for the whole region works.
    # So maybe the problem with querying periods longer than 1 day is only the S2 case 
    products = api.query(footprint,
                    date=[startdate,enddate],
                    platformname=platformname, 
                    cloudcoverpercentage=(0, 30),            
                    producttype=producttype)
                    #,
                    #filename = r'*_{}_*'.format(region))  

    print (len(products.items()))
    nfiles = listdir(trgDir)
    print (nfiles)
    import os
    for key,val in products.items(): 
        # ADD FILTERING FOR LRR OR LNR 
        # ALSO RT( R)

        print (val['filename'] )
        filename = val['filename'] 
        filename = filename[0:-4] + 'zip'
        # Check if the file is already downloaded 
        if 'DTERRENGDATA' not in filename: 
            if os.path.isfile(trgDir+ r'\\'+ filename):
                pass 
                print(filename, "already in folder")
            else:
                try:
                    api.download(key,directory_path=trgDir)     
                except Exception as e: 
                    print (e)

    

    '''api.download_all(products, directory_path=f'W:\\Svlbrd\{platformname}',
                     max_attempts=10, 
                     checksum=True, n_concurrent_dl=2, lta_retry_delay=600)'''
    #for key,val in products.items():
    #    #for k in val.keys():
    #    print (val['producttype'])
        
    if case == 'satmdirr': 
        all_plaftorms = ['Sentinel-2','Sentinel-3'] 
        #download_all = True 
        parser = argparse.ArgumentParser()

        parser.add_argument("--all", required = False, action = "store_true") 


        parser.add_argument("--region", required=False) 
        parser.add_argument("--year", required=False)
        parser.add_argument("--platform", required=False)
        args = parser.parse_args()

        download_all = args.all

        product_types = {
            'Sentinel-2':'S2MSI1C',
            'Sentinel-3':'OL_1_EFR___'
        } 

        if not download_all : 
            print ('not all')
            # Example: python downloadFromColhub --region 1 --year 2020 --platform S3

            parser = argparse.ArgumentParser()
            parser.add_argument("--region", required=True) 
            parser.add_argument("--year", required=True)
            parser.add_argument("--platform", required=True)
            args = parser.parse_args()

            region_id = args.region
            year_of_download = args.year
            
            if args.platform == 'S2':
                platformname = 'Sentinel-2'
            elif args.platform == 'S3':
                platformname = 'Sentinel-3'
            print (args.platform)
            with open('progress.json', "r+") as json_file:
                progress_file = json.load(json_file)
                progress = progress_file[platformname]        

                producttype, region, trgDir = get_all_parameters()
                list_of_err = download_data(producttype, region, trgDir)
            
        else:
            # 'Sentinel-2'] 

            #
            years = ['2017','2018','2019','2020']



#import configparser
'''with open('progress.json', "r+") as json_file:
progress_file = json.load(json_file)

for platformname in all_plaftorms:
if platformname == 'Sentinel-3':
all_regions = S3_settings_table.keys() 
elif platformname == 'Sentinel-2':
all_regions = S2_settings_table.keys() 

progress = progress_file[platformname]'''

#progress['downloaded_years'].append(999)

#json_file.seek(0)
#json.dump(progress_file, json_file,indent = 4)
'''for year_of_download in years:

print ('year loop ', year_of_download) 

for region_id in all_regions:
pproducttype, rregion, ttrgDir = get_all_parameters() 
print ('Region loop:', rregion)

all_months = [4,5,6,7,8,9]
all_months_in = set(progress[str(year_of_download)][str(rregion)]) == set(all_months)
#if 'region' not in progress[str(year_of_download)].keys():


print ('all_months_in', all_months_in)
print (set(all_months)  )                  
print (set(progress[str(year_of_download)][str(rregion)]) == set(all_months))

#progress[str(year_of_download)][str(rregion)] = []
json_file.seek(0)
json.dump(progress_file, json_file,indent = 4)     

if not all_months_in:
list_of_err = download_data(pproducttype, rregion, ttrgDir)
print('finished downloading. errors in files:', list_of_err)
#progress[str(year_of_download)].append(rregion)
#json_file.seek(0)
#json.dump(progress_file, json_file,indent = 4)
else:
print (rregion, 'for year', year_of_download, 'is already downloaded', platformname)'''
            