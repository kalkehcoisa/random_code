#-*- coding: utf-8 -*-

from flask import render_template
from mosca import app, cache
from mosca.models.posts import Post

import os


'''@app.route('/')
@app.route('/home')
def home():
    categorias = Post.objects.all()
    return render_template('mosca/home.html', categorias=categorias)'''


@app.route('/static/<path:filename>')
def serve_static(filename):
    return app.send_static_file(
        os.path.join(app.config['BASE_DIR'], 'static', filename))
