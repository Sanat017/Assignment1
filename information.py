from flask import Flask ,jsonify,json,request,make_response,render_template
from flask_pymongo import PyMongo
app=Flask(__name__)
app.config['MONGO_DBNAME']= 'user_information'
app.config['MONGO_URI']= 'mongodb://sanatkabi:sanat123@ds145669.mlab.com:45669/user_information'
mongo= PyMongo(app)
@app.route('/user',methods=['POST'])
def create_user():
    user = mongo.db.users
    name = request.json['name']
    rollno = request.json['rollno']
    address = request.json['address']
    branch = request.json['branch']
    info= user.find_one({'rollno':rollno})
    if info:
        message = "Roll no. already Exist"
        response = make_response(json.dumps({'message':'Roll no already exist!!!'}), 406)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
     users_id = user.insert({'name':name,'rollno':rollno,'address':address,'branch':branch})
     response = make_response(json.dumps({'message':'Data stored successfully!!!'}), 201)
     response.headers['Content-Type'] = 'application/json'
     return response
@app.route('/user',methods=['GET'])
def get_user():
    user = mongo.db.users
    info=[]
    for q in user.find ( ):
     info.append ( {'name': q['name'], 'rollno': q['rollno'], 'address': q['address'], 'branch': q['branch']} )
    if request.headers['Content-Type'] == 'application/json':
      return jsonify({'information':info})
    elif request.headers['Content-Type'] == 'application/xml':
      template = render_template('test.xml', info=info)
      response = make_response(template )
      response.headers['Content-Type'] = 'application/xml'
      return response

@app.route('/user/<name>',methods=['GET'])
def get_one_user(name):
    user = mongo.db.users
    result=[]
    info=user.find_one({'name':name})

    if info:
      result.append({'name':info['name'],'rollno':info['rollno'],'address':info['address'],'branch':info['branch']})
      if request.headers['Content-Type'] == 'application/json':
       return jsonify ( {'information': result} )
      elif request.headers['Content-Type'] == 'application/xml':
       template = render_template ( 'test2.xml', result=result )
       response = make_response ( template )
       response.headers['Content-Type'] = 'application/xml'
       return response
    else:
        response = make_response(json.dumps({'message':'NO match found'}), 404)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/user/<rollno>',methods=['PUT'])
def update(rollno):
    user = mongo.db.users
    u_name = request.json['name']
    address = request.json['address']
    branch = request.json['branch']
    info = user.find_one({'rollno': rollno})
    if info:
     info['name'] = u_name
     info['address'] = address
     info['branch'] = branch
     user.save(info)
     response = make_response(json.dumps({'message':'Data modified successfully'}), 201)
     response.headers['Content-Type'] = 'application/json'
    else:
        response = make_response(json.dumps({'message':'No match found'}), 404)
        response.headers['Content-Type'] = 'application/json'
        return response

    return response
@app.route('/user/<rollno>',methods=['DELETE'])
def delete(rollno):
    user = mongo.db.users
    info = user.find_one({'rollno': rollno})
    if info:
      user.remove(info)
      response = make_response(json.dumps({'message':'Data remove successfully'}), 201)
      response.headers['Content-Type'] = 'application/json'
    else:
        response = make_response(json.dumps({'message': 'No match found'}), 404)
        response.headers['Content-Type'] = 'application/json'
        return response
    return response
if __name__=='__main__':
  app.run(debug=True)

