from flask import Flask, request, render_template, redirect, url_for
from datetime import date

app = Flask(__name__)

CATEGORIES = ['Food', 'Travel', 'Shopping', 'Bills', 'Entertainment', 'Other']

expenses = []


@app.route('/')
def index():
    total = sum(e['amount'] for e in expenses)
    return render_template('index.html', expenses=expenses, total=total)


@app.route('/add')
def add():
    return render_template('add.html', categories=CATEGORIES, today=date.today().isoformat())


@app.route('/submit', methods=['POST'])
def submit():
    title = request.form.get('title', '').strip()
    category = request.form.get('category', '')
    expense_date = request.form.get('date') or date.today().isoformat()

    try:
        amount = round(float(request.form.get('amount', '')), 2)
    except ValueError:
        amount = 0

    if not title or amount <= 0 or category not in CATEGORIES:
        return redirect(url_for('add'))

    expenses.append({'title': title, 'amount': amount,
                     'category': category, 'date': expense_date})
    return render_template('success.html', title=title, amount=amount, category=category)


@app.route('/summary')
def summary():
    totals = {}
    for e in expenses:
        totals[e['category']] = totals.get(e['category'], 0) + e['amount']
    grand_total = sum(totals.values())
    rows = sorted(totals.items(), key=lambda kv: kv[1], reverse=True)
    return render_template('summary.html', rows=rows, grand_total=grand_total)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8003)
