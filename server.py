from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import sqlite3


class DB:
    conn = None
    cur = None

    def addData(self, dataToAdd):
        Temp = dataToAdd['Temp']
        Hum = dataToAdd['Hum']
        VOC = dataToAdd['VOC']
        PM1 = dataToAdd['PM1']
        PM25 = dataToAdd['PM2.5']
        PM10 = dataToAdd['PM10']

        array = [Temp, Hum, VOC, PM1, PM25, PM10]

        self.cur.execute("INSERT INTO airq VALUES (?, ?, ?, ?, ?, ?)", array)
        self.conn.commit()

    def getData(self):

        temp = self.cur.execute("SELECT temp FROM airq").fetchall()
        hum = self.cur.execute("SELECT hum FROM airq").fetchall()
        voc = self.cur.execute("SELECT voc FROM airq").fetchall()
        pm1 = self.cur.execute("SELECT pm1 FROM airq").fetchall()
        pm25 = self.cur.execute("SELECT pm25 FROM airq").fetchall()
        pm10 = self.cur.execute("SELECT pm10 FROM airq").fetchall()
        json = {
            'Temp': temp,
            'Hum': hum,
            'VOC': voc,
            'PM1': pm1,
            'PM2.5': pm25,
            'PM10': pm10
        }

        # for row in data:
        #     json['Temp'].append(row[0])
        #     json['Hum'].append(row[1])
        #     json['VOC'].append(row[2])
        #     json['PM1'].append(row[3])
        #     json['PM2.5'].append(row[4])
        #     json['PM10'].append(row[5])
        return json

    def __init__(self):
        if self.conn != None:
            return
        self.conn = sqlite3.connect("airQ.db")
        self.cur = self.conn.cursor()
        self.cur.row_factory = lambda cursor, row: row[0]
        # self.cur.execute('CREATE TABLE airq(temp, hum, voc, pm1, pm25, pm10)')
        # self.cur.execute("IF (SELECT name FROM sysobjects where name='airq' ) NOT EXISTS BEGIN CREATE TABLE airq(temp, hum, voc, pm1, pm25, pm10)END")


class S(BaseHTTPRequestHandler):
    dataBase = DB()

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if self.path == '/favico.ico':
            self._set_response()

        if self.path == '/':
            self._set_response()
            f = open('./public/index.html')
            self.wfile.write(bytes(f.read(), "utf-8"))
            f.close()

        if self.path == '/Lyne.js':
            self.send_response(200)
            self.send_header('Content-type', 'application/javascript')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            f = open('./public/Lyne.js')
            self.wfile.write(bytes(f.read(), "utf-8"))

        if self.path == "/getData":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            json_data = json.dumps(self.dataBase.getData())
            self.wfile.write(bytes(json_data, "utf-8"))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode())

        self.dataBase.addData(data)

        self._set_response()

        # print("POST request data"+ data)


if __name__ == '__main__':
    server_address = ('127.0.0.1', 8080)
    httpd = HTTPServer(server_address, S)
    print("Starting http server...")

    httpd.serve_forever()
