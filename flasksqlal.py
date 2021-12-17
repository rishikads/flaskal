from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
meta= db.MetaData()

students = db.Table(
  'students', meta, 
  db.Column('USN', db.String(10), primary_key = True), 
  db.Column('student_name', db.String(50)), 
  db.Column('gender', db.String(1)),
  db.Column('entry_type', db.String(10)),
  db.Column('YOA', db.Integer),
  db.Column('migrated', db.String(1)),
  db.Column('Details_of_transfer', db.String(100)),
  db.Column('admission_in_separate_division', db.String(1)),
  db.Column('Details_of_admission_in_seperate_division', db.String(100)),
  db.Column('YOP', db.Integer),
  db.Column('degree_type', db.String(2)),
  db.Column('pu_marks', db.Integer),
  db.Column('entrance_marks', db.Integer)
)

def create(body):
  N=int(body['N'])
  for i in range(N):
    USN=str(body['USN'])
    student_name=str(body['student_name'])
    gender=str(body['gender'])
    if not re.match("^[m,f]*$", gender):
      return "Error! Only letters m and f allowed!"
      exit()
    entry_type=str(body['entry_type'])
    YOA=int(body['YOA'])
    migrated=str(body['migrated'])
    if migrated=="yes":
      migrated== 1
      Details_of_transfer=str(body['Details_of_transfer'])
    elif migrated=="no":
      migrated== 0
      Details_of_transfer= None
    admission_in_separate_division=str(body['admission_in_separate_division'])
    if admission_in_separate_division=="yes":
      admission_in_separate_division==True
      Details_of_admission_in_seperate_division=str(body['Details_of_admission_in_seperate_division'])
    else:
      admission_in_separate_division==False
      Details_of_admission_in_seperate_division= None
    YOP=int(body['YOP'])
    degree_type=str(body['degree_type'])
    pu_marks=int(body['pu_marks'])
    entrance_marks=int(body['entrance_marks'])
    db.engine.execute(students.insert(),[
        {'USN': USN, 'student_name' : student_name, 'gender' : gender, 'entry_type': entry_type, 'YOA': YOA, 'migrated': migrated,
        'Details_of_transfer': Details_of_transfer, 'admission_in_separate_division': admission_in_separate_division,
        'Details_of_admission_in_seperate_division': Details_of_admission_in_seperate_division, 'YOP': YOP, 'degree_type': degree_type,
        'pu_marks': pu_marks, 'entrance_marks': entrance_marks}
        ])
  data = students.select()
  result = db.engine.execute(data)
  rows= [] 
  for row in result.fetchall():
    rows.append(dict(row))
  return jsonify(rows)

def read(body):
  data = students.select()
  result = db.engine.execute(data)
  rows= [] 
  for row in result.fetchall():
    rows.append(dict(row))
  return jsonify(rows)


def update(body):
    dict_input = dict(body)
    match = dict_input['USN']
    for key, value in dict_input.items():
        updated = students.update().where(students.c.USN==match).values({key:value})
        result = db.engine.execute.execute(updated)
    rows= [] 
    for row in result.fetchall():
        rows.append(dict(row))
    return jsonify(rows)

def delete(body):
    option = body['USN']
    deleted = students.delete().where(students.c.USN == option)
    result = db.engine.execute(deleted)
    return "Deleted"

@app.route('/add', methods = ['POST'])
def assignment():
    body = request.get_json()
    output = create(body)
    return output


@app.route('/read', methods = ['GET'])
def readingAssignment():
    output = read()
    return output


@app.route('/update', methods = ['PUT'])
def updatingAssignment():
    body = request.get_json()
    output = update(body)
    return output    

@app.route('/delete', methods = ['DELETE'])
def deletingAssignment():
    body = request.get_json()
    output = delete(body)
    return output    

if __name__ == '__main__':
    app.run(debug= True, port= 5000)