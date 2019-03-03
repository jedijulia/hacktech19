import json

from app.home import blueprint
from flask import render_template,request,redirect,url_for,jsonify
from flask_login import login_required

from app.home import ebayclass

unsorted_results = "init"
@blueprint.route('/index',methods=['GET', 'POST'])
@login_required
def index():
  global unsorted_results
    if request.method == 'POST':
      search = request.form['search']
      ebay_obj = ebayclass.mainBay()
      #(opts, args) = ebay_obj.init_options()
      resp = ebay_obj.run(search)
      results = json.loads(resp.json())
      search_results = results['searchResult']['item']
      appended_results = ebay_obj.getAppendedResults(search_results)
      return render_template('sr.html',results=appended_results)
    else:
      return render_template('index.html')

title = "OOPS";
subtitle = "OOPS";
price = "OOPS";
material = "OOPS";
emission = "OOPS";

@blueprint.route('/sr',methods=['GET','POST'])
@login_required
def sr():
  global title
  global subtitle
  global price
  global material
  global emission

  if request.method == 'POST':
    title = request.form['title']
    subtitle = request.form['subtitle']
    price = request.form['price']
    material = request.form['material']
    emission = request.form['emission']
    return jsonify(redirect="/home/ei");

@blueprint.route('/ei',methods=['GET','POST'])
@login_required
def ei():
  if request.method == 'GET':
    return render_template('ei.html',product_good_title=title,
                           product_bad_title=unsorted_results[0].title,
                           product_good_images=["/static/images/good-1.jpg","/static/images/good-2.jpg","/static/images/good-3.jpg","/static/images/good-4.jpg","/static/images/good-5.jpg"],
                           product_bad_images=["/static/images/bad-1.jpg","/static/images/bad-2.jpg","/static/images/bad-3.jpg"])
