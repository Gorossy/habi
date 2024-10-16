import pytest
from http.server import HTTPServer
from io import BytesIO
from unittest.mock import patch, MagicMock
import json
from datetime import datetime
from main import MyServer


@pytest.fixture
def mock_connection():
    """
    Fixture to mock the database connection.
    Returns a mocked connection object that provides a predefined set of property data.
    """
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
    """
    Fixture to create and return a function for simulating HTTP requests to the server.
    """
    def _make_request(path):
        """
        Simulate an HTTP GET request to the given path.

        Args:
            path (str): The URL path to request.

        Returns:
            BytesIO: The response from the server, including headers and body.
        """
        request = MagicMock()
        request.makefile.return_value = BytesIO(b'GET %s HTTP/1.1\r\nHost: localhost\r\n\r\n' % path.encode('utf-8'))
        response = BytesIO()

        def mock_send_response(instance, code=200, content_type='application/json'):
            """
            Mock the server's _set_response method to write headers and body to the response.

            Args:
                instance: The server instance.
                code (int): The HTTP status code to return.
                content_type (str): The Content-Type header value.
            """
            response.write(f'HTTP/1.1 {code} {"OK" if code == 200 else "Bad Request"}\r\nContent-Type: {content_type}\r\n\r\n'.encode('utf-8'))
            if code == 200:
                response.write(json.dumps([
                    {
                        'address': 'Calle 123',
                        'city': 'Bogotá',
                        'price': 500000000,
                        'description': 'Inmueble en excelente estado',
                        'status': 'en_venta'
                    }
                ]).encode('utf-8'))

        with patch.object(MyServer, '_set_response', new=mock_send_response):
            MyServer(request, ('127.0.0.1', 0), lambda *args, **kwargs: None)

        response.seek(0)
        return response

    return _make_request


def test_get_inmuebles(mock_connection, make_request):
    """
    Test the /inmuebles endpoint to ensure it returns the expected property data.
    """
    response = make_request('/inmuebles')
    response_lines = response.getvalue().decode().split('\r\n\r\n', 1)
    if len(response_lines) > 1 and response_lines[1].strip():
        response_data = json.loads(response_lines[1])
    else:
        response_data = []

    assert len(response_data) == 1
    assert response_data[0]['address'] == 'Calle 123'
    assert response_data[0]['city'] == 'Bogotá'
    assert response_data[0]['price'] == 500000000
    assert response_data[0]['description'] == 'Inmueble en excelente estado'
    assert response_data[0]['status'] == 'en_venta'


def test_year_in_future(mock_connection, make_request):
    """
    Test the /inmuebles endpoint with a year filter in the future.
    Expects a 400 Bad Request response.
    """
    future_year = datetime.now().year + 1
    response = make_request(f'/inmuebles?year={future_year}')
    response_lines = response.getvalue().decode().split('\r\n\r\n', 1)
    response_status_line = response.getvalue().decode().split('\r\n')[0]

    assert '400 Bad Request' in response_status_line


def test_invalid_year_filter(mock_connection, make_request):
    """
    Test the /inmuebles endpoint with an invalid year filter (non-numeric).
    Expects a 400 Bad Request response.
    """
    response = make_request('/inmuebles?year=abcd')
    response_lines = response.getvalue().decode().split('\r\n\r\n', 1)
    response_status_line = response.getvalue().decode().split('\r\n')[0]

    assert '400 Bad Request' in response_status_line


if __name__ == '__main__':
    pytest.main()