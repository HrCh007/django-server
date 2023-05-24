from django.contrib import admin
from django.urls import include,path
from .views import test,upload_to_s3,call_model_and_ocr,image_classify, floorplan_classify

urlpatterns = [
    path('test/', test , name="test"),
    path('upload-to-s3/', upload_to_s3, name="upload-to-s3"),
    path('call-model-and-ocr/', call_model_and_ocr, name="call-model-and-ocr"),
    path('image-classify/', image_classify, name="image-classify"),
    path('floorplan-classify/', floorplan_classify, name="floorplan-classify")
]
