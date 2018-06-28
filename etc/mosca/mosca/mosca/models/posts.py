#-*- coding: utf-8 -*-

from datetime import datetime
from flask import url_for
from mosca import db
from mosca.helpers import permalinkify


def make_permalink(context=None):
    if context:
        title = context.current_parameters['title']
        permalink = context.current_parameters['permalink']
        if title and not permalink:
            return permalinkify(title)


class Comment(db.EmbeddedDocument):
    created = db.DateTimeField(default=datetime.now, required=True)
    body = db.StringField(verbose_name="Comment", required=True)
    author = db.StringField(verbose_name="Name", max_length=255, required=True)


class Tag(db.EmbeddedDocument):
    title = db.StringField(verbose_name="Title", required=True)


class Post(db.DynamicDocument):
    meta = {
        'collection': 'post',
        'allow_inheritance': True,
        'indexes': ['-created', 'permalink'],
        'ordering': ['-created', 'permalink']
    }

    title = db.StringField(max_length=255, unique=True)
    permalink = db.StringField(
        max_length=255, unique=True,
        default=make_permalink)
    body = db.StringField(required=True)

    author = db.StringField(verbose_name="Name", max_length=255, required=True)
    created = db.DateTimeField(default=datetime.now, required=True)

    comments = db.ListField(db.EmbeddedDocumentField(Comment))
    tags = db.ListField(db.EmbeddedDocumentField(Tag))

    @property
    def post_type(self):
        return self.__class__.__name__

    #@property
    #def __class__(self):
    #    return db.DynamicDocument

    #def __init__(self, *ag, **kw):
    #    for key in kw.keys():
    #        setattr(self, key, kw[key])

    def __repr__(self):
        return u'<Post %r>' % self.title

    def __unicode__(self):
        return u'<Post %r>' % self.title

    def get_absolute_url(self):
        return url_for('post', kwargs={"permalink": self.permalink})


class BlogPost(Post):
    body = db.StringField(required=True)


class Video(Post):
    embed_code = db.StringField(required=True)


class Image(Post):
    image_url = db.StringField(required=True, max_length=255)


class Quote(Post):
    body = db.StringField(required=True)
    author = db.StringField(
        verbose_name="Author Name", required=True, max_length=255)
