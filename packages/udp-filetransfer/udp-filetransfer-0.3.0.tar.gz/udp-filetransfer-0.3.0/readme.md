# UDP Filetransfer
Fast file transfer over UDP Broadcast.

## Install (CLI)
### From PyPI
```bash
pip install udp-filetransfer
```
### From Git
```bash
git clone https://gitlab.com/Trickster-Animations/udp-filetransfer.git
cd udp-filetransfer
poetry || pip install poetry
poetry install
```
Now, you can use it through poetry:  
`poetry run python -m udp_filetransfer`  
To use it from system python, do:
```bash
poetry build
cd dist
pip3 install *.whl
```
Now, you can use it by running:  
`python3 -m udp_filetransfer`

## Usage (CLI)
To send a file:
```
python3 -m udp_filetransfer send [filepath]
```
To receive a file:
```
python3 -m udp_filetransfer receive
```
Note: The receiver has to be started first. 

## Install (Dependency)
Just add the `udp-filetransfer` package, like with any other dependency.

## Usage (Dependency)
```py
# receive.py
import udp_filetransfer
output = udp_filetransfer.receive()
print(output)
```
```py
# send.py
from sys import argv
import udp_filetransfer
udp_filetransfer.send(argv[1])
```
Note: Just like with CLI, the receiver needs to be started first. Otherwise the sender will hang indefinitely. 


## Credits
Package maintained by Trickster Animations