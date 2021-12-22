import server
import mock


## testcase for connecting with server
server_socket = mock.create_autospec(server.ser_sock)
def test_unix_fs(mocker):
    server_socket("127.0.0.1", "12345")
    server_socket.assert_called_once_with("127.0.0.1", "12345")


# import unittest
# import socket
# from time import sleep
# import mock
# import TcpService

# def accept_gen():
#     for i in range(1):
#         mock_socket = mock.MagicMock(name='socket.socket', spec=socket.socket)
#         sleep(1)
#         yield (mock_socket, ['127.0.0.1', 12345])
#     while True:
#         sleep(1) # so I have a chance to kill the process before the OS becomes unresponsive
#         yield socket.error()



# class test_TcpService(unittest.TestCase):

#     @mock.patch('socket.socket', autospec=True)
#     def test_listen_tcp(self, mock_socket):
#         mocked_socket = mock_socket.return_value
#         mocked_socket.accept.side_effect = accept_gen()
#         sts = TcpService()
#         with self.assertRaises(socket.error):
#             sts.listen_tcp()
#             mock_socket.assert_called_once() # trivial POC check, final test would be more thorough...
#         sts.close_tcp()
