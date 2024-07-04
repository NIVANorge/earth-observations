# This Python file uses the following encoding: utf-8
import os, sys
S3_settings_table = {
    '1': {
        'name': "Trondheimsfjord",
        'wtype': 'Marine',
        'resolution': 60,
        'scene': 1800},
    '2': {
        'name': 'Mjosa',
        'wtype': 'Lakes',
        'scene': 1980,
        'resolution': 60
    },
    '3': {
        'name': 'Femunden',
        'wtype': 'Lakes',
        'scene': 1980,
        'resolution': 60
    },
    '4': {
        'name': 'Gjende',
        'wtype': 'Lakes',
        'resolution': 60,
        'scene': 1980
    },
    '5': {
        'name': 'indreOslofjord',
        'wtype': 'Marine',
        'scene': 1980,
        'resolution': 60
    },
    '6': {
        'name': 'Rossvatnet',
        'wtype': 'Lakes',
        'scene': 1800,
        'resolution': 60
    },    
    '7': {
        'name': 'Selbusjoen',
        'wtype': 'Lakes',
        'scene': 1800,
        'resolution': 60
    },
    '8': {
        'name': 'Snaasavatnet',
        'wtype': 'Lakes',
        'resolution': 60,
        'scene': 1800
    }  
    }

S2_settings_table = {
    '1': {
        'name': 'Snaasavatnet',
        'tile': "T32WPS",
        'wtype': 'Lakes',
        'resolution': 60
    },  
    '9': {
        'name': "Selbusjoen",
        'tile': "T32VNR",
        'wtype': 'Lakes',
        'resolution': 60
    },  
    '2': {
        'name': "Femunden_north",
        'tile': "T32VPQ",
        'wtype': 'Lakes',
        'resolution': 60,
        'scene': 1980
    },
    '3': {
        'name': "Femunden_south",
        'tile': "T32VPP",
        'wtype': 'Lakes',
        'resolution': 60,
        'scene': 1980
    },        
    '4': {
        'name': r"Rossvatnet_south",
        'tile': "T33WVN",
        'wtype': 'Lakes',
        'resolution': 60,
        'scene': 1800
    },     
    '5': {
        'name': r"Rossvatnet_north",
        'tile': "T33WVP",
        'wtype': 'Lakes',
        'resolution': 60,
        'scene': 1800
    },      
    '6': {
        'name': "Gjende",
        'tile': "T32VMP",
        'wtype': 'Lakes',
        'resolution': 60,
        'scene': 1980
    },   
    '7': {
        'name': r"Mjosa_north",
        'tile': "T32VNN",
        'wtype': 'Lakes',
        'resolution': 60,
        'scene': 1980
    },  
    '8': {
        'name': r"Mjosa_south",
        'tile': "T32VPN",
        'wtype': 'Lakes',
        'resolution': 60,
        'scene': 1980
    }
}





