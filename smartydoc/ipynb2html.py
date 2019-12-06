# vi: set ft=python sts=4 ts=4 sw=4 et:

import os
from collections import OrderedDict
from html.parser import HTMLParser

class IpyNBHTMLParser(HTMLParser):
    def __init__(self):
        super(IpyNBHTMLParser, self).__init__()
        self.out_html = ''
        self.tag_stack = []
        self.toc_tree = OrderedDict()
        self._cur_toc_pos = OrderedDict()

    def handle_starttag(self, tag, attrs):
        tag_content = {}
        for attr in attrs:
            tag_content[attr[0]] = attr[1]
        # XXX: to be extened
        if tag not in ['meta', 'link', 'img', 'br', 'a']:
            if tag=='h1' or tag=='h2':
                while self.tag_stack[-1] in ['article', 'article_content',
                                             'div', 'section']:
                    self.out_html += '</' + self.tag_stack[-1] + '>\n'
                    self.tag_stack.pop(-1)
                self.tag_stack.append('article')
                self.out_html += "<article id='%s'>\n"%(tag_content['id'])
                self.tag_stack.append('article_content')
                self.out_html += "<article_content>\n"
                self.tag_stack.append(tag)
                h_content = [tag]
                for key in tag_content:
                    if key=='id':
                        h_content.append("%s='%s-title'"%(key, tag_content[key]))
                    else:
                        h_content.append("%s='%s'"%(key, tag_content[key]))
                self.out_html += '<' + ' '.join(h_content) + '>\n'
            elif tag=='h3':
                if self.tag_stack[-1]=='section':
                    self.out_html += '</' + self.tag_stack[-1] + '>\n'
                    self.tag_stack.pop(-1)
                self.tag_stack.append('section')
                self.out_html += "<section id='%s'>\n"%(tag_content['id'])
                self.tag_stack.append(tag)
                h_content = [tag]
                for key in tag_content:
                    if key=='id':
                        h_content.append("%s='%s-title'"%(key, tag_content[key]))
                    else:
                        h_content.append("%s='%s'"%(key, tag_content[key]))
                self.out_html += '<' + ' '.join(h_content) + '>\n'
            elif tag=='h4':
                self.tag_stack.append(tag)
                h_content = [tag]
                for key in tag_content:
                    if key=='id':
                        h_content.append("%s='%s-title'"%(key, tag_content[key]))
                    else:
                        h_content.append("%s='%s'"%(key, tag_content[key]))
                self.out_html += '<' + ' '.join(h_content) + '>\n'
            else:
                self.tag_stack.append(tag)
                h_content = [tag]
                for key in tag_content:
                    h_content.append("%s='%s'"%(key, tag_content[key]))
                self.out_html += '<' + ' '.join(h_content) + '>\n'

            # get TOC tree
            if tag in ['h2', 'h3', 'h4']:
                _tag_level = int(tag[1])
                _cur_toc_tags = list(self._cur_toc_pos.keys())
                _ins_toc_level = sum(
                    [int(item[1]) < _tag_level for item in _cur_toc_tags]
                )

                if len(_cur_toc_tags)==0:
                    self.toc_tree['hlevel'] = tag
                    self.toc_tree[tag_content['id']] = OrderedDict()
                    self._cur_toc_pos[tag] = tag_content['id']
                else:
                    _del_toc_tags = _cur_toc_tags[_ins_toc_level:]
                    for t in _del_toc_tags:
                        self._cur_toc_pos.pop(t)
                    _sel_cur_toc_tags = _cur_toc_tags[:_ins_toc_level]
                    pxy = self.toc_tree
                    for k in _sel_cur_toc_tags:
                        pxy = pxy[self._cur_toc_pos[k]]
                    if ('hlevel' in pxy) and (not pxy['hlevel']==tag):
                        print('Error: Invalid tag encountered while generating contents!')
                        print(tag_content)
                        return
                    else:
                        pxy[tag_content['id']] = OrderedDict()
                        pxy['hlevel'] = tag
                        self._cur_toc_pos[tag] = tag_content['id']

        # XXX: tags to be ignored
        elif tag in ['br']:
            self.out_html += '<' + tag + '>'
        # XXX: tags to be removed
        elif tag in ['a']:
            self.tag_stack.append(tag)
        else:
            h_content = [tag]
            for key in tag_content:
                h_content.append("%s='%s'"%(key, tag_content[key]))
            self.out_html += '<' + ' '.join(h_content) + '>\n'

    def handle_endtag(self, tag):
        if self.tag_stack[-1]==tag:
            if tag=='a':
                self.tag_stack.pop(-1)
            else:
                self.out_html += '</' + tag + '>\n'
                self.tag_stack.pop(-1)
                if tag=='h1' or tag=='h2':
                    self.tag_stack.append('div')
                    self.out_html += '<div>\n'
        elif tag=='body':
            while self.tag_stack[-1] in ['article', 'article_content',
                                         'div', 'section']:
                self.out_html += '</' + self.tag_stack[-1] + '>\n'
                self.tag_stack.pop(-1)
            self.out_html += '</body>\n'
            self.tag_stack.pop(-1)
        else:
            print(self.tag_stack)
            print('Unrecognized tag %s'%(tag))

    def handle_data(self, data):
        if not self.tag_stack[-1]=='a':
            self.out_html += data

    def handle_charref(self, name):
        pass

    def export2html(self, html_file, toc_level=1):
        """toc_level: 0 for no toc"""
        with open(html_file, 'w') as f:
            split_content = self.out_html.split('\n')
            cover_start_flag = False
            for line in split_content:
                #print(line)
                f.write(line+'\n')
                if line=="<article id='cover'>":
                    cover_start_flag = True
                if line=='</article>' and cover_start_flag:
                    if toc_level==1:
                        f.write('<article id="contents">\n')
                        f.write('<article_content>\n')
                        f.write('<h2>目录</h2>\n')
                        f.write('<ul>\n')
                        for k in self.toc_tree:
                            if not k=='hlevel':
                                f.write('<li><a href="#%s-title"></a></li>\n'%(k))
                        f.write('</ul>\n</article_content>\n</article>\n')
                    elif toc_level==2:
                        f.write('<article id="contents">\n')
                        f.write('<article_content>\n')
                        f.write('<h2>目录</h2>\n')
                        for h2 in self.toc_tree:
                            if not h2=='hlevel':
                                f.write('<h3>%s</h3>\n'%(h2))
                                h3s = self.toc_tree[h2]
                                if h3s:
                                    f.write('<ul class="h3">\n')
                                    for h3 in h3s:
                                        if not h3=='hlevel':
                                            f.write('<li><a href="#%s-title"></a></li>\n'%(h3))
                                    f.write('</ul>\n')
                        f.write('</article_content>\n</article>\n')
                    elif toc_level==3:
                        f.write('<article id="contents">\n')
                        f.write('<article_content>\n')
                        f.write('<h2>目录</h2>\n')
                        for h2 in self.toc_tree:
                            if not h2=='hlevel':
                                f.write('<h3>%s</h3>\n'%(h2))
                                h3s = self.toc_tree[h2]
                                if h3s:
                                    f.write('<ul class="h3">\n')
                                    for h3 in h3s:
                                        if not h3=='hlevel':
                                            f.write('<li><a href="#%s-title"></a></li>\n'%(h3))
                                            h4s = h3s[h3]
                                            if h4s:
                                                f.write('<ul class="h4">\n')
                                                for h4 in h4s:
                                                    if not h4=='hlevel':
                                                        f.write('<li><a href="#%s-title"></a></li>\n'%(h4))
                                                f.write('</ul>\n')
                                    f.write('</ul>\n')
                        f.write('</article_content>\n</article>\n')
                    else:
                        # no TOC
                        pass

                    cover_start_flag = False

