# vi: set ft=python sts=4 ts=4 sw=4 et:

import os
import random

import plotly.graph_objects as go
import svgutils.compose as sc


class FigCounter(object):
    """Used for generate figure/table number."""
    def __init__(self, prefix, start_num=1,
                 font_size=12, font_family='Courier New, monospace'):
        """
        `prefix`: string, e.g. fig, figure, table.
        `start_num`: int, default value 1.
        """
        self.prefix = prefix
        self.start_num = start_num
        self.current_num = start_num
        self.font_size = font_size
        self.font_family = font_family
        #self.tmp_dir = os.path.join('/tmp', 'smartydoc-figcounter')
        #if not os.path.exists(self.tmp_dir):
        #    os.makedirs(self.tmp_dir, mode=0o755)

    def add_title(self, fig, title):
        """
        `fig`: a plotly/svgutils Figure object.
        `title`: figure title.
        """
        assert isinstance(fig, go.Figure) or isinstance(fig, sc.Figure)

        # if input a plotly Figure object, convert it into a svg file first
        title_txt = '%s%s  '%(self.prefix, self.current_num) + title
        if isinstance(fig, go.Figure):
            fig.update_layout(
                    title=dict(
                        text=title_txt,
                        x=0.5,
                        y=0.15,
                        font=dict(
                            family=self.font_family,
                            size=self.font_size,
                            color="#000000",
                        )
                    )
            )
 
            # increasing counter number
            self.current_num += 1

            return fig
        else:
            new_width = fig.width
            new_height = fig.height
            new_height.value += 10

            # add title
            new_figure = sc.Figure(new_width.to('px').value,
                                   new_height.to('px').value,
                                   fig,
                                   sc.Text(title_txt,
                                           new_width.to('px').value/2,
                                           new_height.to('px').value-5,
                                           anchor='middle',
                                           size=self.font_size,
                                           font=self.font_family,
                                           #weight="bold",
                                           )
            )
        
            # increasing counter number
            self.current_num += 1

            return new_figure


