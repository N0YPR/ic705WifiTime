import unittest
from unittest.mock import patch

from icom import IC705


@patch('serial.Serial')
class MyTestCase(unittest.TestCase):
    def test_read_date_setting(self, mock_serial):
        mock_serial().read_until.return_value = b'\xfe\xfe\x99\x98\x1a\x05\x01\x65\x20\x23\x01\x04\xfd'
        icom = IC705(debug=True)
        date = icom.read_date_setting()
        self.assertEqual((2023, 1, 4), date)

    def test_read_time_setting(self, mock_serial):
        mock_serial().read_until.return_value = b'\xfe\xfe\x99\x98\x1a\x05\x01\x66\x00\x05\xfd'
        icom = IC705(debug=True)
        date = icom.read_time_setting()
        self.assertEqual((0, 5), date)

if __name__ == '__main__':
    unittest.main()
