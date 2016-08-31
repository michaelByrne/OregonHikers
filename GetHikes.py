import re
from mwclient import Site
import sys
import requests



reload(sys)
sys.setdefaultencoding('utf-8')


class Hike():
    def __init__(self,lat,long):
        self.lat = float(lat)
        self.long = float(long)



def Hikes():
    site = Site(('http','www.oregonhikers.org/'))
    counter = 0
    hikes = []
    for item in site.allpages():
        page_text = item.text()
        if '[[Category:Hikes]]' in page_text:
            if '[[Category:Portland Area]]' in page_text:
                counter += 1
                if (counter==30):
                    break
                m = re.search('(?<=latitude=).{6}', page_text)
                n = re.search('(?<=longitude=).{7}', page_text)
                p = re.search('(?<=Distance\|)(.*)(?=miles}})',page_text)
                q = re.search('(?<=Difficulty\|)(.*)(?=}})',page_text)
                lat = 0.0
                long = 0.0
                distance = 0.0
                difficulty = "None given"
                if (m):
                    try:
                        lat = float(m.group())
                    except:
                        print("no lat given")
                if (n):
                    try:
                        long = float(n.group())
                    except:
                        print("no long given")
                if (p):
                    try:
                        distance = float(p.group())
                    except:
                        print("invalid distance")
                if (q):
                    difficulty = str(q.group())

                hike = Hike(lat, long)
                l = re.search ('Description ===(?s)(.*?)===\s', page_text, re.MULTILINE)
                entry = ""
                if l:
                    page_text = l.group()
                    by_line = []
                    by_line = page_text.splitlines()
                    for line in by_line:
                        try:
                            line = str(line)
                            line = re.sub('[\[]', '', line)
                            line = re.sub('[\]]', '', line)
                            line = re.sub('[\}]', '', line)
                            line = re.sub('[\{]', '', line)
                        except:
                            print("page not cast")
                            #print(line)
                        if line:
                            if not line.startswith(('Description','===','TripReports','RelatedDiscussions','*','Source','(','=','<')):
                                entry = entry + "\n" + line


                hike.desc = entry
                hike.name = item.page_title
                hike.distance = distance
                hike.difficulty = difficulty
                if entry:
                    hikes.append(hike)
                    print("added: " + hike.name)
                    print("lat: " + str(hike.lat))
                    print("long: " + str(hike.long))
    return hikes

hikes = Hikes()

#just testing display
#this is pretty cool

for i in range(len(hikes)):
    name = str(hikes[i].name)
    lat = hikes[i].lat
    long = hikes[i].long
    desc = hikes[i].desc
    difficulty = hikes[i].difficulty
    url = 'https://assign2-byr.appspot.com/_ah/api/hikersapi/v1/hike'
    r = requests.post(url,json={'name':name, 'desc':desc,'lat':lat,'long':long,'difficulty':difficulty})
    print(r.text)
g = requests.get('https://assign2-byr.appspot.com/_ah/api/hikersapi/v1/allhikes')
print(g.text)

