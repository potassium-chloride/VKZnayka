#!/usr/bin/env python3
import os,sys,time,json,urllib.request,subprocess

def bashExec(q):
	return subprocess.check_output(q,shell=True).decode("UTF-8")

#Получить JSON из адреса
def getJSON(url):
	time.sleep(0.4)
	bts = urllib.request.urlopen(url)
	s=bts.read().decode('UTF-8')
	bts.close()
	try:
		return json.loads(s)
	except:
		print(ttt()+"Ошибка запроса! url="+url+";\n\t\tans="+s)
	return json.loads("{}")

api_url="https://api.vk.com/method/"
token=bashExec("cat ~/bin/.token").replace("\n","")#У меня тут токен для вк лежит

class Stat():
	def __init__(self):
		self.objs=[].copy()
		self.counts=[].copy()
		pass
	def add(self,o,count=1):
		if(type(o)==str):
			if(o.replace("\n","").replace("\r","").replace("\t","").replace(" ","")==""):return
		if(o in self.objs):
			self.counts[self.objs.index(o)]+=count
		else:
			self.objs.append(o)
			self.counts.append(count)
	def getMaxes(self,maxnum=10):
		newcounts=self.counts.copy()
		sortedcounts=self.counts.copy()
		sortedcounts.sort()
		sortedcounts.reverse()
		resobjs=[]
		ressorted=[]
		for i in range(min(maxnum,len(sortedcounts))):
			ind=newcounts.index(sortedcounts[i])
			ressorted.append(sortedcounts[i])
			sortedcounts[i]=-100
			resobjs.append(self.objs[ind])
		return resobjs,ressorted

def getFriends(uid):
	friends=getJSON(api_url+"friends.get?user_id="+str(uid)+"&fields=city,bdate,education,universities&v=5.80&access_token="+token)
	return friends['response']['items']

def getUsers(uids):
	if(len(uids)<=200):
		return getJSON(api_url+"users.get?user_ids="+str(uids)[1:-1].replace(" ","")+"&fields=schools,career,military&v=5.80&access_token="+token)['response']
	arr=getJSON(api_url+"users.get?user_ids="+str(uids[:200])[1:-1].replace(" ","")+"&fields=schools,career,military&v=5.80&access_token="+token)['response']
	for i in range(200,len(uids),200):
		tmpstr=str(uids[i:min(len(uids),i+200)])[1:-1].replace(" ","")
		tmparr=getJSON(api_url+"users.get?user_ids="+tmpstr+"&fields=schools,career,military&v=5.80&access_token="+token)['response']
		for k in tmparr:
			arr.append(k)
	return arr

uid=int(sys.argv[1])

frnds=getFriends(uid)
print("Список друзей получен")

city=Stat()
univer=Stat()
faculty=Stat()
chair=Stat()
byear=Stat()
education_status=Stat()
uids=[]
for user in frnds:
	props=list(user.keys())
	uids.append(user['id'])
	if('city' in props):city.add(user['city']['title'])
	if('university_name' in props):univer.add(user['university_name'])
	if('faculty_name' in props):faculty.add(user['faculty_name'])
	if('universities' in props):
		arr=user['universities']
		for u in arr:
			univer.add(u['name'])
			try:faculty.add(u['faculty_name'])
			except:pass
			try:chair.add(u['chair_name'])
			except:pass
			try:education_status.add(u['education_status'])
			except:pass
	if('bdate' in props):
		bdarr=user['bdate'].split(".")
		for i in bdarr:
			if(len(i)>2):
				byear.add(int(i))

print("Город:")
v,sc=city.getMaxes(4)
for i in range(len(v)):
	print(sc[i],"\t",v[i])

print("\nУниверситет:")
v,sc=univer.getMaxes(4)
for i in range(len(v)):
	print(sc[i],"\t",v[i])

print("\nФакультет:")
v,sc=faculty.getMaxes(4)
for i in range(len(v)):
	print(sc[i],"\t",v[i])

print("\nКафедра:")
v,sc=chair.getMaxes(4)
for i in range(len(v)):
	print(sc[i],"\t",v[i])

print("\nСтатус обучения:")
v,sc=education_status.getMaxes(4)
for i in range(len(v)):
	print(sc[i],"\t",v[i])

print("\nГод рождения:")
v,sc=byear.getMaxes()
for i in range(len(v)):
	print(sc[i],"\t",v[i])


school=Stat()
military=Stat()
career=Stat()
frndsasusers=getUsers(uids)
print("Получение доп. информации...")

for user in frndsasusers:
	props=list(user.keys())
	if('schools' in props):
		for sch in user['schools']:
			school.add(sch['name'])
	if('military' in props):
		for sch in user['military']:
			school.add(sch['unit'])
	if('career' in props):
		for sch in user['career']:
			try:school.add(sch['company'])
			except:pass

print("\nШкола:")
v,sc=school.getMaxes(4)
for i in range(len(v)):
	print(sc[i],"\t",v[i])

print("\nВоенная служба:")
v,sc=military.getMaxes(4)
for i in range(len(v)):
	print(sc[i],"\t",v[i])

print("\nКарьера:")
v,sc=career.getMaxes(4)
for i in range(len(v)):
	print(sc[i],"\t",v[i])


