# Salesforce Marketing Cloud -- Response to JSON

This is a small utility library that I built to process responses from the [Salesforce Marketing Cloud SDK](https://github.com/salesforce-marketingcloud/FuelSDK-Python). It returns JSON payloads sometimes and other times it will return a list of SUDS objects.

## Installation

pip install sfmc-to-json

## Rebuild Package

1. Update version in `setup.py` and `__init__.py`
2. `python setup.py sdist bdist_wheel`
3. `twine upload dist/*` 

## Known Issues

Sometimes error messages come back and will be malformed. They will be valid JSON, but you'll see extraneous data in them.