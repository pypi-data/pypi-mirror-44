# flask-compressed

A simple libary to send request and get response with gzip, zlib encodings.

## Usage

### Installation

```shell
pip install flask-compressed
```

### Codes

```python
from flask import Flask
from flask_compressed import FlaskCompressed

flask_app = Flask(__name__)
FlaskCompressed(flask_app)

@flask_app.route('/')
def echo():
    return g.body
```
