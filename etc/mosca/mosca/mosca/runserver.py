#-*- coding: utf-8 -*-

from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple

#from admin import app as admin_app
#from tools import app as tools_app

from mosca import app as index
#import examples.simple.simple

#examples.sqla.simple.build_sample_db()

application = DispatcherMiddleware(
    index,
    {
        #'/quackmin': admin_app,
        #'/tools': tools_app,
    }
)

if __name__ == '__main__':
    run_simple(
        'localhost', 5000, application,
        use_reloader=True,
        use_debugger=True,
        use_evalex=True)
