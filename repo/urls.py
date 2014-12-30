from repo.handlers.accounts import AccountsHandler, AccountsRecoveryHandler, AccountsNewHandler
from repo.handlers.home import HomeHandler
from repo.handlers.orgs import OrgsHandler
from repo.handlers.projects import ProjectsHandler, ProjectsNewHandler, ProjectManageHandler, ProjectDeleteHandler, ProjectRenameHandler, \
    ProjectDescribeHandler, ExploreHandler
from repo.handlers.sessions import LoginHandler, LogoutHandler, SessionsClearHandler

url_patterns = [
    (r'/?$', HomeHandler),

    (r'/projects/?$', ExploreHandler),
    (r'/projects/new/?$', ProjectsNewHandler),

    (r'/sessions/login/?$', LoginHandler),
    (r'/sessions/logout/?$', LogoutHandler),
    (r'/sessions/clear/?$', SessionsClearHandler),

    (r'/accounts/?$', AccountsHandler),
    (r'/accounts/new/?$', AccountsNewHandler),
    (r'/accounts/recover/?$', AccountsRecoveryHandler),

    (r'/([\w+-]+)/?$', OrgsHandler),
    (r'/([\w+-]+)/([\w+-]+)/?$', ProjectsHandler),

    (r'/([\w+-]+)/([\w+-]+)/manage/?$', ProjectManageHandler),
    (r'/([\w+-]+)/([\w+-]+)/rename/?$', ProjectRenameHandler),
    (r'/([\w+-]+)/([\w+-]+)/describe/?$', ProjectDescribeHandler),
    (r'/([\w+-]+)/([\w+-]+)/delete/?$', ProjectDeleteHandler),

    # (r'/([\w+-]+)/([\w+-]+)/versions/?$', ),
    # (r'/([\w+-]+)/([\w+-]+)/versions/([\w+- ]+)/?$', ),
    # (r'/([\w+-]+)/([\w+-]+)/versions/([\w+- ]+)/edit/?$', ),
    # (r'/([\w+-]+)/([\w+-]+)/versions/([\w+- ]+)/delete/?$', ),

]
