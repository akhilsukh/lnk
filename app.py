from flask import Flask, render_template, redirect, url_for, jsonify
from wtforms import Form, URLField, StringField, validators
from flask_bootstrap import Bootstrap
from forms import MainForm
from db import get_all, get_redirect, create_redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cT13FYw7nMowrpsBQBc29zwWhlBZL5j7'
Bootstrap(app)


@app.route("/", methods=['GET', 'POST'])
def index():
    form = MainForm()
    message = False
    if form.validate_on_submit():
        if get_redirect(form.code.data, False):
            message = True
        else:
            message = False
            create_redirect(form.code.data, form.link.data)
            return redirect(url_for('confirmation', code=form.code.data))
    return render_template('index.html', form=form, message=message)


@app.route("/dashboard/<code>")
def confirmation(code):
    return render_template('confirmation.html', code=code)


@app.route('/dashboard')
def dashboard():
    rows = get_all()
    rows = [jsonify(code=row[0], link=row[1], visits=row[2]).get_json() for row in rows]
    return render_template('dashboard.html', rows=rows)


@app.route("/404")
@app.errorhandler(404)
def four_oh_four():
    return render_template('404.html'), 404


@app.route("/<code>")
def redirect_code(code):
    d = get_redirect(code, True)
    if not d:
        return redirect(url_for('404'))
    return redirect(d)


# @app.route("/create/<path:link>")
# @app.route("/create/<path:link>/")
# def insert(link):
#     try:
#         if len(link.split(':')) == 0:
#             return f'<p>Bad create statement.</p>'
#         code = link.split(':')[0]
#         red = link.remove(code + ':')
#
#         connection = sqlite3.connect("links.db")
#         cursor = connection.cursor()
#
#         cursor.execute(f"SELECT link FROM links WHERE code = '{code}'")
#         d = cursor.fetchall()
#         if d:
#             return f'<p>Code already exists.</p>'
#
#         cursor.execute(f"INSERT INTO links VALUES({code}, {red});")
#         connection.commit()
#     except Error:
#         connection.close()
#         return f"<p>Some error occurred: {d}</p>"
#     #        return f"<p>Created link for: {redi}</p>"
#     connection.close()
#     return f"<p>Created link for: {red}</p>"