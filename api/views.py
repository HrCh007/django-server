from django.shortcuts import render
from rest_framework.decorators import permission_classes,api_view
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
import boto3
from botocore.exceptions import NoCredentialsError
import pandas as pd
import json
import re
import time


session = boto3.Session(profile_name='014744699880_DataScience-tol_sandbox')

s3_client = session.client('s3', region_name = 'us-east-1')

def upload_file_to_s3(files):
    
    try:
        for file_obj in files:
            file_name = file_obj.name
            s3_client.upload_fileobj(file_obj, "comprehend-semi-structured-docs-us-east-1-014744699880", "Testing/" + file_name)

        return True
    except NoCredentialsError:
        return False

@api_view(['GET'])
def test(request):
    query = request.query_params.get('query', '')
    print(query)
    return Response({"test": "res"})

@api_view(['POST'])
def upload_to_s3(request):
    files = request.FILES.getlist('files')
    if upload_file_to_s3(files):
        return Response({'message': 'Files uploaded to S3 successfully'})
    else:
        return Response({'message': 'Failed to upload files to S3'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def call_model_and_ocr(request):
    file_name = request.query_params.get('query', '')
    df=pd.read_csv("/home/shtlp0034/Bulk_Invoice_Uploader/invoiceServer/master.csv",  index_col=[0])
    # check if entry for this pdf is present in master csv or not
    contains_value = df["source_pdf"].str.contains(file_name, na=False).any()
    if contains_value:
        return Response({"message":"pdf is already processed"}, status=status.HTTP_200_OK)
    else:
        # call ocr API
        time.sleep(5)
        searchable_pdf_path = ""
        # call model endpoint
        response = {}
        if file_name.lower() == "037.pdf".lower():
            response = {"OEM_MAKE": "CHEVROLET", "OEM_MODEL_NAME": "CK31003", "YEAR": 2022}
            searchable_pdf_path = "037_digitized.PDF"
        # write model response to a file in s3 
        json_data = json.dumps(response)

        pattern = re.compile(".pdf", re.IGNORECASE)
        json_file_name = pattern.sub(".json", file_name)
        s3_client.put_object(Body=json_data, Bucket="comprehend-semi-structured-docs-us-east-1-014744699880", Key="Testing/" + json_file_name)

        
        # store path of searchable pdf and model file in a master csv
        new_row = {"source_pdf": file_name, "digitized_pdf": searchable_pdf_path, "model_file": json_file_name}
        df2 = pd.DataFrame(new_row, index=[0])
        df3 = pd.concat([df, df2], ignore_index = True)
        df3.reset_index()
        print(df3)
        df3.to_csv("/home/shtlp0034/Bulk_Invoice_Uploader/invoiceServer/master.csv")
        return Response({"message":"pdf is processed"}, status=status.HTTP_200_OK)


# def fetch_invoice_data(request):
#     file_name = request.query_params.get('query', '')
#     df=pd.read_csv("/home/shtlp0034/Bulk_Invoice_Uploader/invoiceServer/master.csv",  index_col=[0])
#     df_row = df[df['source_pdf'] == file_name]
#     model_file = df_row['model_file']
#     json_data = s3_client.get_object(Bucket="comprehend-semi-structured-docs-us-east-1-014744699880", Key="Testing/" +  model_file)

@api_view(['GET'])
def image_classify(request):
    url = request.query_params.get('query-parameter', '')
    session = boto3.Session(profile_name='958516987696_DataScience-tol')
    client = session.client('sagemaker-runtime', region_name = 'us-east-1')
    request = {"url": url}
    response = client.invoke_endpoint(
    EndpointName="pytorch-inference-2022-12-15-09-32-36-996",
    ContentType="application/json",
    Accept="application/json",
    Body=json.dumps(request)
    )
    res = (response['Body'].read().decode())
    return Response(res)

@api_view(['GET'])
def floorplan_classify(request):
    url = request.query_params.get('query-parameter', '')
    session = boto3.Session(profile_name='958516987696_DataScience-tol')
    client = session.client('sagemaker-runtime', region_name = 'us-east-1')
    request = {"url": url}
    response = client.invoke_endpoint(
    EndpointName="pytorch-inference-2023-05-24-11-26-16-672",
    ContentType="application/json",
    Accept="application/json",
    Body=json.dumps(request)
    )
    res = (response['Body'].read().decode())
    return Response(res)