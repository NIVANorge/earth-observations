# Earth Observation (EO) and Remote Sensing with ESA Sentinel-1 and Sentinel-2 satellites

A headless version (without GUI) of the ESA toolbox called [SNAP](https://step.esa.int/main/toolboxes/snap/) and the python module ´snappy´ is compiled into the Docker image in this repository. The image is then deployed on a JupyterHub server at [hub.p.niva.no](https://hub.p.niva.no). 

- SNAP v9 docker image [here](https://github.com/mundialis/esa-snap/tree/ubuntu)
- SNAP tutorials [here](https://step.esa.int/main/doc/online-help/#:~:text=Supported%20Platforms,and%20Solaris%EF%BF%BD%20operating%20systems.)
- SNAPPY examples [here](https://github.com/senbox-org/esa-snappy/tree/master/src/main/resources/esa_snappy/examples)

### Data sources
Satellite images and products can be downloaded from:
- Copernicus data space ecosystem [here](https://browser.dataspace.copernicus.eu/)
- MET Norway [here](https://colhub.met.no/#/home)

### ESa toolkits


### Notes
- [SNAP v9](https://senbox.atlassian.net/wiki/spaces/SNAP/pages/50855941/Configure+Python+to+use+the+SNAP-Python+snappy+interface+SNAP+versions+9) needs python 3.6.
- [SNAP v10](https://senbox.atlassian.net/wiki/spaces/SNAP/pages/2499051521/Configure+Python+to+use+the+new+SNAP-Python+esa+snappy+interface+SNAP+version+10) is expected to be released soon