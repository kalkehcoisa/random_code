import uuid

from pyramid.renderers import render
from pyramid.response import Response

from geru.models.pageviews import PageView


def user_tracker_tween(handler, registry):
    """
    This tween creates the session key and tracks all the pages
    accessed for this session.

    It ignores the requests to static files since most requests
    indirectly requires them and it would create tons of trash.
    But, not problem if it did. It would be able to track direct
    access to static files as well.
    """
    def simple_tween(request):
        session = request.session
        if 'user_tracker' not in session:
            session['user_tracker'] = f'{uuid.uuid4()}-{uuid.uuid4()}'

        # to avoid tracking the access to static files
        if not request.path_info.startswith('/static'):
            # save the page view into the database
            try:
                request.dbsession.add(PageView(
                    session_id=session['user_tracker'], url=request.path_info
                ))
                request.dbsession.flush()
            except Exception as e:
                # better handle the exceptions, or it's going to enter into
                # a exception recuring loop
                body = render(
                    'geru:templates/error.jinja2', {'error': e},
                    request=request
                )
                return Response(body, content_type='text/html', status=500)

        response = handler(request)
        return response

    return simple_tween
