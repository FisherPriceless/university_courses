import time
import pandas as pd
import requests
from pymongo import MongoClient
from datetime import datetime, timedelta

def download_and_save_data():

    client = MongoClient('mongodb://localhost:27017/')
    db = client['university_courses']
    collection = db['courses']


    url = "https://api.mockaroo.com/api/501b2790?count=100&key=8683a1c0"


    response = requests.get(url)
    data = response.content.decode('utf-8')


    courses_df = pd.read_csv(pd.compat.StringIO(data))


    courses_df.columns = [col.strip().lower().replace(' ', '_') for col in courses_df.columns]


    courses_data = courses_df.to_dict(orient='records')


    for course in courses_data:
        course['created_at'] = datetime.utcnow()
        collection.insert_one(course)


    collection.create_index("created_at", expireAfterSeconds=600)

    print("Data successfully saved to MongoDB with expiration.")

def data_expired(collection):

    if collection.count_documents({}) == 0:
        return True

    return False

def main():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['university_courses']
    collection = db['courses']


    while True:
        if data_expired(collection):
            print("No data found or data expired. Downloading new data...")
            download_and_save_data()
        else:
            print("Data still valid. Waiting...")


        time.sleep(60)

if __name__ == "__main__":
    main()
