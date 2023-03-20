from flask_app import app
from flask import render_template, redirect,request,session
from flask import flash,url_for 
import os
from werkzeug.utils import secure_filename
from fileinput import filename 
from flask_app.models.adventure import Adventure
from flask_app.models.user import User 

# UPLOAD_FOLDER = '/static/uploads/'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 *1024 

# ALLOWED_EXTENSIONS = set(['png','jpg','gif'])



@app.route('/new/adventure')                              #redirecting to page 3 
def new():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_by_id({"id":session['user_id']})

    if not user:
        return redirect('/user/logout')
    return render_template("new_adventure.html",user=user)


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_by_id({"id":session['user_id']})
    
    if not user:
        return redirect('/user/logout')

    data = {
            'id': id
        }

    #return render_template('dashboard.html', user=user, adventures=Adventure.get_all_adventures_with_creator(data), arrivals=Adventure.get_year())
    return render_template('dashboard.html', user=user, adventures=Adventure.get_all(),arrivals=Adventure.get_year())
    #  return render_template('dashboard.html', user=user.get_user_with_adventures(data),arrivals=Adventure.get_year())



@app.route('/adventure/<int:id>/')
def one_adventure(id):
    return render_template("edit_adventure.html", adventure=Adventure.get_by_id({'id': id}))    


@app.route('/adventure/<int:id>/edit')                  
def edit_adventure(id):
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_by_id({"id":session['user_id']})
    
    if not user:
        return redirect('/user/logout')
    return render_template("edit_adventure.html",user=user,adventure=Adventure.get_one({'id': id}))




@app.route('/adventure/<int:id>/show')
def view_adventure(id):
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_by_id({"id":session['user_id']})
    
    if not user:
        return redirect('/user/logout')

    return render_template('show_adventure.html',user=user,adventure=Adventure.get_one({'id' :id}))




#### POST #####
@app.route('/update/<int:id>/', methods=["POST"])
def update_adventure(id):
    adventure_info = request.form
    if Adventure.is_valid_adventure(adventure_info):
        data = {
        "id" : id,
        "city": request.form['city'],
        "country": request.form['country'],
        "arrival": request.form['arrival'],
        "departure": request.form['departure'],
        "memories": request.form['memories'],
    }
    # if Adventure.is_valid_adventure(adventure_info):
        Adventure.update(data)
        print("PASS")
        return redirect('/dashboard')
    print("FAIL")
    return redirect('/dashboard')




@app.route('/adventure/create', methods=["POST"])
def create_adventure():
    adventure_info = request.form
    if Adventure.is_valid_adventure(adventure_info):
        data = {
            'user_id':session['user_id'],
            'city':request.form['city'],
            'country':request.form['country'],
            'arrival':request.form['arrival'],
            'departure':request.form['departure'],
            'memories':request.form['memories'],
            "user_id": session['user_id']
        }

        
        Adventure.save(data)
        print("PASS")
        return redirect('/dashboard')
    print("FAIL")
    return redirect('/new/adventure')

@app.route('/adventures/<int:id>/destroy')
def destroy(id):
    Adventure.destory({'id':id})
    return redirect('/dashboard')

# def allowed_file(filename):
#     return'.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/up', methods=['POST'])
# def upload_img():
#     if 'file' not in request.files:
#         flash('No file part')
#         return redirect(request.url)
#     file = request.files['file']
#     if file.filename == '':
#         flash('No image selected for uploading')
#         return redirect(request.url)
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
#         #print('upload_image filename: '+ filename)
#         flash('image successful')
#         return render_template('index.html',filename=filename)
#     else:
#         flash('allowed images png-jpg-gif')
#         return redirect(request.url)

# @app.route('/display/<filename>')
# def display_image(filename):
#     #print('display_image filename:' + filename)
#     return redirect(url_for('static', filename='uploads/'+filename), code=301)


