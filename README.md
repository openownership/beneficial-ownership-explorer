# Beneficial Ownership Explorer

Web application for dynamic querying of APIs to explorer beneficial ownership data

## Local Installation

Clone this repository. Create virtual environment e.g.:

```
python3 -m venv .
```

Install dependencies:

```
pip install -r requirements.txt
```

## Configuration

Copy example configuration file (`boexplorer.toml.example`) to `boexplorer.toml` and edit.
Credentials are needed for several of the sources that are queried, and these will need to
be obtained by registering with the relevant organisations. Details can be found in the 
`boexplorer.toml.example` file and each section will need to be filled in with valid credentials, 
e.g.:

```
[sources.estonia_rik.credentials]
user = "<username>"
pass = "<password>"
```

## Running

Run application:

```
reflex run
```

Navigate in browser to local address the application prints out.

