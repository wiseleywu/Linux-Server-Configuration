from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_imageattach.entity import Image, image_attachment
from sqlalchemy_imageattach.stores.fs import HttpExposedFileSystemStore
from sqlalchemy_imageattach.context import store_context
from database_setup import Base, Antibody, Cytotoxin, AntibodyImg, AntibodyLot, CytotoxinImg, CytotoxinLot, ADC, ADCLot

app = Flask(__name__)
fs_store = HttpExposedFileSystemStore('userimages', 'static/images/')
app.wsgi_app = fs_store.wsgi_middleware(app.wsgi_app)

engine = create_engine('sqlite:///biologicscatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Making an API Endpoint (GET Request)
# @app.route('/restaurants/<int:restaurant_id>/menu/JSON')
# def restaurantMenuJSON(restaurant_id):
#     restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
#     items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
#     return jsonify(MenuItems=[i.serialize for i in items])
#
# @app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
# def restaurantMenuItemJSON(restaurant_id, menu_id):
#     items = session.query(MenuItem).filter_by(id=menu_id).one()
#     return jsonify(MenuItems=[items.serialize])

@app.route('/')
@app.route('/home')
def mainMenu():
    return render_template('home.html')

@app.route('/antibody')
def antibodyMenu():
    return render_template('antibody.html')

@app.route('/cytotoxin')
def cytotoxinMenu():
    return render_template('cytotoxin.html')

@app.route('/ADC')
def adcMenu():
    return render_template('adc.html')

@app.route('/templates/edit.html')
def edit():
    return render_template('edit.html')

# @app.route('/')
# @app.route('/restaurants/<int:restaurant_id>/menu')
# def restaurantMenu(restaurant_id):
#     restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
#     items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
#     return render_template('menu.html', restaurant=restaurant, items=items)

# Task 1: Create route for newMenuItem function here
# @app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET','POST'])
# def newMenuItem(restaurant_id):
#     if request.method == 'POST':
#         newItem=MenuItem(name=request.form['name'], restaurant_id=restaurant_id)
#         session.add(newItem)
#         session.commit()
#         flash("new menu item created!")
#         return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
#     else:
#         return render_template('newmenuitem.html', restaurant_id=restaurant_id)
#
# # Task 2: Create route for editMenuItem function here
#
# @app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET','POST'])
# def editMenuItem(restaurant_id, menu_id):
#     editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
#     if request.method == 'POST':
#         if request.form['name']:
#             editedItem.name = request.form['name']
#         session.add(editedItem)
#         session.commit()
#         flash("Menu Item Edited")
#         return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
#     else:
#         return render_template(
#             'editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)
#
# # Task 3: Create a route for deleteMenuItem function here
#
# @app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/',methods=['GET','POST'])
# def deleteMenuItem(restaurant_id, menu_id):
#     deleteItem = session.query(MenuItem).filter_by(id=menu_id).one()
#     if request.method == 'POST':
#         session.delete(deleteItem)
#         session.commit()
#         flash("Menu Item Deleted")
#         return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
#     else:
#         return render_template(
#             'deletemenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=deleteItem)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
