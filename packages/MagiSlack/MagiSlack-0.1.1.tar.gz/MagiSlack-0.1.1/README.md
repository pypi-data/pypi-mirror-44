# MagiSlack
MagiSlack is a fast, easy library for make command-respond style chat bot.

## Installation
- pip install MagiSlack

## Usage
```python
from MagiSlack.io import MagiIO
from MagiSlack.module import MagiModule

def hello_world_callback(*args, **kwargs):
    name = args[0]
    return f'Hello, {kwargs['display_name']}!'
    
if __name__ == '__main__':
    module = MagiModule.MagiModule('SLACK_API_KEY_HERE')
    io = MagiIO.MagiIO(module)
    io.set_callback_func('hello', hello_world_callback)
    
    io.start()
```

## License
MIT license
