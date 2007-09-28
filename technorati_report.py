import urllib2
import BeautifulSoup

def grab_urls():
    url = 'http://www.technorati.com/pop/blogs/'
    s = urllib2.urlopen(url).read()
    u = unicode(s, 'utf-8')
    b = BeautifulSoup.BeautifulSoup(u)
    ol = b('ol')[0]
    links = ol('a', {'class': 'url'})
    urls = [a['href'] for a in links]
    return urls

def is_cc_licensed_lame_way(s):
    return 'http://creativecommons.org/' in s

def is_cc_licensed_rdf_lame_way(s):
    return '<License rdf:about="http://creativecommons.org' in s

def is_cc_licensed_soup_way(s):
    soup = BeautifulSoup.BeautifulSoup(s)
    rel_license = soup('', {'rel': 'license'})
    if rel_license:
        if 'http://creativecommons.org/' in rel_license[0]['href']:
            return True
    return False

def main():
    urls = grab_urls()
    ret = {}
    for url in urls:
        try:
            s = urllib2.urlopen(url).read()
            lame = is_cc_licensed_lame_way(s)
            good = (is_cc_licensed_soup_way(s) or is_cc_licensed_rdf_lame_way(s))

            if lame == good:
                ret[url] = good
            else:
                print 'lame is', lame, 'while RDF lame is', is_cc_licensed_rdf_lame_way(s)
                print 'and rel license way is', is_cc_licensed_soup_way(s)
                print 'for url', url
                ret[url] = True

        except urllib2.URLError, e:
            ret[url] = e
    print ret


    
