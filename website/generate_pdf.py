from flask import Flask, render_template, request, send_file
from fpdf import FPDF
import io

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('our_home.html')

@app.route('/create_pdf')
def create_pdf_page():
    return render_template('create_pdf.html')

@app.route('/create_pdf', methods=['POST'])
def create_pdf():
    text = request.form['text_content']
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for line in text.split('\n'):
        pdf.multi_cell(0, 10, line)

    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)

    return send_file(pdf_output, as_attachment=True, download_name="report.pdf", mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
