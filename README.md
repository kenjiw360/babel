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

Edit the game and server settings in `config.yml`.

```yml
# Server settings
server:
  host: 0.0.0.0
  port: 8080
  book_len: 5

# Client settings
client:
  fps: 60
  camera_sensitivity: 3
  connection:
    host: localhost
    port: 8080
```