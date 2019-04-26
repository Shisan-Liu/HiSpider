from lxml import etree
filename = 'index'
newfilename = 'new'
with open("./HTML/index.html",'r',encoding='utf-8') as f:
    html = f.read()
    html = etree.HTML(html)
    result = etree.tostring(html)       
    html = result.decode('utf-8')                       # 补全html代码
    with open("./HTML/newindex.html",'w',encoding='utf-8') as target:
        target.write(html)
