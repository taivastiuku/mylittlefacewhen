import json
import requests
import sys
import urllib2
import os

username = ""
password = ""

#site = "https://mylittlefacewhen.com/api"
site = "http://0.0.0.0:8000/api"

s = requests.session()
r = s.post(site + "/login/", data={"username":username, "password":password})
print r.status_code

if not json.loads(r.content):
    sys.exit("error at login")

r = s.get(site + "/feedback/")

feedbacks = json.loads(r.content)

f = []
for feedback in feedbacks :
    if not feedback["processed"]:
        f.append(feedback)

for feedback in f:
    url = feedback.get("image")
    print url
    if url:
        try:
            filu = urllib2.urlopen(url)
            filename = url.rpartition("/")[2]
            ext = filename.rpartition(".")[2]
            i = 1
            while os.path.exists("./" + filename):
                filename = filename.partition(".")[0]
                filename = filename + "." + str(i) + "." + ext
                i += 1
            output = open(filename, 'wb')
            output.write(filu.read())
            output.close()
        except Exception, e:
            print e

    print "message: " + feedback["text"]
    
    r = s.put(site + "/feedback/" + str(feedback["id"]) + "/")
    print "processed: " + str(json.loads(r.content)["processed"])

    



    


