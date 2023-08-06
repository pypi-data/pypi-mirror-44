import h5py
import argparse


def h5_structure(h5_group, show_attrs=True, show_data=False):
    """
    Recursively print the tree structure of an HDF5 file or group
    """
    sep = '| '

    def print_group_structure(h5_group, str_prefix):
        for name, group in h5_group.items():
            if isinstance(group, h5py.Dataset):
                if show_data:
                    print(str_prefix + name + ": " + str(group[...]))
                else:
                    print(str_prefix + str(group))
                if show_attrs:
                    print_attributes(group, str_prefix + sep)
            else:
                print(str_prefix + name)
                print_group_structure(group, str_prefix+sep)

    def print_attributes(dset, str_prefix):
        for k, v in dset.attrs.items():
            print(str_prefix, k, ':', v)

    print_group_structure(h5_group, '')


def print_h5(h5_filename, section=None, show_attrs=False, show_data=False):
    """
    API for printing structure/contents of HDF5 file

    Parameters
    ----------
    h5_filename : str
        Name/location of the file to show
    section : str, optional
        Group or dataset of the file to show (the default is None, which shows
        the contents of the whole file)
    show_attrs : bool, optional
        Whether to show dataset attributes (the default is False, which only
        shows dataset contents)
    show_data : bool, optional
        Whether to show the contents of the dataset. *Warning: this can blow up
        with large datasets* (the default is False, which only shows the name
        and size of the dataset)

    """

    h5_file = h5py.File(h5_filename, 'r')
    if section is not None:
        h5_in = h5_file[section]
    else:
        h5_in = h5_file
    h5_structure(h5_in, show_attrs, show_data)
    h5_file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Show the structure and content of an HDF5 file")
    parser.add_argument(
        'filename', type=str,
        help='HDF5 file to show'
    )
    parser.add_argument(
        '--section', type=str,
        help='Show only the contents of this group/dataset')

    parser.add_argument(
        '--show_attrs', dest='show_attrs', action='store_true',
        help='Show attributes of HDF5 datasets?')
    parser.set_defaults(show_attrs=False)
    parser.add_argument(
        '--show_data', dest='show_data', action='store_true',
        help='Show contents of HDF5 datasets? (Otherwise overview only)')
    parser.set_defaults(show_data=False)

    args = parser.parse_args()

    h5_file = h5py.File(args.filename, 'r')
    if args.section is not None:
        h5_in = h5_file[args.section]
    else:
        h5_in = h5_file
    h5_structure(h5_in, show_attrs=args.show_attrs, show_data=args.show_data)
    h5_file.close()
