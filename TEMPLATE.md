ProjectStarter : Template
===

The templates are located in `project/templates` and are based on the [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/) templating format.

# Add a template

To add a template, you need to add a folder in the `project/templates` folder. The name of the folder will correspond to the name of the template.

Then you should at least have a `metadata.yml` file, with at least a `description` field.

# metadata.yml

This file is the one that describes all the template options and behaviors.

Fields:
* `description` : short description of the template
* `requirements [unused]` : required binaries on the system
* `commands` : commands to run after the folder structure is created
* `files` : files to copy to the output project directory, relative to the template root directory
* `options` : list of custom options
* `options.name` : option called `name` that can be used in the command line
* `options.name.description` : small description of the option
* `options.name.files` : files to copy to the output project directory when the option is set
* `options.name.commands` : list of commands to run when the option is set (for the commands to be run, they actually need to be added to the `commands` field with value `"{{ options.name.commands }}`)
* `include_templates` : no matter where placed in the metadata, this field will be expanded with the matching template's metadata fields. If an expanded key already exists, it will not replace single value fields but it will append new values in lists.

Fields expansion is available as the file is first loaded as a yaml file, then parsed like a normal [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/) file, using the loaded data.

See [Jinja2 data section](#jinja2-data) for more details on the custom values available.

Example:

```yaml
description: "Simple description"
requirements:
  - bash
commands:
  - "echo Foo"
  - "{{ options.foo.commands }}"
files:
  - "{{ project.slug }}.txt.j2"
options:
  foo:
    description: "simple description"
    files:
      - "file.txt.j2"
    commands:
      - "echo Bar"
  bar:
    include_templates:
      - template_name
```

# Files

Every file must have a `.j2` extension, except for `metadata.yml`.

You can use any of the [Jinja2 data section](#jinja2-data) values in a file name.

# Directories

You can use any of the [Jinja2 data section](#jinja2-data) values in a file name.

# Jinja2 data

When parsing any [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/) file content, file name or directory name, some data is passed to it.

The data consists of the fields loaded from the `metadata.yml` file and of the following:
* `project.path` : path to the project output directory
* `project.name` : name of the project
* `project.slug` : slug of the project

You can also use the following helpers (usage: `{{ helper(arg1, arg2, ...) }}`):
* `which` : run the `which` command on the given binary name to find its path in the current environment