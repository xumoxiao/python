
# get code of given URL as html text string
# Python3 uses urllib.request.urlopen()
# instead of Python2's urllib.urlopen() or urllib2.urlopen()

#import urllib.request
#
#fp = urllib.request.urlopen("http://www.python.org")
#
#mybytes = fp.read()
## note that Python3 does not read the html code as string
## but as html code bytearray, convert to string with
#mystr = mybytes.decode("utf8")
#
#fp.close()
#
#print(mystr)

# get the code of a given URL as html text string
# Python3 uses urllib.request.urlopen()
# get the encoding used first
# tested with Python 3.1 with the Editra IDE

import urllib.request


def extract(text, sub1, sub2):
    """
    extract a substring from text between first
    occurances of substrings sub1 and sub2
    """
    return text.split(sub1, 1)[-1].split(sub2, 1)[0]


fp = urllib.request.urlopen("http://www.baidu.com")

mybytes = fp.read()

encoding = extract(str(mybytes).lower(), 'charset=', '"')
print('-' * 50)
print("Encoding type = %s" % encoding)
print('-' * 50)

if encoding:
    # note that Python3 does not read the html code as string
    # but as html code bytearray, convert to string with
    mystr = mybytes.decode('utf-8')
    print(mybytes)
else:
    print("Encoding type not found!")

fp.close()
