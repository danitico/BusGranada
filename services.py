from typing import Dict, List

import httpx
from bs4 import BeautifulSoup

from constants import BUS_ENDPOINT


class StopService:
    @classmethod
    def get_stop_information(cls, stop_number: str) -> List[Dict]:
        response = httpx.get(
            BUS_ENDPOINT,
            params={'idparada': stop_number}
        )

        data = list()

        parser = BeautifulSoup(response.text)
        bus_lines = parser.body.table.table.table.table.table.find_all('tr')

        for bus_line in bus_lines[1:]:
            bus_line_data = bus_line.find_all('td')

            data.append({
                'line_number': bus_line_data[0].span.a.text,
                'line_name': bus_line_data[1].text,
                'time_left': int(bus_line_data[2].text.strip())
            })

        return cls.format_message(data)

    @classmethod
    def format_message(cls, bus_lines: List[Dict]) -> str:
        return '\n'.join(
            [
                f"{bus_line['line_number']} - {bus_line['line_name']} - {bus_line['time_left']} {'minutos' if bus_line['time_left'] > 1 else 'minuto'}"
                for bus_line in bus_lines
            ]
        )
