import json
import time
import decouple
import requests
from datetime import date
from decouple import config


USER_FILE="assets/user_data.json"
STATE_FILE = "assets/state_id.json"
DIST_FILE = "assets/dist_id.json"
API_KEY = decouple.config("API_KEY")
BASE_URL = "https://cdn-api.co-vin.in/api"
HEADER = {
	"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36",
	"Accept-Language": "hi_IN",
	"accept": "application/json"
}
counter=""
s=""

#filter user message
def filter_message(chat_id,message):
	global counter
	message=str(message)
	message=message.lower()
	chat_id=str(chat_id)
	command = ["/start", "/help", "/credits", "/notify-start", "/notify-stop","/vaxinfo"]
	s_file = open("assets/sname.txt", "r")
	d_file = open("assets/dname.txt", "r")
	s_data = s_file.read()
	d_data= d_file.read()
	if(message in command):
		counter="command"
	elif(message in s_data):
		user_data(chat_id,message)
		counter="state"
	elif(message in d_data):
		user_data(chat_id, message)
		counter="district"
	elif(message[0].isdigit()):
		user_data(chat_id, message)
		counter="age"
	else:
		counter="error"
	s_file.close()
	d_file.close()
	return counter

#command-click
def command_click(chat_id):
	headers = {
		'Content-Type': 'application/json',
	}
	data = '{"chat_id":"", "text":"Select one command:", "reply_markup": {"keyboard": [["/vaxinfo"],["/credits"],["/help"],["/notify-start"],["/notify-stop"]]}'
	s = data[:12]+f"{chat_id}"+data[12:]
	response = requests.post(
		f'https://api.telegram.org/bot{API_KEY}/sendMessage', headers=headers, data=s)
#state menu
def state_click(chat_id):
	headers = {
		'Content-Type': 'application/json',
	}
	data = '{"chat_id":"", "text":"Select your state:", "reply_markup": {"keyboard": [["Andaman and Nicobar Islands"],["Andhra Pradesh"],["Arunachal Pradesh"],["Assam"],["Bihar"],["Chandigarh"],["Chhattisgarh"],["Dadra and Nagar Haveli"],["Daman and Diu"],["Delhi"],["Goa"],["Gujarat"],["Haryana"],["Himachal Pradesh"],["Jammu and Kashmir"],["Jharkhand"],["Karnataka"],["Kerala"],["Ladakh"],["Lakshadweep"],["Madhya Pradesh"],["Maharashtra"],["Manipur"],["Meghalaya"],["Mizoram"],["Nagaland"],["Odisha"],["Puducherry"],["Punjab"],["Rajasthan"],["Sikkim"],["Tamil Nadu"],["Telangana"],["Tripura"],["Uttar Pradesh"],["Uttarakhand"],["West Bengal"]]}'
	s = data[:12]+f"{chat_id}"+data[12:]
	response = requests.post(
		f'https://api.telegram.org/bot{API_KEY}/sendMessage', headers=headers, data=s)
	chat_id=str(chat_id)
	state=get_state(chat_id)
	while(True):
		if(state==None):
			try:
				state = get_state(chat_id)
			except:
				continue
		else:
			return state

#district menu
def district_click(chat_id,state_name):
	headers = {
		'Content-Type': 'application/json',
	}
	s = ""
	f = open("assets/dist_id.json")
	data = json.load(f)
	for i in data["states"]:
		if state_name.lower() == i['state_name'].lower():
			for j in i["districts"]:
				a = f'["{j["district_name"]}"]'
				s = s+a+","
	h = len(s) - 1
	s = s[:h]
	data = '{"chat_id":"", "text":"Select your District", "reply_markup": {"keyboard": []}'
	li = data.rfind("[")+1
	data2 = data[:li]+s+data[li:]
	data2= data2[:12]+f"{chat_id}"+data2[12:]
	response = requests.post(
		f'https://api.telegram.org/bot{API_KEY}/sendMessage', headers=headers, data=data2)
	chat_id = str(chat_id)
	while(1):
		try:
			d = get_district(chat_id)
			if(len(d)==0):
				d=get_district(chat_id)
				continue
			else:
				break
		except:
			pass
	return d
		
#save user data into json file
def user_data(chat_id,text):
	c=0
	global counter
	s_file = open("assets/sname.txt", "r")
	d_file = open("assets/dname.txt", "r")
	s_data=s_file.read()
	d_data=d_file.read()
	text=str(text).lower()
	with open(USER_FILE,"r") as json_file:
		data=json.load(json_file)
	for i in data["user_data"]:
		if(i["chat_id"]==chat_id):
			c=1
			if text in s_data:
				i["state"]=text
			elif text in d_data:
				i["district"]=text
			elif text[0].isdigit():
				i["age"]=text[:-1]
			with open(USER_FILE, "w") as json_file:
				json.dump(data, json_file)
		else:
			pass
		json_file.close()
	if(c==0):
		with open("assets/user_data.json") as json_file:
			data = json.load(json_file)
		temp = data["user_data"]
		if text in s_data:
			json_data={
				"chat_id":chat_id,
				"state":text,
				"district":"",
				"age":""
				}
		elif text in d_data:
			json_data={
				"chat_id":chat_id,
				"state":"",
				"district":text,
				"age":""
					}
		elif text[0].isdigit():
			temp_text=text[:-1]
			json_data={
				"chat_id": chat_id,
				"state":"",
				"district":"",
				"age":temp_text
				}
		temp.append(json_data)
		with open("assets/user_data.json", "w") as json_file:
			json.dump(data, json_file, indent=4)
		json_file.close()
		s_file.close()
		d_file.close()

# Helper to get_all_dists for a specific state
def get_all_dists_helper(state_name):
	with open(DIST_FILE) as f:
		data = json.load(f)
		for i in data['states']:
			if state_name.lower() == i['state_name'].lower():
				return i['districts']


#extract all chat_id with specific district
def get_chat_id(dname,age_query):
	chat_id=[]
	with open(USER_FILE,"r") as json_file:
		data=json.load(json_file)
	for i in data["user_data"]:
		try:
			age = int(i["age"])
			age_query=int(age_query)
			if age_query==18:
				if(i["district"]==dname and age >=age_query and age<45):
					chat_id.append(i["chat_id"])
				else:
					continue
			else:
				if(i["district"] == dname and age >= age_query):
					chat_id.append(i["chat_id"])
				else:
					continue
		except:
			continue
	return chat_id

# Returns vax info
def get_vax_info(dist_id,age_query):
	vaccine_out = {}
	l=[]
	today = date.today().strftime("%d-%m-%Y")
	edp = BASE_URL + \
		f"/v2/appointment/sessions/public/findByDistrict?district_id={dist_id}&date={today}"
	try:
		r = requests.get(edp, headers=HEADER)
		data = json.loads(r.text)
		age_query = int(age_query)
		try:
			for session in data["sessions"]:
				age = int(session["min_age_limit"])
				if(age_query == 45):
					if(age_query >= age and session["available_capacity"] > 0 and age != 18):
						vaccine_out["name"] = session["name"]
						vaccine_out["address"] = session["address"]
						vaccine_out["pincode"] = session["pincode"]
						vaccine_out["block_name"] = session["block_name"]
						vaccine_out["available_capacity_dose1"] = session["available_capacity_dose1"]
						vaccine_out["available_capacity_dose2"] = session["available_capacity_dose2"]
						vaccine_out["min_age_limit"] = session["min_age_limit"]
						vaccine_out["slots"] = session["slots"]
						vaccine_out["vaccine"] = session["vaccine"]
						vaccine_out["fee_type"] = session["fee_type"]
						dictionary_copy = vaccine_out.copy()
						l.append(dictionary_copy)
					else:
						continue
				elif(age_query==18):
					if(age_query >= age and session["available_capacity"] > 0 and age==18):
						vaccine_out["name"] = session["name"]
						vaccine_out["address"] = session["address"]
						vaccine_out["pincode"] = session["pincode"]
						vaccine_out["block_name"] = session["block_name"]
						vaccine_out["available_capacity_dose1"] = session["available_capacity_dose1"]
						vaccine_out["available_capacity_dose2"] = session["available_capacity_dose2"]
						vaccine_out["min_age_limit"] = session["min_age_limit"]
						vaccine_out["slots"] = session["slots"]
						vaccine_out["vaccine"] = session["vaccine"]
						vaccine_out["fee_type"] = session["fee_type"]
						dictionary_copy = vaccine_out.copy()
						l.append(dictionary_copy)
		except:
			pass
	except:
		get_vax_info(dist_id, age_query)
	return l


#check whether any user is having that state
def check_state(state):
	c=0
	with open(USER_FILE, "r") as json_file:
		data = json.load(json_file)
	for i in data["user_data"]:
		if(i["state"] == state):
			c=1
			break
		else:
			pass
	return c

#to get state associated with that chat_id
def get_state(chat_id):
	with open(USER_FILE, "r") as json_file:
		data = json.load(json_file)
	for i in data["user_data"]:
		if(i["chat_id"]==chat_id):
			return i["state"]

#delete user from user_data.json
def delete_user(chat_id):
	chat_id=str(chat_id)
	delete=[]
	with open(USER_FILE) as json_file:
		data=json.load(json_file)
	for item in data["user_data"]:
		if(item["chat_id"]==chat_id):
			delete.append(data["user_data"].index(item))
	
	for i in reversed(delete):
		del data["user_data"][i]
	with open(USER_FILE,"w") as f:
		json.dump(data,f)

#age click menu
def age_click(chat_id):
	chat_id=str(chat_id)
	headers = {
		'Content-Type': 'application/json',
	}
	data = '{"chat_id":"", "text":"Select your AGE:", "reply_markup": {"keyboard": [["18+"],["45+"]]}'
	s = data[:12]+f"{chat_id}"+data[12:]
	response = requests.post(
		f'https://api.telegram.org/bot{API_KEY}/sendMessage', headers=headers, data=s)
	while(1):
		try:
			age = get_age(chat_id)
			if(len(age) == 0):
				age = get_age(chat_id)
				continue
			else:
				break
		except:
			pass
	return age

#get district associated with that chat_id
def get_district(chat_id):
	with open(USER_FILE, "r") as json_file:
		data = json.load(json_file)
	for i in data["user_data"]:
		if(i["chat_id"] == chat_id):
			return i["district"]

#get age associated with that chat_id
def get_age(chat_id):
	with open(USER_FILE, "r") as json_file:
		data = json.load(json_file)
	for i in data["user_data"]:
		if(i["chat_id"] == chat_id):
			return i["age"]

#to check whether district is there in user_data.json or not
def check_district(dname):
	c = 0
	with open(USER_FILE, "r") as json_file:
		data = json.load(json_file)
	for i in data["user_data"]:
		if(i["district"] == dname):
			c = 1
			break
		else:
			pass
	return c

#sends vaccine info to users
def vax_to_telegram(id, vaccine_info, age_query):
	global s
	if(len(id) > 0):
		for i in range(len(vaccine_info)):
			vaccine = vaccine_info[i]
			s = f"""
Name:{vaccine["name"]}
Pincode: {vaccine["pincode"]}
available capacity dose1: {vaccine["available_capacity_dose1"]}
available capacity dose2: {vaccine["available_capacity_dose2"]}
min_age_limit: {vaccine["min_age_limit"]}
slots: {vaccine["slots"]}
vaccine: {vaccine["vaccine"]}
Fee Type: {vaccine["fee_type"]}"""
			for i in range(0, len(id)):
				chat_id = str(id[i])
				url = f"https://api.telegram.org/bot{API_KEY}/sendMessage?chat_id={chat_id}&text={s}"
				r = requests.post(url)

#get immediate result of vaccine availability
def immediate_vax_info(chat_id,state, dname,age_query):
	dist_id = ""
	state = state.lower()
	dname = dname.lower()
	dist = get_all_dists_helper(state)
	for district in dist:
		if((district["district_name"]).lower() == dname):
			dist_id = district["district_id"]
	vaccine_info = get_vax_info(dist_id, age_query)
	vax_to_telegram([chat_id], vaccine_info, age_query)
