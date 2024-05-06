# Earth Observation (EO) and Remote Sensing with ESA Sentinel-2 and Sentinel-3 satellites

A headless version (without GUI) of the ESA toolbox called [SNAP](https://step.esa.int/main/toolboxes/snap/) and the python module ´snappy´ is compiled into the Docker image in this repository. The image is then deployed on a JupyterHub server at [hub.p.niva.no](https://hub.p.niva.no). 

- SNAP v9 docker image [here](https://github.com/mundialis/esa-snap/tree/ubuntu)
- SNAP tutorials [here](https://step.esa.int/main/doc/online-help/#:~:text=Supported%20Platforms,and%20Solaris%EF%BF%BD%20operating%20systems.)
- SNAPPY examples [here](https://github.com/senbox-org/esa-snappy/tree/master/src/main/resources/esa_snappy/examples)

### Data sources
Satellite images and products can be downloaded from:
- Copernicus data space ecosystem [here](https://browser.dataspace.copernicus.eu/)
- MET Norway [here](https://colhub.met.no/#/home) and [here](https://www.satellittdata.no/en)
- List of [others](https://github.com/kr-stn/awesome-sentinel#data-hubs-and-national-mirrors)


To download
- sentinelsat python package. Documentation [here](https://github.com/sentinelsat/sentinelsat?tab=readme-ov-file)
- Alternative to sentinelsat [here](https://github.com/SDFIdk/CDSETool)

### ESA toolkits


### Naming conventions

- [Sentinel 2](https://sentinels.copernicus.eu/web/sentinel/user-guides/sentinel-3-olci/naming-convention)

### Useful links
- https://eo4society.esa.int/resources/copernicus-rus-training-materials/
- https://github.com/xcube-dev/xcube/tree/main/examples/notebooks
- 
### Notes
- [SNAP v9](https://senbox.atlassian.net/wiki/spaces/SNAP/pages/50855941/Configure+Python+to+use+the+SNAP-Python+snappy+interface+SNAP+versions+9) needs python 3.6.
- [SNAP Python guide](https://senbox.atlassian.net/wiki/spaces/SNAP/pages/19300362/How+to+use+the+SNAP+API+from+Python#HowtousetheSNAPAPIfromPython-ExamplesofSNAPAPIusagefromPython)
- [SNAP v10](https://senbox.atlassian.net/wiki/spaces/SNAP/pages/2499051521/Configure+Python+to+use+the+new+SNAP-Python+esa+snappy+interface+SNAP+version+10) is expected to be released soon
https://www.eumetsat.int/

