from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flashing messages

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('../credentials.json', scope)
client = gspread.authorize(creds)

# Open the workbook and the sheets
workbook = client.open('GET Test')
student_sheet = workbook.worksheet('Sheet1')
product_sheet = workbook.worksheet('products')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        student_id = request.form['student_id']
        records = student_sheet.get_all_records()
        for record in records:
            if record['Student-ID'] == student_id:
                product_records = product_sheet.get_all_records()
                return render_template('dashboard.html', record=record, products=product_records)
        flash("Student ID not found", "error")
    return render_template('index.html')

@app.route('/update', methods=['POST'])
def update():
    student_id = request.form['student_id']
    amount_to_add = int(request.form['amount'])
    quota = request.form['quota']
    access = request.form.getlist('access')
    access_str = '-'.join(access)

    records = student_sheet.get_all_records()
    for idx, record in enumerate(records):
        if record['Student-ID'] == student_id:
            current_amount = int(record['Amount'])
            new_amount = current_amount + amount_to_add
            student_sheet.update_cell(idx + 2, 4, new_amount)  # Amount column
            student_sheet.update_cell(idx + 2, 6, quota)       # Quota column
            student_sheet.update_cell(idx + 2, 7, access_str)  # Access List column
            break

    flash("Details updated successfully", "success")
    return redirect(url_for('index'))

@app.route('/api/student/<student_id>', methods=['GET'])
def api_get_student(student_id):
    record = get_student_record(student_id)
    if record:
        return jsonify(record)
    else:
        return jsonify({'error': 'Student ID not found'}), 404

def get_student_record(student_id):
    records = student_sheet.get_all_records()
    record = next((record for record in records if record['Student-ID'] == student_id), None)
    return record

@app.route('/api/card/<card_id>', methods=['GET'])
def api_get_card(card_id):
    record = get_student_card(card_id)
    if record:
        return jsonify(record)
    else:
        return jsonify({'error': 'Student card not found'}), 404

def get_student_card(card_id):
    records = student_sheet.get_all_records()
    record = next((record for record in records if record['ID'] == card_id), None)
    return record

@app.route('/api/products', methods=['GET'])
def api_get_products():
    products = products_sheet.get_all_records()
    return jsonify(products)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
