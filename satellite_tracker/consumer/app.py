import geopandas as gpd
import os
from datetime import datetime, timedelta, timezone
from flask import Flask
from sqlalchemy import create_engine
from sscws.sscws import SscWs

# Set up flask app
app = Flask(__name__)

# Setup function to write gdf to postgis
def write_database(gdf):

    # Pull in environment variables for PostGIS
    POSTGIS_HOST = os.getenv("POSTGIS_HOST")
    POSTGIS_PORT = os.getenv("POSTGIS_PORT")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_TABLE = os.getenv("POSTGRES_TABLE")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

    # Setup postgis connection
    engine = create_engine(f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGIS_HOST}:{POSTGIS_PORT}/{POSTGRES_DB}')

    # Gdf write to postgis
    gdf.to_postgis(f'{POSTGRES_TABLE}', engine)

# Request sscws
def request_sscws(name, time_prev, time_now):

    # SSC instance
    ssc = SscWs()

    # Send SscWs request - CoordinateSystem.GEO by default - EPSG:4978
    result = ssc.get_locations(
        [name],
        [time_prev, time_now],
    )

    # Pull coordinates
    coords = result['Data'][0]['Coordinates'][0]

    # Debug
    print(coords)

    # Geometry - EPSG:4978
    geometry = gpd.points_from_xy(
        coords['X'],
        coords['Y'],
        coords['Z'],
    )

    # Create GeoDataFrame
    gdf = gpd.GeoDataFrame(coords, geometry=geometry,crs="EPSG:4978")

    # Return gdf
    return gdf

# Build request
def build_request(name):

    # Generate timestamps
    time_now = datetime.now(timezone.utc)
    time_prev = time_now - timedelta(hours=5)

    # Convert to ISO
    time_now = time_now.strftime("%Y-%m-%dT%H:%M:%SZ")
    time_prev = time_prev.strftime("%Y-%m-%dT%H:%M:%SZ")

    # Request locations
    gdf = request_sscws(name, time_prev, time_now)

    # Send to postgis
    write_database(gdf)

# Default request / to request the ISS location
@app.route("/")
def iss():

    # Request ISS
    name = "iss"

    # Build request for iss
    build_request(name)

    # Return
    return f"No input provided, querying ISS location\n"

# Main
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)