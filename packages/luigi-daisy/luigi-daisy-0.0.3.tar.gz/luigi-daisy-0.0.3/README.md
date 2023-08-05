# daisy

Thin wrapper of [luigi](https://github.com/spotify/luigi) for utility.

# Features

## Formatted local targets

Classes inheriting `daisy.FormattedLocalTargetBase` is provided
for dumping and loading objects by one-liner.

``` python
import daisy
import pandas as pd

df = pd.DataFrame({"a": [1,2,3], "b": [4,5,6]})
df
# =>
#    a  b
# 0  1  4
# 1  2  5
# 2  3  6

targ = daisy.CsvTarget("./output.csv")

# dumping
targ.dump(df)

# loading
df2 = targ.load()

df2
# =>
#    a  b
# 0  1  4
# 1  2  5
# 2  3  6

# `daisy.FormattedLocalTargetBase` also inherits `luigi.LocalTaget`
# so that original api is also enabled.
with targ.open("r") as fd:
    s = fd.read()
```

## Default output for task

`daisy.Task` inherits `luigi.Task` and provides default `output` features.

By setting file extension via `ext` attribute,
daisy automatically configure corresponding `FormattedLocalTarget` with default file name.


### Single output

``` python
class TaskA(daisy.Task):
    param1 = daisy.Parameter()
    ext = "csv"
```

is equivalent to:

``` python
class TaskA(luigi.Task):
    param1 = luigi.Parameter()

    def output(self):
        return daisy.CsvTarget("./data/TaskA/TaskA(param1={}).csv".format(self.param1))
```


### Multiple outputs

``` python
class TaskA(daisy.Task):
    param1 = daisy.Parameter()

    ext = {
        "vectors": "npy",
        "metadata": "json"
    }
```

is equivalent to:

``` python
class TaskA(luigi.Task):
    param1 = luigi.Parameter()

    def output(self):
        return {
            "vectors": daisy.NpyTarget("./data/TaskA/TaskA(param1={}).npy".format(self.param1)),
            "metadata": daisy.JsonTarget("./data/TaskA/TaskA(param1={}).json".format(self.param1))
            }
```

Available extension and file types are as follows:

| Target class | Object type | extension |
| --- | --- | --- |
| `CsvTarget` | `pandas.DataFrame` | `csv` |
| `NpyTarget` | `numpy.ndarray` | `npy` |
| `JsonTarget` | `dict` | `json` |
| `PickleTarget` | `object` | `pkl` `pickle` |
| `FeatherTarget` | `pandas.DataFrame` | `feather` |

view [source code](./daisy/formatted_target.py) for detail.


## Configuration

For configuration, edit `[daisy]` section of `luigi.cfg`.

``` INI
[daisy]

# default output directory
data_dir = luigi.Parameter("./data")
```


