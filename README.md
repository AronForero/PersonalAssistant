# PersonalAssistant

A FastAPI-based personal assistant API that handles to-do lists, expenses (personal and shared), and manages user profiles using LangGraph agents. Designed to integrate with **N8N** workflows and **Telegram** for task and expense management.

## Features

- **Task Management**: Create, update, and manage personal tasks with deadlines and status tracking
- **Expense Tracking**: Track personal and shared expenses with categories
- **User Profiles**: Store and manage user preferences, interests, and profile information
- **LangGraph Agents**: Extensible agent system for intelligent task and expense management
- **RESTful API**: Clean FastAPI endpoints for all operations
- **Database Migrations**: Alembic-powered schema versioning
- **N8N Integration**: Designed to work seamlessly with N8N workflows for automation

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **LangGraph**: Agent orchestration framework
- **LangChain**: LLM integration
- **PostgreSQL**: Database
- **SQLAlchemy**: ORM for database operations
- **Alembic**: Database migration tool
- **Pydantic**: Data validation and settings management
- **N8N**: Workflow automation platform (integrated)

## Project Structure

```
PersonalAssistant/
├── app/
│   ├── agents/          # LangGraph agents (manager, supervisor, task_assistant, expense_assistant)
│   ├── api/
│   │   └── routes/     # API endpoints (agents, tasks, expenses, userprofile)
│   ├── core/           # Configuration and dependencies
│   ├── db/             # Database models, CRUD operations, and ORM
│   ├── models/         # Pydantic schemas for API validation
│   └── main.py         # FastAPI application entry point
├── alembic/             # Database migrations
├── run.py              # Application runner script
├── requirements.txt    # Python dependencies
└── .env                # Environment variables (create from .env.example WIP)
```

## Installation

### Prerequisites

- Python 3.9+
- PostgreSQL database
- OpenAI API key (for LLM agents)

### Setup

1. **Clone the repository** (if applicable) or navigate to the project directory

2. **Create and activate virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file** from `.env.example`:
   ```env
   # Database Configuration
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=personal_assistant
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password

   # OpenAI API Key
   OPENAI_API_KEY=your_openai_api_key_here

   # Optional: LangChain and LangSmith
   LANGCHAIN_API_KEY=your_langchain_api_key_here
   LANGSMITH_API_KEY=your_langsmith_api_key_here

   # Agent Configuration
   DEFAULT_MODEL=gpt-4.1-nano
   DEFAULT_TEMPERATURE=0.5
   DEBUG=True
   ```

5. **Set up database**:
   ```bash
   # Create initial migration (if not exists)
   alembic revision --autogenerate -m "Initial schema"
   
   # Apply migrations
   alembic upgrade head
   ```

## Running the Application

### Development Mode

```bash
python run.py
```

The API will be available at `http://127.0.0.1:8000`

### Interactive API Documentation

- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

## API Endpoints

### Health Check
- `GET /health` - Health check endpoint

### Agents
- `GET /api/agents` - List all available agents
- `GET /api/agents/{agent_name}/info` - Get agent information
- `POST /api/agents/{agent_name}/invoke` - Invoke an agent

### Tasks
- `GET /api/task/{user_id}` - Get all tasks for a user
- `GET /api/task/{user_id}/{task_id}` - Get a specific task
- `POST /api/task` - Create a new task
- `PUT /api/task/{task_id}` - Update a task

### Expenses
- `GET /api/expense/{user_id}` - Get all expenses for a user
- `GET /api/expense/{user_id}/{expense_id}` - Get a specific expense
- `POST /api/expense` - Create a new expense
- `PUT /api/expense/{expense_id}` - Update an expense

### User Profile
- `GET /api/userprofile/{user_id}` - Get user profile (Telegram ID)
- `POST /api/userprofile` - Create user profile
- `PUT /api/userprofile/{user_id}` - Update user profile

## Database Migrations

### Create a new migration
```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations
```bash
alembic upgrade head
```

### Rollback last migration
```bash
alembic downgrade -1
```

## Configuration

All configuration is managed through environment variables in `.env`:

- **Database**: Connection settings for PostgreSQL
- **LLM**: OpenAI API key and model configuration
- **Timezone**: Application uses Colombia timezone (UTC-5)

## N8N Integration

This API is designed to work seamlessly with **N8N** workflows. You can:

- **Trigger workflows** from N8N using HTTP Request nodes pointing to API endpoints
- **Receive webhooks** from N8N to process tasks and expenses
- **Automate workflows** that interact with the personal assistant API
- **Integrate with Telegram** through N8N's Telegram nodes combined with this API

### Example simple N8N Workflow

1. **Telegram Trigger** → Receives message from user
2. **HTTP Request** → Calls `/api/agents/{agent_name}/invoke` with user query
3. **Process Response** → Handles agent response and sends back to Telegram

The API's RESTful design makes it easy to integrate with N8N's HTTP Request nodes for complete workflow automation.

## Future Development

The project is designed to support:

- **Manager Agent**: Simple keyword-based routing
- **Supervisor Agent**: LLM-based intelligent routing
- **Task Assistant**: Specialized agent for task management
- **Expense Assistant**: Specialized agent for expense tracking

## License

Copyright (c) 2025 ARMONDATA S.A.S.

All rights reserved.

This software and associated documentation files (the "Software") are proprietary 
and confidential. Unauthorized copying, distribution, modification, or use of this 
Software, via any medium, is strictly prohibited without the express written 
permission of ARMONDATA S.A.S.

For licensing inquiries, please contact ARMONDATA S.A.S.

## Contributing

[Add contribution guidelines if applicable]
