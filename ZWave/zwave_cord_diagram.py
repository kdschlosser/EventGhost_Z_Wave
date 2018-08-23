# # -*- coding: utf-8 -*-
# #
# # This file is part of EventGhost.
# # Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
# #
# # EventGhost is free software: you can redistribute it and/or modify it under
# # the terms of the GNU General Public License as published by the Free
# # Software Foundation, either version 2 of the License, or (at your option)
# # any later version.
# #
# # EventGhost is distributed in the hope that it will be useful, but WITHOUT
# # ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# # FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# # more details.
# #
# # You should have received a copy of the GNU General Public License along
# # with EventGhost. If not, see <http://www.gnu.org/licenses/>.

import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
from matplotlib import text as mtext
import math
import numpy as np
import random
from PIL import Image, ImageChops
from io import BytesIO
import zwave_utils

LW = 0.3


class Node(object):

    def __init__(self, node, nodes, ax, index):
        self.node = node
        self.nodes = nodes
        self.ax = ax
        self.index = index

        num_nodes = float(len(self.node.network.nodes.values()))
        color_offset = zwave_utils.remap(num_nodes, 1.0, 255.0, 255.0, 1.0)
        color_offset = ((color_offset / 1000.0) / 4.0)

        def get_color():
            res = []

            new_c = random.randrange(40, 215)
            while len(res) < 3:
                for old_c in res:
                    if (
                        new_c * (1.0 - color_offset)
                        < old_c <
                        new_c * (1.0 + color_offset)
                    ):
                        new_c = random.randrange(40, 215)
                        break
                else:
                    res += [new_c]

            return tuple(res)

        self.color = get_color()

        while True:
            for n in self.nodes:
                if (
                    sum(self.color) * (1.0 - color_offset)
                    < sum(n.color) <
                    sum(self.color) * (1.0 + color_offset)
                ):
                    self.color = get_color()
                    break
            else:
                break

        self.color_converted = tuple(c / 256.0 for c in self.color)

        self._neighbors = None

    @property
    def id(self):
        return self.node.id

    @property
    def neighbors(self):
        if self._neighbors is None:
            neighbors = list(neighbor for neighbor in self.node.neighbors)

            neighbor_array = [None] * len(self.nodes)

            for neighbor in neighbors:
                for node in self.nodes:
                    if node.id == neighbor:
                        neighbor_index = node.index
                        neighbor_array[neighbor_index] = node
                        break

            self._neighbors = neighbor_array[:]
        return self._neighbors

    @property
    def name(self):
        return self.node.name

    @property
    def room(self):
        return self.node.location

    @property
    def num_routes(self):

        def iter_neighbor(parent, found, checked):
            for neighbor in parent.neighbors:
                if neighbor is None:
                    continue

                if neighbor != self:
                    if neighbor in found or neighbor in checked:
                        continue

                    if neighbor.index == 0:
                        found += [parent]
                        continue

                    checked += [neighbor]
                    found, checked = iter_neighbor(neighbor, found, checked)

            return found, checked

        return len(iter_neighbor(self, [], [])[0])

    def hit_test(self, x, y, rotation, w, h):

        center_x = w / 2
        center_y = h / 2
        start_x, start_y = self.start_coords(rotation, center_x, center_y)
        end_x, end_y = self.end_coords(rotation, center_x, center_y)

        if start_x < x < end_x and start_y < y < end_y:
            return True

        if start_x > x > end_x and start_y < y < end_y:
            return True

        if start_x > x > end_x and start_y > y > end_y:
            return True

        if start_x < x < end_x and start_y > y > end_y:
            return True

    def end_coords(self, rotation, w, h):
        x_start, y_start = self.text_location(rotation)[:2]

        x_end = ((0.95 * x_start) * w) + w
        y_end = (-(0.95 * y_start) * h) + h

        return list(
            (int(round(x)), int(round(y))) for x, y in zip(x_end, y_end)
        )[-1]

    def start_coords(self, rotation, w, h):
        x_start, y_start = self.text_location(rotation)[:2]

        x_start = (x_start * w) + w
        y_start = (-y_start * h) + h

        return list(
            (int(round(x)), int(round(y))) for x, y in zip(x_start, y_start)
        )[0]

    @property
    def width(self):
        width = (
            300.0 /
            (300.0 * float(len(self.nodes))) *
            (360.0 - 1.0 * float(len(self.nodes)))
        )
        return width
        # return (360.0 / float(len(self.nodes))) - 2.0

    @property
    def start_pos(self):
        return (
            (float(self.index) * (self.width + 1.0)) +
            (90.0 - (self.width / 2.0))
        )

    @property
    def end_pos(self):
        return self.start_pos + self.width

    @property
    def neighbor_ids(self):
        return list(
            neighbor.id for neighbor in self.neighbors
            if neighbor is not None
        )

    @property
    def neighbor_pos(self):
        start = self.start_pos
        res = {}

        # noinspection PyShadowingBuiltins
        for id in self.neighbor_ids:
            end = start + self.chord_width
            res[id] = (start, end)
            start = end

        return res

    @property
    def chord_width(self):
        return self.width / float(len(self.node.neighbors))

    def get_neighbor_pos(self, neighbor_id):
        neighbor_pos = self.neighbor_pos

        if neighbor_id in neighbor_pos:
            return neighbor_pos[neighbor_id]

    def text_location(self, rotation=0):
        start = self.start_pos + rotation
        end = self.end_pos + rotation
        linespace = np.linspace(
            (start + 0.25) * np.pi / 180.0,
            (end - 0.25) * np.pi / 180.0,
            100
        )

        x = 0.97 * -np.cos(linespace)
        y = 0.97 * np.sin(linespace)

        return x, y, 0.96 * x, 0.96 * y,

    @zwave_utils.thread_call
    def write_text(self):
        x_1, y_1, x_2, y_2 = self.text_location()
        if self.index == 0:
            font_size = len(self.nodes) * 0.16
        else:
            font_size = len(self.nodes) * 0.22

        CurvedText(
            x=x_1,
            y=y_1,
            text=self.room,
            color=(0.0, 255.0 / 256.0, 0.0),
            fontsize=font_size,
            horizontalalignment='center',
            verticalalignment='center',
            axes=self.ax,
        )
        CurvedText(
            x=x_2,
            y=y_2,
            text=self.name,
            color=(0.0, 255.0 / 256.0, 0.0),
            fontsize=font_size,
            horizontalalignment='center',
            verticalalignment='center',
            axes=self.ax,
        )

    @zwave_utils.thread_call
    def create_node(self):
        start = self.start_pos
        end = self.end_pos

        radius = 1.0
        color = self.color_converted
        width = 0.1

        start *= np.pi / 180.0
        end *= np.pi / 180.0
        opt = 4.0 / 3.0 * np.tan((end - start) / 4.0) * radius

        inner = radius * (1 - width)
        verts = [
            polar2xy(radius, start),
            (
                polar2xy(radius, start) +
                polar2xy(opt, start + 0.5 * np.pi)
            ),
            (
                polar2xy(radius, end) +
                polar2xy(opt, end - 0.5 * np.pi)
            ),
            polar2xy(radius, end),
            polar2xy(inner, end),
            (
                polar2xy(inner, end) +
                polar2xy(opt * (1 - width), end - 0.5 * np.pi)
            ),
            (
                polar2xy(inner, start) +
                polar2xy(opt * (1 - width), start + 0.5 * np.pi)
            ),
            polar2xy(inner, start),
            polar2xy(radius, start),
            ]

        codes = [
            Path.MOVETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.LINETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CLOSEPOLY,
        ]

        path = Path(verts, codes)
        patch = patches.PathPatch(
            path,
            facecolor=color + (0.5,),
            edgecolor=color + (0.4,),
            antialiased=True,
            lw=LW
        )
        self.ax.add_patch(patch)

    @zwave_utils.thread_call
    def create_chords(self):
        chordwidth = 0.7
        radius = 0.9

        neighbors = self.neighbors

        for neighbor in neighbors:
            if neighbor is None:
                continue

            color = self.color_converted

            if self.index != 0 and neighbor.chord_width > self.chord_width:
                color = neighbor.color_converted

            neighbor_pos = self.get_neighbor_pos(neighbor.id)
            node_pos = neighbor.get_neighbor_pos(self.id)

            if None in (neighbor_pos, node_pos):
                continue

            start1, end1 = neighbor_pos
            start2, end2 = node_pos

            # start, end should be in [0, 360)
            if start1 > end1:
                start1, end1 = end1, start1
            if start2 > end2:
                start2, end2 = end2, start2
            start1 *= np.pi / 180.0
            end1 *= np.pi / 180.0
            start2 *= np.pi / 180.0
            end2 *= np.pi / 180.0
            opt1 = 4.0 / 3.0 * np.tan((end1 - start1) / 4.0) * radius
            opt2 = 4.0 / 3.0 * np.tan((end2 - start2) / 4.0) * radius
            rchord = radius * (1 - chordwidth)
            verts = [
                polar2xy(radius, start1),
                (
                    polar2xy(radius, start1) +
                    polar2xy(opt1, start1 + 0.5 * np.pi)
                ),
                polar2xy(radius, end1) + polar2xy(opt1, end1 - 0.5 * np.pi),
                polar2xy(radius, end1),
                polar2xy(rchord, end1),
                polar2xy(rchord, start2),
                polar2xy(radius, start2),
                (
                    polar2xy(radius, start2) +
                    polar2xy(opt2, start2 + 0.5 * np.pi)
                ),
                polar2xy(radius, end2) + polar2xy(opt2, end2 - 0.5 * np.pi),
                polar2xy(radius, end2),
                polar2xy(rchord, end2),
                polar2xy(rchord, start1),
                polar2xy(radius, start1),
            ]

            codes = [
                Path.MOVETO,
                Path.CURVE4,
                Path.CURVE4,
                Path.CURVE4,
                Path.CURVE4,
                Path.CURVE4,
                Path.CURVE4,
                Path.CURVE4,
                Path.CURVE4,
                Path.CURVE4,
                Path.CURVE4,
                Path.CURVE4,
                Path.CURVE4,
            ]

            path = Path(verts, codes)
            patch = patches.PathPatch(
                path,
                facecolor=color + (0.5,),
                edgecolor=color + (0.4,),
                antialiased=True,
                lw=LW
            )
            self.ax.add_patch(patch)


def get_coord(magnitude, degrees):
    # angle = np.radians(degrees)
    x = (magnitude * np.cos(degrees))
    y = (magnitude * np.sin(degrees))
    return x, y


def get_polar(x, y):
    r = np.sqrt(x ** 2 + y ** 2)
    t = np.arctan2(y, x)
    return r, t


def polar2xy(r, theta):
    return np.array([r * np.cos(theta), r * np.sin(theta)])


class Plot(object):

    def __init__(self, network):
        self.network = network

        node_id_list = []
        node_list = [network.controller.node] + network.nodes.values()
        for node in node_list:
            node_id_list += [node.id]

        node_id_list = sorted(node_id_list, key=int)

        self.fig = plt.figure(
            figsize=(len(node_id_list) / 4, len(node_id_list) / 4)
        )
        self.ax = plt.axes([0, 0, 1, 1])
        self.nodes = []

        for i, node_id in enumerate(node_id_list):
            for node in node_list:
                if node.id == node_id:
                    self.nodes += [Node(node, self.nodes, self.ax, i)]
            else:
                continue

    @property
    def image(self):
        self.ax.set_xlim(-1.1, 1.1)
        self.ax.set_ylim(-1.1, 1.1)

        threads = []
        for node in self.nodes:
            threads += [
                node.create_node(),
                node.create_chords(),
                node.write_text()
            ]

        while threads:
            for t in threads[:]:
                if not t.isAlive():
                    threads.remove(t)

        self.ax.axis('off')

        buf = BytesIO()
        plt.savefig(
            buf,
            format='png',
            dpi=600,
            transparent=True,
            bbox_inches='tight',
            pad_inches=0.02
        )
        buf.seek(0)
        image = Image.open(buf)

        bg = Image.new(
            image.mode,
            image.size,
            image.getpixel((0, 0))
        )

        diff = ImageChops.difference(image, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        if bbox:
            img = image.crop(bbox)
            img = img.resize(
                (int(image.size[0] * 0.6), int(image.size[0] * 0.6)),
                Image.ANTIALIAS
            )
        else:
            img = image.resize(
                (int(image.size[0] * 0.6), int(image.size[0] * 0.6)),
                Image.ANTIALIAS
            )

        image.close()
        return img, self.nodes

    def close(self):
        self.ax.clear()
        del self.ax
        # plt.close()


class CurvedText(mtext.Text):
    """
    A text object that follows an arbitrary curve.
    """
    def __init__(self, x, y, text, axes, **kwargs):
        super(CurvedText, self).__init__(x[0], y[0], ' ', **kwargs)

        axes.add_artist(self)

        self.__x = x
        self.__y = y
        self.__zorder = self.get_zorder()

        self.__characters = []
        for c in text:
            t = mtext.Text(0, 0, c, **kwargs)

            t.set_ha('center')
            t.set_rotation(0)
            t.set_zorder(self.__zorder + 1)

            self.__characters.append((c, t))
            axes.add_artist(t)

    def set_zorder(self, zorder):
        super(CurvedText, self).set_zorder(zorder)
        self.__zorder = self.get_zorder()
        for c, t in self.__characters:
            t.set_zorder(self.__zorder + 1)

    def draw(self, renderer, *args, **kwargs):
        self.update_positions(renderer)

    def update_positions(self, renderer):
        x_lim = self.axes.get_xlim()
        y_lim = self.axes.get_ylim()
        fig_w, fig_h = self.axes.get_figure().get_size_inches()
        _, _, w, h = self.axes.get_position().bounds
        aspect = (
            ((fig_w * w) / (fig_h * h)) *
            (y_lim[1] - y_lim[0]) /
            (x_lim[1] - x_lim[0])
        )
        x_fig, y_fig = (
            np.array(l) for l in
            zip(
                *self.axes.transData.transform(
                    [(i, j) for i, j in zip(self.__x, self.__y)]
                )
            )
        )

        x_fig_dist = (x_fig[1:] - x_fig[:-1])
        y_fig_dist = (y_fig[1:] - y_fig[:-1])
        r_fig_dist = np.sqrt(x_fig_dist ** 2 + y_fig_dist ** 2)

        l_fig = np.insert(np.cumsum(r_fig_dist), 0, 0)
        rads = np.arctan2(
            (y_fig[1:] - y_fig[:-1]),
            (x_fig[1:] - x_fig[:-1])
        )

        degs = np.rad2deg(rads)

        rel_pos = 10
        for c, t in self.__characters:
            t.set_rotation(0)
            t.set_va('center')
            bbox1 = t.get_window_extent(renderer=renderer)
            w = bbox1.width

            if rel_pos + w / 2 > l_fig[-1]:
                t.set_alpha(0.0)
                rel_pos += w / 2
                continue

            elif c != ' ':
                t.set_alpha(1.0)

            il = np.where(rel_pos + w / 2 >= l_fig)[0][-1]
            ir = np.where(rel_pos + w / 2 <= l_fig)[0][0]

            if ir == il:
                ir += 1

            used = l_fig[il] - rel_pos
            rel_pos = l_fig[il]

            fraction = (w / 2 - used) / r_fig_dist[il]

            x = self.__x[il] + fraction * (self.__x[ir] - self.__x[il])
            y = self.__y[il] + fraction * (self.__y[ir] - self.__y[il])

            t.set_va(self.get_va())
            bbox2 = t.get_window_extent(renderer=renderer)

            bbox1d = self.axes.transData.inverted().transform(bbox1)
            bbox2d = self.axes.transData.inverted().transform(bbox2)
            dr = np.array(bbox2d[0]-bbox1d[0])

            rad = rads[il]
            rot_mat = np.array([
                [math.cos(rad), math.sin(rad) * aspect],
                [-math.sin(rad) / aspect, math.cos(rad)]
            ])

            drp = np.dot(dr, rot_mat)

            t.set_position(np.array([x, y]) + drp)
            t.set_rotation(degs[il])

            t.set_va('center')
            t.set_ha('center')

            rel_pos += w-used
