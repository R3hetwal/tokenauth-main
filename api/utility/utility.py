from rest_framework.views import APIView
from rest_framework.response import Response
import os
import geopandas as gpd
import psycopg2
import shapefile
import zipfile
from shapely import force_2d
import glob
import numpy as np
from django.contrib.gis.geos import GEOSGeometry
from django.conf import settings
from rest_framework import status
from django.http import HttpResponse

def extract_shapefile(upload_file_path):
    print("ENtering Extract shapefile")
    try:
        print("ENtering try shapefile")
        errors = []
        allowed_extensions = [    
            ".shp",
            ".shx",
            ".dbf",
            ".sbn",
            ".sbx",
            ".fbn",
            ".fbx",
            ".ain",
            ".aih",
            ".atx",
            ".ixs",
            ".mxs",
            ".prj",
            ".shp.xml",
            ".xml",
            ".cpg",
        ]
        file = upload_file_path
        file_path = os.path.dirname(file)
        with zipfile.ZipFile(file, "r") as zip_ref:
            # get zip file contents
            import_extensions = [
                os.path.splitext(file_path)[1].lower()
                for file_path in zip_ref.namelist()
            ]
            # removing empty strings here
            import_extensions = list(filter(None, import_extensions))
            if ".zip" in import_extensions:
                return Response({"Error:Import as separate zipped shapefiles instead."}, 
                                status=400
                                )
            common_extensions = set(import_extensions) - set(allowed_extensions)
            if common_extensions:
                return Response({"Error:Nested layers encountered. Import as separate files instead."},
                    status=400
                )
            zip_ref.extractall(file_path)
            '''The glob.glob() function returns a list of file paths that match the pattern passed to 
            it. Here ** means to match any number of directories and subdirectories. The [0] index is 
            used to select the first file path that matches the pattern, which is assumed to be the 
            shapefile.'''

            shape = glob.glob(r"{}/**/*.shp".format(file_path), recursive=True)[0]
            print(shape)

            geodataframe = gpd.read_file(shape)
            epsg = geodataframe.crs.to_epsg()
            utm_zone = (geodataframe.crs.utm_zone,)
            if epsg != 4326:
                if utm_zone:
                    return Response(
                        {"Error: Invalid spatial reference system. Only import WGS84 (EPSG: 4326)"},
                        status=400
                    )
                else:
                    return Response({"Error: Unknown Coordinate System"}, 
                                    status=400
                    )

            """reomve id column if it exists"""
            if "id" in geodataframe.columns:
                geodataframe.drop("id", inplace=True, axis=1)
                # errors='ignore'

            #remove z dimension if exists
            '''The function being applied is force_2d(), which takes a single geometry object as an 
            argument and returns a 2D version of that geometry object. The apply() method returns a 
            new GeoDataFrame with the modified geometry objects. 
            
            The purpose of this code is to ensure that all geometry objects in the GeoDataFrame are 2D 
            (i.e., have an x-coordinate and a y-coordinate, but not a z-coordinate). Some spatial 
            operations (such as buffering) require 2D geometries, so it's important to ensure that all 
            geometries in a GeoDataFrame are 2D before performing those operations.'''

            geodataframe["geometry"] = geodataframe.geometry.apply(lambda x: force_2d(x))

            """set nan values to None"""
            geodataframe = geodataframe.replace(["NaN", "nan", np.nan], None)
            return ("File Saved Successfully!!!", 200)

    except Exception as e:
        return Response({"error occured : " + str(e)}, status=400)