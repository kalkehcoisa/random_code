import json
import tornado.web
from apps.ans.fetchers.utils.constructors import FETCHER_CONSTRUCTORS
from credentials import FETCHER_CREDENTIALS

class ListFetchersHandler(tornado.web.RequestHandler):
    
        
    def __dump_as_json(self, obj):
        return json.dumps(obj, sort_keys=True, indent=4)
    
        
    def get(self):
        result = []
        for fetcher_contructor in FETCHER_CONSTRUCTORS.values():
            fetcher_data = {
                'title': fetcher_contructor.TITLE,
                'network_id': fetcher_contructor.NETWORK_ID,
                'logins': [],
            }
            
            if fetcher_contructor.NETWORK_ID in FETCHER_CREDENTIALS:
                for lp in FETCHER_CREDENTIALS[fetcher_contructor.NETWORK_ID]:
                    fetcher_data['logins'].append(lp['login'])
                
            result.append(fetcher_data)
            
        self.set_header('Content-Type', 'application/json')
        self.finish(self.__dump_as_json(result))
        
        
        