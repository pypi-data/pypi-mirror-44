# Extract infoboxes from wikidumps

To create a wikidump for a specific category or group of articles, you can use [Wikipedia's special export feature](https://en.wikipedia.org/wiki/Special%3aExport).

Download the .xml file and then you can convert the xml dump to a .js file containing a list of infobox objects.

## Usage
```
$ python3 extract_from_dump.py <xml dump file path> <output file path>
```
