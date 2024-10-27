from flask import Blueprint, render_template
from .get_data import get_comparison_data
from sys import argv


comp = Blueprint('compare', __name__)


@comp.route('/comparison')
def comparison():
    data = get_comparison_data(argv[1], argv[2])
    ret = "<table class='table table-hover text-center'>"
    for prop in next(iter(data.values())):
        ret += "<tr>"
        ret += f"<td class='text-muted'>{prop}</td>"
        for attributes in data.values():
            ret += f"<td>{attributes[prop]}</td>"
        ret += "</tr>"
    ret += "</table>"
    return render_template("comparison.html", text = ret)


@comp.route('/new-comparison')
def new_comparison():
    text = """<div class='d-flex justify-content-center align-items-center vh-100'>
                <h1>Nowe porównanie.</h1>
            </div>
            """
    return render_template("new-comparison.html", text=text)


@comp.route('/my-comparisons')
def my_comparisons():
    text = """<div class='d-flex justify-content-center align-items-center vh-100'>
                <h1>Moje porównania.</h1>
            </div>
            """
    return render_template("my-comparisons.html", text=text)