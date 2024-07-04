
"""
    This script is for download satellite data from colhub.met.no.
    As the new data access system, Copernicus Data Space Ecosytem (CDSE), 
    is implimented to Norwegian collaborative hub (colhub.met.no)
 
    Created by: Pipatthra Saesin (pip@niva.no)
    Created date: 14 June 2024 
 

"""

from sentinelsat import read_geojson, geojson_to_wkt
import requests # to send through POST to the server
from urllib.parse import quote # to encode password if needed
from userAccountColhub import d
import xmltodict
import os

# get username and password from userAccountColhub
username = d['username']
password = d['password']

#footprint = geojson_to_wkt(read_geojson('Oslofjord_test.geojson')) 
startdate = "2024-06-01"
enddate   = "2024-06-12"
platformname = 'Sentinel-3'
cloudcover = 30
# For Sentinel-2 tile variable is 'tile number' of ROI e.g. 'T32VNM'
# For Sentinle-3 tile variable is the 'frame' of ROI e.g. '_1980' 
tile = '_1620_'

if platformname == 'Sentinel-2':
    producttype  = '_MSIL1C_'
elif platformname == 'Sentinel-3':
    producttype = ['_OL_1_EFR____', '_OL_1_ERR____']

def make_search_link(startdate, enddate, platformname, producttype, tile, cloudcover = 30):
    if platformname == 'Sentinel-2':
        #platformfilter = "(platformname:"+platformname+' AND producttype:'+ producttype+")"
        search_url = "https://colhub.met.no/odata/v1/Products?$filter=ContentDate/Start gt datetime'"+startdate+"T00:00:00' and ContentDate/Start lt datetime'" + enddate +"T23:59:59' and substringof('" + producttype +"',Name) and substringof('" + tile +"',Name)" 
        # and ContentGeometry"
    elif platformname == 'Sentinel-3':
        #platformfilter = "(platformname:"+platformname+' AND producttype:'+ producttype+ " AND cloudcoverpercentage:[0 TO " + str(cloudcover) + "])"
        search_url = "https://colhub.met.no/odata/v1/Products?$filter=ContentDate/Start gt datetime'"+startdate+"T00:00:00' and ContentDate/Start lt datetime'" + enddate +"T23:59:59' and substringof('" + tile + "',Name) and substringof('" + producttype[0] +"',Name) or substringof('" + producttype[1] + "',Name)"
    return search_url


search_url = make_search_link(startdate, enddate, platformname, producttype, tile,cloudcover)
print(search_url)
response = requests.get(search_url, auth=(username, password))
productlist = xmltodict.parse(response.content)['feed']['entry']
targetpath = r"C:\Users\pip\OneDrive - NIVA\RemoteSensing\Github_scripts\colhub_test\\"
for i in range(0, 2):
    id = productlist[i]['id']
    urlid = id+'/$value'
    print(urlid)
    productid = requests.get(urlid, auth=(username, password))
    print('get productid')
    productfilename = productlist[i]['title']['#text']+'.zip'
    print('Downloading :', productfilename)
    with open(os.path.join(targetpath, productfilename), 'wb') as fd:
        fd.write(productid.content)
