from fastapi import FastAPI

app = FastAPI()
#static path first and then dynamic path otherwise it will give error.(make it in order)

@app.get('/users/admin')
def admin():
    return {"This is admin"}

@app.get('/users/{name}')
def users(name: str):
    return {"name": name}


#query parameter 
@app.get('/products')
def products(id:int=1, price:int=110):
    return f"This is id {id} and price is {price}"

@app.get('/profile/{user_id}/comments')
def profile(user_id:int, commentid:int):
    return f"Profile of user {user_id} and comment {commentid}"




