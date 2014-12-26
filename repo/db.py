import momoko
from settings.settings import settings
from tornado import gen

dsn = '''
    dbname=repo user=%(user)s password=%(password)s
    host=%(host)s port=%(port)s
''' % {
    'user': settings['db_user'],
    'password': settings['db_password'],
    'host': settings['db_host'],
    'port': settings['db_port']
}

db = momoko.Pool(
    dsn=dsn,
    size=1
)

@gen.coroutine
def map_one(constr, *args):
    cursor = yield momoko.Op(db.execute, *args)
    fetched = cursor.fetchone()
    if fetched is None:
        raise gen.Return(None)
    else:
        raise gen.Return(constr._make(fetched))

@gen.coroutine
def map_all(constr, *args):
    cursor = yield momoko.Op(db.execute, *args)
    objs = [constr._make(obj) for obj in cursor.fetchall()]
    raise gen.Return(objs)