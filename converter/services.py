import os
from PIL import Image
from pdf2docx import Converter
from docx2pdf import convert as cv


def convert_file(file_path, target_format):
    converted_folder = os.path.join('media', 'converted')
    os.makedirs(converted_folder, exist_ok=True)

    supported_formats = ['docx', 'doc', 'txt', 'pdf', 'jpg', 'png', 'jpeg']
    target_format = target_format.lower()
    input_ext = os.path.splitext(file_path)[1][1:].lower()

    if target_format not in supported_formats:
        raise ValueError(f"Целевой формат '{target_format}' не поддерживается.")

    if input_ext == target_format:
        raise ValueError("Формат совпадает с исходным.")

    output_filename = os.path.splitext(os.path.basename(file_path))[0] + '.' + target_format
    output_path = os.path.join(converted_folder, output_filename)

    # DOCX → PDF
    if input_ext == 'docx' and target_format == 'pdf':
        cv(file_path, output_path)

    # Images → PDF
    elif input_ext in ['jpg', 'jpeg', 'png'] and target_format == 'pdf':
        image = Image.open(file_path).convert("RGB")
        image.save(output_path, "PDF")

    # Image → Image
    elif input_ext in ['jpg', 'jpeg', 'png'] and target_format in ['jpg', 'jpeg', 'png']:
        image = Image.open(file_path)
        image.save(output_path, format=target_format.upper())

    else:
        raise ValueError(f"Конвертация из '{input_ext}' в '{target_format}' не реализована.")

    return output_path
