from flask import Blueprint, render_template, request, send_from_directory
from app.controllers import DownloadController as dc
import os

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route("/notesheet", methods=["POST"])
def get_notesheet():
    url = request.form.get('url')
    pdf = dc.get_notesheet_pdf(url)
    print(pdf)
    return render_template("download.html", pdf_filename=pdf)

@main.route("/download/<filename>")
def serve_pdf(filename):
    return send_from_directory(F"{os.getcwd()}/ResultPDFs", filename, as_attachment=True)


