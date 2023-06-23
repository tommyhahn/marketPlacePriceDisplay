from flask import Flask, jsonify, request, Response, send_file, render_template
from flask_cors import CORS
from data_retriever import retrieve_data
from data_transformer import transform_data
import pandas as pd
import xlsxwriter
from io import StringIO, BytesIO

app = Flask(__name__, template_folder='../frontend/public')
CORS(app)


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/api/fetch', methods=['GET'])
def fetch_data():
    raw_data = retrieve_data()
    transformed_output = transform_data(raw_data)

    return jsonify(transformed_output)


@app.route('/api/download', methods=['POST'])
def download():
    # Get the requested format parameter (json/csv/xlsx).
    format_param = request.args.get('format')

    # Retrieve and transform the pricing data from URL.
    raw_data = retrieve_data()
    transformed_output = transform_data(raw_data)

    if format_param == 'csv':
        headers = {'Content-Disposition': 'attachment;filename=transformed_data.csv'}
        csv_string = transform_data_csv(transformed_output)
        return Response(csv_string, mimetype='text/csv', headers=headers)

    elif format_param == 'xlsx':
        headers = {'Content-Disposition': 'attachment;filename=transformed_data.xlsx'}
        xlsx_binary = transform_data_excel(transformed_output)  # Pass in transformed_output as argument
        return Response(
            xlsx_binary,
            headers=headers,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )

    else:
        # Default to returning JSON-format of transformed data.
        response_headers = {
            'Content-Disposition': f'attachment;filename=transformed_pricing.{format_param}',
            'Content-Type': 'application/json'
        }

        json_string_buffer = StringIO()

        pd.DataFrame.from_dict(transformed_output).to_json(json_string_buffer, orient='index')

        return send_file(BytesIO(json_string_buffer.getvalue().encode()),
                         mimetype='application/json',
                         as_attachment=True,
                         attachment_filename=f'transformed_pricing.{format_param}')


def transform_data_csv(transformed_data):
    columns = transformed_data[0].keys()
    csv_str = ','.join(columns) + '\n'
    for row in transformed_data:
        values = [str(row[col]) for col in columns]
        csv_str += ','.join(values) + '\n'
    return csv_str


def transform_data_excel(transformed_data):
    # Create new Excel workbook and worksheet.
    output_file = BytesIO()
    workbook = xlsxwriter.Workbook(output_file)
    worksheet = workbook.add_worksheet()

    # Write column headers.
    columns = transformed_data[0].keys()
    for i, col in enumerate(columns):
        worksheet.write(0, i, col)

    # Write data rows.
    for row_num, row in enumerate(transformed_data):
        values = [str(row[col]) for col in columns]
        for i, value in enumerate(values):
            worksheet.write(row_num + 1, i, value)

    workbook.close()  # Close workbook after writing it out!

    output_file.seek(0)  # Reset seek position to beginning of file.

    return output_file.getvalue()


if __name__ == '__main__':
    app.run(debug=True, port=3000)
