from typing import Tuple

from icom.icomciv import IcomCiv


class IC705(IcomCiv):
    def read_date_setting(self) -> Tuple[int, int, int]:
        response = self._send_command(command=b'\x1a\x05', data=b'\x01\x65')
        return (
            int(f'{response[0]:02x}{response[1]:02x}'),
            int(f'{response[2]:02x}'),
            int(f'{response[3]:02x}'),
        )

    def read_time_setting(self) -> Tuple[int, int]:
        response = self._send_command(command=b'\x1a\x05', data=b'\x01\x66')
        return (
            int(f'{response[0]:02x}'),
            int(f'{response[1]:02x}'),
        )
        pass