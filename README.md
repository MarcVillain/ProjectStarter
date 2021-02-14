ProjectStarter
===

![ProjectStarter](logo.png?raw=true "ProjectStarter logo")

Get straight to coding by automagically creating a project folder with little to no effort.

# Setup

```shell script
pip3 install virtualenv
python3 -m venv venv
source ./venv/bin/activate
```

# Install

```shell script
pip install .
```

# Run

```shell script
project --help
```

or

```shell script
python -m project --help
```

# Example
```shell script
project start bash my_project -o git cli license:mit
```

# Debug

```shell script
pip install -e .
project --help
```

# Test

```shell script
pip install -r requirements-dev.txt
pytest tests
```

# Troubleshooting

* error: invalid command 'bdist_wheel'
  ```
  pip install wheel
  ```

# Templates

The templates are located in `projectstarter/templates`.

Look at [docs/TEMPLATE.md](docs/TEMPLATE.md) for more information.

# Authors

* Marc Villain (marc.villain@epita.fr)

