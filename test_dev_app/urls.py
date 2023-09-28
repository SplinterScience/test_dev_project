from django.urls import path
from . import views

# urlpatterns = [
#     path('upload/', views.upload_json, name='upload_json'),
#     path('', views.home, name='home'),
# ]
urlpatterns = [
    # Map the '/spa/' URL to the SPA template.
    # Map the '/upload/' URL to the view that handles file upload and processing.
    path('', views.upload_json, name='upload_json'),
]