import serial

END_OF_MESSAGE = b'\xfd'

PREAMBLE = b'\xfe\xfe'


class IcomCiv:
    def __init__(self,
                 port: str = '/dev/ttyUSB01',
                 transceiver_address: int = 0x00,
                 controller_address: int = 0x00,
                 debug: bool = False):
        self._serial = serial.Serial(port)
        self._transceiver_address = transceiver_address
        self._controller_address = controller_address
        self._debug = debug

    def _send_command(self, command: bytes, data: bytes = b'') -> bytes:
        bytes_to_send = PREAMBLE + \
                        self._transceiver_address.to_bytes(1, byteorder='big') + \
                        self._controller_address.to_bytes(1, byteorder='big') + \
                        command + \
                        data + \
                        END_OF_MESSAGE

        if self._debug:
            print('Sent: ['+ ', '.join([f'{x:02x}' for x in bytes_to_send]) + ']')

        # write the bytes
        self._serial.write(bytes_to_send)

        # read the response
        response = self._serial.read_until(expected=END_OF_MESSAGE)

        # if the bytes we sent were echoed back at us, read the response again
        if response == bytes_to_send:
            response = self._serial.read_until(expected=END_OF_MESSAGE)

        if self._debug:
            print('Recd: ['+ ', '.join([f'{x:02x}' for x in response]) + ']')

        # strip the preamble, controller_address, transceiver_address, and end_of_message from the response
        response = response[len(PREAMBLE) + 2:-1]

        # if the command we sent is in the response, strip it
        if response.startswith(command):
            response = response[len(command):]

        # if the data we sent is in the response, strip it
        if response.startswith(data):
            response = response[len(data):]

        return response
