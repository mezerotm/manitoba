# manitoba


a python script to install crypto miners on a lot servers at once

## Table of Contents

- [Requirments](#Requirments)
- [Install](#install)
- [Usage](#usage)
- [Maintainers](#maintainers)
- [Contributing](#contributing)
- [License](#license)

## Requirments

- [poetry](https://github.com/python-poetry/poetry)

## Install

```
poetry install
```

## Usage
to run manitoba
```
poetry run python manitoba/main.py
```
### snake-handler
a snake handler is just a way to access servers directly using ssh, the file is simply a JSON Array

```json
[
  {
    "hostname": "127.0.0.1",
    "username": "admin",
    "password": "admin",
    "key_filename: ""
  },
  {
    "hostname": "127.0.0.1",
    "username": "",
    "password": "",
    "key_filename: "/home/user/.ssh/rsa_pub"
  }
]
```

## Maintainers

[@mezerotm](https://github.com/mezerotm)

## Contributing

PRs accepted.

Small note: If editing the README, please conform to the [standard-readme](https://github.com/RichardLitt/standard-readme) specification.

## License

MIT © 2020 Carlos Rincon
