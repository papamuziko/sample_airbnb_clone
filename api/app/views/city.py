from app import *
from app.models.city import City
from app.models.state import State


@app.route('/states/<state_id>/cities', methods=['GET', 'POST'])
@app.route('/states/<state_id>/cities/<city_id>', methods=['GET', 'DELETE'])
@as_json
def cities(state_id=None, city_id=None):
    
    state = None
    try:
        if state_id != None:
            state = State.get(State.id == int(state_id))
    except:
        state = None
    
    if state == None:
        return { 'code': 404, 'msg': "not found" }, 404
    
    if request.method == "GET":
        if city_id != None:
            try:
                city = City.get(City.id == int(city_id), City.state == state)
                return city.to_dict()
            except:
                pass
            return { 'code': 404, 'msg': "not found" }, 404

        return { 'data': [city.to_dict() for city in City.select().where(City.state == state)] }, 200
    
    elif request.method == "POST":
        name = request.form.get('name')

        if City.select().where(City.state == state).where(City.name == name).count() > 0:
            return { 'code': 10002, 'msg': "City already exists in this state" }, 409

        try:
            new_city = City.create(name=name, state=state)
        except IntegrityError:
           return { 'code': 10002, 'msg': "City already exists in this state" }, 409
        except Exception as e:
            raise e 
        
        return new_city.to_dict(), 201

    elif request.method == "DELETE":
        if city_id != None:
            city = None
            try:
                city = City.get(City.id == int(city_id), City.state == state)
            except:
                city = None
            
            if city != None:
                city.delete_instance()
                return {}, 200
                
        return { 'code': 404, 'msg': "not found" }, 404
    
        
