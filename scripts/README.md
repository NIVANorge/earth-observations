# SatelliteInLakes

This repository contains scripts for downloading, correcting and processing satellite images from Sentiel-2 and Sentinel-3. 
Areas of interest cover different lakes and marine areas around Norway.

Related projects: DCS4COOP, 17277-SATINNN_MDIR_II
Early versions of the scripts have been develeped by ABL,
later the work was overtaken by @lisapro
 
#
##  Download data 

There are wo scripts for downloding satellite images: 
* `downloadFromColhub.py` 

    (*In the latest version of the work, we used this module*)

    Uses Sentinelsat python library mto access Sentinel satellite images from the Copernicus Open Access Hub easy.
    User need to crate an account at https://colhub.met.no/ and store credentials in the 
    `userAccountColhub.py` (root folder of the current repository) in the form of dictionary:

    ```
     d = {'apiAddress': 'https://colhub.met.no/',
    'password': '*****',
    'username': '*****'}
    
* `downloadFromCreodias.py`

    Here you will need some manual work and registration at the 
    https://creodias.eu/

Result of downloading - zipped files with L1 (Level 1 Satellite Products)

## Images processing 
Processing includes atmospheric correction of the downloaded Level 1 products, 

`process_S2.py`
For the Sentinel 2 products, we use zepped Level-1 files (W:\Satellite\S2\L1\zip\{name of the region (tile)})
Files are processed with C2RCC algorithm or Acolite. Both correction give separate files .

`process_S3.py`

## C2RCC 

We use C2RCC (Case 2 Regional CoastColor) processor through ESA’s Sentinel toolbox SNAP.
call gpt.exe (Graph Processing Tool,part of SNAP) using subprocess 

gpt can run a list of tasks that have to be passed to it in XML format which can be developed
using the graph-builder interface of SNAP.


processing is the same for Sentinel-2 and Sentinel-3 with different input parameters. 
S2 in one step
S3 has two steps for C2RCC correction .

Result: 


#
## Pixel Extraction 
`pixelExtraction.py`
creates a text file with value for certain coordinates.
Coordinates are read from the coordinates_pixelExtraction.txt

#
## Additional scripts 
`util.py`
containg the dictionaries for setting fro S3 and S2: 
```
S3_settings_table = {
    '1': {
    'name': "Trondheimsfjord",
    'wtype': 'Marine',
    'resolution': 60,
    'scene': 1800},
 ```