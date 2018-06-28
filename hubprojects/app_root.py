from flask import Flask, jsonify, render_template, send_from_directory
from flask_cors import CORS
from database import TinyDBManager


class MyFlask(Flask):
    def make_response(self, rv):
        # auto convert dicts to json response
        if isinstance(rv, dict):
            return jsonify(rv)
        elif isinstance(rv, list):
            return jsonify(rv)
        return super(MyFlask, self).make_response(rv)


app = MyFlask(__name__)
app.config.from_object('config.DevelopmentConfig')
app.db = TinyDBManager()

if app.config['DEVELOP']:
    # force all views to work cors
    CORS(app)


def create_views(app):
    import views
    app.add_url_rule(
        '/repositories/<string:user_id>',
        view_func=views.RepositoriesAPI.as_view('repositories'),
        methods=["GET"]
    )
    app.add_url_rule(
        '/repositories/tag/<string:rep_id>',
        view_func=views.RepositoriesAPI.as_view('tag_repositories'),
        methods=["POST"]
    )

    return app


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html', config=app.config)


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static', path)


if __name__ == '__main__':
    app = create_views(app)
    app.run()
