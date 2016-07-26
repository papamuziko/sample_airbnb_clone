from app import *
from app.models.user import User


@app.route('/users', methods=['GET', 'POST'])
@app.route('/users/<user_id>', methods=['GET', 'PUT', 'DELETE'])
@as_json
def users(user_id=None):
    if request.method == "GET":
        if user_id != None:
            try:
                user = User.get(User.id == int(user_id))
                return user.to_hash(), 200
            except:
                pass
            return { 'code': 404, 'msg': "not found" }, 404

        return { 'data': [user.to_hash() for user in User.select()] }, 200
    
    elif request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password', "")
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')

        try:
            new_user = User.create(email=email, first_name=first_name, last_name=last_name)
        except IntegrityError:
           return { 'code': 10000, 'msg': "Email already exists" }, 409
        except Exception as e:
            raise e 
        new_user.set_password(password)
        return new_user.to_hash(), 201

    elif request.method == "PUT":
        if user_id != None:
            user = None
            try:
                user = User.get(User.id == int(user_id))
            except:
                user = None
            
            if user != None:
                password = request.form.get('password')
                first_name = request.form.get('first_name', user.first_name)
                last_name = request.form.get('last_name', user.last_name)
                
                if password != None:
                    user.set_password(password)
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                return user.to_hash(), 200

        return { 'code': 404, 'msg': "not found" }, 404

    elif request.method == "DELETE":
        if user_id != None:
            user = None
            try:
                user = User.get(User.id == int(user_id))
            except:
                user = None
            
            if user != None:
                user.delete_instance()
                return {}, 200

        return { 'code': 404, 'msg': "not found" }, 404
    
        
