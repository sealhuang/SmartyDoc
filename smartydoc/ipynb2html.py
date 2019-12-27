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
        self._article_intro = OrderedDict()
        self._article_intro_flag = False
        # heading index vars
        self._h2_idx = 0
        self._h3_idx = 0
        self._h4_idx = 0
        self._anchor_link = False

    def handle_starttag(self, tag, attrs):
        tag_content = {}
        for attr in attrs:
            tag_content[attr[0]] = attr[1]
        # XXX: unpaired tags to be extened
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
                if tag=='h1':
                    self.out_html += '<' + ' '.join(h_content) + '>'
                else:
                    self._h2_idx += 1
                    self._h3_idx = 0
                    self._h4_idx = 0
                    self.out_html += '<' + ' '.join(h_content) + '>' + str(self._h2_idx) + '. '
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
                self._h3_idx += 1
                self._h4_idx = 0
                self.out_html += '<' + ' '.join(h_content) + '>' + '.'.join([str(self._h2_idx), str(self._h3_idx)]) + ' '
            elif tag=='h4':
                self.tag_stack.append(tag)
                h_content = [tag]
                for key in tag_content:
                    if key=='id':
                        h_content.append("%s='%s-title'"%(key, tag_content[key]))
                    else:
                        h_content.append("%s='%s'"%(key, tag_content[key]))
                self._h4_idx += 1
                self.out_html += '<' + ' '.join(h_content) + '>' + '.'.join([str(self._h2_idx), str(self._h3_idx), str(self._h4_idx)]) + ' '
            elif tag=='article_intro':
                self.tag_stack.append(tag)
                self._article_intro_flag = True
                self._article_intro[self._h2_idx] = ''
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
            if 'class' in tag_content and tag_content['class']=='anchor-link':
                self._anchor_link = True
        else:
            h_content = [tag]
            for key in tag_content:
                h_content.append("%s='%s'"%(key, tag_content[key]))
            self.out_html += '<' + ' '.join(h_content) + '>\n'

    def handle_endtag(self, tag):
        if self.tag_stack[-1]==tag:
            if tag=='a':
                self.tag_stack.pop(-1)
                if self._anchor_link:
                    self._anchor_link = False
            elif tag=='article_intro':
                self.tag_stack.pop(-1)
                self._article_intro_flag = False
                #print(self._article_intro)
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
        if (not self._anchor_link) and (not self._article_intro_flag):
            self.out_html += data
        if self._article_intro_flag:
            self._article_intro[self._h2_idx] += data

    def handle_charref(self, name):
        pass

    def export2html(self, html_file, toc_level=1,
                    include_article_summary=False):
        """toc_level: 0 for no toc.
        include_article_summary: 'toc', 'intro', or False.
        
        """
        h2_idx = 1
        with open(html_file, 'w') as f:
            split_content = self.out_html.split('\n')
            cover_start_flag = False
            toc_over_flag = False
            for line in split_content:
                #print(line)
                
                # add article summary
                if line.startswith('<article id=') and toc_over_flag:
                    # add article toc
                    if include_article_summary == 'toc':
                        h2_id = line[13:-2]
                        f.write('<article class="article-toc">\n')
                        f.write('<h2>%s</h2>\n'%(h2_id))
                        h3s = self.toc_tree[h2_id]
                        if h3s:
                            f.write('<ul class="summary-list">\n')
                            for h3 in h3s:
                                if h3=='hlevel':
                                    continue
                                f.write('<li>%s</li>\n'%(h3))
                            f.write('</ul>\n')
                        f.write('</article>\n')
 
                    # add article introduction
                    if include_article_summary == 'intro':
                        h2_id = line[13:-2]
                        f.write('<article class="article-summary">\n')
                        f.write('<h2>%s</h2>\n'%(h2_id))
                        if h2_idx in self._article_intro:
                            f.write('<article_intro>')
                            f.write(self._article_intro[h2_idx]+'\n')
                            f.write('</article_intro>\n')
                        f.write('</article>\n')
                        h2_idx += 1

                if line.startswith('<h2 id=') and include_article_summary:
                    continue
                if line[-5:]=='</h2>' and include_article_summary:
                    continue
                
                f.write(line+'\n')
 
                if line=="<article id='cover'>":
                    cover_start_flag = True
                if line=='</article>' and cover_start_flag:
                    # add TOC
                    if toc_level==1:
                        f.write('<article id="contents">\n')
                        f.write('<article_content>\n')
                        f.write('<h2>目录</h2>\n')
                        f.write('<ul>\n')
                        for k in self.toc_tree:
                            if not k=='hlevel':
                                f.write('<li>\n')
                                f.write('<a href="#%s-title" class="toc-title"></a>\n'%(k))
                                f.write('<div class="list-line"></div>\n')
                                f.write('<a href="#%s-title" class="toc-page"></a>\n'%(k))
                                f.write('</li>\n')
                        f.write('</ul>\n</article_content>\n</article>\n')
                    elif toc_level>1:
                        f.write('<article id="contents">\n')
                        f.write('<article_content>\n')
                        f.write('<h2>目录</h2>\n')
                        _h2_tmp_idx = 1
                        for h2 in self.toc_tree:
                            if h2=='hlevel':
                                continue
                            f.write('<h3>%s</h3>\n'%(str(_h2_tmp_idx)+'. ' + h2))
                            _h2_tmp_idx += 1
                            h3s = self.toc_tree[h2]
                            if h3s:
                                f.write('<ul class="h3">\n')
                                for h3 in h3s:
                                    if h3=='hlevel':
                                        continue
                                    #f.write('<li><a href="#%s-title"></a><div class="list-line"></div></li>\n'%(h3))
                                    f.write('<li>\n')
                                    f.write('<a href="#%s-title" class="toc-title"></a>\n'%(h3))
                                    f.write('<div class="list-line"></div>\n')
                                    f.write('<a href="#%s-title" class="toc-page"></a>\n'%(h3))
                                    f.write('</li>\n')
                                    if toc_level>2:
                                        h4s = h3s[h3]
                                        if h4s:
                                            f.write('<ul class="h4">\n')
                                            for h4 in h4s:
                                                if h4=='hlevel':
                                                    continue
                                                #f.write('<li><a href="#%s-title"></a><div class="list-line"></div></li>\n'%(h4))
                                                f.write('<li>\n')
                                                f.write('<a href="#%s-title" class="toc-title"></a>\n'%(h4))
                                                f.write('<div class="list-line"></div>\n')
                                                f.write('<a href="#%s-title" class="toc-page"></a>\n'%(h4))
                                                f.write('</li>\n')
                                            f.write('</ul>\n')
                                f.write('</ul>\n')
                        f.write('</article_content>\n</article>\n')
                    else:
                        # no TOC
                        pass

                    cover_start_flag = False
                    toc_over_flag = True



