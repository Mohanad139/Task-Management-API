from fastapi import FastAPI,Request,Depends,HTTPException
from database import init_db,insert_user,getuser,create_users_table,create_teams_table,insert_team,update_team,delete_team,get_all_teams,retrieve_team,create_projects_table,get_all_projects,retrieve_project,insert_project,update_project,delete_project,create_team_memeber_table,insert_member,update_role,get_team_members,get_user_role,delete_member,get_team_id,create_task_asign_table,create_tasks_table,insert_task,unassign_task,update_taskdb,assign_task,get_all_tasks,get_task_assignees,get_task,delete_task,is_user_assigned
import passlib
from pydantic import BaseModel
from auth import hash_password,verify_password,create_access_token,verify_token
from fastapi.security import HTTPBearer
from datetime import datetime
from typing import Optional




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
async def create_team(team:teams, request: Request,credentials = Depends(security)):
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
            team_id = get_team_id(name)
            insert_member(id,team_id)
            update_role(id,team_id,"owner")


            return {"message": "Team created"}
    return {"error":"Could not create team"}
    


@app.get('/teams')
async def get_allteams(request:Request,credentials = Depends(security)):
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





#                                     TEAM_MEMBERS ENDPOINTS

class getid(BaseModel):
    username : str


@app.post('/teams/{team_id}/members')
async def add_member(team_id:int,users:getid,request:Request,credentials = Depends(security)):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer"):
        token = auth_header.split()[1]
        token = token.strip('"')
        created_by = verify_token(token)
        if created_by:
            user = getuser(created_by)
            id = user[0]
            members = get_team_members(team_id)
            member_ids = [member[0] for member in members]
            if id not in member_ids:
                return {'error':'Not Authorized'}
            role = get_user_role(id,team_id)
            if role == 'member':
                return {'error':'Member can not add'}
            else:
                username = users.username
                name = getuser(username)
                user_id = name[0]
                insert_member(user_id,team_id)
                return {"message": "Member has been added"}            
            
    return "Not Authorized"


@app.get('/teams/{team_id}/members')
async def get_members(team_id: int,request:Request,credentials = Depends(security)):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer"):
        token = auth_header.split()[1]
        token = token.strip('"')
        created_by = verify_token(token)
        if created_by:
            user = getuser(created_by)
            user_id = user[0]   
            members = get_team_members(team_id)
            member_ids = [member[0] for member in members]
            if user_id not in member_ids:
                return {'error':'Not Authorized'}
            values = get_team_members(team_id)

            return {'members': values}
    return "Not Authorized"

class getrole(BaseModel):
    role : str


@app.put('/teams/{team_id}/members/{user_id}')
async def update(team_id: int,user_id: int,new:getrole,request:Request,credentials = Depends(security)):
    if new.role not in ['admin', 'member']:
        return {"error": "Can only set role to admin or member"}
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer"):
        token = auth_header.split()[1]
        token = token.strip('"')
        created_by = verify_token(token)
        if created_by:
            user = getuser(created_by)
            owner_id = user[0]
            role = get_user_role(owner_id,team_id)
            if role == 'admin':
                target_role = get_user_role(user_id,team_id)
                if target_role != 'member':
                    return {"error": "Admins can only change member roles"}
                else:
                    update_role(user_id,team_id,new.role)
                    return {'message':'Role has been updated'}
            elif role == 'owner':
                update_role(user_id,team_id,new.role)
                return {'message':'Role has been updated'}

    return "Not Authorized"
                
@app.delete('/teams/{team_id}/members/{user_id}')
async def remove_member(user_id: int,team_id: int,request:Request,credentials = Depends(security)):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer"):
        token = auth_header.split()[1]
        token = token.strip('"')
        created_by = verify_token(token)
        if created_by:
            user = getuser(created_by)
            owner_id = user[0]
            role = get_user_role(owner_id,team_id)
            if role == 'admin':
                target_role = get_user_role(user_id,team_id)
                if target_role != 'member':
                    return {"error": "Admins can only delete member"}
                else:
                    delete_member(user_id,team_id)
                    return {'message':'Member has been removed'}
            elif role == 'owner':
                delete_member(user_id,team_id)
                return {'message':'Member has been removed'}



    return "Not Authorized"













#                                              CRUD PROJECTS ENDPOINTS

class project_data(BaseModel):
    name : str
    description : str
    status : str


@app.post('/teams/{team_id}/projects')
async def create_project(team_id: int,proj:project_data,request:Request,credentials = Depends(security)):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer"):
        token = auth_header.split()[1]
        token = token.strip('"')
        created_by = verify_token(token)
        if created_by:
            user = getuser(created_by)
            user_id = user[0]
            members = get_user_role(user_id,team_id)
            if members is not None:
                status = proj.status
                if status in ['active','completed','archived']:
                    insert_project(team_id,proj.name,proj.description,user_id,proj.status)
                    return {'message':'Project has been created'}
                else:
                    return {'error':'Status must be (active,completed,archived) '}
    
    return {'error':'Not Authorized'}





@app.get('/teams/{team_id}/projects')
async def get_allprojects(team_id:int,request:Request,credentials = Depends(security)):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer"):
        token = auth_header.split()[1]
        token = token.strip('"')
        created_by = verify_token(token)
        if created_by:
            user = getuser(created_by)
            user_id = user[0]
            members = get_user_role(user_id,team_id)
            if members is not None:
                projects = get_all_projects(team_id)
                return {'Projects':projects}
    return {'error':'Not Authorized'}




@app.get('/projects/{project_id}')
async def get_project(project_id : int,request:Request,credentials = Depends(security)):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer"):
        token = auth_header.split()[1]
        token = token.strip('"')
        created_by = verify_token(token)
        if created_by:
            user = getuser(created_by)
            user_id = user[0]
            project = retrieve_project(project_id)
            if not project:
                return {'error': "Project not found"}
            team_id = project[1]
            members = get_user_role(user_id,team_id)
            if members is not None:
                return {'message':project}
    return {'error':'Not Authorized'}


class updateproj(BaseModel):
    name : str
    description:str
    status:str

@app.put('/projects/{project_id}')
async def update_projects(project_id:int,data:updateproj,request:Request,credentials = Depends(security)):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer"):
        token = auth_header.split()[1]
        token = token.strip('"')
        created_by = verify_token(token)
        if created_by:
            user = getuser(created_by)
            user_id = user[0]
            project = retrieve_project(project_id)
            if not project:
                return {'error': "Project not found"}
            team_id = project[1]
            members = get_user_role(user_id,team_id)
            if members in ['owner','admin']:
                name = data.name
                desc = data.description
                status = data.status
                update_project(project_id,name,desc,status)
                return {'message': 'Project got updated'}
            elif members == 'member':
                if user_id == project[4]:
                    name = data.name
                    desc = data.description
                    status = data.status
                    update_project(project_id,name,desc,status)
                    return {'message': 'Project got updated'}

    
    return {'error':'Not Authorized'}
                



@app.delete('/projects/{project_id}')
async def delete_projects(project_id:int,request:Request,credentials = Depends(security)):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer"):
        token = auth_header.split()[1]
        token = token.strip('"')
        created_by = verify_token(token)
        if created_by:
            user = getuser(created_by)
            user_id = user[0]
            project = retrieve_project(project_id)
            if not project:
                return {'error': "Project not found"}
            team_id = project[1]
            members = get_user_role(user_id,team_id)
            if members in ['owner','admin']:
                delete_project(project_id)
                return {'message':'Project got deleted'}
            elif members == 'member':
                if user_id == project[4]:
                    delete_project(project_id)
                    return {'message':'Project got deleted'}

    return {'error':'Not Authorized'}














#                                         CRUD TASK ENDPOINT
class task_data(BaseModel):
    title :str
    description : str
    status : str
    priority : str
    due_date: Optional[datetime] = None

@app.post('/projects/{project_id}/tasks')
async def create_task(project_id : int,data:task_data,request:Request,credentials = Depends(security)):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer"):
        token = auth_header.split()[1]
        token = token.strip('"')
        created_by = verify_token(token)
        if created_by:
            user = getuser(created_by)
            user_id = user[0]
            project = retrieve_project(project_id)
            if not project:
                return {'error': "Project not found"}
            team_id = project[1]
            members = get_user_role(user_id,team_id)
            if members:
                insert_task(project_id, data.title, data.description, data.status, data.priority,data.due_date, user_id)
                return {'message':'Inserted'}
    return {'error':'Not Authorized'}

@app.get('/projects/{project_id}/tasks')
async def get_tasks(project_id:int,request:Request,credentials = Depends(security)):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer"):
        token = auth_header.split()[1]
        token = token.strip('"')
        created_by = verify_token(token)
        if created_by:
            user = getuser(created_by)
            user_id = user[0]
            project = retrieve_project(project_id)
            if not project:
                return {'error': "Project not found"}
            team_id = project[1]
            members = get_user_role(user_id,team_id)
            if members:
                tasks = get_all_tasks(project[0])
                return {'Tasks': tasks}
            
    return {'Error': 'Not Authorized'}



@app.get('/tasks/{task_id}')
async def retrieve_task(task_id : int,request:Request,credentials = Depends(security)):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer"):
        token = auth_header.split()[1]
        token = token.strip('"')
        created_by = verify_token(token)
        # I have username,user_id,task_id,. I need team_id to check if he is a member of the team.
        if created_by:
            user = getuser(created_by)
            user_id = user[0]
            project_id = get_task(task_id)[1]
            project = retrieve_project(project_id)
            if not project:
                return {'error': "Project not found"}
            team_id = project[1]
            members = get_user_role(user_id,team_id)
            if members:
                task = get_task(task_id)
                return {'Task': task}
            
    return {'Error': 'Not Authorized'}

class updatetask(BaseModel):
    title:str
    description:str
    status:str
    priority:str 
    due_date: Optional[datetime] = None


@app.put('/tasks/{task_id}')
async def update_task(task_id:int,data:updatetask,request:Request,credentials = Depends(security)):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer"):
        token = auth_header.split()[1]
        token = token.strip('"')
        created_by = verify_token(token)

        if created_by:
            user = getuser(created_by)
            user_id = user[0]
            project_id = get_task(task_id)[1]
            project = retrieve_project(project_id)
            if not project:
                return {'error': "Project not found"}
            team_id = project[1]
            members = get_user_role(user_id,team_id)
            task = get_task(task_id)
            if members in ['owner','admin'] or user_id == task[7] or is_user_assigned(task_id, user_id):
                update_taskdb(task_id,data.title, data.description, data.status, data.priority, data.due_date)
                return {'Message':'Data has been updated'}
    return {'Error': 'Not Authorized'}



@app.delete('/tasks/{task_id}')
async def deletetask(task_id:int,request:Request,credentials = Depends(security)):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer"):
        token = auth_header.split()[1]
        token = token.strip('"')
        created_by = verify_token(token)

        if created_by:
            user = getuser(created_by)
            user_id = user[0]
            project_id = get_task(task_id)[1]
            project = retrieve_project(project_id)
            if not project:
                return {'error': "Project not found"}
            team_id = project[1]
            members = get_user_role(user_id,team_id)
            task = get_task(task_id)
            if members in ['owner','admin'] or user_id == task[7]:
                delete_task(task_id)
                return {'Message':'Task has been deleted'}
    return {'Error': 'Not Authorized'}











#                                         CRUD TASK_assignment ENDPOINT

class AssignTask(BaseModel):
    user_ids: list[int]

@app.post('/tasks/{task_id}/assign')
async def assigntask(task_id:int,data:AssignTask,request:Request,credentials = Depends(security)):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer"):
        token = auth_header.split()[1]
        token = token.strip('"')
        created_by = verify_token(token)

        if created_by:
            user = getuser(created_by)
            user_id = user[0]
            project_id = get_task(task_id)[1]
            project = retrieve_project(project_id)
            if not project:
                return {'error': "Project not found"}
            team_id = project[1]
            members = get_user_role(user_id,team_id)
            task = get_task(task_id)

            if members in ['owner','admin'] or user_id == task[7]:
                for id in data.user_ids:
                    member = get_user_role(id,team_id)
                    if (not (is_user_assigned(task_id,id))) and member:
                        assign_task(task_id,id)
                    else:
                        continue
                return {"Message": 'Task has been assigned'}
    return {'Error':'Not Authorized'}

@app.delete('/tasks/{task_id}/unassign/{user_id}')
async def unassigntask(task_id:int,user_id:int,request:Request,credentials = Depends(security)):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer"):
        token = auth_header.split()[1]
        token = token.strip('"')
        created_by = verify_token(token)

        if created_by:
            user = getuser(created_by)
            id = user[0]
            project_id = get_task(task_id)[1]
            project = retrieve_project(project_id)
            if not project:
                return {'error': "Project not found"}
            team_id = project[1]
            members = get_user_role(id,team_id)
            task = get_task(task_id)

            if members in ['owner','admin'] or id == task[7] or id == user_id:
                unassign_task(task_id,user_id)
                return {'Message': 'User has been unassigned'}
    return {'Error': 'Not Authorized'}


@app.get('/tasks/{task_id}/assignees')
async def get_assignees(task_id:int,request:Request,credentials = Depends(security)):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer"):
        token = auth_header.split()[1]
        token = token.strip('"')
        created_by = verify_token(token)

        if created_by:
            user = getuser(created_by)
            id = user[0]
            project_id = get_task(task_id)[1]
            project = retrieve_project(project_id)
            if not project:
                return {'error': "Project not found"}
            team_id = project[1]
            members = get_user_role(id,team_id)

            if members:
                assignees = get_task_assignees(task_id)
                return {'Assigned to :': assignees}
    return {'Error':'Not Authorized'}






