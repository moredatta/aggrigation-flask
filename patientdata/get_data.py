
from flask import Flask,jsonify, request
import json
from bson.json_util import dumps
import pymongo

app = Flask(__name__)

client = pymongo.MongoClient('mongodb://mongo-service:27017/')
covid= client['covid']
aggregated_covid_data = covid['aggregated_covid_data']

@app.route("/get_data", methods=["GET"])
def get_data():
    page = request.args.get('page', 1, type = int)
    per_page = request.args.get('per_page', 3, type = int)
    order = request.args.get('order')
   
    if order in ['DESCENDING','DESC','desc']:
        order=-1
    else:
        order=1
    city = request.args.get('City')
    print(type(city),city)
    sort_by=request.args.get("sort")
    if city:
        patient_data=aggregated_covid_data.find({"City": city}).sort(f"{sort_by}",order).skip(page).limit(per_page)
        
    else:
         patient_data=aggregated_covid_data.find().sort(f"{sort_by}",order).skip(page).limit(per_page)
         
    patient_data=list(patient_data)
    patient_data=dumps(patient_data)
    patient_data=json.loads(patient_data)
    if len(patient_data)==0:
        return jsonify({"messege": 'No Record found'})
    
    return jsonify({"total_count": len(patient_data),"patient_data": patient_data})
    

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000)
   

   
   