from django.urls import path
from .views import ConvertFileView, DownloadFileView, home, convert_view

urlpatterns = [
    path('', home, name='home'),
    path('convert/', convert_view, name='convert'),
    path('download/<int:conversion_id>/', DownloadFileView.as_view(), name='download'),
]