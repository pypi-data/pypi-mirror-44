# Show H5

A simple python-based command-line interface for previewing the contents of HDF5 files.

[PyPi](https://pypi.org/project/show_h5/)

## Install

`pip install show_h5`

## Command line usage

Basic use: `python3 show_h5.py FILENAME`

View usage: `python3 show_h5.py -h`

The following flags are also provided:

- `--section SECTION`: View only the contents of the HDF5 group/dataset within the file
- `--show_attrs`: Show the attributes of the datasets (if not used, defaults to not showing attributes)
- `--show_data`: Show the contents of the datasets (if not used, defaults to only showing the name and dimensions). *Warning: this may blow up with large datasets.*

## API usage

```Python
from show_h5 import print_h5
print_h5(h5_filename, section=None, show_attrs=False, show_data=False)
```

### Parameters

`h5_filename`: (str) Name/location of the file to show

`section`: (str, optional) Group or dataset of the file to show (the default is None, which shows the contents of the whole file)

`show_attrs`: (bool, optional) Whether to show dataset attributes (the default is False, which only shows dataset contents)

`show_data`: (bool, optional) Whether to show the contents of the dataset. *Warning: this can blow up with large datasets* (the default is False, which only shows the name and size of the dataset)