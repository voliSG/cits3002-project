# QB Server

## How to build the QB

```sh
make
```

## Running the QB server

To run a Python QB:

```sh
make run ARGS="8001 python"
```

To run a C QB:

```sh
make run ARGS="8002 c"
```

- You could change the ports from 8001 or 8002 to whatever, so if you choose to do so, make sure to change them in the TM server's `config.py` file in the app folder too.
  