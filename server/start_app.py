from gevent import monkey
monkey.patch_all()

from app import app
import resource

resource.setrlimit(resource.RLIMIT_NOFILE, (4096, 4096))

if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True)
