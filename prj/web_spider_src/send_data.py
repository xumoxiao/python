import urllib.parse
import urllib.request
url = 'http://localhost/login.php'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
values = {
'act' : 'login',
'login[email]' : 'yzhang@i9i8.com',
'login[password]' : '123456'
}
data = urllib.parse.urlencode(values)
req = urllib.request.Request(url, data)
req.add_header('Referer', 'http://www.python.org/')
response = urllib.request.urlopen(req)
the_page = response.read()
print(the_page.decode("utf8"))