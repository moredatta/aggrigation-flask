
import numpy as np
import random
from datetime import datetime,timedelta
import names
from flask import Flask,jsonify
import json
from bson.json_util import dumps
import pymongo
app = Flask(__name__)

client = pymongo.MongoClient('mongodb://mongo-service:27017/')
covid= client['covid']
#aggregated_covid_data = covid['aggregated_covid_data']

def random_date():
        start_date = datetime.strptime("01-02-2021", '%d-%m-%Y')
        end_date = datetime.strptime("31-01-2022", '%d-%m-%Y')
        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        random_date = start_date + timedelta(days=random_number_of_days)
        return random_date

def generate_date():
        present_date=datetime.now()
        return present_date.strftime('%Y%m%d') 

        
@app.route("/generate_random_data", methods=["GET"])
def generate_random_data():
    
        city = ["Mumbai","Delhi","Bangalore","Hyderabad","Ahmedabad","Chennai","Kolkata" ,"Surat","Pune","Jaipur","Lucknow","Kanpur","Nagpur","Indore","Thane","Bhopal","Visakhapatnam","Pimpri & Chinchwad","Patna","Vadodara","Ghaziabad","Ludhiana","Agra","Nashik","Faridabad","Meerut","Rajkot","Kalyan & Dombivali","Vasai Virar","Varanasi"]
        Datalist=[]
        for i in range(200):
                name = names.get_full_name()
                age = np.random.randint(18,70)
                first_dose_date = random_date()
                second_dose_date = first_dose_date + timedelta(days = random.randint(90,100))
                admission_date = random_date()
                discharge_date = admission_date + timedelta(days = random.randint(7,21))
                data={}
                data["Name"] = name
                data["Age"] = age
                data["First Dose Date"] = first_dose_date.strftime('%d-%b-%Y')
                data["Second Dose Date"] = second_dose_date.strftime('%d-%b-%Y')
                data["Admission Date"] = admission_date.strftime('%d-%b-%Y')
                data["Discharge Date"] = discharge_date.strftime('%d-%b-%Y')
                data["City"] = random.choice(city)
                Datalist.append(data)
        present_date=generate_date()
        present_date_collection=covid[f'{present_date}']
        present_date_collection.insert_many(Datalist)
        return jsonify({"messege": "Data inserted"})


@app.route("/get_new_data", methods=["GET"])
def get_new_data():
        present_date=generate_date()
        present_date=covid[f'{present_date}']
        single_data=present_date.find({},{"_id": 0})
        single_data=list(single_data)
        single_data=dumps(single_data)
        single_data=json.loads(single_data)
        #print(single_data)
        return jsonify({"data": single_data,"total_count": len(single_data)})

if __name__== "__main__":
    app.run(host='0.0.0.0',port=9000)
   