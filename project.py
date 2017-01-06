## imported Flask class from flask library
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

## It creates an instance of class with nae of running application.when we run application special variable called name is gets defined from the application
app = Flask(__name__)
## import sql alchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

## create session and connect to db
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
# Making an API End point (GET REQUEST)
@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(Menuitems=[i.serialize for i in items])

# JSON ENDPOINT to one specific menu
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=menuItem.serialize)


# If we enter the route it takes to the hello page.If this is not present if we enter the route it shows error
@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id= restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items = items)

# Route for newMenuitem
@app.route('/restaurant/<int:restaurant_id>/new', methods=['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
       newItem = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)
       print newItem.name
       session.add(newItem)
       session.commit()
       return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))

    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)

#Route for newEditmenuItem
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id = menu_id).one()
    restaurant = session.query(Restaurant).filter_by(id =restaurant_id).one()
    print editedItem.name
    print editedItem.id
    print restaurant_id
    if request.method == 'POST':
       if request.form['name']:
           editedItem.name = request.form['name']
       session.add(editedItem)
       session.commit()
       return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))

    else:
      return render_template('editmenu.html', restaurant_id = restaurant_id, menu_id = menu_id, item = editedItem)


#Route for deleteMenuItem
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    deletedItem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
       session.delete(deletedItem)
       session.commit()
       flash("Menu Item has been deleted")
       return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
      return render_template('deletemenu.html',restaurant_id = restaurant_id, item = deletedItem)


if __name__ == '__main__' :
    app.secret_key = 'super secret key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
