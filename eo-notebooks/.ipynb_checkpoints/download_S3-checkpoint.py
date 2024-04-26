import os
from datetime import date
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt


cloudcoverpercentage=(0, 30)

# read env variables
api = SentinelAPI(os.getenv("SENTINELSAT_USER"),
                  os.getenv("SENTINELSAT_PASSWORD"),
                  "https://finhub.nsdc.fmi.fi/")


footprint = geojson_to_wkt(read_geojson('indre-oslofjord.geojson'))
platformname = 'Sentinel-2'

start_date = date(2024, 4, 1)
end_date = date(2024, 4, 24)

product_types = {
    'Sentinel-3': 'OL_1_EFR___',
}

products = api.query(footprint,
                    date=(start_date, end_date),
                    #platformname='Sentinel-2',
                    #cloudcoverpercentage=(0, 100),
                    producttype='OL_1_EFR___',
                    )

api.download_all_quicklooks(products)
print(products.keys())