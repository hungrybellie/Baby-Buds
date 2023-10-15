from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from .models import Post, Mom, Product, Expert, Comment
from . import db

views = Blueprint("views", __name__)

#------------------------------------------------------------------------
# GENERAL
#------------------------------------------------------------------------
@views.route("/forum")
@views.route("/")
def forum():
    posts = Post.query.all()
    return render_template("forum.html", user=current_user, posts=posts)


@views.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    return render_template("profile.html", user=current_user)


@views.route("/hand-me-down", methods=["GET", "POST"])
def hand_me_down():
    products = Product.query.all()
    return render_template("hand_me_down.html", products=products)


@views.route("/signup")
def signup():
    return render_template('mom_or_expert.html', user=current_user)

#------------------------------------------------------------------------
# POSTS
#------------------------------------------------------------------------
@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        post_title = request.form.get('title')
        post_content = request.form.get('content')

        if not post_content:
            flash('Post cannot be empty', category='error')
        else:
            post = Post(title=post_title, content=post_content, mauthor=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.forum'))

    return render_template('create_post.html', user=current_user)


@views.route("/delete-post/<post_id>")
@login_required
def delete_post(post_id):
    post = Comment.query.filter_by(id=post_id).first()

    if not post:
        flash('Post does not exist.', category='error')
    elif current_user.id != post.mauthor:
        flash('You do not have permission to delete this post.', category='error')
    else:
        db.session.delete(post)
        db.session.commit()

    return redirect(url_for('views.forum'))

#------------------------------------------------------------------------
# COMMENTS
#------------------------------------------------------------------------
@views.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty.', category='error')
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(
                text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist.', category='error')

    return redirect(url_for('views.forum'))


@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Post does not exist.', category='error')
    elif current_user.id != comment.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('views.forum'))

#------------------------------------------------------------------------
# PRODUCTS
#------------------------------------------------------------------------
@views.route("/list-product", methods=['GET', 'POST'])
@login_required
def list_product():
    if request.method == "POST":
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        tags = request.form.getlist('tags')
        img = request.form.get('img')

        if not name:
            flash('Please remember to add a name to your product <3', category='error')
        elif not price:
            flash('Please remember to add a price to your product, or 0.00!')
        elif not tags:
            flash('Please remember to add tags to your product, or 0.00!')
        else:
            product = Product(name=name, description=description, mauthor=current_user.id, price=price, tags=','.join(tags), img=img)
            db.session.add(product)
            db.session.commit()
            flash('Product created!', category='success')
            return redirect(url_for('views.hand_me_down'))

    return render_template('hand_me_down.html', user=current_user)


@views.route("/delete-product/<product_id>")
@login_required
def delete_product(product_id):
    product = Product.query.filter_by(id=product_id).first()

    if not product:
        flash('Product does not exist.', category='error')
    elif current_user.id != product.mauthor:
        flash('You do not have permission to delete this post.', category='error')
    else:
        db.session.delete(product)
        db.session.commit()

    return redirect(url_for('views.hand_me_down'))