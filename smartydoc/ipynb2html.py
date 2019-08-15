# vi: set ft=python sts=4 ts=4 sw=4 et:

import os
from html.parser import HTMLParser

class IpyNBHTMLParser(HTMLParser):
    def __init__(self):
        super(IpyNBHTMLParser, self).__init__()
        self.out_html = ''
        self.toc_html = ''
        self.tag_stack = []

    def handle_starttag(self, tag, attrs):
        tag_content = {}
        for attr in attrs:
            tag_content[attr[0]] = attr[1]
        # XXX: to be extened
        if tag not in ['meta', 'link', 'img', 'br', 'a']:
            if tag=='h1' or tag=='h2':
                while self.tag_stack[-1] in ['article', 'div', 'section']:
                    self.out_html += '</' + self.tag_stack[-1] + '>\n'
                    self.tag_stack.pop(-1)
                self.tag_stack.append('article')
                self.out_html += "<article id='%s'>\n"%(tag_content['id'])
                self.tag_stack.append(tag)
                h_content = [tag]
                for key in tag_content:
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
                    h_content.append("%s='%s'"%(key, tag_content[key]))
                self.out_html += '<' + ' '.join(h_content) + '>\n'
            else:
                self.tag_stack.append(tag)
                h_content = [tag]
                for key in tag_content:
                    h_content.append("%s='%s'"%(key, tag_content[key]))
                self.out_html += '<' + ' '.join(h_content) + '>\n'
            # get TOC info
            if tag in ['h2', 'h3']:
                self.toc_html += '<li><a href="#%s"></a></li>\n'%(tag_content['id'])
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
            while self.tag_stack[-1] in ['article', 'div', 'section']:
                self.out_html += '</' + self.tag_stack[-1] + '>\n'
                self.tag_stack.pop(-1)
            self.tag_stack.pop(-1)
        else:
            print(self.tag_stack)
            print('Unrecognized tag %s'%(tag))

    def handle_data(self, data):
        if not self.tag_stack[-1]=='a':
            self.out_html += data

    def handle_charref(self, name):
        pass

    def export2html(self, html_file):
        with open(html_file, 'w') as f:
            split_toc = self.toc_html.split('\n')
            split_content = self.out_html.split('\n')
            cover_start_flag = False
            for line in split_content:
                print(line)
                f.write(line+'\n')
                if line=="<article id='cover'>":
                    cover_start_flag = True
                if line=='</article>' and cover_start_flag:
                    f.write('<article id="contents">\n')
                    f.write('<h2>目录</h2>\n')
                    f.write('<ul>\n')
                    for item in split_toc:
                        f.write(item+'\n')
                    f.write('</ul>\n</article>\n')
                    cover_start_flag = False

