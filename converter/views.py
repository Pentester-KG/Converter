import os
from PIL import Image
from pdf2docx import Converter


def convert_file(file_path, target_format):
    # Путь к папке для сохранения конвертированных файлов (в папке media/converted)
    converted_folder = os.path.join('media', 'converted')

    # Проверка на существование папки и создание её, если она не существует

    supported_formats = ['docx', 'doc', 'txt', 'pdf', 'jpg', 'png', 'jpeg']
    target_format = target_format.lower()
    input_ext = os.path.splitext(file_path)[1][1:].lower()  # получаем расширение файла без точки

    # Формируем полный путь для сохранения конвертированного файла
    output_filename = os.path.splitext(os.path.basename(file_path))[0] + '.' + target_format
    output_path = os.path.join(converted_folder, output_filename)

    # Проверка на поддерживаемые форматы
    if target_format not in supported_formats:
        raise ValueError(f"Целевой формат '{target_format}' не поддерживается.")

    # Проверка, если целевой формат совпадает с исходным
    if input_ext == target_format:
        raise ValueError("Целевой формат совпадает с исходным — конвертация не требуется.")

    # --- DOCX → PDF ---
    if input_ext == 'docx' and target_format == 'pdf':
        cv = Converter(file_path)
        cv.convert(output_path)
        cv.close()

    # --- Изображения → PDF ---
    elif input_ext in ['jpg', 'jpeg', 'png'] and target_format == 'pdf':
        image = Image.open(file_path)
        image = image.convert("RGB")
        image.save(output_path, "PDF")

    # --- Изображение → Изображение (например: jpg → png) ---
    elif input_ext in ['jpg', 'jpeg', 'png'] and target_format in ['jpg', 'jpeg', 'png']:
        image = Image.open(file_path)
        image.save(output_path, format=target_format.upper())

    # --- DOCX → DOC, TXT → PDF, и т.д. — необработанные кейсы ---
    else:
        raise ValueError(f"Конвертация из '{input_ext}' в '{target_format}' не реализована.")

    return output_path
