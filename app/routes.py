from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from .auth import User
import bcrypt
import os
from bson.objectid import ObjectId
import sys

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return redirect(url_for('main.login'))


@main.route('/register', methods=['GET', 'POST'])
def register():
    db = current_app.config['db']
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if user exists
        if db.users.find_one({'username': username}):
            flash("Username already exists.")
            return redirect(url_for('main.register'))

        # Hash the password before storing it
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        db.users.insert_one({'username': username, 'password': hashed, 'favorites': []})

        flash("Registration successful. Please log in.")
        return redirect(url_for('main.login'))
    return render_template('register.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    db = current_app.config['db']
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_doc = db.users.find_one({'username': username})
        if user_doc and bcrypt.checkpw(password.encode('utf-8'), user_doc['password']):
            user = User(user_doc)
            login_user(user)
            flash("Logged in successfully.")
            return redirect(url_for('main.home'))
        flash("Invalid username or password.")
    return render_template('login.html')


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('main.login'))


# homepage api
@main.route('/home')
@login_required
def home():
    # Displays the home page with the game.
    return render_template('home.html')


# store list api
@main.route('/store_list')
@login_required
def store_list():
    # Displays a simple list of stores (similar to store_search but more basic).
    db = current_app.config['db']
    stores = list(db.stores.find({}))
    return render_template('store_list.html', stores=stores)


# add store api
@main.route('/add_store', methods=['GET', 'POST'])
@login_required
def add_store():
    # Displays a form (GET) to add a new store,
    # and handles the form submission (POST) to insert into MongoDB.
    db = current_app.config['db']

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        location = request.form.get('location')
        image_file = request.files.get('image')

        if image_file and image_file.filename:
            filename = image_file.filename
            upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            upload_path = os.path.join(upload_folder, filename)
            image_file.save(upload_path)
            image_url = f"/static/uploads/{filename}"
        else:
            image_url = "/static/uploads/default.jpg"

        store_doc = {
            "name": name,
            "description": description,
            "location": location,
            "image_url": image_url
        }

        # Insert into store
        result = db.stores.insert_one(store_doc)
        store_id = result.inserted_id
        flash("Store added successfully!")
        return redirect(url_for('main.store_detail', store_id=store_id))

    return render_template('add_store.html')


# store detail api
@main.route('/store_detail/<store_id>')
@login_required
def store_detail(store_id):
    db = current_app.config['db']
    store = db.stores.find_one({"_id": ObjectId(store_id)})
    if not store:
        flash("Store not found.")
        return redirect(url_for('main.store_list'))

    # Fetch reviews from reviews collection
    reviews_cursor = db.reviews.find({"store_id": store_id})
    reviews = list(reviews_cursor)

    return render_template('store_detail.html', store=store, reviews=reviews)


# Search store api
@main.route('/store_search', methods=['GET'])
@login_required
def store_search():
    # Displays a list of stores, and optionally handles
    # filter queries from request.args for advanced searching.
    db = current_app.config['db']
    stores = list(db.stores.find({}))

    return render_template('store_search.html', stores=stores)


# write review api
@main.route('/write_review/<store_id>', methods=['GET', 'POST'])
@login_required
def write_review(store_id):
    db = current_app.config['db']

    # Fetch the store to display its name and ensure it exists
    store = db.stores.find_one({"_id": ObjectId(store_id)})
    if not store:
        flash("Store not found.")
        return redirect(url_for('main.store_search'))
    if request.method == 'POST':
        # Get form data
        price_range = request.form.get('price_range')
        variety = request.form.get('variety')
        customer_service = request.form.get('customer_service')
        review_text = request.form.get('review')

        # Convert numeric fields to integers if needed
        try:
            price_range = int(price_range)
            variety = int(variety)
            customer_service = int(customer_service)
        except ValueError:
            flash("Please enter valid numeric ratings.")
            return redirect(url_for('main.write_review', store_id=store_id))

        # Build the review document
        review_doc = {
            "store_id": store_id,
            "user_id": current_user.get_id(),  # or current_user.id
            "price_range": price_range,
            "variety": variety,
            "customer_service": customer_service,
            "text": review_text
        }

        # Insert into the 'reviews' collection
        db.reviews.insert_one(review_doc)
        flash("Review submitted successfully!")
        return redirect(url_for('main.store_detail', store_id=store_id))

    # For a GET request, just show the form
    return render_template('review.html', store=store, store_id=store_id)


@main.route('/edit_review/<store_id>/<review_id>', methods=['GET', 'POST'])
@login_required
def edit_review(store_id, review_id):
    db = current_app.config['db']

    #Fetch the store
    store = db.stores.find_one({"_id": ObjectId(store_id)})
    if not store:
        flash("Store not found.")
        return redirect(url_for('main.store_list'))
    # Fetch the review
    review_doc = db.reviews.find_one({"_id": ObjectId(review_id)})
    if not review_doc:
        flash("Review not found.")
        return redirect(url_for('main.store_detail', store_id=store_id))

    if request.method == 'POST':

        new_price = int(request.form.get('price_range'))
        new_variety = int(request.form.get('variety'))
        new_service = int(request.form.get('customer_service'))
        new_text = request.form.get('review')
        db.reviews.update_one(
            {"_id": ObjectId(review_id)},
            {
                "$set": {
                    "price_range": new_price,
                    "variety": new_variety,
                    "customer_service": new_service,
                    "text": new_text
                }
            }
        )
        flash("Review updated successfully!")
        return redirect(url_for('main.store_detail', store_id=store_id))
    return render_template('edit.html', store_id=store_id, review=review_doc)


@main.route('/delete_review/<store_id>/<review_id>', methods=['POST'])
@login_required
def delete_review(store_id, review_id):
    db = current_app.config['db']

    # Attempt to delete the review from the database
    result = db.reviews.delete_one({"_id": ObjectId(review_id)})

    if result.deleted_count > 0:
        flash("Review deleted successfully!")
    else:
        flash("Review not found or could not be deleted.")

    return redirect(url_for('main.store_detail', store_id=store_id))


# --------------------------------------------------------  TO DO
@main.route('/favorite_stores')
@login_required
def favorite_stores():
    db = current_app.config['db']
    user = db.users.find_one({"_id": current_user.get_id()})
    if user and "favorites" in user:
        favorite_stores = list(db.stores.find({"_id": {"$in": user["favorites"]}}))
    else:
        favorite_stores = []
    return render_template('favorites.html', favorite_stores = favorite_stores)

# --------------------------------------------------------  TO DO
# @main.route('/add_to_favorites', methods=['POST'])
# @login_required
# def add_to_favorites(store_id):
#     db = current_app.config['db']
#     user = db.users.find_one({"_id": current_user.get_id()})
#     if user and "favorites" in user and store_id in user["favorites"]:
#         flash("Store already in favorites!", "info")
#     else:
#         db.users.update_one(
#             {"_id": current_user.get_id()},
#             {"$addToSet": {"favorites": store_id}},
#         )
#         flash("Store added to favorite successfully!", "success")
        
#     return redirect(url_for('main.store_detail.html', store_id=store_id))

@main.route('/add_to_favorites/<store_id>', methods=['POST'])
@login_required
def add_to_favorites(store_id):
    db = current_app.config['db']
    
    user = db.users.find_one({"_id": current_user.get_id()})
    
    # Ensure 'favorites' exists and store isn't already favorited
    if not user:
        flash("User not found.", "error")
        return redirect(url_for('main.store_detail', store_id=store_id))
    if "favorites" not in user:
        db.users.update_one(
            {"_id": user},
            { "$set": { "favorites": [] } }
        )

    if store_id in user["favorites"]:
        flash("Store already in favorites!", "info")
    else:
        db.users.update_one(
            {"_id": current_user.get_id()},
            {"$addToSet": {"favorites": store_id}}
        )
        flash("Store added to favorites successfully!", "success")

    return redirect(url_for('main.store_detail', store_id=store_id))


@main.route('/submit_guess', methods=['POST'])
@login_required
def submit_guess():
    return redirect(url_for('main.home'))






