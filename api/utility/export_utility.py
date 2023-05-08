import os
import geopandas as gpd
import psycopg2
import shapefile
import zipfile
from django.contrib.gis.geos import GEOSGeometry
from django.conf import settings
from rest_framework import status
from django.http import HttpResponse
import shutil
from datetime import datetime
from sqlalchemy import text as sql_text
from sqlalchemy import create_engine

def layer_exporter(layer_id, output_format, export_dir):
    # Connect to the database
    db_connection_url = os.environ.get("DATABASE_URL", None)
    if not db_connection_url:
        return ("Cannot connect to the database.", 400)

    con = create_engine(db_connection_url)
    sql = (
        f"SELECT id, geom FROM core_projectsiteaddress WHERE id={layer_id}"
    )
    gdf = gpd.read_postgis(sql_text(sql), con.connect())

    if gdf.empty:
        return (f"No data found for layer with id {layer_id}", 404)

    """pack data in different formats"""
    file_url = os.path.join(export_dir, f"{layer_id}.{output_format}")
    # changing the filename if 2 layers has same name
    if os.path.exists(file_url):
        file_url = os.path.join(
            export_dir, f"{layer_id}-1.{output_format}"
        )

    if output_format == "shapefile":
        # create a temporary directory to store shapefile
        shapefile_dir = os.path.join(export_dir, f"{layer_id}-{output_format}")
        os.makedirs(shapefile_dir, exist_ok=True)
        gdf.to_file(os.path.join(shapefile_dir, f"{layer_id}.shp"))

        # create a ZipFile
        zipfile_name = os.path.join(export_dir, f"{layer_id}")
        # changing the zipfile name if 2 layers has same name
        if os.path.exists(zipfile_name + ".zip"):
            zipfile_name = os.path.join(
                export_dir, f"{layer_id}-1"
            )
        base_dir = f"{layer_id}/"
        # add shape files to zip
        shutil.make_archive(
            base_name=zipfile_name, format="zip", root_dir=shapefile_dir
        )
        # clearing the directory
        shutil.rmtree(shapefile_dir)
        file_url = f"{zipfile_name}.zip"
    return (file_url, 200, "Success")

# def layer_exporter(layer_instance, output_format, export_dir):

#     # Connect to the database
#     db_connection_url = os.environ.get(
#         "DATABASE_URL",
#         None
#     )
#     if not db_connection_url:
#         return ("Cannot connect to the database.", 400)

#     con = create_engine(db_connection_url)
#     sql = (
#         # "SELECT id, geom, attributes FROM projects_layerfeature WHERE layer_id="
#         # 'SELECT  site_name, project_id, site_location_id, site_area, way_id WHERE projectsite_id='
#         'SELECT geom FROM core_projectsiteaddress WHERE id='
#         + layer_instance
#     )
    
#     gdf = gpd.read_postgis(sql_text(sql), con.connect())

#     """pack data in different formats"""
#     file_url = os.path.join(export_dir, f"{layer_instance.name}.{output_format}")
#     # changing the filename if 2 layers has same name
#     if os.path.exists(file_url):
#         file_url = os.path.join(
#             export_dir, f"{layer_instance.name}-{layer_instance.id}.{output_format}"
#         )
#     if output_format == "shapefile":
#         # create a temporary directory to store shapefile
#         shapefile_dir = os.path.join(export_dir, f"{layer_instance.id}-{output_format}")
#         os.makedirs(shapefile_dir, exist_ok=True)
#         gdf.to_file(os.path.join(shapefile_dir, f"{layer_instance.name}.shp"))

#         # create a ZipFile
#         zipfile_name = os.path.join(export_dir, f"{layer_instance.name}")
#         # changing the zipfile name if 2 layers has same name
#         if os.path.exists(zipfile_name + ".zip"):
#             zipfile_name = os.path.join(
#                 export_dir, f"{layer_instance.name}-{layer_instance.id}"
#             )
#     base_dir = f"{layer_instance.name}/"
#     # add shape files to zip
#     shutil.make_archive(
#         base_name=zipfile_name, format="zip", root_dir=shapefile_dir
#     )
#     # clearing the directory
#     shutil.rmtree(shapefile_dir)
#     file_url = f"{zipfile_name}.zip"

# def layer_exporter(layer_instance, output_format, export_dir):

#     # Connect to the database
#     db_connection_url = os.environ.get(
#         "DATABASE_URL",
#         None
#     )
#     if not db_connection_url:
#         return ("Cannot connect to the database.", 400)

#     con = create_engine(db_connection_url)
#     sql = (
#         f"SELECT geom FROM core_projectsiteaddress WHERE id={layer_instance.id}"
#     )
    
#     gdf = gpd.read_postgis(sql_text(sql), con.connect())
    
#     """pack data in different formats"""
#     file_url = os.path.join(export_dir, f"{layer_instance.name}.{output_format}")
#     # changing the filename if 2 layers has same name
#     if os.path.exists(file_url):
#         file_url = os.path.join(
#             export_dir, f"{layer_instance.name}-{layer_instance.id}.{output_format}"
#         )
#     if output_format == "shapefile":
#         # create a temporary directory to store shapefile
#         shapefile_dir = os.path.join(export_dir, f"{layer_instance.id}-{output_format}")
#         os.makedirs(shapefile_dir, exist_ok=True)
#         gdf.to_file(os.path.join(shapefile_dir, f"{layer_instance.name}.shp"))

#         # create a ZipFile
#         zipfile_name = os.path.join(export_dir, f"{layer_instance.name}")
#         # changing the zipfile name if 2 layers has same name
#         if os.path.exists(zipfile_name + ".zip"):
#             zipfile_name = os.path.join(
#                 export_dir, f"{layer_instance.name}-{layer_instance.id}"
#             )
#     base_dir = f"{layer_instance.name}/"
#     # add shape files to zip
#     shutil.make_archive(
#         base_name=zipfile_name, format="zip", root_dir=shapefile_dir
#     )
#     # clearing the directory
#     shutil.rmtree(shapefile_dir)
#     file_url = f"{zipfile_name}.zip"
    
#     return file_url, 200, "OK"

