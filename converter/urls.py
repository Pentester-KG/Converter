from django.urls import path
from .views import ConvertFileView, DownloadFileView, home

urlpatterns = [
    path('', home, name='home'),
    path('convert/', ConvertFileView.as_view(), name='convert'),
    path('download/<int:conversion_id>/', DownloadFileView.as_view(), name='download'),
]