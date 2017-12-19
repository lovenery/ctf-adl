# CTF - Advanced Defense Lab

## Env

- Linux
- Python 2.7

## Snippets

```
git clone git@github.com:lovenery/ctf-adl.git
cd ctf-adl/
virtualenv venv # py2
virtualenv --python=python2.7 venv # py3
. venv/bin/activate
pip install -r requirements.txt

export LD_PRELOAD=
export LD_PRELOAD=./libc.so.6
```
