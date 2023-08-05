import os
from collections import namedtuple

import pygame
from pygame.locals import *
import numpy as np
from scipy.spatial.distance import pdist

pygame.init()

# set up colors
colors_dict = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'red255green51': (255, 51, 0),
    'green255red51': (51, 255, 0),
    'red255green102': (255, 102, 0),
    'green255red102': (102, 255, 0),
    'red255green153': (255, 153, 0),
    'green255red153': (153, 255, 0),
    'red255green204': (255, 204, 0),
    'green255red204': (204, 255, 0),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
}

MAX_DRAWS_INNER = 1000
MAX_DRAWS_OUTER = 100


class AbstractStimMaker:
    """parent class for all StimMaker classes
    """

    RectTuple = namedtuple('RectTuple', ['display_surface',
                                         'grid_as_char',
                                         'target_indices',
                                         'distractor_indices'])

    def __init__(self,
                 target_color='red',
                 distractor_color='green',
                 window_size=(227, 227),
                 border_size=None,
                 grid_size=(5, 5),
                 min_center_dist=None,
                 rects_width_height=(10, 30),
                 jitter=5):
        """__init__ function for Stim Makers

        Parameters
        ----------
        target_color : str
            {'red', 'green', 'white', 'blue'}. Default is 'red'.
        distractor_color : str
            {'red', 'green', 'white', 'blue'}. Default is 'green'.
        window_size : tuple
            of length two, representing (width, height) of window in pixels.
        border_size : tuple
            of length two, representing (width, height) of border, distance
            from edge of window within which items should not be displayed.
            Default is None.
        grid_size : tuple
            of length two, representing the number of (rows, columns)
            in the grid on which tareget and distractors will be located.
        min_center_dist : int
            Minimum distance between center point of items. Default is None, in
            which case any distance is permitted. Only used if grid_size is None
            and items are placed randomly instead of on a grid.
        rects_width_height : tuple
            shape of pygame Rect objects that will be plotted,
            (width, height) in pixels. Default is (10, 30).
        jitter : int
            number of pixels to jitter each 'item' in the 'set'
            that will be plotted on the grid. Default is 5.
            Adding jitter is helpful for creating stimuli with the
            same set size but slightly different placements, e.g. for
            augmenting data to train a learning algorithm and encourage
            invariant representations.
        """
        if grid_size is not None:
            if not all([type(grid_size_el) == int for grid_size_el in grid_size]):
                raise ValueError('values for grid size must be positive integers')

            if not all([grid_size_el > 0 for grid_size_el in grid_size]):
                raise ValueError('values for grid size must be positive integers')

        self.target_color = target_color
        self.distractor_color = distractor_color
        self.grid_size = grid_size
        self.min_center_dist = min_center_dist
        self.window_size = window_size
        self.border_size = border_size
        self.rects_width_height = rects_width_height
        self.jitter = jitter

    def _return_rect_for_stim(self, display_surface, rect_to_draw, is_target):
        """this function must return a pygame.rect object
        which the StimMaker.make_stim method will `blit` on
        the stimulus."""
        raise NotImplementedError

    def make_stim(self,
                  set_size=8,
                  num_target=1,
                  ):
        """make visual search stimuli

        Parameters
        ----------
        set_size : int
            Set size, equal to number of targets + distractors.
            Default is 8.
        num_target : int
            Number of targets. Default is 1.

        Returns
        -------
        display_surface : pygame.Surface
            with visual search stimuli plotted on it
        """
        if type(set_size) != int:
            raise TypeError('set size must be an integer')

        if not set_size > 0:
            raise ValueError('set size must be greater than zero')

        if type(num_target) != int:
            raise TypeError('number of targets must be an integer')

        if not num_target >= 0:
            raise ValueError('number of targets must be greater than or equal to zero')

        if num_target > set_size:
            raise ValueError('number of targets cannot be greater than set size')

        if self.grid_size is not None:
            total_grid_elements = self.grid_size[0] * self.grid_size[1]
            if set_size > total_grid_elements:
                raise ValueError('set size {} cannot be greater than number of '
                                 'elements in grid, {}'
                                 .format(set_size, total_grid_elements))

        if type(self.jitter) != int:
            raise TypeError('value for jitter must be an integer')

        if self.grid_size:
            if self.border_size is None:
                grid_size_pixels = self.window_size
            else:
                grid_size_pixels = (self.window_size[0] - self.border_size[0],
                                    self.window_size[1] - self.border_size[1])

            # make grid, randomly select which cells in grid to use
            grid_x = np.arange(1, self.grid_size[0] + 1)
            grid_y = np.arange(1, self.grid_size[1] + 1)
            xx, yy = np.meshgrid(grid_x, grid_y)
            xx = xx.ravel()
            yy = yy.ravel()
            num_cells = self.grid_size[0] * self.grid_size[1]
            cells_to_use = sorted(np.random.choice(np.arange(num_cells),
                                                   size=set_size,
                                                   replace=False))

            xx_to_use = xx[cells_to_use]
            yy_to_use = yy[cells_to_use]

            # find centers of cells we're going to use
            cell_width = round(grid_size_pixels[0] / self.grid_size[0])
            cell_x_center = round((grid_size_pixels[0] / self.grid_size[0]) / 2)
            xx_to_use_ctr = (xx_to_use * cell_width) - cell_x_center

            cell_height = round(grid_size_pixels[1] / self.grid_size[1])
            cell_y_center = round((grid_size_pixels[1] / self.grid_size[1]) / 2)
            yy_to_use_ctr = (yy_to_use * cell_height) - cell_y_center

            if self.border_size:
                xx_to_use_ctr += round(self.border_size[0] / 2)
                yy_to_use_ctr += round(self.border_size[1] / 2)

            # add jitter to those points
            jitter_high = self.jitter // 2
            jitter_low = -jitter_high
            if self.jitter % 2 == 0:  # if even
                # have to account for zero at center of jitter range
                # (otherwise range would be jitter + 1)
                # (Not a problem when doing floor division on odd #s)
                coin_flip = np.random.choice([0, 1])
                if coin_flip == 0:
                    jitter_low += 1
                elif coin_flip == 1:
                    jitter_high -= 1
            jitter_range = np.arange(jitter_low, jitter_high + 1)

            x_jitter = np.random.choice(jitter_range, size=xx_to_use.size)
            xx_to_use_ctr += x_jitter
            y_jitter = np.random.choice(jitter_range, size=yy_to_use.size)
            yy_to_use_ctr += y_jitter

        else:  # if self.grid_size is None
            if self.border_size:
                xx = np.arange(self.border_size[0] + (self.rects_width_height[1] / 2),
                               self.window_size[0] - (self.border_size[0] + (self.rects_width_height[1] / 2) + 1),
                               dtype=int)
                yy = np.arange(self.border_size[1] + (self.rects_width_height[1] / 2),
                               self.window_size[1] - (self.border_size[1] + (self.rects_width_height[1] / 2) + 1),
                               dtype=int)
            else:
                xx = np.arange(self.rects_width_height[1] / 2,
                               self.window_size[0] - (self.rects_width_height[1] / 2))
                yy = np.arange(self.rects_width_height[1] / 2,
                               self.window_size[1] - (self.rects_width_height[1] / 2))

            # draw center points at random
            dists_are_good = False
            less_than_set_size = True
            draws_outer = 0
            while dists_are_good is False:
                draws_outer += 1
                if draws_outer > MAX_DRAWS_OUTER:
                    raise ValueError('could not find suitable set of co-ordinates for set')

                draws_inner = 0
                coords_list = []

                while less_than_set_size is True:
                    xx_to_use_ctr = np.random.choice(xx)
                    yy_to_use_ctr = np.random.choice(yy)
                    coord = [xx_to_use_ctr, yy_to_use_ctr]
                    draws_inner += 1
                    if draws_inner > MAX_DRAWS_INNER:
                        coords_list = []
                        draws_inner = 0

                    if len(coords_list) == 0:
                        coords_list.append(coord)

                        if set_size == 1:
                            # then we're done actually
                            less_than_set_size = False
                            dists_are_good = True
                            # make into an array of size (1,) to prevent crash when we index into them below
                            xx_to_use_ctr = np.asarray([xx_to_use_ctr])
                            yy_to_use_ctr = np.asarray([yy_to_use_ctr])
                    else:
                        coords_list_tmp = list(coords_list)
                        coords_list_tmp.append(coord)
                        coords_list_tmp = np.stack(coords_list_tmp)
                        dists = pdist(coords_list_tmp)

                        if np.any(dists < self.min_center_dist):
                            continue
                        else:
                            coords_list = coords_list_tmp.tolist()

                            if len(coords_list) < set_size:
                                continue
                            else:
                                coords = np.asarray(coords_list)
                                xx_to_use_ctr = coords[:, 0]
                                yy_to_use_ctr = coords[:, 1]
                                dists_are_good = True
                                less_than_set_size = False

        # set up window
        display_surface = pygame.display.set_mode(self.window_size, 0, 32)

        # draw on surface object
        display_surface.fill(colors_dict['black'])
        target_inds = np.random.choice(np.arange(set_size),
                                       size=num_target).tolist()
        rects = []
        target_indices = []
        distractor_indices = []
        if self.grid_size:
            grid_as_char = [''] * num_cells
        else:
            grid_as_char = None

        for item in range(set_size):
            rect_tuple = (0, 0) + self.rects_width_height
            rect_to_draw = Rect(rect_tuple)
            center = (int(xx_to_use_ctr[item]), int(yy_to_use_ctr[item]))
            rect_to_draw.center = center
            if item in target_inds:
                is_target = True
                target_indices.append(center)
                if self.grid_size:
                    grid_as_char[cells_to_use[item]] = 't'
            else:
                is_target = False
                distractor_indices.append(center)
                if self.grid_size:
                    grid_as_char[cells_to_use[item]] = 'd'
            curr_rect = self._return_rect_for_stim(display_surface=display_surface,
                                                   rect_to_draw=rect_to_draw,
                                                   is_target=is_target)
            rects.append(curr_rect)

        if self.grid_size:
            grid_as_char = np.asarray(grid_as_char).reshape(self.grid_size[0], self.grid_size[1]).tolist()

        pygame.display.update()
        return self.RectTuple(display_surface=display_surface,
                              grid_as_char=grid_as_char,
                              target_indices=target_indices,
                              distractor_indices=distractor_indices)


class RectangleStimMaker(AbstractStimMaker):
    """Make visual search stimuli with vertical rectangles
    where target is different color form distractor.
    Considered a stimulus that allows for 'efficient' search."""
    def _return_rect_for_stim(self, display_surface, rect_to_draw, is_target):
        if is_target:
            color = self.target_color
        else:
            color = self.distractor_color
        rect = pygame.draw.rect(display_surface, colors_dict[color], rect_to_draw)
        return rect


class NumberStimMaker(AbstractStimMaker):
    """Make visual search stimuli with digital 2s and 5s.
    Considered a stimulus that results in 'inefficient' search."""
    png_path = os.path.join(os.path.dirname(__file__), 'png')

    numbers_dict = {
        (2, 'red'): 'two_red.png',
        (2, 'green'): 'two_green.png',
        (2, 'white'): 'two_white.png',
        (5, 'red'): 'five_red.png',
        (5, 'green'): 'five_green.png',
        (5, 'white'): 'five_white.png',
    }

    def __init__(self,
                 target_color='white',
                 distractor_color='white',
                 grid_size=(5, 5),
                 min_center_dist=None,
                 window_size=(227, 227),
                 border_size=None,
                 rects_width_height=(30, 30),
                 jitter=5,
                 target_number=2,
                 distractor_number=5):
        """
        Other Parameters
        ----------------
        target_number : int
            Number that is used as target.
            one of {2, 5}. Default is 2.
        distractor_number : int
            Number that is used as a distractor.
            one of {2, 5}. Default is 5.
        """
        super().__init__(target_color=target_color,
                         distractor_color=distractor_color,
                         window_size=window_size,
                         border_size=border_size,
                         grid_size=grid_size,
                         min_center_dist=min_center_dist,
                         rects_width_height=rects_width_height,
                         jitter=jitter)
        self.target_number = target_number
        self.distractor_number = distractor_number
        self.target_png = os.path.join(self.png_path,
                                       self.numbers_dict[(self.target_number,
                                                          self.target_color)])
        self.target = pygame.image.load(self.target_png)
        self.distractor_png = os.path.join(self.png_path,
                                           self.numbers_dict[(self.distractor_number,
                                                              self.distractor_color)])
        self.distractor = pygame.image.load(self.distractor_png)

    def _return_rect_for_stim(self, display_surface, rect_to_draw, is_target):
        """Returns target or distractor"""
        if is_target:
            rect = display_surface.blit(self.target, rect_to_draw)
        else:
            rect = display_surface.blit(self.distractor, rect_to_draw)
        return rect
