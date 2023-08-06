import numpy as np
from skimage.feature import register_translation
from skimage.transform._geometric import SimilarityTransform

from starfish.image._learn_transform.transforms_list import TransformsList
from starfish.imagestack.imagestack import ImageStack
from starfish.types import Axes, TransformType
from starfish.util import click
from ._base import LearnTransformBase


class Translation(LearnTransformBase):

    def __init__(self, reference_stack: ImageStack, axes: Axes, upsampling: int=1):
        """
        Parameters
        ----------
        axes:
            The axes {r, ch, zplane} to iterate over
        reference_stack: ImageStack
            The target image used in skimage.feature.register_translation
        upsampling: int
            upsampling factor (default=1). See
            http://scikit-image.org/docs/dev/api/skimage.feature.html#skimage.feature.register_translation
            for an explanation of this parameter.
        """
        self.upsampling = upsampling
        self.axes = axes
        self.reference_stack = reference_stack

    def run(self, stack: ImageStack, verbose: bool=False, *args) -> TransformsList:
        """
        Iterate over the given axes of an ImageStack and learn the Similarity transform
        based off the reference_stack passed into :py:class:`Translation`'s constructor.
        Only supports 2d data.


        Parameters
        ----------
        stack : ImageStack
            Stack to calculate the transforms on.
        verbose : bool
            if True, report on transformation progress (default = False)

        Returns
        -------
        List[Tuple[Mapping[Axes, int], SimilarityTransform]] :
            A list of tuples containing axes of the Imagestack and associated
            transform to apply.
        """

        transforms = TransformsList()
        reference_image = np.squeeze(self.reference_stack.xarray)
        for a in stack.axis_labels(self.axes):
            target_image = np.squeeze(stack.sel({self.axes: a}).xarray)
            if len(target_image.shape) != 2:
                raise ValueError(
                    f"Only axes: {self.axes.value} can have a length > 1, "
                    f"please use the MaxProj filter."
                )

            shift, error, phasediff = register_translation(src_image=target_image,
                                                           target_image=reference_image,
                                                           upsample_factor=self.upsampling)
            if verbose:
                print(f"For {self.axes}: {a}, Shift: {shift}, Error: {error}")
            selectors = {self.axes: a}
            # reverse shift because SimilarityTransform stores in y,x format
            shift = shift[::-1]
            transforms.append(selectors,
                              TransformType.SIMILARITY,
                              SimilarityTransform(translation=shift))

        return transforms

    @staticmethod
    @click.command("Translation")
    @click.option("--reference-stack", required=True, type=click.Path(exists=True),
                  help="The image to align the input ImageStack to.")
    @click.option("--axes", default="r", type=str, help="The axes to iterate over.")
    @click.option("--upsampling", default=1, type=int, help="Upsampling factor.")
    @click.pass_context
    def _cli(ctx, reference_stack, axes, upsampling):
        ctx.obj["component"]._cli_run(ctx, Translation(
            reference_stack=ImageStack.from_path_or_url(reference_stack),
            axes=Axes(axes), upsampling=upsampling))
