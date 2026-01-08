from fastapi import FastAPI,Request,Depends,HTTPException
from database import init_db,insert_user,getuser,create_users_table,create_teams_table,insert_team,update_team,delete_team,get_all_teams,retrieve_team,create_projects_table,get_all_projects,retrieve_project,insert_project,update_project,delete_project,create_team_memeber_table,insert_member,update_role,get_team_members,get_user_role,delete_member,get_team_id,create_task_asign_table,create_tasks_table,insert_task,unassign_task,update_taskdb,assign_task,get_all_tasks,get_task_assignees,get_task,delete_task,is_user_assigned,create_comment_table,insert_comment,get_comment,get_task_comments,update_comment,delete_comment,create_log_table,insert_activity_log
import passlib
from pydantic import BaseModel, validator, EmailStr
from auth import hash_password,verify_password,create_access_token,verify_token
from fastapi.security import HTTPBearer
from datetime import datetime
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware





create_users_table()
create_teams_table()
create_team_memeber_table()
create_projects_table()
create_tasks_table()
create_task_asign_table()
create_comment_table()
create_log_table()

app = FastAPI()
security = HTTPBearer()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tuesday-git-main-mohanads-projects-7f4efaf5.vercel.app"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)





@app.get('/')
async def home():
    return {"message": "Task Management API"}


#                                REGISTER AND LOGIN ENDPOINTS
class User_reg(BaseModel):
    username : str
    email : str
    password : str

    @validator('username')
    def validator_username(cls,v):
        if not v or not v.strip():
            raise ValueError("Username can not be empty")
        if len(v) <= 3 or len(v) >= 50:
            raise ValueError("Username need to be in range 3 - 50 characters")
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Username can only contain letters, numbers, underscores, and hyphens')
        return v.strip()
    @validator('email')
    def validator_email(cls,v):
        if not v or not v.strip():
            raise ValueError("Email can not be empty")
        if "@" not in v or "." not in v:
            raise ValueError("Wrong Email Format")
        if len(v) > 100:
            raise ValueError("Email must be lower than 100 characters")
        return v.strip().lower()
    
    @validator('password')
    def validate_password(cls, v):
        if not v:
            raise ValueError('Password cannot be empty')
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if len(v) > 128:
            raise ValueError('Password must be less than 128 characters')
        return v


        
        

class User_log(BaseModel):
    username : str
    password : str

    @validator('username')
    def validate_username(cls, v):
        if not v or not v.strip():
            raise ValueError('Username cannot be empty')
        return v.strip()
    
    @validator('password')
    def validate_password(cls, v):
        if not v:
            raise ValueError('Password cannot be empty')
        return v

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
        raise HTTPException(status_code=401, detail='Invalid password or username')
    hashed = values[3]
    check = verify_password(user.password,hashed)
    if check:
        token = create_access_token(username)
        return {"access_token": token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail='Invalid password or username')








@app.get('/me')
async def get_current_user(request: Request, credentials = Depends(security)):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer"):
        token = auth_header.split()[1]
        token = token.strip('"')
        username = verify_token(token)
        if username:
            user = getuser(username)
            return {
                "id": user[0],
                "username": user[1],
                "email": user[2]
            }
    raise HTTPException(status_code=401, detail="Unauthorized")







#                                          CRUD TEAMs ENPOINTS
class teams(BaseModel):
        name : str
        description : str    

        @validator('name')
        def validate_name(cls, v):
            if not v or not v.strip():
                raise ValueError('Team name cannot be empty')
            if len(v) > 100:
                raise ValueError('Team name must be less than 100 characters')
            return v.strip()
        @validator('description')
        def validate_description(cls, v):
            if v and len(v) > 500:
                raise ValueError('Description must be less than 500 characters')
            return v.strip() if v else ''

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
            insert_activity_log(id, 'create_team', 'team', team_id, 'Created Team {name}')


            return {"message": "Team created"}
    raise HTTPException(status_code=401, detail='Could not create a team')
    


@app.get('/teams')
async def get_allteams(request:Request,credentials = Depends(security)):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer"):
        token = auth_header.split()[1]
        token = token.strip('"')
        created_by = verify_token(token)
        if created_by:
            user = getuser(created_by)
            user_id = user[0]
            values = get_all_teams(user_id)
            return values
    raise HTTPException(status_code=401, detail='Not Authorized')


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
    raise HTTPException(status_code=401, detail='Not Authorized')

class updateteam(BaseModel):
    name : str
    description : str

    @validator('name')
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Team name cannot be empty')
        if len(v) > 100:
            raise ValueError('Team name must be less than 100 characters')
        return v.strip()
    
    @validator('description')
    def validate_description(cls, v):
        if v and len(v) > 500:
            raise ValueError('Description must be less than 500 characters')
        return v.strip() if v else ''

@app.put("/teams/{team_id}")
async def update(team_id:int,request:Request,team:updateteam,credentials = Depends(security)):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer"):
        token = auth_header.split()[1]
        token = token.strip('"')
        created_by = verify_token(token)
        if created_by:
            names = getuser(created_by)
            id = names[0]
            user = retrieve_team(team_id)
            if user:
                name = team.name
                desc = team.description
                update_team(team_id,name,desc)
                insert_activity_log(id, 'update', 'team', team_id, 'Updated team {user}')

                return {"message": "Updated"}
    
    raise HTTPException(status_code=401, detail='Not Authorized')

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
                insert_activity_log(user_id, 'delete', 'team', team_id, "Deleted team {team}")
                return {'message': 'Deleted'}
            
    raise HTTPException(status_code=401, detail='Not Authorized')





#                                     TEAM_MEMBERS ENDPOINTS

class getid(BaseModel):
    username : str
    @validator('username')
    def validate_username(cls, v):
        if not v or not v.strip():
            raise ValueError('Username cannot be empty')
        return v.strip()


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
                raise HTTPException(status_code=404, detail='Not Authorized')
            role = get_user_role(id,team_id)
            if role == 'member':
                raise HTTPException(status_code=404, detail='Admin only can add member')
            else:
                username = users.username
                name = getuser(username)
                user_id = name[0]
                insert_member(user_id,team_id)
                insert_activity_log(user_id, 'add_member', 'Team_member', team_id, 'ADDED TEAM MEMBER {username}')
                return {"message": "Member has been added"}            
            
    raise HTTPException(status_code=401, detail='Not Authorized')

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
                    raise HTTPException(status_code=404, detail='Not Authorized')
            values = get_team_members(team_id)

            return {'members': values}
    raise HTTPException(status_code=401, detail='Not Authorized')

class getrole(BaseModel):
    role : str
    @validator('role')
    def validate_role(cls, v):
        valid_roles = ['admin', 'member']
        if v not in valid_roles:
            raise ValueError(f'Role must be one of: {", ".join(valid_roles)}')
        return v


@app.put('/teams/{team_id}/members/{user_id}')
async def update(team_id: int,user_id: int,new:getrole,request:Request,credentials = Depends(security)):
    if new.role not in ['admin', 'member']:
        raise ValueError ("Can only set role to admin or member")
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer"):
        token = auth_header.split()[1]
        token = token.strip('"')
        created_by = verify_token(token)
        if created_by:
            user = getuser(created_by)
            owner_id = user[0]
            role = get_user_role(owner_id,team_id)
            if owner_id == user_id:
                raise HTTPException(status_code=404, detail='Can not change owner role')
            if role == 'admin':
                target_role = get_user_role(user_id,team_id)
                if target_role != 'member':
                    raise HTTPException(status_code=404, detail='Admin can only change member')
                else:
                    update_role(user_id,team_id,new.role)
                    insert_activity_log(user_id, "update_role", 'team_member', team_id, 'Updated Role {user_id} to {new.role}')
                    return {'message':'Role has been updated'}
            elif role == 'owner':
                update_role(user_id,team_id,new.role)
                insert_activity_log(user_id, "update_role", 'team_member', team_id, 'Updated Role {user_id} to {new.role}')
                return {'message':'Role has been updated'}
    raise HTTPException(status_code=401, detail='Not Authorized')
                
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
                    raise HTTPException(status_code=404, detail='Admin can only remove member')
                else:
                    delete_member(user_id,team_id)
                    insert_activity_log(user_id, 'delete_member', 'team_member', team_id, 'DELETED member {created_by}}')
                    return {'message':'Member has been removed'}
            elif role == 'owner':
                delete_member(user_id,team_id)
                insert_activity_log(user_id, 'delete_member', 'team_member', team_id, 'DELETED member {created_by}')
                return {'message':'Member has been removed'}



    raise HTTPException(status_code=401, detail='Not Authorized')













#                                              CRUD PROJECTS ENDPOINTS

class project_data(BaseModel):
    name : str
    description : str
    status : str
    @validator('name')
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Project name cannot be empty')
        if len(v) > 100:
            raise ValueError('Project name must be less than 100 characters')
        return v.strip()
    
    @validator('description')
    def validate_description(cls, v):
        if v and len(v) > 500:
            raise ValueError('Description must be less than 500 characters')
        return v.strip() if v else ''
    
    @validator('status')
    def validate_status(cls, v):
        valid_statuses = ['active', 'completed', 'archived']
        if v not in valid_statuses:
            raise ValueError(f'Status must be one of: {", ".join(valid_statuses)}')
        return v


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
    
    raise HTTPException(status_code=401, detail='Not Authorized')





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
    raise HTTPException(status_code=401, detail='Not Authorized')




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
                raise HTTPException(status_code=404, detail='Project not found')
            team_id = project[1]
            members = get_user_role(user_id,team_id)
            if members is not None:
                return {'message':project}
    raise HTTPException(status_code=401, detail='Not Authorized')


class updateproj(BaseModel):
    name : str
    description:str
    status:str
    @validator('name')
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Project name cannot be empty')
        if len(v) > 100:
            raise ValueError('Project name must be less than 100 characters')
        return v.strip()
    
    @validator('description')
    def validate_description(cls, v):
        if v and len(v) > 500:
            raise ValueError('Description must be less than 500 characters')
        return v.strip() if v else ''
    
    @validator('status')
    def validate_status(cls, v):
        valid_statuses = ['active', 'completed', 'archived']
        if v not in valid_statuses:
            raise ValueError(f'Status must be one of: {", ".join(valid_statuses)}')
        return v

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
                raise HTTPException(status_code=404, detail='Project not found')
            team_id = project[1]
            members = get_user_role(user_id,team_id)
            if members in ['owner','admin']:
                name = data.name
                desc = data.description
                status = data.status
                update_project(project_id,name,desc,status)
                insert_activity_log(user_id, 'update_project', 'project', project_id, "Updated project from {project}")

                return {'message': 'Project got updated'}
            elif members == 'member':
                if user_id == project[4]:
                    name = data.name
                    desc = data.description
                    status = data.status
                    update_project(project_id,name,desc,status)
                    insert_activity_log(user_id, 'update_project', 'project', project_id, "Updated project from {project}")
                    return {'message': 'Project got updated'}

    
    raise HTTPException(status_code=401, detail='Not Authorized')
                



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
                raise HTTPException(status_code=404, detail='Project not found')
            team_id = project[1]
            members = get_user_role(user_id,team_id)
            if members in ['owner','admin']:
                delete_project(project_id)
                insert_activity_log(user_id, 'delete_project', 'project', project_id, "DELETE A PROJECT {project}")
                return {'message':'Project got deleted'}
            elif members == 'member':
                if user_id == project[4]:
                    delete_project(project_id)
                    return {'message':'Project got deleted'}

    raise HTTPException(status_code=401, detail='Not Authorized')














#                                         CRUD TASK ENDPOINT
class task_data(BaseModel):
    title :str
    description : str
    status : str
    priority : str
    due_date: Optional[datetime] = None
    @validator('title')
    def validate_title(cls, v):
        if not v or not v.strip():
            raise ValueError('Task title cannot be empty')
        if len(v) > 100:
            raise ValueError('Task title must be less than 100 characters')
        return v.strip()
    
    @validator('description')
    def validate_description(cls, v):
        if v and len(v) > 1000:
            raise ValueError('Description must be less than 1000 characters')
        return v.strip() if v else ''
    
    @validator('status')
    def validate_status(cls, v):
        valid_statuses = ['todo', 'in_progress', 'done', 'blocked']
        if v not in valid_statuses:
            raise ValueError(f'Status must be one of: {", ".join(valid_statuses)}')
        return v
    
    @validator('priority')
    def validate_priority(cls, v):
        valid_priorities = ['low', 'medium', 'high', 'urgent']
        if v not in valid_priorities:
            raise ValueError(f'Priority must be one of: {", ".join(valid_priorities)}')
        return v

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
                raise HTTPException(status_code=404, detail='Project not found')
            team_id = project[1]
            members = get_user_role(user_id,team_id)
            if members:
                insert_task(project_id, data.title, data.description, data.status, data.priority,data.due_date, user_id)
                return {'message':'Inserted'}
    raise HTTPException(status_code=401, detail='Not Authorized')

@app.get('/projects/{project_id}/tasks')
async def get_tasks(project_id: int,request: Request, credentials = Depends(security), status: Optional[str] = None, priority: Optional[str] = None, assigned_to: Optional[int] = None):
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
                raise HTTPException(status_code=404, detail='Project not found')
            team_id = project[1]
            members = get_user_role(user_id,team_id)
            if members:
                tasks = get_all_tasks(project[0], status, priority, assigned_to)
                return {'Tasks': tasks}
            
    raise HTTPException(status_code=401, detail='Not Authorized')



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
                raise HTTPException(status_code=404, detail='Project not found')
            team_id = project[1]
            members = get_user_role(user_id,team_id)
            if members:
                task = get_task(task_id)
                return {'Task': task}
            
    raise HTTPException(status_code=401, detail='Not Authorized')

class updatetask(BaseModel):
    title:str
    description:str
    status:str
    priority:str 
    due_date: Optional[datetime] = None
    @validator('title')
    def validate_title(cls, v):
        if not v or not v.strip():
            raise ValueError('Task title cannot be empty')
        if len(v) > 100:
            raise ValueError('Task title must be less than 100 characters')
        return v.strip()
    
    @validator('description')
    def validate_description(cls, v):
        if v and len(v) > 1000:
            raise ValueError('Description must be less than 1000 characters')
        return v.strip() if v else ''
    
    @validator('status')
    def validate_status(cls, v):
        valid_statuses = ['todo', 'in_progress', 'done', 'blocked']
        if v not in valid_statuses:
            raise ValueError(f'Status must be one of: {", ".join(valid_statuses)}')
        return v
    
    @validator('priority')
    def validate_priority(cls, v):
        valid_priorities = ['low', 'medium', 'high', 'urgent']
        if v not in valid_priorities:
            raise ValueError(f'Priority must be one of: {", ".join(valid_priorities)}')
        return v


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
                raise HTTPException(status_code=404, detail='Project not found')
            team_id = project[1]
            members = get_user_role(user_id,team_id)
            task = get_task(task_id)
            if members in ['owner','admin'] or user_id == task[7] or is_user_assigned(task_id, user_id):
                update_taskdb(task_id,data.title, data.description, data.status, data.priority, data.due_date)
                insert_activity_log(user_id, 'update_taskdb', 'task', task_id, 'Update a task from {task} to new')
                return {'Message':'Data has been updated'}
    raise HTTPException(status_code=401, detail='Not Authorized')



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
                raise HTTPException(status_code=404, detail='Project not found')
            team_id = project[1]
            members = get_user_role(user_id,team_id)
            task = get_task(task_id)
            if members in ['owner','admin'] or user_id == task[7]:
                delete_task(task_id)
                insert_activity_log(user_id, 'delete_task', 'task', task_id, 'DELETED A TASK {task}')
                return {'Message':'Task has been deleted'}
    raise HTTPException(status_code=401, detail='Not Authorized')











#                                         CRUD TASK_assignment ENDPOINT

class AssignTask(BaseModel):
    user_ids: list[int]

    @validator('user_ids')
    def validate_user_ids(cls, v):
        if not v:
            raise ValueError('Must provide at least one user ID')
        if len(v) > 20:
            raise ValueError('Cannot assign more than 20 users at once')
        if len(v) != len(set(v)):
            raise ValueError('Duplicate user IDs not allowed')
        return v

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
                raise HTTPException(status_code=404, detail='Project not found')
            team_id = project[1]
            members = get_user_role(user_id,team_id)
            task = get_task(task_id)

            if members in ['owner','admin'] or user_id == task[7]:
                for id in data.user_ids:
                    member = get_user_role(id,team_id)
                    if (not (is_user_assigned(task_id,id))) and member:
                        assign_task(task_id,id)
                        insert_activity_log(user_id, 'assign task', 'assign-task', task_id, 'Assigned task to {id}')
                    else:
                        continue
                return {"Message": 'Task has been assigned'}
    raise HTTPException(status_code=401, detail='Not Authorized')

@app.delete('/tasks/{task_id}/unassign/{user_id}')
async def unassigntask(task_id:int,user_id:str,request:Request,credentials = Depends(security)):
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
                raise HTTPException(status_code=404, detail='Project not found')
            team_id = project[1]
            members = get_user_role(id,team_id)
            task = get_task(task_id)
            userid = getuser(user_id)[0]

            if members in ['owner','admin'] or id == task[7] or id == userid:
                unassign_task(task_id,userid)
                insert_activity_log(id, 'unassign_task', 'assign-task', task_id, 'Unassign task from {userid}')
                return {'Message': 'User has been unassigned'}
    raise HTTPException(status_code=401, detail='Not Authorized')


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
                raise HTTPException(status_code=404, detail='Project not found')
            team_id = project[1]
            members = get_user_role(id,team_id)

            if members:
                assignees = get_task_assignees(task_id)
                return {'Assigned to :': assignees}
    raise HTTPException(status_code=401, detail='Not Authorized')









class CommentData(BaseModel):
    comment: str
    @validator('comment')
    def validate_comment(cls, v):
        if not v or not v.strip():
            raise ValueError('Comment cannot be empty')
        if len(v) > 2000:
            raise ValueError('Comment must be less than 2000 characters')
        return v.strip()



#                                                  CRUD COMMENTS ENDPOINTS
@app.post('/tasks/{task_id}/comments')
async def create_comment_endpoint(task_id:int,data:CommentData,request:Request,credentials = Depends(security)):
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
                raise HTTPException(status_code=404, detail='Project not found')
            team_id = project[1]
            members = get_user_role(id,team_id)
            if members:
                insert_comment(task_id,data.comment,id)
                return {'Message':'Comment has been inserted'}
    raise HTTPException(status_code=401, detail='Not Authorized')

@app.get('/tasks/{task_id}/comments')
async def getallcomments(task_id:int,request:Request,credentials = Depends(security)):
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
                raise HTTPException(status_code=404, detail='Project not found')
            team_id = project[1]
            members = get_user_role(id,team_id)
            if members:
                comments = get_task_comments(task_id)
                return {'Comments': comments}
            
    raise HTTPException(status_code=401, detail='Not Authorized')


@app.get('/comments/{comment_id}')
async def get_comment_endpoints(comment_id:int,request:Request,credentials = Depends(security)):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer"):
        token = auth_header.split()[1]
        token = token.strip('"')
        created_by = verify_token(token)
        # I have user_id,username,comment_id I want project_id,task_id
        if created_by:
            user = getuser(created_by)
            id = user[0]
            comment = get_comment(comment_id)
            task_id = comment[1]
            project_id = get_task(task_id)[1]
            project = retrieve_project(project_id)
            if not project:
                raise HTTPException(status_code=404, detail='Project not found')
            team_id = project[1]
            members = get_user_role(id,team_id)
            if members:
                return {'Comment':comment}
    raise HTTPException(status_code=401, detail='Not Authorized')

@app.put('/comments/{comment_id}')
async def update_comment_ednpoint(comment_id:int,data:CommentData,request:Request,credentials = Depends(security)):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer"):
        token = auth_header.split()[1]
        token = token.strip('"')
        created_by = verify_token(token)
        # I have user_id,username,comment_id I want project_id,task_id
        if created_by:
            user = getuser(created_by)
            id = user[0]
            comment = get_comment(comment_id)
            task_id = comment[1]
            project_id = get_task(task_id)[1]
            project = retrieve_project(project_id)
            if not project:
                raise HTTPException(status_code=404, detail='Project not found')
            team_id = project[1]
            members = get_user_role(id,team_id)
            if members and id == comment[3]:
                update_comment(comment_id,data.comment)
                insert_activity_log(id, 'update comment', 'comment', comment_id, "From {comment} to {data.comment}")
                return {'Message':'Comment has been updated'}
    raise HTTPException(status_code=401, detail='Not Authorized')

@app.delete('/comments/{comment_id}')
async def delete_comment_endpoint(comment_id:int,request:Request,credentials = Depends(security)):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer"):
        token = auth_header.split()[1]
        token = token.strip('"')
        created_by = verify_token(token)
        # I have user_id,username,comment_id I want project_id,task_id
        if created_by:
            user = getuser(created_by)
            id = user[0]
            comment = get_comment(comment_id)
            task_id = comment[1]
            project_id = get_task(task_id)[1]
            project = retrieve_project(project_id)
            if not project:
                raise HTTPException(status_code=404, detail='Project not found')
            team_id = project[1]
            members = get_user_role(id,team_id)
            if members in ['owner','admin'] or id == comment[3]:
                delete_comment(comment_id)
                insert_activity_log(id, 'delete_comment', 'comment',comment_id, 'Deleted a comment : {comment}')
                return {'Message':'Comment has been deleted'}
    raise HTTPException(status_code=401, detail='Not Authorized')





