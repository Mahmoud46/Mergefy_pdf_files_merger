from flask import Flask, make_response, render_template, jsonify, request
import base64
import os
from PyPDF2 import PdfMerger
from random import randint
app = Flask(__name__)


def save_pdfs(pdfs):
    for pdf in os.listdir('./static/pdfs/merged_pdf'):
        os.remove(f'./static/pdfs/merged_pdf/{pdf}')

    paths = []
    for pdf in pdfs:
        pdf_file = base64.b64decode(pdf.split(',')[1])
        pdf_path = f'./static/pdfs/pdf_list/{randint(0,99999999999999999)}_file.pdf'
        paths.append(pdf_path)
        with open(pdf_path, 'wb') as f:
            f.write(pdf_file)
    return paths


def merge_pdfs(pdfs_path):
    pdf_merged_file = PdfMerger()

    for pdf in pdfs_path:
        pdf_merged_file.append(pdf)

    pdf_merged_path = f'./static/pdfs/merged_pdf/{randint(0,10000000)}_merged_file.pdf'
    pdf_merged_file.write(pdf_merged_path)
    pdf_merged_file.close()

    for pdf in pdfs_path:
        os.remove(pdf)

    return pdf_merged_path


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/request', methods=['GET', 'POST'])
def get_request():
    if request.method == "POST":
        req = request.get_json()
        res = make_response(
            jsonify({'Message': "Transformation has been done successfully", 'path': merge_pdfs(save_pdfs(req['codes']))}), 200)
        return res


if (__name__ == '__main__'):
    app.run()
