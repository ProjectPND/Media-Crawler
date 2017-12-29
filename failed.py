import os

media = "failed.txt"
with open(media) as f:
	listMedia = f.readlines()
listMedia = [x.strip() for x in listMedia] 

for item in listMedia:
	os.system("python app.py %s"%(item))
