from flask import Flask, Blueprint, redirect, url_for, render_template, jsonify, request
from flask_login import login_required, current_user
from .forms import CategoryForm
from .models import db, Category
from datetime import datetime

category = Blueprint(
    "category",
    __name__,
    static_folder="static",
    template_folder="templates"
)

@category.route("/add", methods = ["POST", "GET"])
@login_required
def add():
    form = CategoryForm()
    categories = Category.query.all()
    cate_list = [(cate.id, cate.name) for cate in categories]
    form.parent_id.choices = cate_list

    if form.validate_on_submit():
        if form.parent_id.data:
            is_child = True
        is_child = False
        category = Category(
            name = form.name.data,
            abstract=form.abstract.data,
            is_child=is_child,
            parent_id=form.parent_id.data
        )
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('category.cate_list'))
    return render_template("category/add.html", form = form)

@category.route("/cate_list")
@login_required
def cate_list():
    cate_list = Category.query.all()
    return render_template("category/cate_list.html", cate_list = cate_list)

@category.route("/edit/<int:cate_id>", methods = ["POST", "GET"])
@login_required
def edit(cate_id):
    # return jsonify(cate_id)
    current_cate = Category.query.get_or_404(cate_id)
    form = CategoryForm()
    #populate data into select field
    categories = Category.query.all()
    cate_list = [(cate.id, cate.name) for cate in categories]
    form.parent_id.choices = cate_list
    

    if request.method == "GET":
        #populate current category data into abstract and parent_id field
        form.abstract.data = current_cate.abstract
        form.parent_id.data = current_cate.parent_id
    elif form.validate_on_submit():
        if current_cate.id != form.parent_id.data:
            is_child = True
        is_child = False

        current_cate.is_child = is_child
        current_cate.name = form.name.data
        current_cate.abstract = form.abstract.data
        current_cate.parent_id = form.parent_id.data
        current_cate.is_child = is_child
        current_cate.modified_date = datetime.now()
        db.session.commit()
        return redirect(url_for('category.cate_list'))
    return render_template('category/edit.html', form = form, category = current_cate)

@category.route("/delete/<int:cate_id>", methods = ["POST", "GET"])
@login_required
def delete(cate_id):
    current_cate = Category.query.filter_by(id = cate_id).first()
    db.session.delete(current_cate)
    db.session.commit()
    return redirect(url_for('category.cate_list'))