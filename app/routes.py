#!/usr/bin/env python3
# -*- coding: utf8 -*-
"""App init files"""

from flask import (render_template,
        request, redirect,
        url_for, flash
        )
from app import app, db
from datetime import datetime
from app.database import Product
from app.forms import ProductForm

@app.route("/")
def index():
    version = {
        "ok": True,
        "messaging": "success",
        "version": "1.0.0",
        "server_time": datetime.now().strftime("%F %H:%M:%S")
    }
    return render_template("index.html", version=version)

@app.route("/products")
def get_products():
    products = Product.query.all()
    return render_template("product_list.html", product_list = products)

@app.route("/archive")
def get_archive():
    products = Product.query.all()
    return render_template("archive_product_list.html", product_list = products)


@app.route("/products/<int:pid>")
def get_product_detail(pid):
    product = Product.query.filter_by(id=pid).first()
    form = ProductForm(request.form)
    reviews = product.reviews.split('~')
    return render_template("product_detail.html", product=product, form=form, reviews=reviews)

@app.route("/products/inactive/<int:pid>", methods=["POST"])
def delete_product(pid):
    product = Product.query.filter_by(id=pid).first()
    product.active = False
    db.session.commit()
    flash("Product Deleted!")
    return redirect(url_for("get_products"))

@app.route("/products/active/<int:pid>", methods=["POST"])
def restore_product(pid):
    product = Product.query.filter_by(id=pid).first()
    product.active = True
    db.session.commit()
    flash("Product Restored!")
    return redirect(url_for("get_products"))

@app.route("/products/reviews/<int:pid>", methods=["POST"])
def add_review(pid):
    form = ProductForm(request.form)
    product = Product.query.filter_by(id=pid).first()
    new_reviews = product.reviews + "~" + form.reviews.data
    print(new_reviews)
    product.reviews = new_reviews
    db.session.commit()
    flash("Review posted!")
    return redirect(url_for("get_products"))

@app.route("/products/<int:pid>", methods=["POST"])
def update_product(pid):
    form = ProductForm(request.form)
    if form.validate():
        product = Product.query.filter_by(id=pid).first()
        product.name = form.name.data
        product.price = form.price.data
        product.quantity = form.quantity.data
        product.description = form.description.data
        if product.quantity > 500:
            category = "success"
        elif product.quantity > 100:
            category = "warning"
        else:
            category = "danger"
            
        product.category = category
        
        db.session.commit()
        flash("Product updated!")
        return redirect(url_for("get_products"))
    # if validations dont pass, for now we'lll have a redirect
    # # to get_products   
    flash("Invalid data") 
    return redirect(url_for('get_products'))

@app.route("/products/registrations")
def create_product_form():
    """Renders the create product form"""
    form = ProductForm()
    return render_template("create_form.html", form=form)

@app.route("/products/modifications/<int:pid>")
def update_product_form(pid):
    form = ProductForm()
    product = Product.query.filter_by(id=pid).first()
    return render_template("update_form.html", form=form, product=product)

@app.route("/products", methods=["POST"]) 
def create_product(): 
    """Create a new product""" 
    form = ProductForm(request.form) 
    if form.validate(): 
        product = Product() 
        product.name = form.name.data 
        product.price = form.price.data 
        product.quantity = form.quantity.data 
        product.description = form.description.data
        product.active = form.is_active.data

        if product.quantity > 500:
            category = "success"
        elif product.quantity > 100:
            category = "warning"
        else:
            category = "danger"
            
        product.category = category

        db.session.add(product) 
        db.session.commit() 
        flash("Product created!") 
        return redirect(url_for('get_products'))
    else: 
        flash("Invalid data") 
        return redirect(url_for('get_products'))
    