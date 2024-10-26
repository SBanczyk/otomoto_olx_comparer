from flask import Blueprint ,render_template
from .get_data import get_comparison_data
from sys import argv


views = Blueprint('views', __name__)


@views.route('/')
def home():
    data = get_comparison_data(argv[1], argv[2])
    ret = "<table class='table table-hover text-center'>"
    for prop in next(iter(data.values())):
        ret += "<tr>"
        ret += f"<td class='text-muted'>{prop}</td>"
        for attributes in data.values():
            ret += f"<td>{attributes[prop]}</td>"
        ret += "</tr>"
    ret += "</table>"
    return render_template("home.html", text = ret)