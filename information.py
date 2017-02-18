from flask import Flask ,jsonify,json,request,make_response,render_template
from flask_pymongo import PyMongo
import xmltodict
app=Flask(__name__)
app.config['MONGO_DBNAME']= 'user_information'
app.config['MONGO_URI']= 'mongodb://sanatkabi:sanat123@ds145669.mlab.com:45669/user_information'
mongo= PyMongo(app)
@app.route('/user',methods=['POST'])
def create_user():
    user = mongo.db.users
    if request.headers['Content-Type'] == 'application/xml':
        obj = xmltodict.parse(request.data)['val']
        info = user.find_one({'rollno': obj['rollno']})
        if info:
            response = make_response(json.dumps({'message': 'Roll no already exist!!!'}),406)
            response.headers['Content-Type'] = 'application/xml'
            return response
        else:
            users_id = user.insert({'name': obj['name'], 'rollno': obj['rollno'], 'address': obj['address'],'branch': obj['branch']})
            response = make_response(json.dumps ({'message': 'Data stored successfully!!!'}), 201)
            response.headers['Content-Type'] = 'application/xml'
            return response

    elif request.headers['Content-Type'] == 'application/json':
       name = request.json['name']
       rollno = request.json['rollno']
       address = request.json['address']
       branch = request.json['branch']
       info = user.find_one ( {'rollno': rollno} )
       if info:
           response = make_response(json.dumps({'message':'Roll no already exist!!!'}), 406)
           response.headers['Content-Type'] = 'application/json'
           return response
       else:
           users_id = user.insert({'name':name,'rollno':rollno,'address':address,'branch':branch})
           response = make_response(json.dumps({'message':'Data stored successfully!!!'}), 201)
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

@app.route('/user/<rollno>',methods=['GET'])
def get_one_user(rollno):
    user = mongo.db.users
    result=[]
    info=user.find_one({'rollno':rollno})

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
    info = user.find_one({'rollno': rollno})
    if info:
       if request.headers['Content-Type'] == 'application/xml':
          obj = xmltodict.parse ( request.data )['val']
          info['name'] = obj['name']
          info['address'] = obj['address']
          info['branch'] = obj['branch']
          user.save(info)
          response = make_response ( json.dumps ( {'message': 'Data modified successfully'} ), 201 )
          response.headers['Content-Type'] = 'application/xml'
          return response
       elif request.headers['Content-Type'] == 'application/json':
           info['name'] = request.json['name']
           info['address'] = request.json['address']
           info['branch'] = request.json['branch']
           user.save(info)
           response = make_response(json.dumps({'message':'Data modified successfully'}), 201)
           response.headers['Content-Type'] = 'application/json'
    else:
       response = make_response(json.dumps({'message':'No match found'}), 404)
       response.headers['Content-Type'] = 'application/json'
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

