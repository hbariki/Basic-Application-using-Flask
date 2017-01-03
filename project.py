## imported Flask class from flask library
from flask import Flask, render_template, request, redirect, url_for

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
       session.add(newItem)
       session.commit()
       return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))

    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)

#Route for newEditmenuItem 
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
    return "page to edit a menu item. Task 2 complete!"

#Route for deleteMenuItem 
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete a menu item. Task 3 complete!"

if __name__ == '__main__' :
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
    



