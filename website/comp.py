import sqlite3
import os
import json
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from .get_data import get_comparison_data


comp = Blueprint('compare', __name__)


@comp.route('/comparison', methods=['GET', 'POST'])
def comparison():
    session.pop('comparison_ok', None)
    car_1_url = request.args.get('car_1')
    car_2_url = request.args.get('car_2')
    try:
        data = get_comparison_data(car_1_url, car_2_url)
    except:
        text="""<div class='d-flex justify-content-center align-items-center vh-100' style='max-height: 90vh'>
                <h3>Jeden z linków nie jest poprawny.</h3>
                </div>"""
        return render_template("comparison.html", text=text)
    text = "<table class='table table-hover text-center'>"
    text += "<tr><th></th><th>Samochód 1</th><th>Samochód 2</th>"
    i = 1
    for prop in next(iter(data.values())):
        if prop == 'currency':
            continue
        text += "<tr>"
        text += "<td class='text-muted'>"
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
    text += f"""<tr><td class='text-muted'>Link</td><td><a href='{car_1_url}' target='_blank'>{car_1_url}</a></td>
            <td class='text-muted'><a href='{car_2_url}' target='_blank'>{car_2_url}</a></td></tr>"""
    text += "</table>"
    if request.method == 'POST':
        try:
            conn = sqlite3.connect(os.path.join(os.getcwd(), os.getenv('DB_NAME')))
            result = conn.cursor().execute("select * from cars where url=?", (car_1_url, )).fetchall()
            if len(result) > 0:
                car_1_id = result[0][0]
            else:
                conn.cursor().execute("insert into cars(brand, model, production_year, price, url) values(?, ?, ?, ?, ?)",
                                      (data['car_1']['brand'], data['car_1']['model'],
                                        data['car_1']['year'], data['car_1']['price'],
                                        car_1_url))
                conn.commit()
                result = conn.cursor().execute("select * from cars where url=?", (car_1_url, )).fetchall()
                car_1_id = result[0][0]
            result = conn.cursor().execute("select * from cars where url=?", (car_2_url, )).fetchall()
            if len(result) > 0:
                car_2_id = result[0][0]
            else:
                conn.cursor().execute("insert into cars(brand, model, production_year, price, url) values(?, ?, ?, ?, ?)", (data['car_2']['brand'], data['car_2']['model'],
                                            data['car_2']['year'], data['car_2']['price'],
                                            car_2_url))
                conn.commit()
                result = conn.cursor().execute("select * from cars where url=?", (car_2_url, )).fetchall()
                car_2_id = result[0][0]
            conn.cursor().execute("insert into comparisons(user_id, car1_id, car2_id, is_active) values(?, ?, ?, 1)",
                                  (session['user_id'], car_1_id, car_2_id))
            conn.commit()
            flash("Dodano do moich porównań.")
            conn.close()
        except:
            flash("Podczas dodawania pojazdów wystąpił błąd.")
    session['comparison_ok'] = True
    return render_template("comparison.html", text=text)


@comp.route('/new-comparison',  methods=['GET', 'POST'])
def new_comparison():
    data = request.form.get('car_1')
    if request.method == 'POST':
        car_1 = request.form.get('car_1')
        car_2 = request.form.get('car_2')
        return redirect(url_for('compare.comparison', car_1=car_1, car_2=car_2))
    return render_template("new-comparison.html")


@comp.route('/my-comparisons', methods=['GET', 'POST'])
def my_comparisons():
    try:
        conn = sqlite3.connect(os.path.join(os.getcwd(), os.getenv('DB_NAME')))
        comparisons = conn.cursor().execute("""select CA1.brand, CA1.model, CA1.production_year, CA1.price, CA1.url,
                                            CA2.brand, CA2.model, CA2.production_year, CA2.price, CA2.url,
                                            CO.comparison_id, CO.is_active
                                            from comparisons CO join cars CA1 on CO.car1_id = CA1.car_id
                                            join cars CA2 on CO.car2_id = CA2.car_id
                                            where CO.is_active = 1 and CO.user_id=?""", (session['user_id'], )).fetchall()
        text = ""
        if len(comparisons) > 0:
            for comparison in comparisons:
                text += f"""<li class='list-group-item text-center'>
                            <a class='text-reset' href='/comparison?car_1={comparison[4]}&car_2={comparison[9]}'>
                            {comparison[0]} {comparison[1]} z {comparison[2]} za {comparison[3]}
                            <br />vs<br />
                            {comparison[5]} {comparison[6]} z {comparison[7]} za {comparison[8]}
                            </a>
                            <br />
                            <button type="button" class="close" onClick="deleteComparison({comparison[10]})">
                                <span>&times;</span>
                            </button>
                            </li><br />"""
        else:
            text = ""
        conn.close()
    except:
        flash("Podczas ładowania porównań wystąpił błąd.")
    if request.method == 'POST':
        try:
            conn = sqlite3.connect(os.path.join(os.getcwd(), os.getenv('DB_NAME')))
            conn.cursor().execute("update comparisons set is_active=0 where user_id=?", (session['user_id'], ))
            conn.commit()
            conn.close()
            return redirect(url_for('compare.my_comparisons'))
        except:
            flash("Podczas czyszczenia listy porównań wystąpił błąd.")
    return render_template("my-comparisons.html", text=text)


@comp.route('/delete-comparison', methods=['GET', 'POST'])
def delete_comparison():
    js = json.loads(request.data)
    try:
        conn = sqlite3.connect(os.path.join(os.getcwd(), os.getenv('DB_NAME')))
        conn.cursor().execute("update comparisons set is_active=0 where comparison_id=?", (js['comparison_id'], ))
        conn.commit()
        conn.close()
        return redirect(url_for('compare.my_comparisons'))
    except:
        flash("Podczas usuwania porównania wystąpił błąd.")
    return jsonify({})