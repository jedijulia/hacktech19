import json

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
         results = json.loads(resp.json())
         search_results = results['searchResult']['item']
         #Pass the above list of items for further enquiry - get material
         appended_results = ebay_obj.getAppendedResults(search_results)
         return render_template('sr.html',results=appended_results)
    else:
      return render_template('index.html')

@blueprint.route('/<template>')
@login_required
def route_template(template):
    return render_template(template + '.html',
                           product_good_title="Burlap Bag",
                           product_bad_title="Plastic Retail Bag",
                           product_good_description="1.Multi-Function eco-friendly Burlap Bags for storing small object items such as small gifts, coins, jewelry, makeup bottle cream jar and any other of your small daily items to keep all of them in a bag clean and organized.2.Comes with Unique Double Drawstring for easy fasten and avoid object item lost.3.Inner is made of soft material which prevent scratching or keeping items clean when storing.4.Wide use application: Suitable Gift Bag for Wedding Favor Gift, Crafting DIY Projects, Home use, Travelling, Beach Theme Wedding Favor, and any other occasions.",
                           product_bad_description="T-Shirt Carry-Out Bags Small Thank you bags Grocery, Convenience stores, Restaurant take out, Carry-out",
                           product_good_images=["/static/images/good-1.jpg","/static/images/good-2.jpg","/static/images/good-3.jpg","/static/images/good-4.jpg","/static/images/good-5.jpg"],
                           product_bad_images=["/static/images/bad-1.jpg","/static/images/bad-2.jpg","/static/images/bad-3.jpg"]
                           )
