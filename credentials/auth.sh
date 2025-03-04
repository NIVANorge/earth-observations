export ACCESS_TOKEN=$(curl -d 'client_id=cdse-public' \
                    -d 'username=<username>' \
                    -d 'password=<password>' \
                    -d 'grant_type=password' \
                    'https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token' | \
                    python3 -m json.tool | grep "access_token" | awk -F\" '{print $4}')