"""
General and more specific filters.

Filters return unit scaled images. They have to be converted to whatever to
your custom dynamics using move_dynamics()

"""
from scipy import signal
from scipy.ndimage.filters import gaussian_filter
import numpy as np


def move_dynamics(matrix, target_min_bound=0.0, target_max_bound=255.0,
                  init_min_bound=0.0, init_max_bound=255.0, convert_uint=False,
                  init_to_content=False):
    """
    Transform pixel dynamics to another scale given by the following bounds
    [target_min_bound, target_max_bound]

    Parameters
    ----------
    matrix : np.ndarray
        Something
    target_min_bound : float
        Lower bound of the new scale
    target_max_bound : float
        Upper bound of the new scale
    convert_uint : bool
        True if you want unsigned integers in order to create images.

    """
    # Fix in case the input as minimum values lower than user definitions
    # in init_min_bound
    smin = np.min(matrix)
    if smin < init_min_bound:
        init_min_bound = smin

    # Fix in case the input as maximum values greater than user definitions
    # in init_max_bound
    smax = np.max(matrix)
    if smax > init_max_bound:
        init_max_bound = smax

    if init_to_content is True:
        init_min_bound = smin
        init_max_bound = smax

    # Inverting in case of bad usage
    if target_max_bound < target_min_bound:
        tmp = target_min_bound
        target_min_bound = target_max_bound
        target_max_bound = tmp

    dyn_range = target_max_bound - target_min_bound

    matrix = ((matrix - init_min_bound) / (init_max_bound - init_min_bound)) \
        * dyn_range + target_min_bound

    if convert_uint is True:
        return matrix.astype(np.uint8)

    return matrix


def isogradient(gdal_band, blur_radius=7):
    """
    Transform a raster band of a GDAL dataset containing DEM information
    into a slope map as a numpy array.

    Parameters
    ----------
    gdal_band : GDAL dataset band (output of ds.GetRasterBand(i))
        GDAL band containing DEM information.
    blur_radius : int
        Blurring radius in pixels, to blur out compression effects and
        eventual artifacts. If the radius == 0 then no blur is applied.

    Returns
    -------
    np.ndarray image of the slope map scaled to one.

    """

    k_1 = np.array([[-1, -1, -1],
                    [0, 0, 0],
                    [1, 1, 1]])
    k_2 = np.array([[-1, 0, 1],
                    [-1, 0, 1],
                    [-1, 0, 1]])
    k_3 = np.array([[-1, -1, 0],
                    [-1, 0, 1],
                    [0, 1, 1]])
    k_4 = np.array([[0, -1, -1],
                    [1, 0, -1],
                    [1, 1, 0]])

    arr = gdal_band.ReadAsArray()
    conv = np.abs(signal.convolve2d(arr, k_1, mode="same", boundary="symm"))
    for kernel in [k_2, k_3, k_4]:
        conv += np.abs(signal.convolve2d(arr, kernel, mode="same",
                                         boundary="symm"))

    conv = conv / 4.0

    # Scaling the histogram [0 - 1.0]
    conv = move_dynamics(conv, target_min_bound=0.0, target_max_bound=1.0,
                         init_to_content=True)

    # Blurring artifacts
    if blur_radius > 0:
        conv = gaussian_filter(conv, sigma=blur_radius)
        conv = move_dynamics(conv, target_min_bound=0.0, target_max_bound=1.0,
                             init_to_content=True)

    return conv


def bands_average(mapy, bands, weights=None, stop_at_index=None):
    """
    Mix bands with average.

    Parameters
    ----------
    mapy : Mapstery Map
        Something
    bands : list
        list of bands indexes to mix
    weights : optional, list
        Weights to apply to their respective bands
    stop_at_index : optional, int
        Index of bands to stop the averaging.

    Returns
    -------
    An array of the mix with real values of the weighted average

    Example
    -------
    >>> import mapstery as mp
    >>> shadow_mix = mp.filter.bands_average(M, [k+1 for k in range(168)])

    """
    if weights is None:
        weights = []

    if len(bands) <= 1:
        print("No bands average has been done. Too few bands indicated for the mix.")
        return None

    if weights == [] or weights is None:
        weights = np.ones(len(bands))

    stop_at_index = len(weights)
    if stop_at_index <= 0:
        stop_at_index = len(weights)

    if stop_at_index > len(bands):
        stop_at_index = len(bands)

    print("Integrating band {}".format(bands[0]))
    band_mix = weights[0] * mapy.get_band(int(bands[0])).ReadAsArray()
    print("[+] Integrating band {} weighted {}".format(bands[0], weights[0]))

    w_val = 1
    for k in bands[1:stop_at_index]:
        print("[+] Integrating band {} weighted {}".format(k, weights[w_val]))
        band_mix += weights[w_val] * mapy.get_band(int(k)).ReadAsArray()
        w_val += 1

    band_mix = band_mix / stop_at_index

    return band_mix


def integrate_shadows(mapy, bands, integration_horizon=5, offset=0):
    """
    Integrate shadows over the next bands as they represent the coming
    shadows.

    Parameters
    ----------
    mapy :
        Original dataset containing the sun-angle-computed shadows.
    bands :
        Bands indexes to be associated, in chronological orders.
    integration_horizon :
        How many steps ahead should be considered for shadow integration.
    offset :
        Start from a different index in bands, useful when recalled.

    """
    integrated_list = []

    # Generate weights focusing on the first entries of the polynomial
    # decrease.
    weights = polynomial_decrease(
        np.int(integration_horizon*2), 2, 6)[:integration_horizon]

    # Cycle
    stop = len(bands) - len(weights)
    for start in bands[offset:]:
        bands_subset = []
        if start > stop:
            # Cycle the band subset to the beginning to have same size as
            # weights.
            bands_subset = bands[start:]
            bands_subset = np.append(
                bands_subset, bands[:(len(weights)-len(bands_subset))])

        else:
            # entire slice is consecutive
            bands_subset = bands[start:start+len(weights)]

        new_shadow = bands_average(mapy, bands_subset, weights)
        integrated_list.append(new_shadow)

    return integrated_list


def polynomial_decrease(units, a_power=2.0, b_power=2.0):
    """ Return a polynomial decrease of the form (1-x^a)^b """
    if units < 3:
        units = 3

    x_val = np.linspace(0.0, 1.0, units)
    return np.power(1 - np.power(x_val, a_power), b_power)
