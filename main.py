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
    system = 'Nintendo DS'
    max_pages = 30

    if len(sys.argv) > 1:
        system = sys.argv[1]

        if len(sys.argv) == 3:
            if sys.argv[2].isnumeric():
                max_pages = int(sys.argv[2])
            else:
                sys.exit(f'Error: {sys.argv[2]} is not a number')
    
    print(f'Searching the first {max_pages} pages on GameHacking.org for {system} requests...\n')

    for x in range(0, max_pages):
        response = search(x)
        
        if response.status_code == 200:
            filtered_code_requests = filter_code_requests(response, system)

            if filtered_code_requests:
                print(filtered_code_requests)
