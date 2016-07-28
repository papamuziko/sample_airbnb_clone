from app import *
from app.models.state import State


@app.route('/states', methods=['GET', 'POST'])
@app.route('/states/<state_id>', methods=['GET', 'DELETE'])
@as_json
def states(state_id=None):
    
    if request.method == "GET":
        if state_id != None:
            try:
                state = State.get(State.id == int(state_id))
                return state.to_dict()
            except:
                pass
            return { 'code': 404, 'msg': "not found" }, 404

        return { 'data': [state.to_dict() for state in State.select()] }, 200
    
    elif request.method == "POST":
        name = request.form.get('name')
        
        try:
            new_state = State.create(name=name)
        except IntegrityError:
           return { 'code': 10001, 'msg': "State already exists" }, 409
        except Exception as e:
            raise e 
        
        return new_state.to_dict(), 201

    elif request.method == "DELETE":
        if state_id != None:
            state = None
            try:
                state = State.get(State.id == int(state_id))
            except:
                state = None
            
            if state != None:
                state.delete_instance()
                return {}, 200

        return { 'code': 404, 'msg': "not found" }, 404
    
        
