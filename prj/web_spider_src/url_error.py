import urllib.request
import sys

req = urllib.request.Request('http://www.baidu.com')
print(req)

#try :
#    urllib.request.urlopen(req)
#except (urllib.error.URLError,e):
#    print( e.reason )
#    print("Unexpected error:", sys.exc_info()[0])
#    raise

