from repo.models.orgs import namespace_of
from tornado import gen


@gen.coroutine
def redirect_to_user_page(handler, user=None):
    user_page = yield get_user_page(handler, user)
    handler.redirect('/' + user_page)

@gen.coroutine
def get_user_page(handler, user=None):
    if user is None:
        user = yield handler.current_user_secure
    namespace = yield namespace_of(user)
    raise gen.Return(namespace.name)
