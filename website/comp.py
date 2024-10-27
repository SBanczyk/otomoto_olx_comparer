from flask import Blueprint, render_template, request, redirect, url_for
from .get_data import get_comparison_data
from sys import argv


comp = Blueprint('compare', __name__)


@comp.route('/comparison', methods=['GET', 'POST'])
def comparison():
    car_1 = request.args.get('car_1')
    car_2 = request.args.get('car_2')
    try:
        data = get_comparison_data(car_1, car_2)
    except ValueError:
        return render_template("comparison.html", text = "<h1 style='text-align:center'>Niepoprawny link.</h1>")
    text = "<table class='table table-hover text-center'>"
    i = 1
    for prop in next(iter(data.values())):
        if prop == 'currency':
            continue
        text += "<tr>"
        text += f"<td class='text-muted'>"
        if prop == 'brand':
            text += "Marka"
        elif prop == 'model':
            text += "Model"
        elif prop == 'year':
            text += "Rok produkcji"
        elif prop == 'fuel':
            text += "Paliwo"
        elif prop == 'engine_size':
            text += "Pojemność silnika"
        elif prop == 'power':
            text += "Moc"
        elif prop == 'gearbox':
            text += "Skrzynia biegów"
        elif prop == 'mileage':
            text += "Przebieg"
        elif prop == 'price':
            text += "Cena"
        elif prop == 'website':
            text += "Portal aukcyjny"
        text += "</td>"
        for attributes in data.values():
            text += f"<td>{attributes[prop]}"
            if prop == 'price':
                car_number = f"car_{i}"
                if data[car_number]['currency'] == "zł":
                    text += " PLN"
                else:
                    text += f" {data[car_number]['currency']}"
                i += 1
            if prop == 'power':
                text += " KM"
            if prop == 'engine_size':
                text += " cm3"
            if prop == 'mileage':
                text += " km"
            text += "</td>"
        text += "</tr>"
    text += "</table>"
    text += "<div class='text-center mt-3'> <form method='POST'> <button type='submit' class='btn btn-primary btn-lg'>Dodaj do moich porównań</button> </form> </div>"
    if request.method == 'POST':
        return redirect(url_for('views.home'))
    return render_template("comparison.html", text=text)


@comp.route('/new-comparison',  methods=['GET', 'POST'])
def new_comparison():
    data = request.form.get('car_1')
    if request.method == 'POST':
        car_1 = request.form.get('car_1')
        car_2 = request.form.get('car_2')
        return redirect(url_for('compare.comparison', car_1=car_1, car_2=car_2))
    return render_template("new-comparison.html")


@comp.route('/my-comparisons')
def my_comparisons():
    text = """<div class='d-flex justify-content-center align-items-center vh-100' style='max-height: 90vh'>
                <h1>Moje porównania.</h1>
            </div>
            """
    return render_template("my-comparisons.html", text=text)
