from http.server import SimpleHTTPRequestHandler, HTTPServer
import logging

class MainHandler(SimpleHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

def main(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
    logging.basicConfig(level=logging.INFO)
    server_address = ("", 80)
    with server_class(server_address, handler_class) as httpd:
        logging.info('Starting httpd...\n')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.server_close()
            logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    main()