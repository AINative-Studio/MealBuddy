from setuptools import setup, find_packages

setup(
    name="mealbuddy",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn[standard]>=0.24.0",
        "sqlalchemy[asyncio]>=2.0.23",
        "alembic>=1.13.0",
        "asyncpg>=0.28.0",
        "python-jose[cryptography]>=3.3.0",
        "passlib[bcrypt]>=1.7.4",
        "python-multipart>=0.0.6",
        "python-dotenv>=1.0.0",
        "pydantic[email]>=2.5.2",
        "pydantic-settings>=2.1.0",
        "email-validator>=2.0.0",
        "python-multipart>=0.0.6",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.12.0",
            "pytest-asyncio>=0.21.1",
            "black>=23.11.0",
            "isort>=5.12.0",
            "mypy>=1.7.0",
        ],
    },
    python_requires=">=3.9",
)
