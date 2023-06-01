from flask import Flask, render_template, request, send_file
import os
from docx import Document
from PIL import Image
import img2pdf
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from docx2pdf import convert

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    file = request.files['file']
    convert_type = request.form['convertType']

    # Save the uploaded file to the server
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)

    if convert_type == 'pdf':
        if file.filename.endswith('.docx'):
            # Convert Word document to PDF
            pdf_path = convert_doc_to_pdf(file_path)
        elif file.filename.endswith('.txt'):
            # Convert plain text file to PDF
            pdf_path = convert_txt_to_pdf(file_path)
        elif file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            # Convert image file to PDF
            pdf_path = convert_image_to_pdf(file_path)
        else:
            return 'Conversion not supported.'

        return send_file(pdf_path, as_attachment=True)

    elif convert_type == 'txt':
        # Convert other file types to plain text
        if file.filename.endswith('.docx'):
            doc = Document(file_path)
            txt_path = os.path.join('converted', 'converted.txt')
            with open(txt_path, 'w') as txt_file:
                for paragraph in doc.paragraphs:
                    txt_file.write(paragraph.text + '\n')
            return send_file(txt_path, as_attachment=True)
        elif file.filename.endswith('.pdf'):
            # Convert PDF to plain text using external tool/library
            # Implement your PDF to text conversion logic here
            return 'Conversion not implemented for PDF files.'
        else:
            return 'Conversion not supported.'

def convert_doc_to_pdf(file_path):
    # Convert Word document to PDF using docx2pdf library
    pdf_path = os.path.join('converted', 'converted.pdf')
    convert(file_path, pdf_path)
    return pdf_path

def convert_txt_to_pdf(file_path):
    # Convert plain text file to PDF using reportlab library
    pdf_path = os.path.join('converted', 'converted.pdf')
    with open(file_path, 'r') as txt_file:
        text = txt_file.read()
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.drawString(100, 750, text)
    c.save()
    return pdf_path

def convert_image_to_pdf(file_path):
    # Convert image file to PDF using img2pdf library
    pdf_path = os.path.join('converted', 'converted.pdf')
    with open(pdf_path, "wb") as pdf_file:
        image = Image.open(file_path)
        pdf_bytes = img2pdf.convert(image.filename)
        pdf_file.write(pdf_bytes)
    return pdf_path

if __name__ == '__main__':
    app.run(debug=True)
