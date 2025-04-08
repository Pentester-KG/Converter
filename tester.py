import pdf2docx


document_pdf = 'media/uploads/Эссе1.pdf'
document_docx = 'media/converted/Esse1.docx'

cv = pdf2docx.Converter(document_pdf)
cv.convert(document_docx)
cv.close()