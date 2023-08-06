# servussimplifytext
*Python3 module to simplify text removing unnecesary symbols.*

## Installation
### Install with pip
```
pip3 install -U servussimplifytext
```

## Usage
```
In [1]: import servussimplifytext

In [2]: servussimplifytext.simplify_text("Hola. á")
Out[2]: 'Hola.'

In [3]: servussimplifytext.simplify_text_no_symbols("Hola. á")
Out[3]: 'Hola'
```
