import unittest
from unittest.mock import patch, MagicMock
import socket
from io import StringIO

import socket

def download_file(filename):
    """Connect to the server and request a file download."""
    # Define the server address
    host = '127.0.0.1'
    port = 12345

    # Create socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((host, port))
        print(f"Connected to server on port {port}")

        # Send the filename to the server
        client_socket.sendall(filename.encode())

        # Receive the file content or error message from the server
        response = b""
        while True:
            part = client_socket.recv(1024)
            if not part:
                break
            response += part

        print("Received from server:")
        print(response.decode())

    finally:
        # Close the connection
        client_socket.close()
        print("Connection closed.")

def main():
    # Example usage
    filename = input("Enter the filename to download: ")
    download_file(filename)

class NullWriter(StringIO):
    def write(self, txt):
        pass

class TestDownloadFile(unittest.TestCase):
    @patch('socket.socket')
    def test_download_file_success(self, mock_socket):
        """Test file download when the file exists."""
        print('Testing file download success ...')
        host = '127.0.0.1'  # Localhost
        port = 12345        # Port to listen on

        mock_socket_instance = MagicMock()
        mock_socket.return_value = mock_socket_instance

        # Mock the recv to simulate receiving chunks of file content
        mock_socket_instance.recv.side_effect = [
            b"Hello, this is the content of example.txt",
            b""
        ]

        # Execute
        filename = "example.txt"
        download_file(filename)

        # Assertions
        mock_socket_instance.connect.assert_called_with((host, port))
        print(f"connect called with: {mock_socket_instance.connect.call_args}")
        mock_socket_instance.sendall.assert_called_with(b"example.txt")
        print(f"sendall called with: {mock_socket_instance.sendall.call_args}")


    @patch('socket.socket')
    def test_download_file_non_existing(self, mock_socket):
        """Test file download when the file doesn't exist."""
        print('Testing file download not exist ...')
        host = '127.0.0.1'  # Localhost
        port = 12345        # Port to listen on

        mock_socket_instance = MagicMock()
        mock_socket.return_value = mock_socket_instance

        # Simulate receiving "File not found." from the server
        mock_socket_instance.recv.side_effect = [b"File not found.", b""]

        # Execute
        filename = "non_existent_file.txt"
        download_file(filename)

        # Assertions
        mock_socket_instance.connect.assert_called_with((host, port))
        print(f"connect called with: {mock_socket_instance.connect.call_args}")
        mock_socket_instance.sendall.assert_called_with(b"non_existent_file.txt")
        print(f"sendall called with: {mock_socket_instance.sendall.call_args}")
        mock_socket_instance.recv.assert_called_with(1024)
        print(f"recv called with: {mock_socket_instance.recv.call_args}")

if __name__ == '__main__':
    # Run the unit tests
    unittest.main()
