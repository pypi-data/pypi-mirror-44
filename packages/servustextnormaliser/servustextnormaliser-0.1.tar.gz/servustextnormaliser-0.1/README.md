# servustextnormaliser
*Python3 module to normalise text.*

## Installation
### Install with pip
```
pip3 install -U servustextnormaliser
```

## Usage
```
In [1]: import servustextnormaliser

In [2]: text_normaliser = servustextnormaliser.TextNormaliser()

In [3]: text_normaliser.normalise("Hello, ¡I'll be normalised!")

Out[3]: 'Hello I will be normalised'
```
