from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import processor
import json
import ast
import nltk


app = Flask(__name__)
app.config['SECRET_KEY'] = 'enter-a-very-secretive-key-3479373'
intents = json.loads(open('job_intents.json', encoding='utf-8').read())


class StatementForm(FlaskForm):
    statement = StringField('Statement', validators=[DataRequired()])
    submit = SubmitField('Click to check intent')


@app.route('/', methods=["GET", "POST"])
def index():
    form = StatementForm()
    if form.validate_on_submit():
        question = form.statement.data
        result = processor.predict_class(question, processor.model)
        result_ = str(result).lstrip('[').rstrip(']')
        result_dict = ast.literal_eval(result_)
        jibu = processor.getResponse(result_dict, intents)

        flash(f'The statement {form.statement.data} has the following intent', 'success')
        return redirect(url_for('chatResponse', data=result, jibu=jibu))

    return render_template('index.html', form=form)


@app.route('/result', methods=["GET", "POST"])
def chatResponse():
    data = request.args.get('data')
    jibu = request.args.get('jibu')

    return render_template('response.html', result=data, jibu=jibu)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='6060', debug=True)
