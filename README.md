# Library of Babel

## Environment Setup

Create and activate the Conda environment from `environment.yml`:

```bash
conda env create -f environment.yml
conda activate babel
```

## Running the project

### 1. Start the server

```bash
python -m server
```

### 2. Start the client

```bash
python -m client
```

## Editing settings

Edit the connection settings in `constants.py`.

```python
BOOK_LEN=5
HOST = "localhost"
PORT = 8080
```