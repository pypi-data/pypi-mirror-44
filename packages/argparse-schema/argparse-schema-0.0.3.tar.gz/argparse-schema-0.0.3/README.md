# argparse-schema [![Build Status](https://travis-ci.com/FebruaryBreeze/argparse-schema.svg?branch=master)](https://travis-ci.com/FebruaryBreeze/argparse-schema) [![codecov](https://codecov.io/gh/FebruaryBreeze/argparse-schema/branch/master/graph/badge.svg)](https://codecov.io/gh/FebruaryBreeze/argparse-schema) [![PyPI version](https://badge.fury.io/py/argparse-schema.svg)](https://pypi.org/project/argparse-schema/)

Parse Argument with JSON Schema.

## Installation

Need Python 3.6+.

```bash
pip install argparse-schema
```

## Usage

[Schema](./tests/argument_config.json):

```json
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "title": "argument_config",
  "description": "Arg-parse Schema UnitTest",
  "type": "object",
  "properties": {
    "config": {
      "type": "string"
    },
    "resume": {
      "type": "boolean"
    },
    "scale": {
      "type": "number",
      "default": 1.0
    }
  },
  "required": [
    "config"
  ]
}
```

Python Code:

```python
# demo.py
import argparse_schema

print(argparse_schema.parse(schema='./tests/argument_config.json'))
```

Run with arguments:

```bash
python3 demo.py --config /path/to/config.py
#> {'config': '/path/to/config.py', 'resume': False, 'scale': 1.0}
```

CLI:

```bash
argparse-schema --schema_path tests/argument_config.json
#> Show help for [tests/argument_config.json]:
#> usage: argparse-schema [-h] --config CONFIG [--resume] [--scale SCALE]
#>
#> Arg-parse Schema UnitTest
#>
#> optional arguments:
#>   -h, --help       show this help message and exit
#>   --config CONFIG  path of config file
#>   --resume         resume from checkpoint or not
#>   --scale SCALE    scale of image
```
