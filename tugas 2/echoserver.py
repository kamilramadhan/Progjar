import socket
import unittest
from io import StringIO
from unittest.mock import patch, MagicMock

def handle_client_connection(client_socket, addr):
    """Handle a single client connection."""
    print(f"Got a connection from {addr}")

    # Receiving message
    message = client_socket.recv(1024)
    print(f"Received from client: {message.decode()}")

    # Sending back the same message (echo)
    client_socket.send(message)
    print(f"Sending back to client: {message.decode()}")

    # Close the socket
    client_socket.close()

def start_server():
    """Start the server and listen for incoming connections."""
    # Create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Define address
    host = '127.0.0.1'
    port = 12345

    # Bind address to socket
    server_socket.bind((host, port))

    # Listen
    server_socket.listen(1)
    print(f"Listening on {host}:{port} ...")
    try:
        while True:
            # Accept connection from client
            client_socket, addr = server_socket.accept()
            handle_client_connection(client_socket, addr)
    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        # Close socket
        server_socket.close()

class TestServer(unittest.TestCase):
    @patch('socket.socket')
    def test_handle_client_connection(self, mock_socket):
        """Test handling of a client connection."""
        print('Test handle_client_connection ...')
        mock_client_socket = MagicMock()
        mock_addr = ('127.0.0.1', 12345)

        # Simulate the message that is received by the server
        mock_client_socket.recv.return_value = b'Welcome into this client-server-client sending message program!'

        # Handle the client connection
        handle_client_connection(mock_client_socket, mock_addr)

        # Assert that `recv` method was called with the expected size of 1024 bytes
        mock_client_socket.recv.assert_called_with(1024)
        print(f"recv called with: {mock_client_socket.recv.call_args}")

        # Assert that the message sent back to the client is the same as the received message
        mock_client_socket.send.assert_called_with(b'Welcome into this client-server-client sending message program!')
        print(f"send called with: {mock_client_socket.send.call_args}")

        # Ensure that the socket was closed after the interaction
        mock_client_socket.close.assert_called_once()
        print(f"close called with: {mock_client_socket.close.call_args}")

    @patch('socket.socket')
    def test_start_server(self, mock_socket):
        """Test starting of the server and listening for connections."""
        print('Test start_server ...')
        mock_server_socket = MagicMock()
        mock_client_socket = MagicMock()
        mock_addr = ('127.0.0.1', 12345)

        # Mock the socket creation and the accepting of client connections
        mock_socket.return_value = mock_server_socket
        mock_server_socket.accept.side_effect = [(mock_client_socket, mock_addr), KeyboardInterrupt]

        # Simulate the message received from the client
        mock_client_socket.recv.return_value = b'Welcome into this client-server-client sending message program!'

        try:
            start_server()
        except KeyboardInterrupt:
            pass

        print(f"accept called with: {mock_server_socket.accept.call_args}")

        # Assert the server binds to the specified address and port
        mock_server_socket.bind.assert_called_once_with(('127.0.0.1', 12345))
        print(f"bind called with: {mock_server_socket.bind.call_args}")

        # Assert that the server listens for incoming connections
        mock_server_socket.listen.assert_called_once_with(1)
        print(f"listen called with: {mock_server_socket.listen.call_args}")

class NullWriter(StringIO):
    def write(self, txt):
        pass

if __name__ == '__main__':
    # Run unittest with a custom runner that suppresses output
    runner = unittest.TextTestRunner(stream=NullWriter())
    unittest.main(testRunner=runner, exit=False)

    # Uncomment this if you want to run the server program, not running the unit test
    # start_server()
