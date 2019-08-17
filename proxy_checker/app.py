import urllib2, socket

socket.setdefaulttimeout(180)


fproxy = "proxylist.txt"
with open(fproxy) as f:
    proxyList = f.readlines()
proxyList = [x.strip() for x in proxyList] 

fsite = "urllist.txt"
with open(fsite) as f:
    siteList = f.readlines()
siteList = [x.strip() for x in siteList] 

def is_bad_proxy(pip,url):    
    try:        
        proxy_handler = urllib2.ProxyHandler({'http': pip})        
        opener = urllib2.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib2.install_opener(opener)        
        req=urllib2.Request(url)  # change the url address here
        # req=urllib2.Request('http://www.google.com')  # change the url address here
        sock=urllib2.urlopen(req)
    except urllib2.HTTPError, e:        
        print 'Error code: ', e.code
        return e.code
    except Exception, detail:
        print "ERROR:", detail
        return 1
    return 0

for item in proxyList:
    for url in siteList:
        if is_bad_proxy(item,url):
            print "Bad Proxy", url +' - '+ item
            # print "Bad Proxy", item
        else:
            print url +' - '+ item, "is working"
            # print item, "is working"

# print siteList
