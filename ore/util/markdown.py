import os.path
import dukpy

basepath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def load_dukpy_ctx():
    result = os.path.join(basepath, 'node_modules')
    if not os.path.exists(result):
        raise ValueError("Unable to locate node_modules directory - is Ore installed correctly?")

    ctx = dukpy.RequirableContext([result])
    return ctx


def load_mdit(ctx):
    with open(os.path.join(basepath, 'ore/core/static/ore/js/markdown.js'), 'r') as f:
        return ctx.evaljs(f.read())

ctx = load_dukpy_ctx()
mdit = None


def compile(text, context={}):
    global mdit
    if mdit is None:
        mdit = load_mdit(ctx)

    return mdit.render(text)
