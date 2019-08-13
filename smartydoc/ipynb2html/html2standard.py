# vi: set ft=python sts=4 ts=4 sw=4 et:

from ipynbhtmlparser import IpyNBHTMLarser

def module_test():
    # load test.html
    content = open('test.html').readlines()
    content = [line.strip() for line in content]
    content = [line for line in content if len(line)]

    parser = IpyNBHTMLParser()
    for line in content:
        #print(line)
        parser.feed(line)
        #print(parser.tag_stack)

    with open('test_standard.html', 'w') as f:
        f.write(parser.out_html)


if __name__=='__main__':
    module_test()

