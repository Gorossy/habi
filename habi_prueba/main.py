import os
from dotenv import load_dotenv
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from database import create_connection

load_dotenv()

class MyServer(BaseHTTPRequestHandler):

    def _set_response(self, code=200, content_type='application/json'):
        self.send_response(code)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def do_GET(self):

        if self.path == "/swagger.yaml":
            self.send_response(200)
            self.send_header('Content-type', 'text/yaml')
            self.end_headers()
            with open('swagger.yaml', 'r') as file:
                self.wfile.write(file.read().encode('utf-8'))

        elif self.path.startswith("/inmuebles"):
            params = self._get_query_params()

            year_filter = params.get('year', None)
            city_filter = params.get('city', None)
            status_filter = params.get('status', None)

            connection = create_connection()
            cursor = connection.cursor(dictionary=True)

            query = """
            SELECT
                p.address,
                p.city,
                p.price,
                p.description,
                s.name AS status
            FROM
                property p
            INNER JOIN
                (
                    SELECT
                        sh1.property_id,
                        sh1.status_id,
                        sh1.update_date
                    FROM
                        status_history sh1
                    INNER JOIN
                        (
                            SELECT
                                property_id,
                                MAX(update_date) AS max_update_date
                            FROM
                                status_history
                            GROUP BY
                                property_id
                        ) sh2 ON sh1.property_id = sh2.property_id AND sh1.update_date = sh2.max_update_date
                ) sh ON p.id = sh.property_id
            INNER JOIN
                status s ON sh.status_id = s.id
            WHERE
                s.name IN ('pre_venta', 'en_venta', 'vendido')
                AND p.address IS NOT NULL
                AND p.city IS NOT NULL
                AND p.price IS NOT NULL
                AND p.year IS NOT NULL
            """

            filters = []
            params_values = []

            if year_filter:
                filters.append("AND p.year = %s")
                params_values.append(year_filter)

            if city_filter:
                filters.append("AND p.city = %s")
                params_values.append(city_filter)

            if status_filter:
                filters.append("AND s.name = %s")
                params_values.append(status_filter)

            if filters:
                query += " " + " ".join(filters)

            cursor.execute(query, params_values)
            rows = cursor.fetchall()
            connection.close()

            self._set_response()
            self.wfile.write(json.dumps(rows, default=str).encode('utf-8'))

    def _get_query_params(self):
        from urllib.parse import urlparse, parse_qs
        query_components = parse_qs(urlparse(self.path).query)
        params = {k: v[0] for k, v in query_components.items()}
        return params

def run():
    port = int(os.getenv("PORT", 8080))
    server_address = ('', port)
    httpd = HTTPServer(server_address, MyServer)
    print(f'Servidor corriendo en el puerto {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
