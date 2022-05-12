from flask import Flask, render_template, jsonify, request, redirect, url_for,flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import processor
import json
import ast

app = Flask(__name__)
app.config['SECRET_KEY'] = 'enter-a-very-secretive-key-3479373'


class StatementForm(FlaskForm):
    statement = StringField('Statement', validators=[DataRequired()])
    submit = SubmitField('Click to check intent')


@app.route('/', methods=["GET", "POST"])
def index():
    form = StatementForm()
    if form.validate_on_submit():
        question = form.statement.data
        response = processor.predict_class(question, processor.model)
        flash(f'The statement {form.statement.data} has the following intent')
        print(response)
        return redirect(url_for('chatResponse', data=response))

    return render_template('index.html', form=form)


@app.route('/result', methods=["GET", "POST"])
def chatResponse():
    data = request.args.get('data')

    return render_template('response.html', result=data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='6060', debug=True)
