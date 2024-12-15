# -*- coding: utf-8 -*- noqa
import json
import logging
import sys
import traceback

from http.server import BaseHTTPRequestHandler, HTTPServer, HTTPStatus

from database import Database


class Server(BaseHTTPRequestHandler):
    """Server Running."""

    data_base = Database()

    def log_request(self, code='No Code', size='No Size'):
        """Log an accepted request.

        This is called by send_response().

        Unicode control characters are replaced with escaped hex
        before writing the output to stderr.
        """
        if isinstance(code, HTTPStatus):
            code = code.value

        message = self.requestline

        self.log_message(
            'Request: %s\nCode: %s\nSize: %s',
            message.translate(self._control_char_table),
            str(code),
            str(size)
        )

    def log_error(self, error_format, *args):
        """
        Log an error.

        This is called when a request cannot be fulfilled.  By
        default it passes the message on to log_message().

        Arguments are the same as for log_message().
        """
        error = ("From: %s\n%s" % (
            self.address_string(),
            (error_format % args).translate(self._control_char_table),

        )).replace(
            "  ", "\t"
        ).replace(
            "\n", "\n\t\t"
        )

        logging.error(error)

    def log_message(self, message_format, *args):
        """
        Log an arbitrary message.

        This is used by all other logging functions.  Override
        it if you have specific logging wishes.

        The first argument, FORMAT, is a format string for the
        message to be logged.  If the format string contains
        any % escapes requiring parameters, they should be
        specified as subsequent arguments (it's just like
        printf!).

        The client ip and current date/time are prefixed to
        every message.
        """
        message = ("From: %s\n%s" % (
            self.address_string(),
            message_format % args,

        )).replace(
            "  ", "\t"
        ).replace(
            "\n", "\n\t\t"
        )

        logging.info(message)

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        """
        HTTP Server Get request.

        Returns
        -------
        None.

        """
        if self.path == '/favico.ico':
            self.send_response(204)
            self.end_headers()

        elif self.path == '/':
            self._set_response()
            f = open('./public/index.html')
            self.wfile.write(bytes(f.read(), "utf-8"))
            f.close()

        elif self.path == '/lyne':
            self.send_response(200)
            self.send_header('Content-type', 'application/javascript')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            f = open('./public/Lyne.js')
            self.wfile.write(bytes(f.read(), "utf-8"))

        elif self.path == "/get-data":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            json_data = json.dumps(self.data_base.get_data())
            self.wfile.write(bytes(json_data, "utf-8"))

        else:
            self.send_response(303)
            self.send_header("Location", "/")
            self.end_headers()
            # self.send_error(404, f"'{self.path}' was not found")

    def do_POST(self):
        """
        HTTP Server Post request.

        Returns
        -------
        None.

        """
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode())

        self.data_base.add_data(data)

        self._set_response()


if __name__ == '__main__':
    logging

    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        force=True,
        format='[%(asctime)s] %(levelname)s:\n\tModule: "%(module)s"\n\t' +
        'Function: "%(funcName)s"\n\tLine: %(lineno)d\n\t\t%(message)s\n',
    )

    is_serving = False

    try:
        logging.info('Configuring HTTP Server.')
        server_address = ('', 8080)
        logging.info('HTTP Server Configured.')

        logging.info(
            'Starting HTTP Server in address "{0}" and port "{1}".'.format(
                *server_address
            )
        )
        http_server = HTTPServer(server_address, Server)
        logging.info(
            'HTTP Server started in address "{0}" and port "{1}".'.format(
                *http_server.socket.getsockname()
            )
        )

        is_serving = True
        logging.info('HTTP Server serving forever.')
        http_server.serve_forever()

        is_serving = False
        logging.critical(
            'HTTPS Server did not serve correctly but also did not raise an' +
            ' exception.'
        )

    except KeyboardInterrupt:
        logging.info('Manual stop.')

    except:  # noqa
        logging.error(
            traceback.format_exc()[:-1].replace(
                "  ", "\t"
            ).replace(
                "\n", "\n\t\t"
            )
        )

    finally:
        if "http_server" in globals():
            logging.info('Stopping HTTP Server.')
            if is_serving:
                http_server.shutdown()
            http_server.server_close()
            del http_server
            logging.info('HTTP Server Stopped.')
        logging.shutdown()
        sys.exit()
