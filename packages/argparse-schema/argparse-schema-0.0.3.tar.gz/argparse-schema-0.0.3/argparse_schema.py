import argparse
import json
from pathlib import Path
from typing import Optional, Sequence, Union


def parse(schema: Union[dict, str, Path], args: Optional[Sequence[str]] = None) -> dict:
    if not isinstance(schema, dict):
        with open(str(schema)) as f:
            schema: dict = json.load(f)
    assert 'type' in schema and schema['type'] == 'object'
    assert 'properties' in schema

    required_set = set(schema.get('required', []))

    type_map = {
        'string': str,
        'integer': int,
        'number': float,
        'boolean': bool
    }

    parser = argparse.ArgumentParser(description=schema.get('description'))
    for name, value in schema.get('properties', {}).items():
        assert isinstance(value, dict)

        type = type_map[value.get('type')]
        default = value.get('default')
        description = value.get('description')
        required = name in required_set

        if type is bool:
            parser.add_argument(f'--{name}', action='store_true', help=description, required=required)
        else:
            parser.add_argument(f'--{name}', type=type, default=default, help=description, required=required)

    return vars(parser.parse_args(args=args))


def main():  # pragma: no cover
    schema_path = parse(schema={
        'type': 'object',
        'properties': {
            'schema_path': {
                'type': 'string',
                'description': 'argparse schema file path'
            }
        },
        'required': [
            'schema_path'
        ],
    })['schema_path']

    print(f'Show help for schema file [{schema_path}]:')
    parse(schema=schema_path, args=['-h'])


if __name__ == '__main__':  # pragma: no cover
    main()
