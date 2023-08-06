"""
Mapstery Map Class File
"""
import json
import struct
import numpy as np
import gdal
#import gdalconst
from PIL import Image

class Map():
    """
    Mapstery Map Class

    Arguments
    ---------
    dataset : optional, gdal.Dataset
        pass
    rows : optional, int
        pass
    cols : optional, int
        pass

    Attributes
    ----------
    datatype : gdal.GDT_UInt32
        pass

    dataset : gdal.Dataset
        pass

    Methods
    -------

    """
    def __init__(self, dataset=None, cols=500, rows=500):
        self._dataset = None if dataset is None else dataset
        #self._default_datatype = gdal.GDT_UInt32
        self._default_datatype = gdal.GDT_Float32
        self._default_driver = "MEM"
        self._default_rows = rows
        self._default_cols = cols

    @property
    def datatype(self):
        """ datatype attribute getter """
        return self._default_datatype

    @datatype.setter
    def datatype(self, new_default_datatype):
        """ datatype attribute setter """
        self._default_datatype = new_default_datatype
        return self._default_datatype

    @property
    def dataset(self):
        """ dataset attribute getter """
        return self._dataset

    @dataset.setter
    def dataset(self, data_path):
        """
        Set the internal dataset to an existing one or create one by reading a
        file from data_path if that is a string. This file could be a JSON
        file with a dictionnary containing the different layers

        Parameters
        ----------
        data_path : GDAL dataset object OR GDAL filename OR JSON filename
            Path to file or dataset to load to Map class.

        """
        # Setting a dataset directly, if applicable
        if isinstance(data_path, gdal.Dataset):
            self.__load_gdal_dataset(data_path)

        elif isinstance(data_path, str):
            json_input = False
            if len(data_path) > 5 and data_path[-5:] == ".json":
                json_input = True

            # --- Reading a file path of an image
            if json_input is False:
                self.__load_gdal_file(data_path)
            else:
                self.__load_json(data_path)

        else:
            raise TypeError("Input is neither a gdal.Dataset or a file path.")

    @property
    def total_bands(self):
        """ total_bands attribute getter """
        if self._dataset is None:
            return None

        return self._dataset.RasterCount

    def __load_json(self, data_path):
        """ Load a dataset using gdal by a json file. """
        print("Loading multi-layer information from a JSON file.")
        json_file = open(data_path)
        input_bands = json.load(json_file)

        for key in input_bands:
            if not isinstance(input_bands[key], str):
                continue

            tmp_ds = gdal.Open(input_bands[key])
            if tmp_ds is None:
                print("(EE) File " + input_bands[key] + " count not be loaded.")
                continue
            elif self._dataset is None:
                self._default_cols = tmp_ds.RasterXSize
                self._default_rows = tmp_ds.RasterYSize

            if tmp_ds.RasterCount == 1:
                self.add_band(tmp_ds.GetRasterBand(1), key,
                              band_info=input_bands[key])
            else:
                bands_indexes = [i for i in range(tmp_ds.RasterCount)]
                for k in bands_indexes:
                    self.add_band(tmp_ds.GetRasterBand(k), key + "_" + str(k),
                                  band_info=input_bands[key])

        return self._dataset

    def __load_gdal_file(self, data_path):
        """ Load a dataset using gdal by file path. """
        self._dataset = gdal.Open(data_path)
        return self._dataset

    def __load_gdal_dataset(self, data_path):
        """ Load an already existing gdal dataset. """
        self._dataset = data_path
        return self._dataset

    def add_band(self, data_array, band_name, new_band=True, band_info=""):
        """
        Add one band (channel or layer) to the dataset

        Parameters
        ----------
        data_array : GDAL band or np.ndarray
            pass
        band_name : str
            Name to be set in the description of the band.
        new_band : bool (Default: True)
            Option to create new band or modify existing one.
        band_info : str
            Information that may be applied to the band.

        Returns
        -------
        True or False : bool
            Success or failure of band creation.

        """
        if isinstance(data_array, gdal.Band):
            data_array = data_array.ReadAsArray()

        # Create a new dataset if necessary
        if self._dataset is None:
            if isinstance(data_array, np.ndarray):
                print("This is happening")
                print(data_array.shape)
                self._default_cols = data_array.shape[1]
                self._default_rows = data_array.shape[0]

            print("Creating a {} file of size (cols, rows) = ({}, {})".format(
                self._default_driver,
                self._default_cols,
                self._default_rows))

            gdal_driver = gdal.GetDriverByName(self._default_driver)
            self._dataset = gdal_driver.Create(
                "/tmp/mapstery.mem", self._default_cols, self._default_rows,
                0, self._default_datatype)

        # Adding or getting the new band with its meta data
        current_band = None
        if new_band:
            b_mat = self._dataset.AddBand(self._default_datatype)
            print(" ------------- Creating a new band: " +
                  band_name + " " + str(self._dataset.RasterCount))
            current_band = self._dataset.GetRasterBand(self._dataset.RasterCount)

        else:
            print(" ------------- Overwriting an existing band: " +
                  band_name + " " + str(self._dataset.RasterCount))
            current_band = self._dataset.GetLayerByName(band_name)

        # --- Setting band information
        if current_band is None:
            return False

        current_band.SetDescription(band_name)
        current_band.SetMetadataItem("NAME", band_name)
        if band_info != "":
            current_band.SetMetadataItem("INFO", band_info)

        # Writing the band
        # TODO: improvement, copy on band input
        current_band.WriteArray(data_array)
        return True

    def get_band_info(self, band_index):
        """ Return band info for a specific band index within dataset. """
        return self._dataset.GetRasterBand(band_index).GetMetadataItem("INFO")

    def transform_band(self, band_name_or_index, transform_func):
        """
        Output a numpy array of the transformed

        Parameters
        ----------
        band_name_or_index : str
            Index of name of a band
        transform_func : function
            A function that take as input a 2D numpy array and output same
            sized numpy array.

        """
        b_mat = self.get_band(band_name_or_index)
        return transform_func(b_mat.ReadAsArray())

    def get_band(self, band_name_or_index):
        """
        Returns the band named band_name from the internal dataset.

        Parameters
        ----------
        band_name_or_index: str or int
            Name of the band to return.

        Returns
        -------
        band : np.ndarray
            The desired band to be returned.

        """
        band = None
        if isinstance(band_name_or_index, int):
            band = self.get_band_by_index(band_name_or_index)

        elif isinstance(band_name_or_index, str):
            band = self.get_band_by_name(band_name_or_index)

        else:
            raise ValueError("Arguments is not an int or str.")

        return band

    def get_band_by_index(self, band_index):
        """ Returns the band named band_name from the internal dataset. """
        if self._dataset is None:
            return None

        return self._dataset.GetRasterBand(band_index)

    def get_band_by_name(self, band_name):
        """ Returns the band named band_name from the internal dataset. """
        if self._dataset is None:
            return None

        for i in range(self._dataset.RasterCount):
            if self._dataset.GetRasterBand(i + 1).GetMetadataItem("NAME") == band_name:
                return self._dataset.GetRasterBand(i + 1)

        return None

    def get_pixel(self, coord, bands=None):
        """
        Return a vector of a pixel values across the selected bands.

        Parameters
        ----------
        coord : tuple or np.ndarray
            The x and y positions.
        bands : list
            pass

        Returns
        -------
        pixel_vector : np.ndparray
            Vector containing the pixel values.

        """
        pixel_vector = []

        if self._dataset is None:
            return np.array(pixel_vector)

        if bands is None:
            bands = [k+1 for k in range(self._dataset.RasterCount)]

        for i in bands:
            band = self.get_band(i)
            if band is None:
                # considering zero if the band does not exist
                pixel_vector.append(0)

            else:
                pixel_value = 0.0
                try:
                    pixel_value = band.ReadRaster(
                        xoff=coord[0], yoff=coord[1], xsize=1, ysize=1,
                        buf_xsize=1, buf_ysize=1,
                        buf_type=self._default_datatype)
                    # type(pixel_value) is binary string (bytes)
                    pixel_value = struct.unpack('f', pixel_value)[0]

                except Exception as eee:
                    pixel_value = 0.0
                    print(eee)

                pixel_vector.append(pixel_value)

        return np.array(pixel_vector)

    def save(self, output_file, driver="GTiff", options=None):
        """
        Save the in Memory dataset into a GTiff or any other indicated driver.

        Parameters
        ----------
        output_file : str
            The file name for the output GeoTiff file.
        driver : str (default: "GTiff")
            Output file driver passed to gdal.
        options : list of str (default: None)
            Passable options to gdal for saving the output file.

        """

        if options is None:
            options = ["COMPRESS=LZMA", "NUM_THREADS=8"]

        elif isinstance(options, list):
            for i in options:
                if not isinstance(i, str):
                    raise TypeError("options arg should be a list of strings!")

        else:
            raise TypeError("options arg should be a list of strings!")

        dst_ds = gdal.GetDriverByName(driver).CreateCopy(output_file,
                                                         self._dataset, 0,
                                                         options=options)
        dst_ds.FlushCache()
        del dst_ds

    def save_band(self, band_name, output_file, dynamics=255.0):
        """
        Extract a band by name and save it into an array

        Parameters
        ----------
        band_name : int or str
            Band to extract
        output_file:
            File path of the output to be written, must contain an image
            extension.
        dynamics : float (default: 255.0)
             Pixels will take values from 0 to this argument value.

        Returns
        -------
        True or False Bool
            Returns bool corresponding to success or failure of save.

        """
        band = self.get_band(band_name)

        if band is None:
            print("Band not found: {}".format(band_name))
            return False

        arr = band.ReadAsArray()

        arr_min = np.min(arr)
        arr = (arr-arr_min) * dynamics / (np.max(arr) - arr_min)
        raster = Image.fromarray(arr.astype(np.uint8))
        raster.save(output_file)
        return True
