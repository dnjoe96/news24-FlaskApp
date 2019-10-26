from app import app, mysql
from flask import render_template, request, redirect, flash, url_for
from app.forms import RegistrationForm
from werkzeug.security import generate_password_hash, check_password_hash

# configure databases
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'user1'
app.config['MYSQL_PASSWORD'] = 'Praise@1234'
app.config['MYSQL_DB'] = 'blackbook'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = generate_password_hash(form.password.data)

        # create cursor
        cur = mysql.connection.cursor()

        # execute query
        cur.execute('INSERT INTO new_users (name, email, username, password) VALUES (%s, %s, %s, %s)',
                    (name, email, username, password))

        # commit to database
        mysql.connection.commit()

        # close connection
        cur.close()

        flash('You are now registered', 'success')
        return redirect(url_for('index'))   # redirects user back to the index page

    return render_template('register.html', form=form, name='Sign Up')
