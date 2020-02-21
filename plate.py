import base64
import sqlite3
import datetime
import requests


image_path = 'image url'
secret_key = 'API KEY FROM : https://towardsdatascience.com/heres-how-to-read-license-plate-with-10-lines-of-python-cc9b7a3b4b7c'

with open(image_path, 'rb') as image_file:
    img_base64 = base64.b64encode(image_file.read())

url = ('https://api.openalpr.com/v2/recognize_bytes'
       +'?recognize_vehicle=1&country=eu&secret_key={}'.format(secret_key))
r = requests.post(url, data=img_base64)
try:
    print({
        'plate': r.json()['results'][0]['plate'],
        'Brand': r.json()['results'][0]['vehicle']['make'][0]['name'],
        'color': r.json()['results'][0]['vehicle']['color'][0]['name']
    })

except:
    print('plate can not be identified ')

plate = r.json()['results'][0]['plate']
brand = r.json()['results'][0]['vehicle']['make'][0]['name']
color = r.json()['results'][0]['vehicle']['color'][0]['name']

# sql
conn= sqlite3.connect('plate.db')
c=conn.cursor()
def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS platerecognition(Id INTEGER PRIMARY KEY  AUTOINCREMENT, plate VARCHAR(30),Brand,color TEXT)')

def data_entry(plate,brand,color):
    c.execute(""" INSERT INTO platerecognition
          (plate, Brand, color) VALUES (?,?,?)""", (plate, brand, color))

    conn.commit()
    c.close()
    conn.close()

create_table()
data_entry(plate,brand,color)


