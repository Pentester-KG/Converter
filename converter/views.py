# # import os
# # from PIL import Image
# # from django.http import FileResponse, JsonResponse
# # from django.shortcuts import render
# # from pdf2docx import Converter
# #
# # from converter.forms import FileConversionForm
# #
# #
# # def convert_file(file_path, target_format):
# #     converted_folder = os.path.join('media', 'converted')
# #     os.makedirs(converted_folder, exist_ok=True)
# #
# #     supported_formats = ['docx', 'doc', 'txt', 'pdf', 'jpg', 'png', 'jpeg']
# #     target_format = target_format.lower()
# #     input_ext = os.path.splitext(file_path)[1][1:].lower()
# #
# #     output_filename = os.path.splitext(os.path.basename(file_path))[0] + '.' + target_format
# #     output_path = os.path.join(converted_folder, output_filename)
# #
# #     if target_format not in supported_formats:
# #         raise ValueError(f"Целевой формат '{target_format}' не поддерживается.")
# #
# #     if input_ext == target_format:
# #         raise ValueError("Целевой формат совпадает с исходным.")
# #
# #     # DOCX → PDF
# #     if input_ext == 'docx' and target_format == 'pdf':
# #         cv = Converter(file_path)
# #         cv.convert(output_path)
# #         cv.close()
# #
# #     # Изображения → PDF
# #     elif input_ext in ['jpg', 'jpeg', 'png'] and target_format == 'pdf':
# #         image = Image.open(file_path)
# #         image = image.convert("RGB")
# #         image.save(output_path, "PDF")
# #
# #     # Изображение → Изображение
# #     elif input_ext in ['jpg', 'jpeg', 'png'] and target_format in ['jpg', 'jpeg', 'png']:
# #         image = Image.open(file_path)
# #         image.save(output_path, format=target_format.upper())
# #
# #     else:
# #         raise ValueError(f"Конвертация из '{input_ext}' в '{target_format}' не реализована.")
# #
# #     return JsonResponse({'file_url': '/media/converted/' + os.path.basename(output_path)})
# #
# #
# # def convert_view(request):
# #     if request.method == 'POST':
# #         form = FileConversionForm(request.POST, request.FILES)
# #         if form.is_valid():
# #             try:
# #                 # Сохраняем загруженный файл
# #                 uploaded_file = request.FILES['file']
# #                 file_path = os.path.join('media', 'uploads', uploaded_file.name)
# #                 os.makedirs(os.path.dirname(file_path), exist_ok=True)
# #
# #                 with open(file_path, 'wb+') as destination:
# #                     for chunk in uploaded_file.chunks():
# #                         destination.write(chunk)
# #
# #                 # Конвертируем файл
# #                 target_format = form.cleaned_data['target_format']
# #                 converted_path = convert_file(file_path, target_format)
# #
# #                 # Возвращаем конвертированный файл пользователю
# #                 response = FileResponse(open(converted_path, 'rb'))
# #                 response['Content-Disposition'] = f'attachment; filename="{os.path.basename(converted_path)}"'
# #                 return response
# #
# #             except Exception as e:
# #                 return render(request, 'error.html', {'error': str(e)})
# #     else:
# #         form = FileConversionForm()
# #
# #     return render(request, 'index.html', {'form': form})
# import os
# from django.shortcuts import render, redirect
# from django.http import FileResponse
# from .forms import FileConversionForm
# from .models import Conversion
# from django.conf import settings
# from docx import Document as DocxDocument
# from pdf2docx import Converter
# # from pdfminer.high_level import extract_text
# # import openpyxl
#
#
# def home(request):
#     if request.method == 'POST':
#         form = FileConversionForm(request.POST, request.FILES)
#         if form.is_valid():
#             document = form.save(commit=False)
#             file_name = document.original_file.name
#             document.original_format = file_name.split('.')[-1].lower()
#             document.save()
#
#             # Конвертация документа
#             convert_document(document)
#
#             return redirect('download', document_id=document.id)
#     else:
#         form = FileConversionForm()
#     return render(request, 'index.html', {'form': form})
#
#
# def convert_document(document):
#     original_path = document.original_file.path
#     original_format = document.original_format
#     target_format = document.target_format
#
#     output_path = os.path.join(settings.MEDIA_ROOT, 'converted',
#                                f"{os.path.splitext(os.path.basename(original_path))[0]}.{target_format}")
#
#     try:
#         if original_format == 'pdf' and target_format == 'docx':
#             cv = Converter(original_path)
#             cv.convert(output_path)
#             cv.close()
#         elif original_format == 'docx' and target_format == 'pdf':
#             doc = DocxDocument(original_path)
#             doc.save(output_path)
#         # elif original_format == 'pdf' and target_format == 'txt':
#         #     text = extract_text(original_path)
#         #     with open(output_path, 'w', encoding='utf-8') as f:
#         #         f.write(text)
#         # Добавьте другие варианты конвертации по необходимости
#
#         document.converted_file.name = os.path.join('converted', os.path.basename(output_path))
#         document.conversion_status = 'success'
#     except Exception as e:
#         document.conversion_status = f'error: {str(e)}'
#
#     document.save()
#
#
# def download(request, document_id):
#     document = Conversion.objects.get(id=document_id)
#     if document.converted_file:
#         response = FileResponse(document.converted_file.open(), as_attachment=True)
#         return response
#     return redirect('home')
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
from .serializers import FileConvertSerializer
from .services import convert_file
from django.core.files.storage import FileSystemStorage

class FileConvertAPIView(APIView):
    def get(self, request):
        return render(request, 'index.html')
    def post(self, request):
        serializer = FileConvertSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        uploaded_file = serializer.validated_data['file']
        target_format = serializer.validated_data['target_format']

        # Сохраняем временно загруженный файл
        fs = FileSystemStorage(location='media/temp/')
        filename = fs.save(uploaded_file.name, uploaded_file)
        temp_path = fs.path(filename)

        try:
            output_path = convert_file(temp_path, target_format)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"converted_file": output_path})

