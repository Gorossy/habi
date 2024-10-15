import pytest
from http.server import HTTPServer
from io import BytesIO
from unittest.mock import patch, MagicMock
import json
from main import MyServer

@pytest.fixture
def mock_connection():
    with patch('main.create_connection') as mock_conn:
        mock_conn.return_value.cursor.return_value.fetchall.return_value = [
            {
                'address': 'Calle 123',
                'city': 'Bogotá',
                'price': 500000000,
                'description': 'Inmueble en excelente estado',
                'status': 'en_venta'
            }
        ]
        yield mock_conn

@pytest.fixture
def make_request():
    def _make_request(path):
        request = MagicMock()
        request.makefile.return_value = BytesIO(b'GET %s HTTP/1.1\r\nHost: localhost\r\n\r\n' % path.encode('utf-8'))
        response = BytesIO()

        def mock_send_response(*args, **kwargs):
            response.write(b'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n')
            response.write(json.dumps([
                {
                    'address': 'Calle 123',
                    'city': 'Bogotá',
                    'price': 500000000,
                    'description': 'Inmueble en excelente estado',
                    'status': 'en_venta'
                }
            ]).encode('utf-8'))

        with patch.object(MyServer, 'send_response', new=mock_send_response):
            MyServer(request, ('127.0.0.1', 0), lambda *args, **kwargs: None)

        response.seek(0)
        return response

    return _make_request

def test_get_inmuebles(mock_connection, make_request):
    response = make_request('/inmuebles')
    response_lines = response.getvalue().decode().split('\r\n\r\n', 1)
    if len(response_lines) > 1:
        response_data = json.loads(response_lines[1])
    else:
        response_data = []

    assert len(response_data) == 1
    assert response_data[0]['address'] == 'Calle 123'
    assert response_data[0]['city'] == 'Bogotá'
    assert response_data[0]['price'] == 500000000
    assert response_data[0]['description'] == 'Inmueble en excelente estado'
    assert response_data[0]['status'] == 'en_venta'

if __name__ == '__main__':
    pytest.main()