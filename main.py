#!/usr/bin/env python3

from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import List
import requests
import sys


@dataclass
class CodeRequest:

    name: str
    user: str
    system: str
    game: str
    date: str 


system_lookup = {
    # Atari
    **dict.fromkeys(['2600'], '2600'),
    **dict.fromkeys(['jaguar'], 'Jaguar'),
    **dict.fromkeys(['lynx'], 'Lynx'),
    # Other
    **dict.fromkeys(['3do interactive'], '3DO Interactive'),
    **dict.fromkeys(['nec turbografx16/pc engine'], 'NEC TurboGrafx16/PC Engine'),
    **dict.fromkeys(['nec turbografx16/pc engine cd'], 'NEC TurboGrafx16/PC Engine CD'),
    **dict.fromkeys(['philips cd-i'], 'Philips CD-i'),
    **dict.fromkeys(['snk neogeo'], 'SNK NeoGeo'),
    **dict.fromkeys(['tiger game.com'], 'Tiger Game.com'),
    # Sega
    **dict.fromkeys(['dreamcast', 'dc'], 'Dreamcast'),
    **dict.fromkeys(['game gear', 'gg'], 'Game Gear'),
    **dict.fromkeys(['genesis 32x'], 'Genesis 32X'),
    **dict.fromkeys(['genesis/mega drive', 'md'], 'Genesis/Mega Drive'),
    **dict.fromkeys(['master system', 'ms'], 'Master System'),
    **dict.fromkeys(['saturn'], 'Saturn'),
    **dict.fromkeys(['sega cd'], 'Sega CD'),
    # Nintendo
    **dict.fromkeys(['famicom disk system', 'fds'], 'Famicom Disk System'),
    **dict.fromkeys(['game boy', 'gb'], 'Game Boy'),
    **dict.fromkeys(['game boy advance', 'gba'], 'Game Boy Advance'),
    **dict.fromkeys(['game boy color', 'gbc'], 'Game Boy Color'),
    **dict.fromkeys(['gamecube', 'gc', 'gcn', 'ngc'], 'Gamecube'),
    **dict.fromkeys(['nintendo 3ds', '3ds'], 'Nintendo 3DS'),
    **dict.fromkeys(['nintendo 3ds (dlc)', '3ds dlc'], 'Nintendo 3DS (DLC)'),
    **dict.fromkeys(['nintendo 64', 'n64'], 'Nintendo 64'),
    **dict.fromkeys(['nintendo ds', 'nds', 'ds'], 'Nintendo DS'),
    **dict.fromkeys(['nintendo entertainment system', 'nes'], 'Nintendo Entertainment System'),
    **dict.fromkeys(['super nintendo', 'snes'], 'Super Nintendo'),
    **dict.fromkeys(['virtual boy', 'vb'], 'Virtual Boy'),
    **dict.fromkeys(['wii'], 'Wii'),
    **dict.fromkeys(['wii (dlc)', 'wii dlc'], 'Wii (DLC)'),
    # Microsoft
    **dict.fromkeys(['msx'], 'MSX'),
    # Sony
    **dict.fromkeys(['playstation', 'ps1', 'psx'], 'Playstation'),
    **dict.fromkeys(['playstation 2', 'ps2'], 'Playstation 2'),
    **dict.fromkeys(['playstation 3', 'ps3'], 'Playstation 3'),
    **dict.fromkeys(['playstation 3 (psn)', 'ps3 psn'], 'Playstation 3 (PSN)'),
    **dict.fromkeys(['playstation portable', 'psp'], 'Playstation Portable'),
    **dict.fromkeys(['playstation portable (psn)', 'psp psn'], 'Playstation Portable (PSN)'),
    **dict.fromkeys(['playstation vita', 'psv', 'ps vita', 'vita'], 'Playstation Vita'),
    **dict.fromkeys(['playstation vita (psn)', 'psv psn', 'ps vita psn', 'vita psn'], 'Playstation Vita (PSN)')
}


def search(page: int = 0) -> requests.Response:
    return requests.get(f'https://gamehacking.org/requests/{page}')


def format_code_request(code_request) -> CodeRequest:
    return CodeRequest(
        code_request[0].get_text(),
        code_request[1].get_text(),
        code_request[2].get_text(),
        code_request[3].get_text(),
        code_request[4].get_text()
    )


def filter_code_requests(response: requests.Response, system: str) -> List[CodeRequest]:
    soup = BeautifulSoup(response.text, 'html.parser')
    code_requests = soup.find('table', {'class': 'table table-striped'}).find_all('tr')
    filtered_code_requests = []

    for x in range(1, len(code_requests)):  # Start at index 1 to skip the header
        code_request = code_requests[x].find_all('td')
        
        if code_request[2].get_text() == system:
            filtered_code_requests.append(format_code_request(code_request))

    return filtered_code_requests


if __name__ == '__main__':
    system = 'nintendo ds'
    max_pages = 30

    if len(sys.argv) > 1:
        system = sys.argv[1].lower()

        if len(sys.argv) == 3:
            if sys.argv[2].isnumeric():
                max_pages = int(sys.argv[2])
            else:
                sys.exit(f'Error: {sys.argv[2]} is not a number')
    
    system = system_lookup.get(system)

    if system:
        print(f'Searching the first {max_pages} pages on GameHacking.org for {system} requests...\n')

        for x in range(0, max_pages):
            response = search(x)
            
            if response.status_code == 200:
                filtered_code_requests = filter_code_requests(response, system)

                if filtered_code_requests:
                    print(filtered_code_requests)
    else:
        sys.exit('Error: GameHacking.org does not support this system')
