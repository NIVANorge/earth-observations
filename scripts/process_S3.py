'''
Created on 19. okt. 2018
author: ELP,ABL
e-mail: elp@niva.no
'''
import os
import sys
import os.path
from os.path import exists
from os import listdir
import subprocess
from datetime import datetime
from processing import createRGB, atmcorr_c2rcc, atmcorr_acolite, dim2nc, pixelExt
import zipfile
import shutil
import json
import numpy as np
tmp_work_folder = r'D:\S3\work'
sensor = 'S3'


def unzip_file(f):
    try: 
        os.makedirs(tmp_work_folder)
    except: 
        pass
    tmp_files = listdir(tmp_work_folder)
    if len(tmp_files) > 0:
        print ('There are more than 1 file in the folder')
        shutil.rmtree(tmp_work_folder)
        print ('Cleared the work temp directory, continue .. ')
    try: 
        zip_ref = zipfile.ZipFile(f, 'r')
        zip_ref.extractall(tmp_work_folder)
        zip_ref.close()
        unzipped_folders = listdir(tmp_work_folder)
        
        #assert len(unzipped_folders) == 1, ('there are more than 1 file in the folder D:\S3\work')
        unzipped_folder = unzipped_folders[0]
        tmpff = os.path.join(tmp_work_folder,unzipped_folder,'xfdumanifest.xml') 
    except zipfile.BadZipfile:
        print ("Bad Zip file for this path, skip",f)
        unzipped_folder,tmpff = None, None
    return(unzipped_folder,tmpff) 



def main(to_createRGB = False, to_atmcorr_c2rcc = False):
    print (to_createRGB, to_createRGB == False, 'to_createRGB')
    '''
    All files needs to be unzipped, which is done first,
    since L1 files are stored on the NAS-disk as zip-files. 
    All process is done for one file at the time.  
    '''
    lst = sorted(listdir(srcdir))
    for fil in lst: 
        len_progress = len(progress[roi])
        print ("####### processed {} of total {}".format(len_progress,len(lst)))
        percent = (np.float64(len_progress)/np.float64(len(lst)))*100.00
        print ("####### {} %  of {} is processed".format(percent,roi))  
        if fil != 'RGB':
            month = int(fil[20:22])
            if (month < 3) or (month > 10):
                print (fil)
                print ('This is a month with too high zenit angle (the sun is too low), this scene will not be processed this scene.....')
            else:
                srcfil = os.path.join(srcdir,fil)
                if srcfil not in progress[roi]:
                    try:
                        unzipped_folder,tmpff = unzip_file(srcfil)
                    except IOError as err:
                        print (err)
                        unzipped_folder = None
                    if not unzipped_folder == None:      
                        if to_createRGB:
                            '''
                            .createRGB makes RGB file using L1-files. 
                            '''
                            #trgdir = r'W:\Satellite\S3\L1/' + lake + r'/RGB'
                            trgdir = r'W:\Satellite\S3\L1\zip\_{}\RGB'.format(scene)
                            if not os.path.exists(trgdir):
                                os.makedirs(trgdir)
                            if not exists(os.path.join(trgdir,fil[:-3]+ 'SEN3.tif')):
                                createRGB(trgdir, tmpff, sensor)
                            else: 
                                'Already exists'
                        if to_atmcorr_c2rcc:
                            trgdir = r'W:\Satellite\S3/L2/NIVA/c2rcc/_300m/{}/{}'.format(wtype,roi)
                            prop = r'S3_OLCI_{}.properties'.format(roi)
                            atmcorr_c2rcc(tmpff,trgdir,prop,sensor)

                        progress[roi].append(srcfil)
                        json_file.seek(0)
                        json.dump(proc_progress_file, json_file,indent = 4)
                        print ('delete', os.path.join(tmp_work_folder,unzipped_folder))
                        shutil.rmtree(os.path.join(tmp_work_folder,unzipped_folder), ignore_errors=True)
                else:
                    pass 
                    #print ("file is already processed")

def get_params(region_id):
    roi = S3_settings_table[region_id]["name"]
    wtype = S3_settings_table[region_id]["wtype"]  
    #tile = S3_settings_table[region_id]["tile"]   
    resolution = S3_settings_table[region_id]['resolution']    
    scene = S3_settings_table[region_id]['scene']
    srcdir = r'W:\Satellite\S3\L1\zip\_{}'.format(scene)
    return roi,wtype,resolution,scene,srcdir

if __name__ == '__main__':

    from util import S3_settings_table
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", required = False, action = "store_true") 
    parser.add_argument("--region", required=False) 
    args = parser.parse_args()
    process_all = args.all #False #True
    print (process_all, 'to process all the files ')


    with open('process_progress_s3.json', "r+") as json_file:
        proc_progress_file = json.load(json_file)
        progress = proc_progress_file["Sentinel-3"]

        if process_all:
            all_regions = S3_settings_table.keys()
            #
            for region_id in all_regions:
                print (region_id)
                roi,wtype,resolution,scene,srcdir = get_params(region_id)
                main(to_createRGB = False, to_atmcorr_c2rcc = True)       

                '''if roi not in ['Trondheimsfjord','Femunden','Mjosa',"Gjende","Snaasavatnet","Rossvatnet","Selbusjoen"]:
                    print (roi)

                else:
                    print (roi, 'already processed')'''
                print ('*********FINISHED',roi)
        else: 
            parser = argparse.ArgumentParser()
            parser.add_argument("--region", required=True) 
            args = parser.parse_args()
            region_id = args.region

            roi,wtype,resolution,scene,srcdir = get_params(region_id)

            main(to_createRGB = False, to_atmcorr_c2rcc=True)