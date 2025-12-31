from fastapi import FastAPI,Request,Depends
from database import init_db,insert_user,getuser,create_users_table,create_teams_table,insert_team,update_team,delete_team,get_all_teams,retrieve_team
import passlib
from pydantic import BaseModel
from auth import hash_password,verify_password,create_access_token,verify_token
from fastapi.security import HTTPBearer



create_users_table()

app = FastAPI()
security = HTTPBearer()





@app.get('/')
async def home():
    return {"message": "Task Management API"}


#                                REGISTER AND LOGIN ENDPOINTS
class User_reg(BaseModel):
    username : str
    email : str
    password : str


class User_log(BaseModel):
    username : str
    password : str

@app.post("/register")
async def register(user:User_reg):
    username = user.username
    email = user.email
    password = user.password


    hashed = hash_password(password)

    insert_user(username,email,hashed)
    return {"message": "Successfully registered"}

@app.post('/login')
async def login(user:User_log):
    username = user.username

    values = getuser(username)
    if values is None:
        return {"error": "Invalid username or password"}
    hashed = values[3]
    check = verify_password(user.password,hashed)
    if check:
        token = create_access_token(username)
        return {"access_token": token, "token_type": "bearer"}
    else:
        return {"error": "Invalid username or password"}


#                                          CRUD TEAMs ENPOINTS
class teams(BaseModel):
        name : str
        description : str    

@app.post('/teams')
async def create_team(request:Request,team:teams, credentials = Depends(security)):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer"):
        token = auth_header.split()[1]
        token = token.strip('"')
        created_by = verify_token(token)
        if created_by:
            user = getuser(created_by)
            id = user[0]
            name = team.name
            desc = team.description

            insert_team(name,desc,id)
            return {"message": "Team created"}
    return {"error":"Could not create team"}
    


@app.get('/teams')
async def get_teams(request:Request,credentials = Depends(security)):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer"):
        token = auth_header.split()[1]
        token = token.strip('"')
        created_by = verify_token(token)
        if created_by:
            values = get_all_teams()
            return values
    return {"error": "Unauthorized"}


@app.get("/teams/{team_id}")
async def get_team(request:Request,team_id:int,credentials = Depends(security)):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer"):
        token = auth_header.split()[1]
        token = token.strip('"')
        created_by = verify_token(token)
        if created_by:
            value = retrieve_team(team_id)

            return value
    return {"error": "Unauthorized"}

class updateteam(BaseModel):
    name : str
    description : str

@app.put("/teams/{team_id}")
async def update(team_id:int,request:Request,team:updateteam,credentials = Depends(security)):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer"):
        token = auth_header.split()[1]
        token = token.strip('"')
        created_by = verify_token(token)
        if created_by:
            user = retrieve_team(team_id)
            if user:
                name = team.name
                desc = team.description
                update_team(team_id,name,desc)

                return {"message": "Updated"}
    
    return {"error": "Unauthorized"}

@app.delete("/teams/{team_id}")
async def delete(team_id:int,request:Request,credentials = Depends(security)):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer"):
        token = auth_header.split()[1]
        token = token.strip('"')
        created_by = verify_token(token)
        if created_by:
            user = getuser(created_by)
            user_id = user[0]

            team = retrieve_team(team_id)
            if team and team[3] == user_id:
                delete_team(team_id)
                return {'message': 'Deleted'}
            
    return {"error": "Unauthorized"}