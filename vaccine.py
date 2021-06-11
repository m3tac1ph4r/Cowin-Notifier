import json
import time
import helper
import decouple
import requests
from datetime import datetime, timedelta, date


USER_FILE = "assets/user_data.json"
STATE_FILE = "assets/state_id.json"
DIST_FILE = "assets/dist_id.json"
API_KEY = decouple.config("API_KEY")
BASE_URL = "https://cdn-api.co-vin.in/api"
HEADER = {
	"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36",
	"Accept-Language": "hi_IN",
	"accept": "application/json"
}

dt = datetime.now()
s=""

def vaccine_available(age_query):
	id = []
	s_file = open("assets/sname.txt", "r")
	lines = s_file.readlines()
	for state in lines:
		state = state[:-1]
		c = helper.check_state(state)
		if(c == 1):
			dist = helper.get_all_dists_helper(state)
			for district in dist:
				dname = str(district["district_name"]).lower()
				print(dname)
				dc=helper.check_district(dname)
				if(dc==1):
					id = helper.get_chat_id(dname, age_query)
					vaccine_info = helper.get_vax_info(district["district_id"],age_query)
					vax_to_telegram(id, vaccine_info, age_query)

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

def main():
	global dt
	print(dt)
	while(1):
		now = datetime.now()
		current_time = str(now.strftime("%H:%M"))
		if(datetime.now()>dt):
			vaccine_available("18")
			vaccine_available("45")
			return 1
		elif(current_time=="10:00" or current_time=="10:30" or current_time=="11:00" or current_time=="11:30"):
			vaccine_available("18")
			return 0
		else:
			time.sleep(60)

if __name__ == "__main__":
	# global dt
	while(1):
		dt = datetime.now() + timedelta(hours=3.5)
		a=main()
		if(a==0):
			b=main()
		else:
			continue

