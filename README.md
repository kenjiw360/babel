# Library of Babel

Sort the Library of Babel with friends!

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

Edit the game and server settings in `constants.py`.

```python
# Sever connectivity
HOST = "localhost"
PORT = 8080

# Server settings
BOOK_LEN = 5

# Game settings
FPS = 165
```