from django.http import FileResponse
from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage

from .models import Conversion
from .serializers import FileUploadSerializer
import os
from pdf2docx import Converter
from PIL import Image

from converter_backend import settings


class ConvertFileView(APIView):
    def post(self, request):
        try:
            # Получаем файл и параметры
            file = request.FILES['file']
            target_format = request.data.get('target_format', 'docx')

            # Здесь должна быть ваша логика конвертации
            # Например, создаем временный файл:
            output_path = os.path.join('media', 'converted', f'converted_file.{target_format}')

            # В реальном коде здесь происходит конвертация
            # ...

            # Открываем файл для чтения в бинарном режиме
            file = open(output_path, 'rb')

            # Создаем ответ с файлом
            response = FileResponse(file)

            # Устанавливаем правильные заголовки
            response['Content-Disposition'] = f'attachment; filename="converted_file.{target_format}"'
            response['Content-Type'] = 'application/octet-stream'

            return response

        except Exception as e:
            # Возвращаем JSON при ошибке
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DownloadFileView(APIView):
    def get(self, request, conversion_id):
        conversion = get_object_or_404(Conversion, id=conversion_id)
        file_path = os.path.join(settings.MEDIA_ROOT, conversion.converted_file.name)
        return FileResponse(open(file_path, 'rb'), as_attachment=True)


def home(request):
    return render(request, 'index.html')