cmd_folder = 'C:/Program Files/snap/bin/'
from util import S2_settings_table, S3_settings_table
import os
import subprocess
import glob

def pixelExt(coordinates,srcdir,trgdir,outPutFile):
    
    cmd_line=os.path.join(cmd_folder, 'gpt.exe PixEx')
    productPath = srcdir + r'\*.nc' # This should likely include the list of files instead of just one source directory!
    cmdwget = '{} -PcoordinatesFile={} -PsourceProductPaths={} -PoutputDir={} -PoutputFilePrefix={} -PwindowSize=3'.format(
            cmd_line, coordinates, productPath, trgdir, outPutFile)
    print (cmdwget)   
    subprocess.call(cmdwget) 


trgdir_s3 = r'W:\Satellite\S3\pixelExtraction'
trgdir_s2 = r'W:\Satellite\S2\pixelExtraction'
trgdir_s2_icor = r'W:\Satellite\S2\pixelExtraction_icor'
#outputfile = r'testExtractionS3'


#coordinates = r'coordinates_pixelExtraction.txt'
coordinates = r'stations_koordinates_fullList_v1.txt'

def extract_s3():
    
    # pixel extraction for S3 (need to merge files first)
    for n in S3_settings_table.keys():
        region =  S3_settings_table[n]['name']   
        category = S3_settings_table[n]['wtype']
        print (region,category)
        
        srcdir = r'W:\Satellite\S3\L2\NIVA\c2rcc\_300m\{}\{}\Merged_S3_data'.format(category,region)
        outputfile = str(region) + '_pixelExtraction'
        pixelExt(coordinates,srcdir,trgdir_s3,outputfile)
        

# pixel extraction for S3 (need to merge files first)
def extract_s2():
    for n in S2_settings_table.keys():
        region =  S2_settings_table[n]['name']   
        category = S2_settings_table[n]['wtype']
        resolution = S2_settings_table[n]['resolution']    
        print (region,category)
        srcdir = r'W:\Satellite\S2\L2\{}\{}\C2RCC\_{}m'.format(category,region,resolution)
        #srcdir = r'W:\Satellite\S3\L2\NIVA\c2rcc\_300m\{}\{}'.format(category,region)
        outputfile = str(region) + '_pixelExtraction'
        pixelExt(coordinates,srcdir,trgdir_s2,outputfile)
        
def extract_s2_iCOR_v101():
    regions = ['32VNM', '32VNR', '32VPL', '33XWG']
    for r in regions:
        print ('region', r)
        srcdir = fr"W:\Satellite\S2\L2\iCOR\V101\{r}\2019\altogether"
        outputfile = 'iCOR_V101_' + str(r) + '_pixelExtraction'
        print ('\n',outputfile)
        pixelExt(coordinates,srcdir,trgdir_s2_icor,outputfile)

def extract_s2_iCOR_v103():
    regions = ['32VNM', '32VNR', '32VPL', '33XWG']
    
    for reg in regions:
        for year in ['2018','2019','2020']:
            if os.path.exists(rf"W:\Satellite\S2\L2\iCOR\V103\0028_NIVA\{reg}\{year}"):
                print ('region', reg, 'year',year)
                srcdir = fr"W:\Satellite\S2\L2\iCOR\V103\0028_NIVA\{reg}\{year}\altogether"
                outputfile = 'iCOR_V103_' + str(reg) + str(year) + '_pixelExtraction'
                print ('\n',outputfile)
                pixelExt(coordinates,srcdir,trgdir_s2_icor,outputfile)        



#pixelExt(r'coordinates_pixelExtraction.txt',srcdir,trgdir_s2_icor,outputfile)  


#extract_s2_iCOR_v101()
#extract_s2_iCOR_v103()
extract_s3()
#extract_s2()
#import pandas as pd
#df = pd.read_csv(coordinates,sep = ';')
#df.to_csv('stations_koordinates_fullList_v1.txt',index = False, sep = '\t')
#print (df.head())