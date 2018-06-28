import json
import tornado.web
from tornado import gen


from apps.ans.fetchers.utils.constructors import FETCHER_CONSTRUCTORS
from datetime import datetime
from credentials import FETCHER_CREDENTIALS


class FetchDocumentHandler(tornado.web.RequestHandler):
    
    
    def __dump_as_json(self, obj):
        return json.dumps(obj, sort_keys=True, indent=4)
    
    
    
    def get_arguments_as_strings(self, args=None):
        if args is None:
            args = self.request.arguments
        
        result = {}
        for key, value in args.items():
            if key.endswith('[]'):
                result[key[:-2]] = [v.decode() for v in value]
            else:
                result[key] = value[-1].decode()
            
        return result
    
    
    
    @tornado.web.asynchronous
    @gen.coroutine
    def get(self):
        yield self.__ans_fetch_document()
        
        
    
    @tornado.web.asynchronous
    @gen.coroutine
    def post(self):
        yield self.__ans_fetch_document()
        
        
    
    @gen.coroutine
    def __ans_fetch_document(self):
        args = self.get_arguments_as_strings()
        
        REQUIRED_ARGUMENTS = ['date-start', 'date-end', 'network-id', 'login']
        for req_argument in REQUIRED_ARGUMENTS:
            if req_argument not in args:
                raise Exception('Argument "%s" required' % req_argument)
        
        parameters = {
            'login': args['login'],
        }
        try:
            parameters['date-start'] = \
                datetime.strptime(args['date-start'].replace('-', ''),
                    '%Y%m%d')
            parameters['date-end'] = \
                datetime.strptime(args['date-end'].replace('-', ''),
                    '%Y%m%d')
        except ValueError:
            raise Exception('Date end and date start should be in ISO format')
        
        if parameters['date-end'] < parameters['date-start']:
            raise Exception('Date end cannot be before date-start')
        
        if args['network-id'] not in FETCHER_CONSTRUCTORS:
            raise Exception('Unknown network ID: %s' % args['network-id'])
        
        if args['network-id'] not in FETCHER_CREDENTIALS:
            raise Exception('Unknown login: %s' % args['login'])
        
        found = False
        for credentials in FETCHER_CREDENTIALS[args['network-id']]:
            if credentials['login'] == args['login']:
                parameters['password'] = credentials['password']
                found = True
                break
            
        if not found:
            raise Exception('Unknown login: %s' % args['login'])
        
        FETCHER = FETCHER_CONSTRUCTORS[args['network-id']]
        fetcher = FETCHER()
        
        data = yield fetcher.fetch(parameters)
        result = {
            'data': data,
            'login': parameters['login'],
            'date-start': parameters['date-start'].strftime('%Y-%m-%d'),
            'date-end': parameters['date-end'].strftime('%Y-%m-%d'),
            'network-id': args['network-id'],
        }
        
        self.set_header('Content-Type', 'application/json')
        self.finish(self.__dump_as_json(result))
    
    
    
    
    
    
    