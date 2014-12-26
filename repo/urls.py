from repo.handlers.accounts import AccountsHandler, AccountsRecoveryHandler, AccountsNewHandler
from repo.handlers.home import HomeHandler
from repo.handlers.sessions import LoginHandler, LogoutHandler, SessionsClearHandler
from repo.handlers.users import UsersHandler

url_patterns = [
    (r'/?$', HomeHandler),

    (r'/sessions/login/?$', LoginHandler),
    (r'/sessions/logout/?$', LogoutHandler),
    (r'/sessions/clear/?$', SessionsClearHandler),

    (r'/accounts/?$', AccountsHandler),
    (r'/accounts/new/?$', AccountsNewHandler),
    (r'/accounts/recover/?$', AccountsRecoveryHandler),

    (r'/\w+/?$', UsersHandler)
]
