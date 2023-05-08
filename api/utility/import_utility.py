from api.utility.utility import extract_shapefile
import geopandas as gpd
import psycopg2
import shapefile
import zipfile
from django.contrib.gis.geos import GEOSGeometry
from django.conf import settings
from rest_framework import status
from django.http import HttpResponse
from rest_framework.decorators import api_view
import os
from rest_framework.response import Response

@api_view(["POST",])
def import_layer(request):
    upload_file = request.data.get("upload_file", None)
    if not upload_file:
        return Response({"Error : Upload File is mandatory."}, status=400)
    
    upload_dir_name = "uploads/"
    if not os.path.exists(upload_dir_name):
        os.makedirs(upload_dir_name)
    
    upload_file_path = f'{upload_dir_name}{upload_file.name}'

    with open(upload_file_path, 'wb+') as fl:
        for chunk in upload_file.chunks():
            fl.write(chunk)

    extract_shapefile(upload_file_path)
    return Response({"File saved successfully!!!"}, status=200)