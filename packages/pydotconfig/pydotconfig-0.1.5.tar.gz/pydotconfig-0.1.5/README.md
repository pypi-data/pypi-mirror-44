DotConfig
---------

Super simple python module for parsing structured config files with overrides

Install via:

```
pip install pydotconfig
```

## Example

```
import dotconfig
import os

# Try using these to override the config file values
# For example: export DCFG_BAR='Green Eggs'
ENVVARS = {
    'foo': 'DCFG_FOO',
    'bar': 'DCFG_BAR'
}

DEFAULTS = {
    'foo': 'spam',
    'bar': 'eggs'
}

if __name__ == '__main__':
    cfg = dotconfig.Config('example', 'settings',
                        envvars=ENVVARS, defaults=DEFAULTS,
                        template_file='template.yaml')

    print(cfg.to_dict())
```
