""" classes to represent sections of config.ini file """
import attr
from attr.validators import instance_of, optional
from attr import converters


@attr.s
class GeneralConfig:
    """represents [GENERAL] section of config.ini file

    Attributes
    ----------
    output_dir : str
        path to directory where images and .json file created by running searchstims
        should be saved
    json_filename : str
        name of .json file that will be created with information about images created
    num_target_present : int
        number of visual search stimuli to generate with target present.
        If specified in this section and not specified in the section for a specific stimulus,
        then this value will be used. If specified in another section, that value overrides
        this one.
    num_target_absent : int
        number of visual search stimuli to generate with target absent
        If specified in this section and not specified in the section for a specific stimulus,
        then this value will be used. If specified in another section, that value overrides
        this one.
    set_sizes : list
        of int, "set sizes" that should be generated
        If specified in this section and not specified in the section for a specific stimulus,
        then this value will be used. If specified in another section, that value overrides
        this one.
    """
    output_dir = attr.ib(validator=instance_of(str))
    json_filename = attr.ib(validator=instance_of(str))
    num_target_present = attr.ib(converter=converters.optional(int))
    num_target_absent = attr.ib(converter=converters.optional(int))
    set_sizes = attr.ib(validator=optional(instance_of(list)))


# ----------------- validator functions used by RectangleConfig and NumberConfig ---------------------------------------
def check_border_size(instance, attribute, value):
    if len(value) != 2:
        raise ValueError(f"border size tuple should be two elements, got {value}")


@attr.s
class RectangleConfig:
    """represent [RECTANGLE] section of config.ini file

    Attributes
    ----------
    rects_width_height : tuple
        two element tuple, (width, height). The size of rectangles that contain
        items (target + distractors) in the visual search stimulus.
        For RectangleConfig this is literally the size of the rectangles that are
        displayed on the visual search stimulus. Default is (10, 30).
        In order of (width, height) because that's what PyGame expects.
    image_size : tuple
        two element tuple, (rows, columns). This will be the size of an input
        to the neural network architecture that you're training.
    grid_size : tuple
        two element tuple, (rows, columns). Represents the "grid" that the
        visuals search stimulus is divided into, where each cell in that
        grid can contain an item (either the target or a distractor). The
        total number of cells will be rows * columns.
    border_size : tuple
        two element tuple, (rows, columns). The size of the border between
        the actual end of the image and the grid of cells within the image
        that will contain the items (target + distractors).
        Optional; default is None. Useful if you are worried about edge effects.
    min_center_dist : int
        minimum distance to maintain between the center of items.
        Useful if you are worried about crowding effects.
        Optional; default is None.
    jitter : int
        maximum value of jitter applied to center points of items. Default is 5.
    target_color : str
        color of target. For RectangleConfig, default is 'red'.
    distractor_color : str
        color of target. For RectangleConfig, default is 'green'.
    """
    rects_width_height = attr.ib(validator=instance_of(tuple), default=(10, 30))
    @rects_width_height.validator
    def check_rects_width_height(self, attribute, value):
        if len(value) != 2:
            raise ValueError(f"rects_width_height tuple should be two elements, got {value}")

    image_size = attr.ib(validator=instance_of(tuple), default=(227, 227))
    @image_size.validator
    def check_image_size(self, attribute, value):
        if len(value) != 2:
            raise ValueError(f"image_size tuple should be two elements, got {value}")

    grid_size = attr.ib(validator=instance_of(tuple), default=(5,5))
    @grid_size.validator
    def check_grid_size(self, attribute, value):
        if len(value) != 2:
            raise ValueError(f"grid size tuple should be two elements, got {value}")

    border_size = attr.ib(validator=optional([instance_of(tuple), check_border_size]),
                          default=None)
    min_center_dist = attr.ib(validator=optional(instance_of(int)), default=None)
    jitter = attr.ib(validator=instance_of(int), default=5)
    target_color = attr.ib(validator=instance_of(str), default='red')
    distractor_color = attr.ib(validator=instance_of(str), default='green')


def number_validator(instance, attribute, value):
    if value not in (2, 5):
        raise ValueError(f'{attribute} must be either 2 or 5, not {value}')
    if (
                (attribute == 'target_number' and value == instance.distractor_number)
            or
                (attribute == 'distractor_number' and value == instance.target_number)
    ):
            raise ValueError(f"target number should not equal distractor number but both are {value}")


@attr.s
class NumberConfig:
    """represent [NUMBER] section of config.ini file

    Attributes
    ----------
    rects_width_height : tuple
        two element tuple, (width, height). The size of rectangles that contain
        items (target + distractors) in the visual search stimulus.
        For NumberConfig this must be the size of the .png images that contain the
        number shapes, (30, 30).
        In order of (width, height) because that's what PyGame expects.
    image_size : tuple
        two element tuple, (rows, columns). This will be the size of an input
        to the neural network architecture that you're training.
    grid_size : tuple
        two element tuple, (rows, columns). Represents the "grid" that the
        visuals search stimulus is divided into, where each cell in that
        grid can contain an item (either the target or a distractor). The
        total number of cells will be rows * columns.
    border_size : tuple
        two element tuple, (rows, columns). The size of the border between
        the actual end of the image and the grid of cells within the image
        that will contain the items (target + distractors).
        Optional; default is None. Useful if you are worried about edge effects.
    min_center_dist : int
        minimum distance to maintain between the center of items.
        Useful if you are worried about crowding effects.
        Optional; default is None.
    jitter : int
    target_color : int
        color of target. For NumberConfig, default is 'white'.
    distractor_color : int
        color of target. For NumberConfig, default is 'white'.
    target_number : int
    distractor_number : int
    """
    rects_width_height = attr.ib(validator=instance_of(tuple), default=(30, 30))
    @rects_width_height.validator
    def check_rects_width_height(self, attribute, value):
        if len(value) != 2:
            raise ValueError(f"rects_width_height tuple should be two elements, got {value}")

    image_size = attr.ib(validator=instance_of(tuple), default=(227, 227))
    @image_size.validator
    def check_image_size(self, attribute, value):
        if len(value) != 2:
            raise ValueError(f"image_size tuple should be two elements, got {value}")

    grid_size = attr.ib(validator=instance_of(tuple), default=(5,5))
    @grid_size.validator
    def check_grid_size(self, attribute, value):
        if len(value) != 2:
            raise ValueError(f"grid size tuple should be two elements, got {value}")

    border_size = attr.ib(validator=optional([instance_of(tuple), check_border_size]),
                          default=None)
    min_center_dist = attr.ib(validator=optional(instance_of(int)), default=None)
    jitter = attr.ib(validator=instance_of(int), default=5)
    target_color = attr.ib(validator=instance_of(str), default='white')
    distractor_color = attr.ib(validator=instance_of(str), default='white')
    target_number = attr.ib(validator=[instance_of(int), number_validator], default=2)
    distractor_number = attr.ib(validator=[instance_of(int), number_validator], default=5)


@attr.s
class Config:
    """class to represent all sections of config.ini file

    Attributes
    ----------
    general: TrainConfig
        represents [TRAIN] section
    rectangle: RectangleConfig
        represents [RECTANGLE] section
    number: NumberConfig
        represents [NUMBER] section
    """
    general = attr.ib(GeneralConfig)
    rectangle = attr.ib(validator=optional(instance_of(RectangleConfig)), default=None)
    number = attr.ib(validator=optional(instance_of(NumberConfig)), default=None)
