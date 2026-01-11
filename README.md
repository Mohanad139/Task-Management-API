# MoTask Backend

REST API for MoTask - a collaborative project management platform built with FastAPI and PostgreSQL.

## 🚀 Live Demo

- **API**: https://task-management-api-production-a18c.up.railway.app
- **Frontend**: https://task-frontend-green-delta.vercel.app
- **API Docs**: https://task-management-api-production-a18c.up.railway.app/docs

## ✨ Features

- JWT-based authentication
- Team management with role-based access control
- Project organization and tracking
- Task assignment and status management
- Comment system for collaboration
- RESTful API design

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **Authentication**: JWT tokens
- **Deployment**: Railway

## 📋 API Endpoints

### Authentication
- `POST /register` - Create new account
- `POST /login` - Login and get JWT token
- `GET /me` - Get current user info

### Teams
- `GET /teams` - List user's teams
- `POST /teams` - Create new team
- `DELETE /teams/{id}` - Delete team
- `POST /teams/{id}/members` - Add team member
- `PUT /teams/{id}/members/{user_id}` - Update member role

### Projects
- `GET /teams/{id}/projects` - List team projects
- `POST /teams/{id}/projects` - Create project
- `PUT /projects/{id}` - Update project
- `DELETE /projects/{id}` - Delete project

### Tasks
- `GET /projects/{id}/tasks` - List project tasks
- `POST /projects/{id}/tasks` - Create task
- `PUT /tasks/{id}` - Update task
- `DELETE /tasks/{id}` - Delete task
- `POST /tasks/{id}/assign` - Assign users to task
- `DELETE /tasks/{id}/unassign/{user_id}` - Unassign user

### Comments
- `GET /tasks/{id}/comments` - List task comments
- `POST /tasks/{id}/comments` - Add comment
- `PUT /comments/{id}` - Update comment
- `DELETE /comments/{id}` - Delete comment

## 🏃 Local Development

### Prerequisites
- Python 3.10+
- PostgreSQL

### Setup

1. Clone the repository
```bash
git clone https://github.com/Mohanad139/Task-Management-API
cd Task-Management-API
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```


4. Start server
```bash
uvicorn app:app --reload
```

API will be available at `http://localhost:8000`

## 📦 Project Structure
```
motask-backend/
├── app.py              # FastAPI app and routes
├── database.py         # Database connection
├── requirements.txt    # Python dependencies
└── README.md
```

## 🔐 Environment Variables

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string (auto-set by Railway) |
| `JWT_SECRET_KEY` | Secret key for JWT tokens |

## 🚀 Deployment on Railway

1. Push code to GitHub
2. Create new project on Railway
3. Deploy from GitHub repo
4. Add PostgreSQL database
5. Add environment variable: `JWT_SECRET_KEY`
6. Railway auto-generates `DATABASE_URL`
7. Deploy!

## 📝 License

MIT License - feel free to use this project for learning and portfolio purposes.

## 👤 Author

**Mohanad Bahammam**
- GitHub: [@yourusername](https://github.com/Mohanad139)
- LinkedIn: [Your Profile](https://www.linkedin.com/in/mohanad-bahammam-5891b7380/)

## 🙏 Acknowledgments

Built as a portfolio project to demonstrate full-stack development skills with modern web technologies.