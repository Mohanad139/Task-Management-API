# Task Management API

A REST API for managing teams, projects, and tasks with role-based permissions. Built with FastAPI and PostgreSQL.

## 🔗 Live Demo

**Swagger Docs:** http://3.18.101.209:8000/docs

## 🛠️ Tech Stack

- FastAPI (Python)
- PostgreSQL (AWS RDS)
- JWT Authentication
- Docker
- AWS EC2 + RDS

## ✨ Features

- User authentication with JWT
- Team management with roles (owner/admin/member)
- Project and task CRUD operations
- Multiple users per task
- Comments with edit tracking
- Activity logging
- Filter tasks by status, priority, assignee

## 🚀 Quick Start
```bash
git clone https://github.com/Mohanad139/Task-Management-API.git
cd Task-Management-API
docker compose up --build
```

Access at: http://localhost:8000/docs

## 📊 Database Schema

- **users** - Authentication and profiles
- **teams** - Workspaces with members
- **projects** - Belong to teams
- **tasks** - Work items with status/priority
- **task_assignments** - Many-to-many user-task relationship
- **comments** - Task discussions
- **activity_logs** - Audit trail

## 🌐 Deployment

- **Database:** AWS RDS PostgreSQL
- **Server:** AWS EC2 with Docker
- **Access:** http://3.18.101.209:8000

## 📝 Main Endpoints

- `POST /register` - Create account
- `POST /login` - Get JWT token
- Team, project, task CRUD at `/teams`, `/projects`, `/tasks`
- Full docs at `/docs`

## 🔮 Next Steps

- React frontend
- Real-time updates
- File attachments
- Notifications

---

Built with FastAPI by [@Mohanad139](https://github.com/Mohanad139)