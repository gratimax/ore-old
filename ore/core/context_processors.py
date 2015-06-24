from django.conf import settings


def build_stamp(request):
    return {
        'ore_build_stamp': settings.BUILD_STAMP,
    }
