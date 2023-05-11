# Test Manager

Simple web server from scratch written in python

## Setup (Development)

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

## Architecture

### Routing & Endpoints

Routing can be configured in `app/routes.py`

API routes should be prefixed with `/api` and are defined in `app/api`
Page routes are defined in `app/pages`, and HTML templates are by default in `app/pages/templates`
Configure the api and template folder name in `app/config.py`

### Database

The database uses Python's `pickle` module to serialise and deserialise data to and from a file
Find the pickles in `app/pickles`, along with some scripts to seed them

### Server

When a request is made, the server will attempt to find a matching route in `app/routes.py` and execute the corresponding function
This function will return a `Response` object, which contains the status code, additional headers, and content of the response
The server will then set the response with this information and send it back to the client
