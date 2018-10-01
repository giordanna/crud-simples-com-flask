from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from flask import Flask
from flask import request, redirect, url_for, render_template, flash, jsonify
app = Flask(__name__)

engine = create_engine("sqlite:///restaurantMenu.db")
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

# Restaurants routing and CRUD
@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template("restaurants.html", restaurants = restaurants)

@app.route('/restaurants/restaurant/JSON')
def restaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(restaurants = [r.serialize for r in restaurants])

@app.route('/restaurants/restaurant/<int:restaurant>/JSON')
def restaurantItemJSON(restaurant):
    myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurant).one()
    return jsonify(restaurantItem = myRestaurantQuery.serialize)

@app.route('/restaurants/create', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        newItem = Restaurant(name = request.form['name'])
        session.add(newItem)
        session.commit()
        flash("New restaurant created!")
        return redirect(url_for("showRestaurants"))
    else: 
        return render_template("newRestaurant.html")

@app.route('/restaurants/<int:restaurant>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant):
    restaurantItem = session.query(Restaurant).filter_by(id = restaurant).one()
    if restaurantItem is None:
        return showRestaurants()
    else:
        if request.method == 'POST':
            restaurantItem.name = request.form['name']
            session.add(restaurantItem)
            session.commit()
            flash("The restaurant has been edited!")
            return redirect(url_for("showRestaurants"))
        else: 
            return render_template("editRestaurant.html", restaurant = restaurantItem)

@app.route('/restaurants/<int:restaurant>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant):
    restaurantItem = session.query(Restaurant).filter_by(id = restaurant).one()
    if restaurantItem is None:
        return showRestaurants()
    else:
        if request.method == 'POST':
            session.delete(restaurantItem)
            session.commit()
            flash("The restaurant has been deleted!")
            return redirect(url_for("showRestaurants"))
        else: 
            return render_template("deleteRestaurant.html", restaurant = restaurantItem)

# Menu items routing and CRUD
@app.route('/restaurants/<int:restaurant>/')
def showMenuItems(restaurant):
    myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurant).one()
    if myRestaurantQuery is None:
        return showRestaurants()
    else:
        items = session.query(MenuItem).filter_by(restaurant_id = restaurant).all()
        return render_template("menuItems.html", restaurant = myRestaurantQuery, items = items)

@app.route('/restaurants/<int:restaurant>/menu/JSON')
def restaurantMenuJSON(restaurant):
    myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurant).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant).all()
    return jsonify(menuItems = [i.serialize for i in items])

@app.route('/restaurants/<int:restaurant>/menu/<int:menu_item>/JSON')
def restaurantMenuItemJSON(restaurant, menu_item):
    menuItem = session.query(MenuItem).filter_by(id = menu_item, restaurant_id = restaurant).one()
    return jsonify(menuItem = menuItem.serialize)

@app.route('/restaurants/<int:restaurant>/create', methods=['GET', 'POST'])
def newMenuItem(restaurant):
    myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurant).one()
    if myRestaurantQuery is None:
        return showRestaurants()
    else:
        if request.method == 'POST':
            newItem = MenuItem(name = request.form['name'],
                            description = request.form['description'],
                            price = request.form['price'],
                            course = request.form['course'],
                            restaurant = myRestaurantQuery)
            session.add(newItem)
            session.commit()
            flash("New menu item created!")
            return redirect(url_for("showMenuItems", restaurant = myRestaurantQuery.id))
        else: 
            return render_template("newMenuItem.html", restaurant = myRestaurantQuery)

@app.route('/restaurants/<int:restaurant>/<int:menu_item>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant, menu_item):
    menuItem = session.query(MenuItem).filter_by(id = menu_item, restaurant_id = restaurant).one()
    if menuItem is None:
        return showRestaurants()
    else:
        if request.method == 'POST':
            menuItem.name = request.form['name']
            menuItem.description = request.form['description']
            menuItem.price = request.form['price']
            menuItem.course = request.form['course']
            session.add(menuItem)
            session.commit()
            flash("The menu item has been edited!")
            return redirect(url_for("showMenuItems", restaurant = menuItem.restaurant_id))
        else: 
            return render_template("editMenuItem.html", item = menuItem)

@app.route('/restaurants/<int:restaurant>/<int:menu_item>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant, menu_item):
    menuItem = session.query(MenuItem).filter_by(id = menu_item, restaurant_id = restaurant).one()
    if menuItem is None:
        return showRestaurants()
    else:
        if request.method == 'POST':
            session.delete(menuItem)
            session.commit()
            flash("The menu item has been deleted!")
            return redirect(url_for("showMenuItems", restaurant = menuItem.restaurant_id))
        else: 
            return render_template("deleteMenuItem.html", item = menuItem)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)