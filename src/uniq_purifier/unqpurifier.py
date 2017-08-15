from src.parse import htmlParser as parse
from src.altparse import alt_htmlparser as altparse
from urllib.parse import urlsplit, urlunsplit


def split_links(link, basetocheck, parser):
    inlinks = []
    outlinks = []
    link=str(link)
    print(link)
    if ( ("–" in link) or (" " in link) ):
       return inlinks, outlinks
    #if (parse.isParsable(link)):
    
    if (parser==1):
        t, html_page = parse.parse(link)
        if (not t):
            return inlinks, outlinks
        soup = parse.make_soup(html_page=html_page)
        links = parse.get_links(soup)
    else:
        t, html_page=altparse.parse(link)
        if (not t):
            return inlinks, outlinks
        links=altparse.get_links(html_page)
        
    
    for index in links:
        index=str(index)
        if ( (basetocheck in index) and (index[0:4]=='http') ):
            inlinks.append(index)
        elif(index[0:4]=='http'):
            splited = urlsplit(index)
            base = "{0.scheme}://{0.netloc}/".format(splited)
            outlinks.append(base)
        
    outlinks=set(outlinks)
    outlinks=list(outlinks)
    print(outlinks)
    inlinks=set(inlinks)
    inlinks=list(inlinks)
    return inlinks, outlinks


def clean_links(outlinks, linkToCheck):   #merged in split_link
    clear_outlinks = []
    for link in outlinks:
        splited = urlsplit(link)
        base = "{0.scheme}://{0.netloc}/".format(splited)
        check = "{0.netloc}".format(urlsplit(linkToCheck))
        if (check.count(".")==2):
            www, link, dom = check.split(".")
        else:
            link, dom = check.split(".")
        checkIt = link + "." + dom
        if base[:4] == 'http' and checkIt not in base:
            clear_outlinks.append(base)
    return clear_outlinks


def find_outlinks(link, checkin, basetocheck, n):
    inlinks = link
    inlinks2 = []
    
    if (n==1):
        basetocheck=getBaseToCheck(link)
        
    inlinks, outlinks = split_links(link, basetocheck, 2)
    if n==1:
        print(len(inlinks))
        
    if (n==1):
        if (len(inlinks)==0):
            checkin=False
        else:
            checkin=True
    if n == 2:
        return checkin, outlinks
    count=0
    for i in inlinks:
        # find_outlinks()
        count=count+1
        print(count)
        ch, outlink = find_outlinks(i, checkin, basetocheck, n+1)
        for j in outlink:
            if j not in outlinks:
                # inlinks.append(j)
                outlinks.append(j)
    return checkin, outlinks


def getBaseToCheck(link):
    check = "{0.netloc}".format(urlsplit(link))

    if (check.count(".")==2):
        www, link2check, dom = check.split(".")
    elif (check.count(".")==1):
        link2check, dom = check.split(".")
    elif (check.count(".")==3):
        www, link2check, blog, dom = check.split(".")
    else:
        www, link2check, blog, bla, dom = check.split(".")
    return link2check


#link=
#print(getBaseToCheck(link))
#bs2ch=getBaseToCheck(link)
#print(split_links(link, bs2ch, 1)[0])
#in2, out = find_outlinks(link, False, bs2ch, 1)
#print(out)
#print(find_outlinks('http://www.sport24.gr/', len('http://www.sport24.gr/'), 1))
#link='http://www.sport24.gr/'
#print(clean_links(split_links('http://www.sport24.gr/', len('http://www.sport24.gr/'))[1],link))
#inlinks=split_links('http://www.sport24.gr/',2)[1]
#print(inlinks)
#out1=split_links('http://www.sport24.gr/',1)[1]
#print(" ")
#print(out1)
#in2, out2= find_outlinks('http://www.sport24.gr/',False,1)
#print(in2)
#print(" ")
#print(out2)
#print(split_links('http://www.sport24.gr/')[1])
#splited = urlsplit(link)
#print(splited)
#base = "{0.scheme}://{0.netloc}/".format(splited)
#print(base)
#check = "{0.netloc}".format(urlsplit(link))
#print(check)
#www, link, dom = check.split(".")
#print(www,link,dom)
