
from flask import Flask,jsonify
import pymongo
import requests
app = Flask(__name__)
client = pymongo.MongoClient('mongodb://mongo-service:27017/')
covid= client['covid']
aggregated_covid_data = covid['aggregated_covid_data']

@app.route("/aggrigation", methods=["GET","POST"])
def aggrigation():
  result = requests.get("http://192.168.59.102:31600/get_new_data")

  result = result.json()
  result = result["data"]
  print(type(result))
  print(result)
  aggregated_covid_data.insert_many(result)
  aggregated_covid_data.aggregate([{"$group":{"_id":{"Age":"$Age"},"count": {"$sum": 1}}},{"$out":"by_age" }])
  aggregated_covid_data.aggregate([{"$group":{"_id":{"City":"$City"},"count": {"$sum": 1}}},{"$out":"by_City" }])
  aggregated_covid_data.aggregate([{"$group":{"_id":{"Admission Date":"$Admission Date"},"count": {"$sum": 1}}},{"$out":"by_Admission Date" }])
  aggregated_covid_data.aggregate([{"$group":{"_id":{"Second Dose Date":"$Second Dose Date"},"count": {"$sum": 1}}},{"$out":"by_Second Dose Date" }])
  aggregated_covid_data.aggregate([{"$group":{"_id":{"Discharge Date":"$Discharge Date"},"count": {"$sum": 1}}},{"$out":"by_Discharge Date" }])
  return jsonify({"covid_data": 'data inserted'})  

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True,port=7000)

