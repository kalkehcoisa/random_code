#-*- coding: utf-8 -*-

import base64

from flask import render_template, request
from flask.ext.classy import FlaskView, route
from mosca import app

CHARSETS = (
    "UTF-8",
    "ASCII",
    "CP1256",
    "ISO-8859-1",
    "ISO-8859-2",
    "ISO-8859-6",
    "ISO-8859-15",
    "Windows-1252",
)


class ToolsViews(FlaskView):
    route_base = '/tools/'

    @route('/')
    def tools_list(self):
        tools = []
        return render_template('tools/list.html', tools=tools)

    @route('/base64/encode', methods=['GET'])
    def tools_base64encode(self):
        return render_template(
            'tools/base64/encode.html',
            view='encode',
            CHARSETS=CHARSETS)

    @route('/base64/encode', methods=['POST'])
    def tools_base64encode_post(self):
        data = request.form.get('data')
        charset = request.form.get('charset')
        encoded = base64.b64encode(bytes(data, charset)).decode(charset)
        return render_template(
            'tools/base64/encode.html',
            encoded=encoded, view='encode',
            data=data, charset=charset,
            CHARSETS=CHARSETS)

    @route('/base64/decode', methods=['GET'])
    def tools_base64decode_get(self):
        return render_template(
            'tools/base64/decode.html', view='decode',
            CHARSETS=CHARSETS)

    @route('/base64/decode', methods=['POST'])
    def tools_base64decode_post(self):
        data = request.form.get('data')
        charset = request.form.get('charset')
        try:
            decoded = str(base64.b64decode(data.encode(charset)), charset)
        except UnicodeDecodeError as e:
            decoded = str(e)
        return render_template(
            'tools/base64/decode.html',
            decoded=decoded, view='decode',
            data=data, charset=charset,
            CHARSETS=CHARSETS)

    @route('/docs/cpf', methods=['GET'])
    def tools_docs_cpf_get(self):
        return render_template(
            'tools/docs/cpf.html')

    @route('/url/encode', methods=['GET'])
    def tools_urlencode(self):
        tools = []
        return render_template('tools/url/encode.html', tools=tools)

    @route('/url/decode')
    def tools_urldecode(self):
        tools = []
        return render_template('tools/url/decode.html', tools=tools)
