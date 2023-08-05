# HeaderIndexer
A system to bind aliases to indexes of headers in a matrix. 

Given a dict of header aliases paired to the actual header value (or an iterable of possible values)
creates a dict with entries {'alias': column_index} 

Includes interactive prompts to manually select headers when unable to find, and optional duplicate
checks for aliases sharing indexes

## Installation
```
pip install headerindexer
```

## Using HeaderIndexer
 ```python
from headerindexer import HI
indexer = HI()
headers = ["Date", "OS", "TrackingID", "DNSHostname", b"DNSHostname", 77]
aliases = {
    b'hostname':     ["DNSHostname", b'DNSHostname'],
    "track":        ("1TrackingID1", 'TrackingID'),
    "OS":           "OperatingSystem",
    7:              77
}
aliases_to_indexes = indexer.run(headers, aliases)

```

Assume we've extracted a row of headers from a spreadsheet. Create a dictionary like aliases, and 
pass them both to indexer (HI.run()) 
 
```python
# aliases_to_indexes, generated above
{b'hostname': 3, 'track': 2, 'OS': 1, 7: 5}
```
The returned dictionary can be used to reliably call on the appropriate column by given aliases

### Headers not found/Duplicates headers

By default, when an alias' header cannot be located headerindexer will prompt the user to manually 
select from a list of all headers, one by one

Additionally HI.allow_duplicates can be set to False in or after init, enabling a similar mode of 
prompting whenever two or more aliases share the same index value 

