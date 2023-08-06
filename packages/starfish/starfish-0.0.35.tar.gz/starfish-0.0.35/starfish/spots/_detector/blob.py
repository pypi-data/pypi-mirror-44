from typing import Optional, Union

import numpy as np
import pandas as pd
import xarray as xr
from skimage.feature import blob_dog, blob_doh, blob_log

from starfish.imagestack.imagestack import ImageStack
from starfish.intensity_table.intensity_table import IntensityTable
from starfish.types import Axes, Features, Number, SpotAttributes
from starfish.util import click
from ._base import SpotFinderAlgorithmBase
from .detect import detect_spots, measure_spot_intensity

blob_detectors = {
    'blob_dog': blob_dog,
    'blob_doh': blob_doh,
    'blob_log': blob_log
}


class BlobDetector(SpotFinderAlgorithmBase):

    def __init__(
            self,
            min_sigma: Number,
            max_sigma: Number,
            num_sigma: int,
            threshold: Number,
            overlap: float = 0.5,
            measurement_type='max',
            is_volume: bool = True,
            detector_method: str = 'blob_log'
    ) -> None:
        """Multi-dimensional gaussian spot detector

        This method is a wrapper for skimage.feature.blob_log

        Parameters
        ----------
        min_sigma : float
            The minimum standard deviation for Gaussian Kernel. Keep this low to
            detect smaller blobs.
        max_sigma : float
            The maximum standard deviation for Gaussian Kernel. Keep this high to
            detect larger blobs.
        num_sigma : int
            The number of intermediate values of standard deviations to consider
            between `min_sigma` and `max_sigma`.
        threshold : float
            The absolute lower bound for scale space maxima. Local maxima smaller
            than thresh are ignored. Reduce this to detect blobs with less
            intensities.
        overlap : float [0, 1]
            If two spots have more than this fraction of overlap, the spots are combined
            (default = 0.5)
        measurement_type : str ['max', 'mean']
            name of the function used to calculate the intensity for each identified spot area
        detector_method: str ['blob_dog', 'blob_doh', 'blob_log']
            name of the type of detection method used from skimage.feature, default: blob_log

        Notes
        -----
        # TODO ambrosejcarr: revisit after changing dtype assumptions of library to float in [0, 1]
        This spot detector is very sensitive to the threshold that is selected, and the threshold
        is defined as an absolute value -- therefore it must be adjusted depending on the datatype
        of the passed image.

        See Also
        --------
        http://scikit-image.org/docs/dev/auto_examples/features_detection/plot_blob.html

        """
        self.min_sigma = min_sigma
        self.max_sigma = max_sigma
        self.num_sigma = num_sigma
        self.threshold = threshold
        self.overlap = overlap
        self.is_volume = is_volume
        self.measurement_function = self._get_measurement_function(measurement_type)
        try:
            self.detector_method = blob_detectors[detector_method]
        except ValueError:
            raise ValueError("Detector method must be one of {blob_log, blob_dog, blob_doh}")

    def image_to_spots(self, data_image: Union[np.ndarray, xr.DataArray]) -> SpotAttributes:
        """
        Find spots using a gaussian blob finding algorithm

        Parameters
        ----------
        data_image : Union[np.ndarray, xr.DataArray]
            ImageStack containing blobs to be detected

        Returns
        -------
        SpotAttributes :
            DataFrame of metadata containing the coordinates, intensity and radius of each spot

        """

        fitted_blobs_array: np.ndarray = self.detector_method(
            data_image,
            self.min_sigma,
            self.max_sigma,
            self.num_sigma,
            self.threshold,
            self.overlap
        )

        if fitted_blobs_array.shape[0] == 0:
            return SpotAttributes.empty(extra_fields=['intensity', 'spot_id'])

        # create the SpotAttributes Table
        columns = [Axes.ZPLANE.value, Axes.Y.value, Axes.X.value, Features.SPOT_RADIUS]
        fitted_blobs = pd.DataFrame(data=fitted_blobs_array, columns=columns)

        # convert standard deviation of gaussian kernel used to identify spot to radius of spot
        converted_radius = np.round(fitted_blobs[Features.SPOT_RADIUS] * np.sqrt(3))
        fitted_blobs[Features.SPOT_RADIUS] = converted_radius

        # convert the array to int so it can be used to index
        rounded_blobs = SpotAttributes(fitted_blobs.astype(int))

        rounded_blobs.data['intensity'] = measure_spot_intensity(
            data_image, rounded_blobs, self.measurement_function)
        rounded_blobs.data['spot_id'] = np.arange(rounded_blobs.data.shape[0])

        return rounded_blobs

    def run(
            self,
            data_stack: ImageStack,
            blobs_image: Optional[Union[np.ndarray, xr.DataArray]]=None,
            reference_image_from_max_projection: bool=False,
            *args,
    ) -> IntensityTable:
        """find spots in an ImageStack

        Parameters
        ----------
        data_stack : ImageStack
            stack containing spots to find
        blobs_image : Union[np.ndarray, xr.DataArray]
        reference_image_from_max_projection : bool
            if True, compute a reference image from the maximum projection of the channels and
            z-planes

        Returns
        -------
        IntensityTable :
            3d tensor containing the intensity of spots across channels and imaging rounds

        """

        intensity_table = detect_spots(
            data_stack=data_stack,
            spot_finding_method=self.image_to_spots,
            reference_image=blobs_image,
            reference_image_from_max_projection=reference_image_from_max_projection,
            measurement_function=self.measurement_function,
            radius_is_gyration=False)

        return intensity_table

    @staticmethod
    @click.command("BlobDetector")
    @click.option(
        "--min-sigma", default=4, type=int, help="Minimum spot size (in standard deviation)")
    @click.option(
        "--max-sigma", default=6, type=int, help="Maximum spot size (in standard deviation)")
    @click.option(
        "--num-sigma", default=20, type=int, help="Number of sigmas to try")
    @click.option(
        "--threshold", default=.01, type=float, help="Dots threshold")
    @click.option(
        "--overlap", default=0.5, type=float,
        help="dots with overlap of greater than this fraction are combined")
    @click.option(
        "--show", default=False, is_flag=True, help="display results visually")
    @click.option(
        "--detector_method", default='blob_log',
        help="str ['blob_dog', 'blob_doh', 'blob_log'] name of the type of "
             "detection method used from skimage.feature. Default: blob_log"
    )
    @click.pass_context
    def _cli(ctx, min_sigma, max_sigma, num_sigma, threshold, overlap, show, detector_method):
        instance = BlobDetector(min_sigma, max_sigma, num_sigma, threshold, overlap,
                                detector_method=detector_method)
        #  FIXME: measurement_type, is_volume missing as options; show missing as ctor args
        ctx.obj["component"]._cli_run(ctx, instance)
