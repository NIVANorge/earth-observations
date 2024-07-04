# Module for downloading Sentinel satellite images from the 
# Copernicus Open Access Hub https://scihub.copernicus.eu/

import zipfile
import datetime
from datetime import date, timedelta
import os
from geojson import Polygon
from os import listdir
import shutil
from os.path import exists
#Sentinelsat makes searching, downloading and retrieving the metadata of Sentinel satellite images from the Copernicus Open Access Hub easy. 
#https://pypi.org/project/sentinelsat/
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt

import subprocess
# Put your credentials from 

try:
    from  userAccountColhub import d
except:

 d = {'apiAddress': 'https://colhub.met.no/',
    'username': 'lisapro',
    'password': ""}


# Path for the temporary folder, there will be saved temporary files for intermediate processing steps. 
tmp_work_folder = r'.\work'



# Path to the gpt program 
cmd_path_gpt = r'C:/Program Files/snap/bin/gpt.exe'
cmd_path_acolite = r'D:\\acolite_py_win\dist\\acolite\\acolite.exe'


def download_files(api,products,dataDir):
    for key,val in products.items(): 

        filename = val['filename'][0:-4] + 'zip' 

        if 'DTERRENGDATA' not in filename: 
            # Check if the file is already downloaded
            if os.path.isfile(dataDir+ r'\\'+ filename):
                print(filename, "already in folder")
            else:
                if 'T32VMP' in filename: 
                    print ('download correct tile')
                    try:
                        api.download(key,directory_path=dataDir)     
                    except Exception as e: 
                        print ('Exception', e)


def unzip_file(f):
    tmp_files = listdir(tmp_work_folder)
    print ('unzip')
    if len(tmp_files) > 0:
        print ('There are more than 1 file in the folder')
        shutil.rmtree(tmp_work_folder)
        print ('Cleared the work temp directory, continue .. ')
    try: 
        print(f)
        zip_ref = zipfile.ZipFile(f, 'r')
        zip_ref.extractall(tmp_work_folder)
        zip_ref.close()
        unzipped_folders = listdir(tmp_work_folder)
        
        #assert len(unzipped_folders) == 1, ('there are more than 1 file in the folder D:\S3\work')
        unzipped_folder = unzipped_folders[0]

        #OBS! I am not sure about 'MTD_MSIL1C.xml
        # The file we will be working with will be MTD_MSIL1C.xml , the same name on each folder 
        tmpff = os.path.join(tmp_work_folder,unzipped_folder,'MTD_MSIL1C.xml')  

    except zipfile.BadZipfile:
        print ("Bad Zip file for this path, skip",f)
        unzipped_folder,tmpff = None, None
    return(unzipped_folder,tmpff) 

def atmcorr_c2rcc_s2_2(Sl1cProduct,trgDIR,prop,filename):
    print ("in atmcorr_c2rcc_s2")
    
    targetname='C2RCC_idepix_' + Sl1cProduct[-80:-20] + '.nc'
    trgfname=os.path.join(trgDIR,targetname)
    #print (trgfname)
    
    if not exists(trgfname):
        wg = str(cmd_path_gpt + S2_atmcorr_c2rcc_step[0]) 
        print ('Running C2RCC on '  + Sl1cProduct)
        properties = properties_path + prop
        print ('properties',properties)
        cmdwget = '%s -p %s -t %s %s -f %s' %(wg, properties, trgfname, Sl1cProduct, 'NetCDF4-BEAM') #Sl1cProduct is the sourcefile that should be processed. 
        #print (cmdwget)    
        try: 
            subprocess.call(cmdwget)
        except:
            print('something went wrong')
    else: 
        print (trgfname +' already exist in ' + trgDIR)    

def atmcorr_c2rcc_s2(Sl1cProduct,trgdir_Level2,properties_file,filename):
    '''Atmosphere correction using C2RCC algorithm'''

    targetname='C2RCC_idepix_' + filename.rsplit('.', 1)[0] + '.nc'
    trgfname = os.path.join(trgdir_Level2,targetname)

    #S2_atmcorr_c2rcc_step =  r'D:\\Prosjekt\satelitt\\Kopi_import_MERIS_ftp\\S2MSI_s2resample_subset_idepix_c2rcc.xml'

    if not exists(trgfname):
        xml_graph_prop = r'S2MSI_s2resample_subset_idepix_c2rcc.xml'

        print ('*****')
        print ('Running C2RCC on '  + Sl1cProduct)
        #properties = properties_path + prop
        #print ('properties',properties)
        #Sl1cProduct is the sourcefile that should be processed. 
        print ("cmd_path_gpt", cmd_path_gpt)
        print ("xml_graph_prop", xml_graph_prop)
        print ("properties_file", properties_file)
        print (trgfname,"trgfname")
        print ('Sl1cProduct',Sl1cProduct)
        print ('*****')

        cmdwget = f'{cmd_path_gpt} {xml_graph_prop} -p {properties_file} -t {trgfname} {Sl1cProduct} -f NetCDF4-BEAM' 
        ### processDataset.bash resample_s2.xml resample_20m.properties "/Eodata/toProcess" "/Eodata/toProcess/output" resampled20m
        try: 
            subprocess.call(cmdwget)
        except:
            print('something went wrong')
    else: 
        print (trgfname +' already exist in ' + trgDIR)       

def atmcorr_acolite(srcfil,settfil):
    srcfil = srcfil[:-15]
    cmdwget = '%s --cli --settings=%s --image=%s' %(cmd_path_acolite, settfil, srcfil)
    #print (cmdwget)
    print ('\nrunning atmcorr_acolite')
    try:   
        subprocess.call(cmdwget)
    except:
        print('\nsomething went wrong')
        return False
    return True    


def main_process_files(dataDir, to_pixelExt = False, to_createRGB = False, to_atmcorr_c2rcc = False, to_atmcorr_acolite = False,
                        properties_c2rcc = None,properties_acolite = None):

    # list all files in a directory 
    lst = sorted(listdir(dataDir))

    # loop over the files 
    for filen in lst: 

        if filen not in ('RGB','L2'):
            
            srcfil = os.path.join(dataDir,filen)

            # Unzip file with the impage 
            # Example of unzipped folder name S2B_MSIL1C_20210624T131719_N0300_R124_T33XWH_20210624T135347.SAFE
            # inside there will be a main file MTD_MSIL1C.xml ( we will work with it, tempff)
            unzipped_folder,tmpff = unzip_file(srcfil)

            # Correct image for atmosphere using c2rcc method 
            if to_atmcorr_c2rcc:

                # Get the properties file for atm correction (depends on the region)
                #prop = r'S2_MSI_60m_Gjende.properties'  for example   
                fname = filen.rsplit('.', 1)[0]
                trgdir_Level2 = f'{dataDir}/L2/{fname}'

                #atmcorr_c2rcc(srcfil,trgdir,modul,prop,sensor)
                atmcorr_c2rcc_s2(tmpff,trgdir_Level2,properties_c2rcc,filen)

            if to_atmcorr_acolite:
                print ("to_atmcorr_acolite", to_atmcorr_acolite)

                #settfil = r'D:\Prosjekt\satelitt\Kopi_import_MERIS_ftp\acoliteSetting\{}_MSI_acoliteSettings_{}.txt'.format(sensor,roi)
                #properties_acolite
                res = atmcorr_acolite(tmpff,properties_acolite)

            shutil.rmtree(os.path.join(tmp_work_folder,unzipped_folder), ignore_errors=True)


def make_download_request(dataDir):

    # connect to the API
    print (d['username'], d['password'])

    api = SentinelAPI(d['username'], d['password'],'https://colhub.met.no/') #,d['apiAddress']

    # Define the beginning and the end of your query here
    startdate = '20210618'
    enddate = '20210623'
    # Define tha maximum cloud coverage (if there are more cloud, images won't be downloaded)
    maxclouds = 50 # Filter products by the cloud coverage (in %)
    # Specify the polygon for you area of interest
    # You can use http://geojson.io or 
    # https://www.keene.edu/campus/maps/tool/ to create a polygon 

    #footprint = geojson_to_wkt(read_geojson('SIOS_buoy.geojson')) 
    footprint = geojson_to_wkt(read_geojson('Gjende.geojson')) 
    
    platformname = 'Sentinel-2' #( Another option is Sentinel-3)

    # You won't need to change it 
    product_types = {
        'Sentinel-2':'S2MSI1C',# 1C is a level 1C
        'Sentinel-3':'OL_1_EFR___',
        'Sentinel-3':'OL_1_LRR___'
    }    
    producttype = product_types[platformname] 


    products = api.query(footprint,
                        date=[startdate,enddate],
                        platformname="Sentinel-2", 
                        cloudcoverpercentage=(0, maxclouds),            
                        producttype="S2MSI1C")

    #products = query_products(api,footprint,startdate,enddate,producttype,platformname,maxclouds)
    download_files(api,products,dataDir)

if __name__ == '__main__':


    # Specify path where you want to save the files 
    dataDir = r'./Data'

    make_download_request(dataDir)
    
    properties_c2rcc  = 'properties\S2_MSI_60m_Gjende_test.properties'
    properties_acolite = 'acoliteSetting\S2_MSI_acoliteSettings_Gjende_test.txt'
    main_process_files(dataDir,to_atmcorr_c2rcc = True,properties_c2rcc = properties_c2rcc,
    properties_acolite = properties_acolite,to_atmcorr_acolite = True)
