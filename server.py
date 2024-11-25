import json
import logging
import traceback

import boto3 as aws

from botocore.exceptions import ClientError
from datetime import datetime, timezone
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
        
        save_data(data)
        
        logging.debug(post_data)
        logging.debug("POST request data"+ data)


def save_data(data):
    try:
            logging.info("Saving data to S3 Bucket.")
            
            logging.debug(datetime.now(timezone.utc))
            
            bucket.put_object(Body=data, Key=str(datetime.now(timezone.utc)))
            bucket.wait_until_exists()
            
    except ClientError as error:
        logging.error(traceback.format_exc()[:-1].replace("  ", "\t").replace("\n", "\n\t\t"))
    

if __name__ == '__main__':
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
        
    logging

    logging.basicConfig(
        filename=config['logging_file'],
        filemode="w",
        level=logging.DEBUG,
        force=True,
        format='[%(asctime)s] %(levelname)s:\n\tModule: "%(module)s"\n\tFunction: "%(funcName)s"\n\tLine: %(lineno)d\n\t\t%(message)s\n',
    )
    
    try:
        bucket = aws.resource('s3').Bucket(config['bucket_name'])
            
        server_address = ('', config['port'])
        
        httpd = HTTPServer(server_address, S)
        
        logging.info("Starting...")
        
        httpd.serve_forever()
        
    except:
        logging.error(traceback.format_exc()[:-1].replace("  ", "\t").replace("\n", "\n\t\t"))
    finally:
        logging.info("Stopping...")
        logging.shutdown()
