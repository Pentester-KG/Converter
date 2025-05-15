# from django import forms
#
# class FileConversionForm(forms.Form):
#     file = forms.FileField(label="Выберите файл")
#     target_format = forms.ChoiceField(
#         label="Целевой формат",
#         choices=[
#             ('pdf', 'PDF'),
#             ('docx', 'DOCX'),
#             ('jpg', 'JPG'),
#             ('png', 'PNG'),
#             ('txt', 'TXT')
#         ]
#     )
from django import forms
from .models import Conversion


class FileConversionForm(forms.ModelForm):
    FORMAT_CHOICES = [
        ('pdf', 'PDF'),
        ('docx', 'DOCX'),
        ('txt', 'TXT'),
        ('xlsx', 'XLSX'),
    ]

    target_format = forms.ChoiceField(choices=FORMAT_CHOICES)

    class Meta:
        model = Conversion
        fields = ['original_file', 'target_format']