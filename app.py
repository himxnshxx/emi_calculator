from flask import Flask, render_template, request
import math

app = Flask(__name__)

def calculate_emi(principal, rate, tenure):
    rate = rate / (12 * 100)  
    tenure = tenure * 12      
    emi = (principal * rate * math.pow(1 + rate, tenure)) / (math.pow(1 + rate, tenure) - 1)
    return round(emi, 2)

def generate_schedule(principal, rate, tenure):
    rate = rate / (12 * 100)
    tenure = tenure * 12
    emi = calculate_emi(principal, rate * 12 * 100 / 12, tenure / 12)
    schedule = []
    for month in range(1, tenure + 1):
        interest_payment = round(principal * rate, 2)
        principal_payment = round(emi - interest_payment, 2)
        principal -= principal_payment
        schedule.append([month, emi, principal_payment, interest_payment, round(principal, 2)])
    return schedule

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            principal = float(request.form['principal'])
            rate = float(request.form['rate'])
            tenure = int(request.form['tenure'])

            if principal <= 0 or rate <= 0 or tenure <= 0:
                return render_template('index.html', error="Invalid input values.")

            emi = calculate_emi(principal, rate, tenure)
            schedule = generate_schedule(principal, rate, tenure)

            return render_template('index.html', emi=emi, schedule=schedule)
        except ValueError:
            return render_template('index.html', error="Please enter valid numeric values.")

    return render_template('index.html', emi=None, schedule=None)

if __name__ == "__main__":
    app.run(debug=True)
