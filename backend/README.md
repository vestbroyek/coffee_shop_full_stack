# Coffee Shop Backend

## Getting Started

### Installing Dependencies
#### PIP Dependencies

Install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.