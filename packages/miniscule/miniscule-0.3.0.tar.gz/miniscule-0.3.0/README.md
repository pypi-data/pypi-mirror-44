# miniscule

Miniscule library for flexible YAML configuration files, inspired by
[Aero](https://github.com/juxt/aero).

## Example

Create a file `config.yaml` with the following contents:

```yaml
server:
  host: !or [!env HOST, localhost]
  port: !or [!env PORT, 8000]
debug: !env DEBUG
database:
  name: my_database
  user: my_user
  password: !env DB_PASSWORD
secret: !aws/sm secret
```

Then, in Python:

```python
from miniscule import read_config

config = read_config('config.yaml')
```

Now, `config` holds a dictionary with the structure of the `config.yaml` file,
in which the tagged fields have been replaced.
