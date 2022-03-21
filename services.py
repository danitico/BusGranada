from typing import Dict, List

import httpx
from bs4 import BeautifulSoup

from constants import BUS_ENDPOINT, NO_BUSES


class StopService:
    @classmethod
    def get_stop_information(cls, stop_number: str) -> List[Dict]:
        response = httpx.get(
            BUS_ENDPOINT,
            params={'idparada': stop_number}
        )

        data = list()

        parser = BeautifulSoup(response.text)
        try:
            bus_lines = parser.body.table.table.table.table.table.find_all('tr')
        except:
            return NO_BUSES

        for bus_line in bus_lines[1:]:
            bus_line_data = bus_line.find_all('td')

            data.append({
                'line_number': bus_line_data[0].span.a.text,
                'line_name': bus_line_data[1].text,
                'time_left': bus_line_data[2].text.strip()
            })

        return cls.format_message(data)

    @classmethod
    def format_minutes_left(time_left) -> str:
        try:
            time_left_integer = int(time_left)
        except:
            return 'Llegando'

        return f"{time_left_integer} {'minutos' if time_left_integer > 1 else 'minuto'}"

    @classmethod
    def format_message(cls, bus_lines: List[Dict]) -> str:
        return '\n'.join(
            [
                f"{bus_line['line_number']} - {bus_line['line_name']} - {cls.format_minutes_left(bus_line['time_left'])}"
                for bus_line in bus_lines
            ]
        )
