from flask import Flask, request, render_template
import requests
import csv

app = Flask(__name__, template_folder='templates')


def write_to_csv(data):
    with open('converted_data.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Currency', 'Code', 'Bid', 'Ask'])
        for item in data:
            writer.writerow(item)


@app.route('/')
def index():
    response = requests.get('http://api.nbp.pl/api/exchangerates/tables/C?format=json')
    data = response.json()
    rates = data[0]['rates']
    currency_codes = [rate['code'] for rate in rates]
    return render_template('index.html', currency_codes=currency_codes)


@app.route('/', methods=['POST'])
def convert():
    response = requests.get('http://api.nbp.pl/api/exchangerates/tables/C?format=json')
    data = response.json()
    rates = data[0]['rates']

    selected_code = request.form['currency_code']
    amount = float(request.form['amount'])

    selected_rate = None
    for rate in rates:
        if rate['code'] == selected_code:
            selected_rate = rate
            break

    cost_in_pln = amount * selected_rate['bid']

    data = [[selected_rate['currency'], selected_code, selected_rate['bid'], selected_rate['ask']]]
    write_to_csv(data)

    return render_template('result.html', amount=amount, selected_code=selected_code, cost_in_pln=round(cost_in_pln, 2))


if __name__ == '__main__':
    app.run(debug=True)
