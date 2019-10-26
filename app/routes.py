from flask import render_template, session, flash, redirect, request, url_for, session, logging
from app import app, mysql
# from app.data import Articles
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps  # this is used to block unauthorised access of the dashboard when not in session
from app.forms import ArticleForm


@app.route('/')
def index():
    return render_template('index.html', name='Home Pge')


def is_logged_in(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized access, Please login', 'danger')
            return redirect(url_for('login'))

    return wrapped


@app.route('/about')
def about():
    return render_template('about.html', name='About')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # get form field
        username = request.form['username']
        password_entered = request.form['password']

        if username or password_entered:

            # create cursor
            cur = mysql.connection.cursor()
            result = cur.execute('SELECT * FROM new_users WHERE username = %s', [username])

            if result > 0:
                data = cur.fetchone()
                password = data['password']
                # compare passwords
                if check_password_hash(password, password_entered):
                    # passed
                    session['logged_in'] = True
                    session['username'] = username

                    flash('you are now logged in', 'success')
                    return redirect(url_for('dashboard'))
                    # return 'password match'
                else:
                    error = 'Invalid login'
                    return render_template('login.html', error=error)
            else:
                error = 'User not found'
                return render_template('login.html', error=error)

    return render_template('login.html', name='Login')


# dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    cur = mysql.connection.cursor()

    result = cur.execute('SELECT * FROM articles')
    article = cur.fetchall()

    if result > 0:
        return render_template('dashboard.html', articles=article, name='dashboard')
    else:
        msg = 'No Article found'
        return render_template('dashboard.html', msg=msg, name='dashboard')

    cur.close()


# form class
@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data

        # creating cursor
        cur = mysql.connection.cursor()

        cur.execute('INSERT INTO articles(title, body, author) VALUES (%s, %s, %s)', (title, body, session['username']))
        mysql.connection.commit()
        cur.close()
        flash('Article created', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_article.html', name='Article', form=form)


@app.route('/edit_article/<string:id>/', methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):
    cur = mysql.connection.cursor()
    result = cur.execute('SELECT * FROM articles WHERE id=%s', [id])
    article = cur.fetchone()

    form = ArticleForm(request.form)

    # populating form
    form.title.data = article['title']
    form.body.data = article['body']

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']

        # creating cursor
        cur = mysql.connection.cursor()

        app.logger.info(title)

        cur.execute('UPDATE articles SET title=%s, body=%s WHERE id=%s', (title, body, id))
        mysql.connection.commit()
        cur.close()
        flash('Article Updated', 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit_article.html', name='Article', form=form)


@app.route('/delete_article/<string:id>/', methods=['POST'])
@is_logged_in
def delete_article(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM articles WHERE id=%s', [id])
    mysql.connection.commit()
    cur.close()
    flash('Article deleted', 'success')
    return redirect(url_for('dashboard'))


@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


@app.route('/articles')
def articles():
    cur = mysql.connection.cursor()

    result = cur.execute('SELECT * FROM articles')
    article = cur.fetchall()

    if result > 0:
        return render_template('articles.html', articles=article, name='Articles')
    else:
        msg = 'No Article found'
        return render_template('articles.html', msg=msg, name='Articles')

    cur.close()


@app.route('/article/<string:id>/')
def article(id):
    cur = mysql.connection.cursor()

    result = cur.execute('SELECT * FROM articles WHERE id=%s', [id])
    article = cur.fetchone()

    return render_template('article.html', article=article, name='article')

    cur.close()
    article = Articles()
    return render_template('article.html', articles=article, id=id, name='Articles')
