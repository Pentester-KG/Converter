from django.urls import path
from .views import FileConvertAPIView

urlpatterns = [
    path('api/convert/', FileConvertAPIView.as_view(), name='file-convert'),

]
