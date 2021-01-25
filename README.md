# gh-requests-filter

Filters GameHacking.org's requests page by system.

## Dependencies

`bs4` and `requests` are required and can be installed via `pip3` with this command:

```shell
% pip3 install bs4 && pip3 install requests
```

## Usage

Navigate to the directory with the script and run:

```shell
% python3 main.py system max_number_of_pages
```

`system` and `max_number_of_pages` are optional command line arguments. By default, the script will filter using Nintendo DS as the system and the current number of pages as of January 24th, 2021 3:10 EST, which is 30.
