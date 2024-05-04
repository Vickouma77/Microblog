from flask import(
   flash, 
   redirect, 
   render_template,
   request,
   url_for
)
from app import app, db
from app.forms import LoginForm
from flask_login import(
   current_user, 
   login_user, 
   logout_user, 
   login_required
   )
import sqlalchemy as sa
from app.models import User
from urllib.parse import urlsplit

@app.route('/')
@app.route('/index')
@login_required
def index():
   posts = [
      {
         'author': 'James',
         'body': 'Always huffing and puffing'
      },
      {
         'author': 'Linzie',
         'body': 'Growing metals and irons'
      },
      {
         'author': 'Mainoo',
         'body': 'Ole on the wheel'
      }
   ]

   return render_template('index.html', title='Home', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
   if current_user.is_authenticated:
      return redirect(url_for('index'))
   form = LoginForm()
   if form.validate_on_submit():
      user = db.session.scalar(
         sa.select(User).where(User.username == form.username.data))
      if user is None or not user.check_password(form.password.data):
         flash('Invalid Username or Password')
         return redirect(url_for('login'))
      login_user(user, remember=form.remember_me.data)
      next_page = request.args.get('next')
      if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
      return redirect(next_page)
   return render_template('login.html', title='sign in', form=form)

@app.route('/logout')
def logout():
   logout_user()
   return redirect(url_for('index'))