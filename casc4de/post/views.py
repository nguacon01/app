from flask import Flask, Blueprint, redirect, url_for, render_template, jsonify, flash, request
from flask_login import login_required, current_user
from .forms import PostForm
from .models import db,Post
from casc4de.category.models import Category

post = Blueprint(
    "post",
    __name__,
    static_folder="static",
    template_folder="templates"
)

@post.route("/add", methods = ["POST", "GET"])
@login_required
def add():
    form = PostForm()
    #populate data into select field
    categories = Category.query.all()
    cate_list = [(cate.id, cate.name) for cate in categories]
    form.cate_id.choices = cate_list

    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            abstract=form.abstract.data,
            cate_id=form.cate_id.data,
            content=form.content.data
        )
        db.session.add(post)
        db.session.commit()
        flash("New article has been added")
        return redirect(url_for("post.post_list"))
    return render_template("post/add.html", form = form)

@post.route("/post_list")
@login_required
def post_list():
    post_list = Post.query.all()
    return render_template("post/post_list.html", post_list = post_list)

@post.route("/edit/<int:post_id>", methods = ["POST", "GET"])
@login_required
def edit(post_id):
    form = PostForm()
    current_post = Post.query.get_or_404(post_id)
    #populate data into select field
    categories = Category.query.all()
    cate_list = [(cate.id, cate.name) for cate in categories]
    form.cate_id.choices = cate_list

    if request.method == "GET":
        form.cate_id.data = current_post.cate_id
        form.abstract.data = current_post.abstract
        form.content.data = current_post.content
    elif form.validate_on_submit():
        current_post.cate_id=form.cate_id.data
        current_post.title=form.title.data
        current_post.abstract=form.abstract.data
        current_post.content=form.content.data

        db.session.flush()
        db.session.commit()
        return redirect(url_for("post.post_list"))
    return render_template("post/edit.html", form = form, post = current_post)

@post.route("/delete/<int:post_id>", methods = ["POST", "GET"])
@login_required
def delete(post_id):
    current_post = Post.query.get_or_404(post_id)
    db.session.delete(current_post)
    db.session.commit()
    flash("A post has been deleted!")
    return redirect(url_for("post.post_list"))