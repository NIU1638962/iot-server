import logging
import traceback
from http.server import BaseHTTPRequestHandler, HTTPServer

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = post_data.decode()
        self._set_response()

        logging.debug("POST request data"+ data)

    

if __name__ == '__main__':
    logging

    logging.basicConfig(
        filename="logging.log",
        filemode="w",
        level=logging.DEBUG,
        force=True,
        format='[%(asctime)s] %(levelname)s:\n\tModule: "%(module)s"\n\tFunction: "%(funcName)s"\n\tLine: %(lineno)d\n\t\t%(message)s\n',
    )
    
    try:
        server_address = ('', 8080)
        
        httpd = HTTPServer(server_address, S)
        
        logging.info("Starting...")
        
        httpd.serve_forever()
        
    except:
        logging.error(traceback.format_exc()[:-1].replace("  ", "\t").replace("\n", "\n\t\t"))
    finally:
        logging.info("Stopping...")
        logging.shutdown()
