# Test Manager

Simple web server from scratch written in python

## Setup

### Initialise the Virtual Environment

```bash
python3 -m venv venv
```

### Activate the Virtual Environment

On Unix:

```bash
source venv/bin/activate
```

On Windows:

```bash
.\venv\Scripts\activate.bat # CMD
.\venv\Scripts\Activate.ps1 # Powershell
```

### Install Dependencies
  
```bash
pip install -r requirements.txt
```

## Run the Server

```bash
python main.py
```

## Development

To test template generation:

```bash
python -m tests.test_template
```
