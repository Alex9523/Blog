from app import app
from flask import render_template
from models import Post, Tag
from forms import PostForm
from flask import request, redirect, url_for
from app import db


@app.route('/create' , methods=['GET','POST'])
def create_post():

	if request.method =='POST' :
		title = request.form['title']
		body = request.form['body']
		
		try:
			post = Post(title=title, body=body)
			db.session.add(post)
			db.session.commit()
		except:
			print('Something wrong')

		return redirect('/')

	form = PostForm()
	return render_template('create_post.html' , form=form)

@app.route('/<slug>/edit/', methods=['POST','GET'])
def edit_post(slug):
	post = Post.query.filter(Post.slug==slug).first()

	if request.method == 'POST':
		form = PostForm(formdata=request.form, obj=post)
		form.populate_obj(post)
		db.session.commit()
		return redirect(url_for('post_detail',slug=post.slug))
	form = PostForm(obj=post)
	return render_template('edit_post.html', post = post, form=form)


@app.route('/main')
def main():
	return render_template('main.html') 

@app.route('/')
def blog():
	q = request.args.get('q')
	if q:
		posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q)).all()
	else:
		posts = Post.query.order_by(Post.created.desc())
	return render_template('blog.html', posts=posts) 

@app.route('/<slug>')
def post_detail(slug):
	post = Post.query.filter(Post.slug==slug).first()
	tags = post.tags
	return render_template('post_detail.html', post=post, tags=tags)
