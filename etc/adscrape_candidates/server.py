import tornado.ioloop
import tornado.web

from apps.ans.handlers.list_fetchers import ListFetchersHandler
from apps.ans.handlers.fetch_document import FetchDocumentHandler

PORT = 5050


def make_app():
    return tornado.web.Application([
        # ANS handlers
        (r'/list-fetchers', ListFetchersHandler),
        (r'/get', FetchDocumentHandler),
        
    ], debug=True)



if __name__ == '__main__':
    print('Server port %d...' % PORT, flush=True)
    app = make_app()
    app.listen(PORT)
    tornado.ioloop.IOLoop.current().start()