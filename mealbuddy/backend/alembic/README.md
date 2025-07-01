# Database Migrations

This directory contains Alembic database migrations for the MealBuddy application.

## Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL database
- Dependencies installed (run `pip install -e .` from the project root)

### Configuration

1. Ensure your `.env` file is properly configured with the correct database connection string.
2. The migrations will use the `DATABASE_URL` environment variable from your `.env` file.

## Migration Commands

### Create a new migration

```bash
alembic revision --autogenerate -m "description of changes"
```

### Apply all pending migrations

```bash
alembic upgrade head
```

### Rollback the last migration

```bash
alembic downgrade -1
```

### Check current migration status

```bash
alembic current
```

## Best Practices

1. Always review the generated migration scripts before applying them.
2. Test migrations in a development environment before applying to production.
3. Never modify migration files after they have been applied to a production database.
4. Use descriptive migration messages that explain the purpose of the changes.

## Troubleshooting

### Common Issues

1. **Database Connection Errors**: Verify your `.env` file has the correct database credentials.
2. **Migration Conflicts**: If you encounter conflicts, you may need to manually resolve them or recreate your database.
3. **Async Issues**: Ensure all database operations in your migration scripts are synchronous.

### Resetting the Database

In development, you can reset the database with:

```bash
dropdb -U postgres mealbuddy
createdb -U postgres mealbuddy
alembic upgrade head
```

## Version Control

- Always commit migration files to version control.
- Never delete migration files that have been applied to production.
- Coordinate with your team when creating and applying migrations to avoid conflicts.
