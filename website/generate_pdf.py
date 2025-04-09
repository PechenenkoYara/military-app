# from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask import Blueprint, Flask, render_template, request, send_file
from fpdf import FPDF
import io

# app = Flask(name)
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
    equipment = request.form['items']

    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('TimesNewRoman', '', 'website/static/fonts/times.ttf', uni=True)
    pdf.set_font('TimesNewRoman', '', 12)

    pdf.cell(200, 10, txt="АКТ приймання-передачі гуманітарної (благодійної) допомоги", ln=True, align='C')
    pdf.cell(200, 10, txt=f'{date} року', ln=True, align='C')
    pdf.cell(200, 10, txt=f"м. {city}", ln=True, align='C')
    pdf.ln(3)
    usable_width = pdf.w - 2 * pdf.l_margin
    pdf.multi_cell(usable_width, 10, txt=f"{volunteer_side} в особі {volunteer_name}, {volunteer_position}\
 , що діє на підставі {volunteer_basis} з однієї сторони, та {recipient_side}\
в особі {recipient_name}, {recipient_position}, що діє на підставі {recipient_basis} з іншої сторони,")

    pdf.cell(200, 10, txt = 'Уклали цей Акт приймання-передачі гуманітарної благодійної допомоги про таке:', ln=True)
    pdf.cell(200, 10, txt = '1. Благодійник передав, а Отримувач отримав таку гуманітарну допомогу:', ln=True)

    amount = 0
    money = 0
    rows = equipment.strip().split('\n')

    # pdf.set_font('TimesNewRoman', '', 7)
    pdf.cell(10, 10, '№', border=1, align='C')
    pdf.cell(50, 10, 'Назва матеріальних цінностей', border=1, align='C')
    pdf.cell(30, 10, 'Одиниця виміру', border=1, align='C')
    pdf.cell(20, 10, 'Кількість', border=1, align='C')
    pdf.cell(35, 10, 'Ціна за одиницю', border=1, align='C')
    pdf.cell(35, 10, 'Загальна вартість', border=1, align='C')
    pdf.ln()

    for i, row in enumerate(rows, start=1):
        parts = [p.strip() for p in row.split(',')]

        name, unit, q, p = parts
        total = int(q) * int(p)

        pdf.cell(10, 8, str(i), border=1, align='C')
        pdf.cell(50, 8, name, border=1)
        pdf.cell(30, 8, unit, border=1, align='C')
        pdf.cell(20, 8, q, border=1, align='C')
        pdf.cell(35, 8, p, border=1, align='C')
        pdf.cell(35, 8, str(total), border=1, align='C')
        pdf.ln()

        amount += int(q)
        money += int(total)

    pdf.cell(180, 10, txt=f"УСЬОГО: {amount} шт. {money} грн", ln=True)

    pdf.ln(10)
    pdf.multi_cell(180, 10, txt="2. Матеріальні цінності передано в належному стані, Сторони претензій одна до одної не мають.")
    pdf.multi_cell(180, 10, txt="3. Цей Акт набуває чинності з дати його підписання уповноваженими представниками обох Сторін.")
    pdf.multi_cell(180, 10, txt="4. Цей Акт складено у двох примірниках, які мають однакову юридичну силу для обох Сторін.")
    pdf.ln(10)

    pdf.cell(200, 10, txt="Місцезнаходження і реквізити сторін", ln=True)
    pdf.cell(200, 10, txt="БЛАГОДІЙНИК _______________________ ОТРИМУВАЧ ДОПОМОГИ _________________________", ln=True)

    pdf_output = io.BytesIO()
    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    pdf_output.write(pdf_bytes)
    pdf_output.seek(0)

    return send_file(pdf_output, as_attachment=True, download_name="report.pdf", mimetype='application/pdf')
