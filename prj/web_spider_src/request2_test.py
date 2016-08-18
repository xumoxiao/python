import requests
html = requests.get("http://www.baidu.com")
print(html)
code = html.encoding
print(code)
page_status = html.status_code
print(page_status)

with open('test.txt','w',encoding='utf-8') as f:
    f.write(html.text)




ff = open('test1.txt','w',encoding='utf-8')
with open('test.txt',encoding='utf-8')as f:
    for line in f:
            ff.write(line)