# Module for downloading Sentinel satellite images from the 
# Copernicus Open Access Hub https://scihub.copernicus.eu/

from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
import datetime
from datetime import date, timedelta
import os
from geojson import Polygon
from userAccountColhub import d



def query_products(footprint,startdate,enddate,producttype,maxclouds=100):

    # At least for Sentinel-3 querying for the whole region works.
    # So maybe the problem with querying periods longer than 1 day is only the S2 case 

    products = api.query(footprint,
                    date=[startdate,enddate],
                    platformname=platformname, 
                    cloudcoverpercentage=(0, maxclouds),            
                    producttype=producttype)

    return products

def download_files(products,trgDir):
        for key,val in products.items(): 

            # ADD FILTERING FOR LRR OR LNR 
            # ALSO RT( R)

            print (val['filename'] )
            filename = val['filename'] 
            filename = filename[0:-4] + 'zip'
             
            if 'DTERRENGDATA' not in filename: 

                # Check if the file is already downloaded
                if os.path.isfile(trgDir+ r'\\'+ filename):
                    print(filename, "already in folder")
                else:
                    try:
                        api.download(key,directory_path=trgDir)     
                    except Exception as e: 
                        print (e)


if __name__ == '__main__':

    # connect to the API
    api = SentinelAPI(d['username'], d['password'],d['apiAddress'])

    startdate = '20200618'
    enddate = '20200926'
    maxclouds = 30 # Filter products by the cloud coverage (in %)

    # Specify the polygon for you area of interest
    # You can use http://geojson.io or 
    # https://www.keene.edu/campus/maps/tool/ to create a polygon 

    footprint = geojson_to_wkt(read_geojson('SIOS_buoy.geojson')) 

    platformname = 'Sentinel-2' #( Another option is Sentinel-3)

    product_types = {
        'Sentinel-2':'S2MSI1C',# 1C is a level 1C
        'Sentinel-3':'OL_1_EFR___',
        'Sentinel-3':'OL_1_LRR___'
    }    

    producttype = product_types[platformname] 

    # Specify path where you want to save the files 
    trgDir = f'W:\\Svlbrd\\{platformname}'


    products = query_products(footprint,startdate,enddate,producttype,maxclouds)
    download_files(products,trgDir)


    



    #for key,val in products.items():
    #    #for k in val.keys():
    #    print (val['producttype'])
        
