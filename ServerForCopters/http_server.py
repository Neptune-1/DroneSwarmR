from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import time

import rospy
from clever import srv


class MWT(object):
    """Memoize With Timeout"""
    _caches = {}
    _timeouts = {}

    def __init__(self, timeout=2):
        self.timeout = timeout

    def collect(self):
        """Clear cache of results which have timed out"""
        for func in self._caches:
            cache = {}
            for key in self._caches[func]:
                if (time.time() - self._caches[func][key][1]) < self._timeouts[func]:
                    cache[key] = self._caches[func][key]
            self._caches[func] = cache

    def __call__(self, f):
        self.cache = self._caches[f] = {}
        self._timeouts[f] = self.timeout

        def func(*args, **kwargs):
            kw = sorted(kwargs.items())
            key = (args, tuple(kw))
            try:
                v = self.cache[key]
                print("cache")
                if (time.time() - v[1]) > self.timeout:
                    raise KeyError
            except KeyError:
                print("new")
                v = self.cache[key] = f(*args,**kwargs),time.time()
            return v[0]
        func.func_name = f.__name__
        return func


rospy.init_node('telem_server')
get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)


@MWT(timeout=0.1)
def get_telem(frame_id):
    return get_telemetry(frame_id=frame_id)


class HttpProcessor(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        path = path.replace('/', '')
        try:
            params = [
                'armed', 'frame_id', 'mode',
                'pitch', 'roll', 'voltage',
                'vx', 'vy', 'vz',
                'x', 'y', 'yaw',
                'yaw_rate', 'z'
            ]
            telemetry = get_telem(frame_id=path)
            telem = {}
            for e in params:
                attr = getattr(telemetry, e)
                if type(attr) is float:
                    attr = round(attr, 3)
                telem[e] = attr
            resp = json.dumps(telem)
            self.send_response(200)
            self.send_header('content-type', 'application/json')
            self.end_headers()
            self.wfile.write(resp)
        except rospy.service.ServiceException as e:
            self.send_response(404)
            self.end_headers()
            self.wfile.write('404: ' + str(e))
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write('500: ' + str(e))


server_address = ('', 8081)
httpd = HTTPServer(server_address, HttpProcessor)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print('exit')
