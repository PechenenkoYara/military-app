# from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask import Blueprint, Flask, render_template, request, send_file
from fpdf import FPDF
import io

# app = Flask(__name__)
generate_pdf = Blueprint('generate_pdf', __name__)

@generate_pdf.route('/')
def home():
    return render_template('our_home.html')

@generate_pdf.route('/create_pdf_form')
def create_pdf_form():
    return render_template('create_pdf.html')

@generate_pdf.route('/create_pdf', methods=['POST'])
def create_pdf():
    text = request.form['text_content']
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, 'Smt:', ln=True)
    pdf.cell(0, 10, 'equipment', ln=True)
    pdf.ln(10)

    for line in text.split('\n'):
        pdf.multi_cell(0, 10, line)
    pdf_output = io.BytesIO()
    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    pdf_output.write(pdf_bytes)
    pdf_output.seek(0)

    return send_file(pdf_output, as_attachment=True, download_name="report.pdf", mimetype='application/pdf')

# if __name__ == '__main__':
#     app.run(debug=True)
