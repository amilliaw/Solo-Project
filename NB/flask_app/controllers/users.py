from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)

#### GET METHODS #### 

@app.route('/')
def index():
    return render_template('index.html')


# @app.route('/user/account')
# def account():
#     data ={
#         'id': session['user_id']
#     }
#     return render_template('user_account.html',user=User.get_one_adventures(data))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')



#### POST #### 

@app.route('/register',methods=['POST'])
def create():
    if not User.validate_create(request.form):
        return redirect('/')
    #if not filled our write returns to main page
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password']) #hash pw
    }
    id = User.save(data)
    session['user_id'] = id

    return redirect('/dashboard')



@app.route('/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid Email or Password!","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid email or password!","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard') #

