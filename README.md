# BioUtils

This repo contains various bioinformatics utilities.
It is currently under development.

To use it I have built a CLI, here is a quickstart:
```shell
git clone https://github.com/Egeyae/BioUtils
cd BioUtils
python3 -m virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 cli.py -h
```

General usage is: `python3 cli.py <tool> [tool options]`


### Installation

Here we detail how to install the tool as a system-wide tool on Linux.

The install.sh file take care of the virtualenv + requirements installation too.
```shell
sudo ./install.sh
```
sudo is required to create a wrapper in /usr/local/bin/
