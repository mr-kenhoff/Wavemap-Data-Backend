import os.path
import h5py
import numpy as np

# Local modules
from sample import Sample


class Dataset:

    FILE_EXTENSION = ".hdf"

    def __init__(self, directory, name, write_access=True):

        self.__directory = directory
        self.__name = name

        # Open HDF5 file
        self.__path = os.path.join(directory, name + Dataset.FILE_EXTENSION)
        self.__file = h5py.File(self.__path, "a")

        # Initialize Device subclass
        self.__device = Dataset.Device(self.__file)

        # Initialize Samples subclass
        self.__samples = Dataset.Samples(self.__file)


    class Device:
        def __init__(self, file):
            self.__file = file

        @property
        def name(self):
            if "device_name" in self.__file.attrs:
                return self.__file.attrs["device_name"]
            else:
                return None

        @name.setter
        def name(self, name):
            if isinstance(name, str):
                self.__file.attrs["device_name"] = name
            else:
                raise Exception("Device name must be a string")

        @property
        def version(self):
            if "device_version" in self.__file.attrs:
                return self.__file.attrs["device_version"]
            else:
                return None

        @version.setter
        def version(self, version):
            if isinstance(version, str):
                self.__file.attrs["device_version"] = version
            else:
                raise Exception("Device version must be a string")

    class Samples:
        def __init__(self, file):
            self.__file = file

        def __len__(self):
            return 8

        def __getitem__(self, i):
            print(i)

        def append(self, sample):
            if not isinstance(sample, Sample):
                raise Exception("Can only append instances of type 'Sample' to dataset")


    @property
    def name(self):
        return self.__name

    @property
    def device(self):
        return self.__device

    @property
    def samples(self):
        return self.__samples

    def close(self):
        self.__file.flush()
        self.__file.close()


if __name__ == '__main__':
    from spectrum import Spectrum
    from gps import GPS

    dataset = Dataset("./", "Neustadt")

    sample = Sample(
        time     = np.datetime64("now"),
        spectrum = Spectrum([],[]),
        gps      = GPS(8.3, 2.5)
    )

    dataset.close()
