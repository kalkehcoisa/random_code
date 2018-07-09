from pyramid.response import Response
from pyramid_restful.views import APIView

from geru.models.pageviews import PageView


def includeme(config):  # noqa
    config.add_route('requests', '/requests/')
    config.add_view(RequestView.as_view(), route_name='requests')
    config.add_route('request', '/requests/{id}/')
    config.add_view(RequestDetailView.as_view(), route_name='request')

    config.add_route('sessions', '/sessions/')
    config.add_view(SessionView.as_view(), route_name='sessions')
    config.add_route('session', '/sessions/{id}/')
    config.add_view(SessionDetailView.as_view(), route_name='session')


class RequestView(APIView):
    """
    Responsible for listing all the available requests.
    """

    def get(self, request, *args, **kwargs):
        requests = [
            i.to_dict(exclude=['session_id'])
            for i in request.dbsession.query(PageView).all()
        ]
        return Response(json_body={'requests': requests})


class RequestDetailView(APIView):
    """
    Responsible for listing all details of a request.
    """

    def get(self, request, id, *args, **kwargs):
        r = request.dbsession.query(PageView).get(id)
        if r is None:
            return Response(
                json_body={'error': 'Not Found'},
                status=404
            )
        return Response(json_body={'request': r.to_dict()})


class SessionView(APIView):
    """
    Responsible for listing all the available sessions.
    """

    def get(self, request, *args, **kwargs):
        sessions = [
            {'session_id': i.session_id}
            for i in request.dbsession.query(PageView.session_id).distinct()
        ]
        return Response(json_body={'sessions': sessions})


class SessionDetailView(APIView):
    """
    Responsible for listing all the requests bound to a session.
    """

    def get(self, request, id, *args, **kwargs):
        r = request.dbsession.query(PageView).filter(
            PageView.session_id == id
        )
        if r.count() == 0:
            return Response(
                json_body={'error': 'Not Found'},
                status=404
            )
        session = [i.to_dict(exclude=['session_id']) for i in r]
        return Response(json_body={'session': session})
