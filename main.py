import uvicorn

from fastapi import FastAPI,Body,Depends

from app.model import PostSchema,UserSchema,UserLoginSchema

from app.auth.jwt_handler import signJwt

from app.auth.jwt_bearer import jwtBearer
app=FastAPI()


posts = [
    {
        "id": 1,
        "title": "Penguins ",
        "text": "Penguins are a group of aquatic flightless birds."
    },
    {
        "id": 2,
        "title": "Tigers ",
        "text": "Tigers are the largest living cat species and a memeber of the genus panthera."
    },
    {
        "id": 3,
        "title": "Koalas ",
        "text": "Koala is arboreal herbivorous maruspial native to Australia."
    },

]

users=[]

## get for testing
@app.get('/',tags=['test'])


def greet():
    return {'hello':'world'}


## get posts

@app.get('/posts',tags=['posts'])

def get_posts():
    return {"data":posts}

##get posts for id

@app.get('/posts/{id}',tags=["posts"])

def get_one_post(id:int):
    if id>len(posts):
        return {
            "error":"Post with this id doesn't exist"

        }
    for post in posts :
        if post["id"]==id:
            return {
                "data":post
            }
## post a blog post a hadler por creating a post

@app.post('/posts',dependencies=[Depends(jwtBearer())] , tags=['posts'])

def add_post(post:PostSchema):
    post.id=len(posts)+1
    posts.append(post.__dict__)
    return {
        "success":"post addied"
    }

@app.post('/users/signup',tags=["user"])

def user_signup(user:UserSchema=Body(default=None)):
    users.append(user)

    return signJwt(user.email)

def check_user(data:UserLoginSchema):
    print(data)
    
    for user in users:
        if user.email==data.email and user.password==data.password:
            return True
        return False
    
@app.post('/user/login',tags=["user"])

def user_login(user:UserLoginSchema=Body(default=None)):
    if check_user(user):
        return signJwt(user.email)
    else:
        return {
            "error":"Invalid login details"
        }