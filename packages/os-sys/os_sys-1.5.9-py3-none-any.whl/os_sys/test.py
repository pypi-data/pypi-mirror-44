from devserver import build
import devserver

def index(request):
    return build.HTTPResponse('post: %s <br> get: %s' % (str(request.POST), str(request.GET)))
devserver.build.config(index=index)
