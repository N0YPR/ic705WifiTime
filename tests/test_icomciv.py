import unittest
from unittest.mock import patch

from callee import ArgThat, StartsWith, EndsWith, Regex

from icom.icomciv import IcomCiv

@patch('serial.Serial')
class Test_IcomCiv(unittest.TestCase):
    def test_send_command_sends_preamble(self, mock_serial):
        icom = IcomCiv()
        icom._send_command(b'\x00')
        mock_serial().write.assert_called_with(StartsWith(b'\xfe\xfe'))

    def test_send_command_sends_end_of_message(self, mock_serial):
        icom = IcomCiv()
        icom._send_command(b'\x00')
        mock_serial().write.assert_called_with(EndsWith(b'\xfd'))

    def test_send_command_sends_transceiver_address(self, mock_serial):
        icom = IcomCiv(transceiver_address=0x98, debug=True)
        icom._send_command(b'\x00')
        # 3rd byte should be transceiver address
        mock_serial().write.assert_called_with(Regex(b'..\x98.*'))

    def test_send_command_sends_controller_address(self, mock_serial):
        icom = IcomCiv(controller_address=0x99, debug=True)
        icom._send_command(b'\x00')
        # 4th byte should be controller address
        mock_serial().write.assert_called_with(Regex(b'...\x99.*'))

    def test_send_command_sends_single_byte_command(self, mock_serial):
        icom = IcomCiv(debug=True)
        command = b'\xaa'
        icom._send_command(command)
        # the command should be the penultimate byte
        mock_serial().write.assert_called_with(Regex(b'.*' + command + b'.'))

    def test_send_command_sends_double_byte_command(self, mock_serial):
        icom = IcomCiv(debug=True)
        command = b'\xaa\xab'
        icom._send_command(command)
        # the command should be the penultimate bytes
        mock_serial().write.assert_called_with(Regex(b'.*' + command + b'.'))

    def test_send_command_sends_data(self, mock_serial):
        icom = IcomCiv(debug=True)
        command = b'\xaa\xab'
        data = b'\xac\xad'
        icom._send_command(command, data=data)
        # the data should be the penultimate bytes
        mock_serial().write.assert_called_with(Regex(b'.*' + data + b'.'))

    def test_send_command_reads_until_end_of_message_once_if_no_echo(self, mock_serial):
        mock_serial().read_until.return_value = b'\xfe\xfe\x99\x98\xfb\xfd'
        icom = IcomCiv(transceiver_address=0x98, controller_address=0x99, debug=True)
        icom._send_command(b'\x00')
        self.assertEqual(1, mock_serial().read_until.call_count)

    def test_send_command_reads_until_end_of_message_twice_if_echo(self, mock_serial):
        mock_serial().read_until.side_effect = [
            b'\xfe\xfe\x98\x99\x00\xfd',
            b'\xfe\xfe\x99\x98\xfb\xfd'
            ]
        icom = IcomCiv(transceiver_address=0x98, controller_address=0x99, debug=True)
        icom._send_command(b'\x00')
        self.assertEqual(2, mock_serial().read_until.call_count)

    def test_send_command_returns_OK(self, mock_serial):
        mock_serial().read_until.return_value = b'\xfe\xfe\x99\x98\xfb\xfd'
        icom = IcomCiv(transceiver_address=0x98, controller_address=0x99, debug=True)
        response = icom._send_command(b'\x00')
        self.assertEqual(b'\xfb', response)

    def test_send_command_returns_NG(self, mock_serial):
        mock_serial().read_until.return_value = b'\xfe\xfe\x99\x98\xfa\xfd'
        icom = IcomCiv(transceiver_address=0x98, controller_address=0x99, debug=True)
        response = icom._send_command(b'\x00')
        self.assertEqual(b'\xfa', response)

    def test_send_command_returns_response_data(self, mock_serial):
        mock_serial().read_until.return_value = b'\xfe\xfe\x99\x98\x00\x00\x01\x01\x88\xfd'
        icom = IcomCiv(transceiver_address=0x98, controller_address=0x99, debug=True)
        response = icom._send_command(b'\x00\x00', data=b'\x01\x01')
        self.assertEqual(b'\x88', response)


if __name__ == '__main__':
    unittest.main()
