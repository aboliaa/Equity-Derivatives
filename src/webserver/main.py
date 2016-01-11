WEBPY = "webpy"

class WebServer():
    def __init__(self, webserver_type=WEBPY):
        module = __import__(webserver_type)
        self.webserver = module.WServer()

    def make_app(self):
        self.webserver.make_app()

    def run_app(self):
        self.webserver.run_app()

if __name__ == "__main__":
    srv = WebServer()
    srv.make_app()
    srv.run_app()
