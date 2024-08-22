import os
import requests
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)

# Configurações do Mailgun
MAILGUN_DOMAIN = 'ep.mydomain.com'  
MAILGUN_API_KEY = '' 
RECIPIENT_EMAILS = ['flaskaulasweb@zohomail.com', 'e.pelegrini@aluno.ifsp.edu.br']

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

def send_email(subject, body, recipients):
    response = requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={"from": f"Flask App <mailgun@{MAILGUN_DOMAIN}>",
              "to": recipients,
              "subject": subject,
              "text": body})

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        
        session['name'] = form.name.data

        # Enviar e-mail notificando o cadastro de um novo usuário
        subject = "Novo usuário cadastrado"
        body = f"Usuário cadastrado: {form.name.data}"
        send_email(subject, body, RECIPIENT_EMAILS)

        return redirect(url_for('index'))
    
    return render_template('index.html', form=form, name=session.get('name'))

if __name__ == "__main__":
    app.run(debug=True)
