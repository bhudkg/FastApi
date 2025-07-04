from fastapi import FastAPI
app = FastAPI()

@app.get('/')
def index():
    return "Hello world"


@app.get('/property')
def property():
    return "this is property"

@app.get('/movies')
def movies():
    return {'movies': ['movie1', 'movie2', 'movie3']}



#id here is a path parameter
@app.get('/property/{id}')
def property(id):
    return {f"This is id for property {id}"}

#path parameter with type check
@app.get('/property_type/{id}')
def property(id: int):
    return {f"This is int property {id}"}

#documentation for api created using automatic.
