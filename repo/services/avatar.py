import hashlib


def avatar_url(email, size = None):
    m = hashlib.md5()
    m.update(email.lower())
    if size:
        return '//www.gravatar.com/avatar/%s?s=%i' % (m.hexdigest(), size)
    else:
        return '//www.gravatar.com/avatar/%s' % m.hexdigest()
