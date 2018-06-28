#-*- coding: utf-8 -*-

from flask import Blueprint, request, redirect, render_template, url_for
from flask.ext.mongoengine.wtf import model_form
from flask.views import MethodView
from mosca.models.posts import Post, Comment

posts = Blueprint('posts', __name__, template_folder='templates')


class ListView(MethodView):

    def get(self):
        posts = Post.objects.all()
        return render_template('posts/list.html', posts=posts)


class DetailView(MethodView):

    form = model_form(Comment, exclude=['created'])

    def get_context(self, permalink):
        post = Post.objects.get_or_404(permalink=permalink)
        form = self.form(request.form)

        context = {
            "post": post,
            "form": form
        }
        return context

    def get(self, permalink):
        context = self.get_context(permalink)
        return render_template('posts/detail.html', **context)

    def post(self, permalink):
        context = self.get_context(permalink)
        form = context.get('form')

        if form.validate():
            comment = Comment()
            form.populate_obj(comment)

            post = context.get('post')
            post.comments.append(comment)
            post.save()

            return redirect(url_for('posts.detail', permalink=permalink))

        return render_template('posts/detail.html', **context)


# Register the urls
posts.add_url_rule('/', view_func=ListView.as_view('list'))
posts.add_url_rule('/<permalink>/', view_func=DetailView.as_view('detail'))
