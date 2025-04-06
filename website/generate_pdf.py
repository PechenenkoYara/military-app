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
    date = request.form['date']
    city = request.form['city']
    volunteer_side = request.form['volunteer_side']
    volunteer_name = request.form['volunteer_name']
    volunteer_position = request.form['volunteer_position']
    volunteer_basis = request.form['volunteer_basis']
    recipient_side = request.form['recipient_side']
    recipient_name = request.form['recipient_name']
    recipient_position = request.form['recipient_position']
    recipient_basis = request.form['recipient_basis']

    pdf = FPDF()
    pdf.add_page()
    # pdf.add_font('DejaVu', '', 'website/static/fonts/DejaVuSans.ttf', uni=True)
    # pdf.set_font('DejaVu', '', 12)
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="АКТ приймання-передачі гуманітарної (благодійної) допомоги", ln=True, align='C')
    pdf.cell(200, 10, txt=f'"___" ____________ 20__ року', ln=True, align='C')
    pdf.cell(200, 10, txt=f"м. {city}", ln=True, align='C')
    pdf.ln(10)

    # pdf.cell(200, 10, txt="Звіт", ln=True, align='C')
    # pdf.cell(200, 10, txt="Необхідне обладнання: ", ln=True)
    # pdf.cell(200, 10, txt="Дата: " + date, ln=True)

    pdf_output = io.BytesIO()
    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    pdf_output.write(pdf_bytes)
    pdf_output.seek(0)

    return send_file(pdf_output, as_attachment=True, download_name="report.pdf", mimetype='application/pdf')