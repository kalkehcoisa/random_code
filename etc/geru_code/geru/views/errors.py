from pyramid.renderers import render
from pyramid.response import Response


def includeme(config):
    config.add_notfound_view(notfound_view, append_slash=True)


def notfound_view(request):
    """
    View for when a nonexistent (404) is accessed.
    """

    html = render(
        'geru:templates/404.jinja2',
        {'request': request},
        request=request
    )
    return Response(html, status=404)
