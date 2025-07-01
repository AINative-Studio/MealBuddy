# MealBuddy

AI-Powered Meal Planning Application

## 🚀 Features

- **Personalized Meal Plans**: AI-generated meal plans based on your preferences
- **Pantry Integration**: Sync with your pantry and fridge inventory
- **Dietary Restrictions**: Support for various dietary needs and preferences
- **Grocery Lists**: Automatically generated shopping lists
- **Recipe Management**: Save and organize your favorite recipes

## 🏗️ Project Structure

```
mealbuddy/
├── backend/               # FastAPI backend
│   ├── app/               # Application code
│   │   ├── api/           # API routes
│   │   ├── core/          # Core configurations
│   │   ├── db/            # Database models and migrations
│   │   ├── models/        # SQLAlchemy models
│   │   └── main.py        # FastAPI application
│   ├── tests/             # Backend tests
│   ├── alembic/           # Database migrations
│   └── requirements.txt   # Python dependencies
│
├── frontend/              # Next.js frontend
│   ├── src/
│   │   ├── app/          # Next.js 13+ app directory
│   │   ├── components/    # Reusable components
│   │   └── styles/       # Global styles
│   └── package.json      # Frontend dependencies
│
├── docs/                 # Project documentation
├── scripts/              # Utility scripts
└── docker-compose.yml    # Docker Compose configuration
```

## 🛠️ Development Setup

### Prerequisites

- Docker and Docker Compose (recommended)
- Node.js 18+ (if not using Docker)
- Python 3.11+ (if not using Docker)
- PostgreSQL 13+ (if not using Docker)

### With Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/mealbuddy.git
   cd mealbuddy
   ```

2. **Start the development environment**
   ```bash
   make init-db     # Initialize the database
   make up          # Start all services
   ```

3. **Access the applications**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Database: PostgreSQL at localhost:5432

### Without Docker

#### Backend Setup

1. **Set up Python environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Set up database**
   - Create a PostgreSQL database named `mealbuddy_dev`
   - Update the database connection in `backend/.env`

3. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

4. **Start the backend server**
   ```bash
   uvicorn app.main:app --reload
   ```

#### Frontend Setup

1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Start the development server**
   ```bash
   npm run dev
   ```

## 🧪 Testing

### Run tests
```bash
make test
```

### Run linters
```bash
make lint
```

### Format code
```bash
make format
```

## 🚀 Deployment

### Production Build
```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with ❤️ using FastAPI and Next.js
- Inspired by the need for better meal planning solutions
- Thanks to all contributors who have helped with this project!
