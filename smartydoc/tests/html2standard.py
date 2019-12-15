# vi: set ft=python sts=4 ts=4 sw=4 et:

from smartydoc.ipynb2html import IpyNBHTMLParser

def module_test():
    # load test.html
    content = open('test.html').readlines()
    content = [line.strip() for line in content]
    content = [line for line in content if len(line)]

    parser = IpyNBHTMLParser()
    for line in content:
        #print(line)
        #print(parser.tag_stack)
        parser.feed(line)

    parser.export2html('test_standard.html', toc_level=1,
                       include_article_summary=False)


if __name__=='__main__':
    module_test()

