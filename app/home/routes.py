from app.home import blueprint
from flask import render_template,request
from flask_login import login_required

from app.home import ebayclass


@blueprint.route('/index',methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
         search = request.form['search']
         ebay_obj = ebayclass.mainBay()
         #(opts, args) = ebay_obj.init_options()
         resp = ebay_obj.run(search)
         return render_template('index.html',success_message=str(resp.json()))  
     
    return render_template('index.html')


@blueprint.route('/<template>')
@login_required
def route_template(template):
    return render_template(template + '.html')
