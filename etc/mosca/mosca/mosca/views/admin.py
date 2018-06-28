from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView

from flask.ext.mongoengine.wtf import model_form

from mosca.auth import requires_auth
from mosca.models.posts import Post, BlogPost, Video, Image, Quote, Comment
from mosca import db

admin = Blueprint('admin', __name__, template_folder='templates')


class List(MethodView):
    decorators = [requires_auth]
    cls = Post

    def get(self):
        posts = self.cls.objects.all()
        return render_template('admin/list.html', posts=posts)


class Detail(MethodView):

    decorators = [requires_auth]
    # Map post types to models
    class_map = {
        'post': BlogPost,
        'video': Video,
        'image': Image,
        'quote': Quote,
    }

    def get_context(self, permalink=None):

        if permalink:
            post = Post.objects.get_or_404(permalink=permalink)
            #print(post.__class__)
            # Handle old posts types as well
            cls = post.__class__
            form_cls = model_form(cls,  exclude=('created', 'comments'))
            if request.method == 'POST':
                form = form_cls(request.form, inital=post._data)
            else:
                form = form_cls(obj=post)
        else:
            # Determine which post type we need
            cls = self.class_map.get(request.args.get('type', 'post'))
            post = cls()
            form_cls = model_form(cls,  exclude=('created', 'comments'))
            form = form_cls(request.form)
        context = {
            "post": post,
            "form": form,
            "create": permalink is None
        }
        return context

    def get(self, permalink):
        context = self.get_context(permalink)
        return render_template('admin/detail.html', **context)

    def post(self, permalink):
        context = self.get_context(permalink)
        form = context.get('form')

        if form.validate():
            post = context.get('post')
            form.populate_obj(post)
            post.save()

            return redirect(url_for('admin.index'))
        return render_template('admin/detail.html', **context)


# Register the urls
admin.add_url_rule('/admin/', view_func=List.as_view('index'))
admin.add_url_rule(
    '/admin/create/',
    defaults={'permalink': None},
    view_func=Detail.as_view('create'))
admin.add_url_rule('/admin/<permalink>/', view_func=Detail.as_view('edit'))
