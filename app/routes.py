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

@app.route("/products/<int:pid>")
def get_product_detail(pid):
    product = Product.query.filter_by(id=pid).first()
    return render_template("product_detail.html", product=product)


@app.route("/products/<int:pid>", methods=["POST"])
def update_product(pid):
    form = ProductForm(request.form)
    if form.validate():
        product = Product.query.filter_by(id=pid).first()
        product.name = form.name.data
        product.price = form.price.data
        product.quantity = form.quantity.data
        product.description = form.description.data
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
    prod_form = ProductForm()
    return render_template("create_form.html", form=prod_form)

@app.route("/products/modifications/<int:pid>")
def update_product_form(pid):
    form = ProductForm()
    product = Product.query.filter_by(id=pid).first()
    return render_template("update_form.html", form=form, product=product)

@app.route("/products", methods=["POST"]) 
def create_product(): 
    """Create a new product""" 
    form = ProductForm(request.form) 
    if form.validate(): product = Product() 
    product.name = form.name.data 
    product.price = form.price.data 
    product.quantity = form.quantity.data 
    product.description = form.description.data 
    db.session.add(product) 
    db.session.commit() 
    flash("Product created!") 
    return redirect(url_for('get_products')) 
    flash("Invalid data") 
    return redirect(url_for('get_products'))