# vi: set ft=python sts=4 ts=4 sw=4 et:

import os

def draw_table(head, cells, foot=None):
    """Draw a data table.
    Args:
        `head`  : table header, a list of string
        `cells` : table content, a list of list, each list of data corresponds
                  to one row in the table.
        `foot`  : table footer, a list of string, None for default.

    Example:
        draw_table(header=['col A', 'col B', 'col C', 'col D'],
                   cells=[[1, 'a', 'text', 2.15],
                          [2, 'b', 'info', 3.14],
                          [3, 'c', 'book', 8.0 ]])

    """
    # check input data type
    assert isinstance(head, list) and isinstance(cells, list)

    html_content = []
    
    # add table spec
    html_content.append('<table border="1">')
    
    # add table head
    html_content.append('<thead>')
    html_content.append('<tr>')
    for item in head:
        html_content.append('<th>%s</th>'%(item))
    html_content.append('</tr>')
    html_content.append('</thead>')
    
    # add table foot
    if foot:
        html_content.append('<tfoot>')
        html_content.append('<tr>')
        for item in foot:
            html_content.append('<td>%s</td>'%(item))
        html_content.append('</tr>')
        html_content.append('</tfoot>')
    
    # add table body
    html_content.append('<tbody>')
    for c in cells:
        html_content.append('<tr>')
        for item in c:
            html_content.append('<td>%s</td>'%(item))
        html_content.append('</tr>')
    html_content.append('</tbody>')

    # table end
    html_content.append('</table>')

    return '\n'.join(html_content)


