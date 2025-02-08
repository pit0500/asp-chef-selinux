# ASP Chef SELinux

This project processes SELinux policy rules from a file (`rules.txt`) and generates Answer Set Programming (ASP) code. The main script (`generate_facts.py`) performs the following steps:

1. **Reads policy rules:** Opens `rules.txt` and reads its content.
2. **Parses policies:** Uses a regular expression to extract policy components (subjects, object type, class type, permissions, and optional parameters) from the rules.
3. **Generates ASP code:** Converts the parsed policies into ASP facts with a specific format.
4. **Opens a browser:** Constructs a URL using the generated ASP facts (via the `pack_asp_chef_url` function from the `dumbo_asp.queries` module) and opens the URL in the default web browser.

## Prerequisites

Before running the project, ensure you have the following installed:

- **Python 3.11** or later versions.
- **Required Python packages:**
  - `dumbo_asp` (which provides ASP utilities and the `pack_asp_chef_url` function)
  - `rich` (for enhanced terminal output)
  
These dependencies can be installed via [Poetry](https://python-poetry.org/).

### Using Poetry

Simply run:

```bash
poetry install
```

If you don't have Poetry installed, you can install it via pipx which is the simplest method:

```bash
pipx install poetry
```

then you can run the above command.

## Usage

After installing all the depenencies via Poetry, you can run the project by executing the following command:

```bash
cd asp_chef_selinux
poetry run python generate_facts.py
```

## Changing the Input File
If you want to use a different file as input, you can change the `input_file` variable in the `generate_facts.py` script or you can simply replace the `rules.txt`.

The file was populated via the following command on a SELinux-enabled system:

```bash
sudo seinfo -a > file.txt
```

## Final Notes

We recommend using Firefox as the default browser for the project. If you want to use a different browser please be aware that the url length could exceed the maximum length supported by some browsers.
