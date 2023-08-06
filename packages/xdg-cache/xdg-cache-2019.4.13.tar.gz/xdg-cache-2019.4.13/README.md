<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/xdg-cache.svg?longCache=True)](https://pypi.org/project/xdg-cache/)

#### Installation
```bash
$ [sudo] pip install xdg-cache
```

#### Functions
function|`__doc__`
-|-
`xdg_cache.exists(key)` |return True if cache exists, else False
`xdg_cache.read(key)` |return a file content string, return None if cache not exist
`xdg_cache.rm(key)` |remove cache file
`xdg_cache.write(key, string)` |write string to cache

#### Examples
```python
>>> import xdg_cache
>>> xdg_cache.write("key",'value')
>>> xdg_cache.read("key")
'value'
>>> xdg_cache.path("key")
'~/.cache/key'
>>> xdg_cache.exists("key")
True
>>> xdg_cache.rm("key")
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>