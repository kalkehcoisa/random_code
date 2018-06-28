from flask.views import MethodView
import requests

from app_root import app


HEADERS = {'Authorization': 'Bearer {}'.format(app.config['ACCESS_TOKEN'])}


class RepositoriesAPI(MethodView):

    def _apply_values(self, query, values_dict):
        for k, v in values_dict.items():
            query = query.replace(':' + k + ':', str(v))
        return query

    def _get_http_data(self, user_id, last_item):
        query = """
        query {
          user(login: ":login:") {
            name
            starredRepositories(first: 50, after: :last_item:) {
              pageInfo {
                hasNextPage
                endCursor
              }
              totalCount
              edges {
                node {
                  id
                  name
                  url
                  description
                  languages(first: 1) {
                    edges {
                      node {
                        name
                      }
                    }
                  }
                }
              }
            }
          }
        }
        """
        query = self._apply_values(query, {
            'login': user_id,
            'last_item': last_item
        })
        r = requests.post(
            'https://api.github.com/graphql',
            json={'query': query},
            headers=HEADERS
        )
        data = r.json()
        import json
        with open('./http_invalid_request.txt', 'w') as outfile:
            json.dump(data, outfile)
        return data

    def _simplify_insert(self, user_id, dados):
        edges = dados['data']['user']['starredRepositories']['edges']
        output = []
        for rep in edges:
            item = rep['node'].copy()
            item['user_id'] = user_id
            item['language'] = list(map(
                lambda x: x['node']['name'],
                rep['node']['languages']['edges']
            ))
            if len(item['language']) > 1:
                item['language'] = item['language'][0]
            item['tags'] = []
            output.append(item)
            if not app.db.exist('id', item['id']):
                app.db.insert(item)
        return output

    def _get_all_http_data(self, user_id):
        next_page = True
        last_item = 'null'

        output = []
        while next_page:
            dados = self._get_http_data(user_id, last_item)
            if 'errors' in dados:
                return dados
            page_info = dados['data']['user']['starredRepositories']['pageInfo']
            next_page = page_info['hasNextPage']
            last_item = '"' + page_info['endCursor'] + '"'

            output.extend(self._simplify_insert(user_id, dados))

        return output

    def get(self, user_id=''):
        """
        Create a new user
        ---
        tags:
          - users
        definitions:
          - schema:
              id: Group
              properties:
                name:
                 type: string
                 description: the group's name
        parameters:
          - in: body
            name: body
            schema:
              id: User
              required:
                - email
                - name
              properties:
                email:
                  type: string
                  description: email for user
                name:
                  type: string
                  description: name for user
                address:
                  description: address for user
                  schema:
                    id: Address
                    properties:
                      street:
                        type: string
                      state:
                        type: string
                      country:
                        type: string
                      postalcode:
                        type: string
                groups:
                  type: array
                  description: list of groups
                  items:
                    $ref: "#/definitions/Group"
        responses:
          201:
            description: User created
        """

        # don't allow empty queries
        if not user_id:
            return {'errors': 'Empty Query'}

        # if the data exists in the database
        # don't do unnecessary http requests
        if app.db.exist('user_id', user_id):
            return app.db.search('user_id', user_id)

        # tinydb doesn't implement limit, offset
        # so, always all the data
        output = self._get_all_http_data(user_id)

        return output

    def post(self):
        """
        Creates new tags for repositories.
        """
        return {}
