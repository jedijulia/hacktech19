import json

from app.home import blueprint
from flask import render_template,request,redirect,url_for,jsonify
from flask_login import login_required

from app.home import ebayclass


from app.home import ranker



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
    unsorted_results = appended_results[0]
    ranker_obj = ranker.Ranker()
    ranked_list = ranker_obj.rankThem(appended_results)
    return render_template('sr.html',results=ranked_list)
  else:
    return render_template('index.html')

title = "OOPS";
price = "OOPS";
material = "OOPS";
emission = "OOPS";
image = "OOPS";

@blueprint.route('/sr',methods=['GET','POST'])
@login_required
def sr():
  global title
  global price
  global material
  global emission
  global image

  if request.method == 'POST':
    title = request.form['title']
    price = request.form['price']
    material = request.form['material']
    emission = request.form['emission']
    image = request.form['image']
    return jsonify(redirect="/home/ei")

@blueprint.route('/ei',methods=['GET','POST'])
@login_required
def ei():
  global title
  global price
  global material
  global emission
  global image
  global unsorted_results
  pg_emission_mult = float(emission) * float(23.78)
  pp_emission_mult = float(unsorted_results['emission']) * float(23.78)
  if request.method == 'GET':
    return render_template('ei.html',
                           pg_title=title,
                           pg_price=price,
                           pg_material=material,
                           pg_emission=emission,
                           pg_emission_m=pg_emission_mult,
                           pg_image=image,
                           pp_title=unsorted_results['title'],
                           pp_image=unsorted_results['gallleryURL'],
                           pp_material=unsorted_results['material'],
                           pp_emission=unsorted_results['emission'],
                           pp_emission_m=pp_emission_mult,
                           pp_price=unsorted_results['price'])
