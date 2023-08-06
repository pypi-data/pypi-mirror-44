from itertools import product
from json import loads
from typing import Dict, List, Union

import numpy as np
import pandas as pd
import xarray as xr

from starfish.expression_matrix.expression_matrix import ExpressionMatrix
from starfish.types import (
    Axes,
    Coordinates,
    DecodedSpots,
    Features,
    LOG,
    SpotAttributes,
    STARFISH_EXTRAS_KEY
)
from starfish.util.dtype import preserve_float_range


class IntensityTable(xr.DataArray):
    """Container for spot/pixel features extracted from image data

    An IntensityTable is comprised of each feature's intensity across channels and imaging
    rounds, where features are typically spots or pixels. This forms an
    ``(n_feature, n_channel, n_round)`` tensor implemented as an xarray.DataArray object.
    In addition to the basic xarray methods, IntensityTable implements:

    Methods
    -------
    empty_intensity_table(spot_attributes, n_ch, n_round)
        creates an IntensityTable with all intensities equal to zero

    from_spot_data(intensities, spot_attributes)
        creates an IntensityTable from a 3d array and a spot attributes dataframe

    synthetic_intensities(codebook, num_z=12, height=50, width=40, n_spots=10, \
            mean_fluor_per_spot=200, mean_photons_per_fluor=50)
        creates an IntensityTable with synthetic spots, given a codebook

    save(filename)
        save the IntensityTable to netCDF

    load(filename)
        load an IntensityTable from netCDF

    Examples
    --------
    Create an IntensityTable using the ``synthetic_intensities`` method::

        >>> from starfish.util.synthesize import SyntheticData
        >>> sd = SyntheticData(n_ch=3, n_round=4, n_codes=2)
        >>> codes = sd.codebook()
        >>> sd.intensities(codebook=codes)
        <xarray.IntensityTable (features: 2, c: 3, h: 4)>
        array([[[    0.,     0.,     0.,     0.],
                [    0.,     0.,  8022., 12412.],
                [11160.,  9546.,     0.,     0.]],

               [[    0.,     0.,     0.,     0.],
                [    0.,     0., 10506., 10830.],
                [11172., 12331.,     0.,     0.]]])
        Coordinates:
        * features   (features) MultiIndex
        - z          (features) int64 7 3
        - y          (features) int64 14 32
        - x          (features) int64 32 15
        - r          (features) float64 nan nan
        * c          (c) int64 0 1 2
        * h          (h) int64 0 1 2 3
          target     (features) object 08b1a822-a1b4-4e06-81ea-8a4bd2b004a9 ...

    """

    @staticmethod
    def _build_xarray_coords(
            spot_attributes: SpotAttributes, channel_index: np.ndarray, round_index: np.ndarray
    ) -> Dict[str, np.ndarray]:
        """build a non-multi-index set of coordinates for intensity-table"""
        coordinates = {
            k: (Features.AXIS, spot_attributes.data[k].values)
            for k in spot_attributes.data}
        coordinates.update({
            Features.AXIS: np.arange(len(spot_attributes.data)),
            Axes.CH.value: channel_index,
            Axes.ROUND.value: round_index
        })
        return coordinates

    @classmethod
    def empty_intensity_table(
            cls, spot_attributes: SpotAttributes, n_ch: int, n_round: int,
    ) -> "IntensityTable":
        """Create an empty intensity table with pre-set axis whose values are zero

        Parameters
        ----------
        spot_attributes : pd.MultiIndex
            MultiIndex containing spot metadata. Must contain the values specifid in Constants.X,
            Y, Z, and RADIUS.
        n_ch : int
            number of channels measured in the imaging experiment
        n_round : int
            number of imaging rounds measured in the imaging experiment

        Returns
        -------
        IntensityTable :
            empty IntensityTable

        """
        if not isinstance(spot_attributes, SpotAttributes):
            raise TypeError('parameter spot_attributes must be a starfish SpotAttributes object.')

        channel_index = np.arange(n_ch)
        round_index = np.arange(n_round)
        data = np.zeros((spot_attributes.data.shape[0], n_ch, n_round))
        dims = (Features.AXIS, Axes.CH.value, Axes.ROUND.value)
        coords = cls._build_xarray_coords(spot_attributes, channel_index, round_index)

        intensity_table = cls(
            data=data, coords=coords, dims=dims,
        )

        return intensity_table

    @classmethod
    def from_spot_data(
            cls, intensities: Union[xr.DataArray, np.ndarray], spot_attributes: SpotAttributes,
            *args, **kwargs) -> "IntensityTable":
        """Table to store image feature intensities and associated metadata

        Parameters
        ----------
        intensities : np.ndarray[Any]
            intensity data
        spot_attributes : pd.DataFrame
            Name(s) of the data dimension(s). Must be either a string (only
            for 1D data) or a sequence of strings with length equal to the
            number of dimensions. If this argument is omitted, dimension names
            are taken from ``coords`` (if possible) and otherwise default to
            ``['dim_0', ... 'dim_n']``.
        args :
            additional arguments to pass to the xarray constructor
        kwargs :
            additional keyword arguments to pass to the xarray constructor

        Returns
        -------
        IntensityTable :
            IntensityTable containing data from passed ndarray, annotated by spot_attributes

        """

        if len(intensities.shape) != 3:
            raise ValueError(
                f'intensities must be a (features * ch * round) 3-d tensor. Provided intensities '
                f'shape ({intensities.shape}) is invalid.')

        if not isinstance(spot_attributes, SpotAttributes):
            raise TypeError('parameter spot_attributes must be a starfish SpotAttributes object.')

        coords = cls._build_xarray_coords(
            spot_attributes,
            np.arange(intensities.shape[1]),
            np.arange(intensities.shape[2]))

        dims = (Features.AXIS, Axes.CH.value, Axes.ROUND.value)

        intensities = cls(intensities, coords, dims, *args, **kwargs)
        return intensities

    def get_log(self):
        """Deserialize and return a list of pipeline components that have been applied
         throughout a starfish session to create this Intensity Table"""

        if STARFISH_EXTRAS_KEY in self.attrs and LOG in self.attrs[STARFISH_EXTRAS_KEY]:
            return loads(self.attrs[STARFISH_EXTRAS_KEY])[LOG]
        else:
            raise RuntimeError('No log info found.')

    @property
    def has_physical_coords(self):
        return Coordinates.X in self.coords and Coordinates.Y in self.coords

    def save(self, filename: str) -> None:
        """Save an IntensityTable as a Netcdf File

        Parameters
        ----------
        filename : str
            Name of Netcdf file

        """
        self.to_netcdf(filename)

    def save_mermaid(self, filename: str) -> pd.DataFrame:
        """
        Writes a .csv.gz file in columnar format that is readable by MERMAID visualization
        software.

        To run MERMAID, follow the installation instructions for that repository and simply
        replace the data.csv.gz file with the output of this function.

        Parameters
        ----------
        filename : str
            name for compressed-gzipped MERMAID data file. Should end in '.csv.gz'

        See Also
        --------
        https://github.com/JEFworks/MERmaid

        """

        # verify the IntensityTable has been decoded
        if Features.TARGET not in self.coords.keys():
            raise RuntimeError(
                'IntensityTable must be decoded before it can be converted to MERMAID input.'
            )

        # construct the MERMAID dataframe. As MERMAID adds support for non-categorical variables,
        # additional columns can be added here
        df = self.to_features_dataframe()
        column_order = [
            Axes.X,
            Axes.Y,
            Features.TARGET,
            Features.TARGET,  # added twice to support simultaneous coding
        ]
        mermaid_data = df[column_order]

        # write to disk
        mermaid_data.to_csv(filename, compression='gzip', index=False)

    @classmethod
    def load(cls, filename: str) -> "IntensityTable":
        """load an IntensityTable from Netcdf

        Parameters
        ----------
        filename : str
            File to load

        Returns
        -------
        IntensityTable

        """
        loaded = xr.open_dataarray(filename)
        intensity_table = cls(
            loaded.data,
            loaded.coords,
            loaded.dims,
            attrs=loaded.attrs,
        )
        return intensity_table

    def show(self, background_image: np.ndarray) -> None:
        """show spots on a background image"""
        raise NotImplementedError

    @classmethod
    def synthetic_intensities(
            cls, codebook, num_z: int=12, height: int=50, width: int=40, n_spots=10,
            mean_fluor_per_spot=200, mean_photons_per_fluor=50
    ) -> "IntensityTable":
        """Create an IntensityTable containing synthetic spots with random locations

        Parameters
        ----------
        codebook : Codebook
            starfish codebook object
        num_z :
            number of z-planes to use when localizing spots
        height :
            y dimension of each synthetic plane
        width :
            x dimension of each synthetic plane
        n_spots :
            number of spots to generate
        mean_fluor_per_spot :
            mean number of fluorophores per spot
        mean_photons_per_fluor :
            mean number of photons per fluorophore.

        Returns
        -------
        IntensityTable

        """

        # TODO nsofroniew: right now there is no jitter on x-y positions of the spots
        z = np.random.randint(0, num_z, size=n_spots)
        y = np.random.randint(0, height, size=n_spots)
        x = np.random.randint(0, width, size=n_spots)
        r = np.empty(n_spots)
        r.fill(np.nan)  # radius is a function of the point-spread gaussian size
        spot_attributes = SpotAttributes(
            pd.DataFrame(
                {Axes.ZPLANE.value: z,
                 Axes.Y.value: y,
                 Axes.X.value: x,
                 Features.SPOT_RADIUS: r}
            )
        )

        # empty data tensor
        data = np.zeros(shape=(n_spots, *codebook.shape[1:]))

        targets = np.random.choice(
            codebook.coords[Features.TARGET], size=n_spots, replace=True)
        expected_bright_locations = np.where(codebook.loc[targets])

        # create a binary matrix where "on" spots are 1
        data[expected_bright_locations] = 1

        # add physical properties of fluorescence
        data *= np.random.poisson(mean_photons_per_fluor, size=data.shape)
        data *= np.random.poisson(mean_fluor_per_spot, size=data.shape)

        # convert data to float for consistency with starfish
        data = preserve_float_range(data)
        assert 0 < data.max() <= 1

        intensities = cls.from_spot_data(data, spot_attributes)
        intensities[Features.TARGET] = (Features.AXIS, targets)

        return intensities

    @classmethod
    def from_image_stack(
            cls,
            image_stack,
            crop_x: int=0, crop_y: int=0, crop_z: int=0
    ) -> "IntensityTable":
        """Generate an IntensityTable from all the pixels in the ImageStack

        Parameters
        ----------
        crop_x : int
            number of pixels to crop from both top and bottom of x
        crop_y : int
            number of pixels to crop from both top and bottom of y
        crop_z : int
            number of pixels to crop from both top and bottom of z
        image_stack : ImageStack
            ImageStack containing pixels to be treated as intensities

        Returns
        -------
        IntensityTable :
            IntensityTable containing one intensity per pixel (across channels and rounds)

        """

        # verify the image is large enough to crop
        assert crop_z * 2 < image_stack.shape['z']
        assert crop_y * 2 < image_stack.shape['y']
        assert crop_x * 2 < image_stack.shape['x']

        zmin = crop_z
        ymin = crop_y
        xmin = crop_x
        zmax = image_stack.shape['z'] - crop_z
        ymax = image_stack.shape['y'] - crop_y
        xmax = image_stack.shape['x'] - crop_x
        cropped_stack = image_stack.sel({Axes.ZPLANE: (zmin, zmax),
                                         Axes.Y: (ymin, ymax),
                                         Axes.X: (xmin, xmax)})

        data = cropped_stack.xarray.transpose(
            Axes.ZPLANE.value,
            Axes.Y.value,
            Axes.X.value,
            Axes.CH.value,
            Axes.ROUND.value,
        )

        # (pixels, ch, round)
        intensity_data = data.values.reshape(
            -1, image_stack.num_chs, image_stack.num_rounds)

        # IntensityTable pixel coordinates
        z = np.arange(zmin, zmax)
        y = np.arange(ymin, ymax)
        x = np.arange(xmin, xmax)

        feature_attribute_data = pd.DataFrame(
            data=np.array(list(product(z, y, x))),
            columns=['z', 'y', 'x']
        )
        feature_attribute_data[Features.SPOT_RADIUS] = np.full(
            feature_attribute_data.shape[0], fill_value=0.5
        )

        pixel_coordinates = SpotAttributes(feature_attribute_data)

        return IntensityTable.from_spot_data(intensity_data, pixel_coordinates)

    @staticmethod
    def concatanate_intensity_tables(intensity_tables: List["IntensityTable"]):
        # TODO VARY CONCAT LOGIC IF TILES OVERLAP
        # This method is a starting point for handling tile overlap, right now
        # it does a simple concat but people want other overlap logic implmented
        return xr.concat(intensity_tables, dim=Features.AXIS)

    def to_features_dataframe(self) -> pd.DataFrame:
        """Generates a dataframe of the underlying features multi-index.
        This is guaranteed to contain the features x, y, z, and radius.

        Returns
        -------
        pd.DataFrame

        """
        return pd.DataFrame(dict(self[Features.AXIS].coords))

    def to_decoded_spots(self) -> DecodedSpots:
        """
        Generates a dataframe containing decoded spot information. Guaranteed to contain physical
        spot coordinates (z, y, x) and gene target. Does not contain pixel coordinates.
        """
        if Features.TARGET not in self.coords.keys():
            raise RuntimeError(
                "Intensities must be decoded before a DecodedSpots table can be produced.")
        df = self.to_features_dataframe()
        pixel_coordinates = pd.Index([Axes.X, Axes.Y, Axes.ZPLANE])
        df = df.drop(pixel_coordinates.intersection(df.columns), axis=1).drop(Features.AXIS, axis=1)
        return DecodedSpots(df)

    def to_expression_matrix(self) -> ExpressionMatrix:
        """Generates a cell x gene count matrix where each cell is annotated with spatial metadata

        Requires that spots in the IntensityTable have been assigned to cells.

        Returns
        -------
        ExpressionMatrix :
            cell x gene expression table
        """
        if Features.CELL_ID not in self.coords:
            raise KeyError("IntensityTable must have 'cell_id' assignments for each cell before "
                           "this function can be called. See starfish.TargetAssignment.Label.")
        grouped = self.to_features_dataframe().groupby([Features.CELL_ID, Features.TARGET])
        counts = grouped.count().iloc[:, 0].unstack().fillna(0)
        if self.has_physical_coords:
            grouped = self.to_features_dataframe().groupby([Features.CELL_ID])[[
                Axes.X, Axes.Y, Axes.ZPLANE, Coordinates.X, Coordinates.Y, Coordinates.Z]]
        else:
            grouped = self.to_features_dataframe().groupby([Features.CELL_ID])[[
                Axes.X, Axes.Y, Axes.ZPLANE]]
        min_ = grouped.min()
        max_ = grouped.max()
        coordinate_df = min_ + (max_ - min_) / 2
        metadata = {name: (Features.CELLS, data.values) for name, data in coordinate_df.items()}
        metadata[Features.AREA] = (Features.CELLS, np.full(counts.shape[0], fill_value=np.nan))
        # add genes to the metadata
        metadata.update({Features.GENES: counts.columns.values})
        metadata.update({Features.CELL_ID: (Features.CELLS, counts.index.values)})

        mat = ExpressionMatrix(
            data=counts.values,
            dims=(Features.CELLS, Features.GENES),
            coords=metadata,
            name='expression_matrix'
        )
        return mat

    def feature_trace_magnitudes(self) -> np.ndarray:
        """Return the magnitudes of each feature across rounds and channels

        Returns
        -------
        np.ndarray :
            vector of feature norms

        """
        feature_traces = self.stack(traces=(Axes.CH.value, Axes.ROUND.value))
        norm = np.linalg.norm(feature_traces.values, ord=2, axis=1)  # 2 = feature magnitudes

        return norm
