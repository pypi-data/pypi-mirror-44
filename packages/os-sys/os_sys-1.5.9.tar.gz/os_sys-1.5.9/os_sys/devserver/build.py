try:
    from . import server
except:
    import server
__all__ = ['path', 'config', 'HTTPResponse', 'paths']
def paths(port, **programs):

    server.run_(port, **programs)
def config(port=9999, **programs):
    paths(port, **programs)
def HTTPResponse(response):
    return response
def path(program, name, *args, **kwargs):
    return name, program
