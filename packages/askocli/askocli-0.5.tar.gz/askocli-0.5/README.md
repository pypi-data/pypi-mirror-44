Askocli
========

AskOcli allow an [AskOmics](https://github.com/askomics/askomics) user to integrate file with the command line into a distant [AskOmics](https://github.com/askomics/askomics).

Requirment
----------

- python3
- python3-venv

Installation
------------

Install from pip

    pip install askocli

Or from sources;

Clone the repository

    git clone https://github.com/askomics/askocli.git
    cd askocli

Set up and activate a virtual environment:

    python3 -m venv venv
    source venv/bin/activate

Install the script in the virtual environment:

    python3 setup.py install

Usage example
-------------

Integration

    askocli integrate -a http://localhost:6543 -k mYap1Key path/to/file.csv
    askocli integrate -a http://localhost:6543 -k mYap1Key -e gene transcript -t Arabidopsis_thaliana path/to/file.gff
    askocli integrate -a http://localhost:6543 -k mYap1Key path/to/file.ttl


History
-------

- 0.1: Initial release!
    - Integrate CSV file into a distant AskOmics
- 0.2: 
   - Use API key instead of password
   - Integrate GFF and TTL
- 0.3: APIkey
   - Use only the API key without the username to login
   - Better error managment
   - Option `-c`, `--columns` to force the columns types
   - Option `--key-columns` to set the key columns
   - Option `--public` to integrate public data
   - Option `--disabled-columns` to don't integrate a columns of a TSV
- 0.3.2
   - FIX error message
- 0.4: Bed files integration
	- Integration of Bed files
	- Option `--uri` to specify an uri for the entity
	- Option `--headers` to set custom headers for TSV files
- 0.5: Compatibility with AskOmics 19.01.2
