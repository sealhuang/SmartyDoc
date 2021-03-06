# vi: set ft=python sts=4 ts=4 sw=4 et:

import os
from math import ceil

from PIL import Image

import plotly.graph_objects as go
import svgutils.compose as sc


class FigCounter(object):
    """Used for generate figure/table number."""
    def __init__(self, prefix, start_num=1, font_size=12,
                 font_family='Courier New, monospace'):
        """
        `prefix`: string, e.g. fig, figure, table.
        `start_num`: int, default value 1.
        """
        self.prefix = prefix
        self.start_num = start_num
        self.current_num = start_num
        self.font_size = font_size
        self.font_family = font_family
        # defaul width: 600 px ~ 169 mm
        self.output_width = 600

    def set_width(self, w):
        """Set width of the output image in px."""
        if isinstance(w, int):
            self.output_width = w
        else:
            print('Invalid input value, only int data type supported.')

    def get_current_num(self):
        """Get next counter number."""
        # increasing counter number
        self.current_num += 1
        return self.current_num - 1

    def add_title(self, fig, title, y_pos=-0.2, w=None):
        """
        `fig`: a plotly/svgutils Figure object, or the path of a png file.
        `title`: figure title.
        `w`: output image width in px.
        """
        if isinstance(fig, str):
            if not os.path.exists(fig):
                print('File %s does exist!'%(fig))
                return
            if not os.path.splitext(os.path.abspath(fig))[-1]=='.png':
                print('Only png image supported.')
                return

            im = Image.open(fig)
            if w:
                _w = w
            else:
                _w = self.output_width
            _scalar = _w * 1.0 / im.width
            
            svg_fig = sc.Figure(_w, ceil(_scalar * im.height),
                                sc.Image(
                                    im.width,
                                    im.height,
                                    fig
                                ).scale(_scalar)
            )
            
            fig = svg_fig

        assert isinstance(fig, go.Figure) or isinstance(fig, sc.Figure)

        # if input a plotly Figure object, convert it into a svg file first
        title_txt = '%s%s  '%(self.prefix, self.current_num) + title
        if isinstance(fig, go.Figure):
            # compute image size
            if w:
                _w = w
            else:
                _w = self.output_width
            if not fig.layout.width is None:
                _scalar = _w * 1.0 / fig.layout.width
            else:
                # default width is 700px
                _scalar = _w * 1.0 / 700

            if not fig.layout.height is None:
                _h = fig.layout.height * _scalar
            else:
                # default height is 450px
                _h = 450.0 * _scalar
           
            title_annotation = go.layout.Annotation(
                            xref = 'paper',
                            yref = 'paper',
                            x = 0.5,
                            y = y_pos,
                            xanchor = 'center',
                            yanchor = 'top',
                            text = title_txt,
                            font = dict(
                                family = self.font_family,
                                size = self.font_size,
                                color = "#000000",
                            ),
                            showarrow = False,
            )

            fig.update_layout(
                width = _w,
                height = _h,
                annotations = list(fig.layout['annotations']) + [title_annotation],
            )
 
            # increasing counter number
            self.current_num += 1

            return fig
        else:
            # compute image size
            if w:
                _w = w
            else:
                _w = self.output_width
            _scalar = _w * 1.0 / fig.width.value
            _h = fig.height.value * _scalar + 25

            if y_pos==-0.2:
                text_y = _h - 5
            else:
                assert y_pos<=1 and y_pos>=0
                text_y = int(_h*(1-y_pos))
            
            # if w < default output width, add margin
            if _w < self.output_width:
                _outw = self.output_width
                _move_x = int((_outw - _w) / 2)
            else:
                _outw = _w
                _move_x = int((_outw - _w) / 2)

            # add title
            new_figure = sc.Figure(_outw, _h,
                                   fig.scale(_scalar).move(_move_x, 0),
                                   sc.Text(title_txt,
                                           _outw / 2,
                                           text_y,
                                           anchor='middle',
                                           size=self.font_size,
                                           font=self.font_family,
                                           )
            )
        
            # increasing counter number
            self.current_num += 1

            return new_figure


