# Django ORM & Database Migrations: Deep-Dive Guide

## Overview & Core Concepts

### What is Django ORM?
The **Django Object-Relational Mapper (ORM)** is an abstraction layer that enables 
developers to interact with database engines (PostgreSQL, MySQL, SQLite, Oracle) using Python 
classes and objects instead of writing raw SQL queries.

- **Models as Blueprints**: Python classes inheriting from `django.db.models.Model` define table
  schemas, fields, relationships, validation constraints, and business logic.
- **Portability**: Database queries written via Django ORM automatically compile to target
  database
  dialect SQL.

### What are Database Migrations?
Django Migrations act as a version control system for your database schema. Instead of manually 
executing `CREATE TABLE` or `ALTER TABLE` SQL commands, Django generates declarative Python
scripts
in your app's `migrations/` directory that record incremental changes over time.

```
+------------------+     makemigrations      +-----------------------+
|  models.py       |  ------------------->   |  migrations/000X.py   |
|  (Current Schema)|  (Diffs models vs state)|  (Python Instructions)|
+------------------+                         +-----------------------+
                                                         |
                                                         | migrate
                                                         v (Compiles to SQL)
                                             +-----------------------+
                                             |   Database Schema     |
                                             |  + django_migrations  |
                                             +-----------------------+
```

---

## Models as the Single Source of Truth

Django models define the structure of your database tables.

```python
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "categories"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True, default="")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="recipes"
    )
    cooking_time_minutes = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "recipes"
        indexes = [
            models.Index(
                fields=["is_published", "-updated_at"],
                name="idx_recipe_pub_updated",
            ),
        ]
```

### Key Field Options & Schema Impact
- `null=True`: Database level. Allows column to store `NULL` values.
- `blank=True`: Application level. Form/serializer validation allows empty input.
- `default=val`: Provides default value for new rows.
- `db_index=True`: Creates database index on column.
- `unique=True`: Adds `UNIQUE` constraint at database level.
- `on_delete`: Configures foreign key constraint cascade rules (`CASCADE`, `PROTECT`,
  `SET_NULL`).

---

## Creating Migrations (`makemigrations`)

The `makemigrations` management command inspects your `models.py` files, compares them against 
existing migration state in `migrations/`, and generates new Python migration scripts.

```bash
# Generate migrations for all installed apps
uv run python manage.py makemigrations

# Generate migrations for a specific app
uv run python manage.py makemigrations core

# Generate an empty migration file for custom data migrations
uv run python manage.py makemigrations core --empty --name populate_categories

# Preview changes without writing migration files
uv run python manage.py makemigrations --dry-run

# Exit with error code if unmigrated model changes exist (ideal for CI pipelines)
uv run python manage.py makemigrations --check
```

### Migration File Structure
Generated migration files inherit from `django.db.migrations.Migration` and contain:
1. `dependencies`: List of tuple pairs `('app_name', 'migration_name')` that must execute
   before.
2. `operations`: Sequential list of operation instances (`CreateModel`, `AddField`,
   `RunPython`).

```python
# app/core/migrations/0002_add_recipe_fields.py
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="recipe",
            name="is_published",
            field=models.BooleanField(default=False),
        ),
    ]
```

---

## Applying & Managing Migrations (`migrate`)

The `migrate` command executes unapplied migration scripts against the targeted database.

```bash
# Apply all pending migrations across all apps
uv run python manage.py migrate

# Apply migrations up to a specific migration file
uv run python manage.py migrate core 0002

# Roll back all migrations for an app
uv run python manage.py migrate core zero

# View pending and applied migrations across apps
uv run python manage.py showmigrations

# Output raw SQL executed by a specific migration without touching DB
uv run python manage.py sqlmigrate core 0002

# Fake apply a migration (updates django_migrations without running SQL)
uv run python manage.py migrate core 0002 --fake
```

### Tracking Migrations (`django_migrations` table)
Django tracks state by recording applied migrations in a metadata table named
`django_migrations`:
- Columns: `id`, `app`, `name`, `applied` (timestamp).
- When running `migrate`, Django queries `django_migrations`, compares applied records with
  local
  migration files, builds a dependency DAG (Directed Acyclic Graph), and executes remaining
nodes.

---

## Advanced Migration Patterns

### 1. Data Migrations (`RunPython`)
When you need to transform or seed data alongside schema changes, use custom data migrations.

> **CRITICAL**: Never import models directly inside migration files (`from core.models import
> Recipe`).
> Always use `apps.get_model('app_name', 'ModelName')` to fetch historical model definitions
> matching
> the exact point in migration timeline.

```python
# Generated via: manage.py makemigrations core --empty --name split_user_name
from django.db import migrations


def forward_split_name(apps, schema_editor):
    User = apps.get_model("core", "User")
    for user in User.objects.all():
        parts = user.full_name.split(" ", 1)
        user.first_name = parts[0]
        user.last_name = parts[1] if len(parts) > 1 else ""
        user.save(update_fields=["first_name", "last_name"])


def reverse_split_name(apps, schema_editor):
    User = apps.get_model("core", "User")
    for user in User.objects.all():
        user.full_name = f"{user.first_name} {user.last_name}".strip()
        user.save(update_fields=["full_name"])


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_add_first_last_name"),
    ]

    operations = [
        migrations.RunPython(
            code=forward_split_name,
            reverse_code=reverse_split_name,
        ),
    ]
```

### 2. Direct SQL Execution (`RunSQL`)
For database-specific features (e.g. PostgreSQL triggers, stored procedures, extension
creation):

```python
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL(
            sql="CREATE INDEX CONCURRENTLY idx_recipe_title_trgm ON recipes USING gin (title
                gin_trgm_ops);",
            reverse_sql="DROP INDEX CONCURRENTLY IF EXISTS idx_recipe_title_trgm;",
        ),
    ]
```

### 3. Squashing Migrations
As a project grows, hundreds of migration files slow down test suites and deployment runs.
Squashing compresses linear migrations into a single consolidated migration.

```bash
# Squash migrations 0001 through 0015 into one
uv run python manage.py squashmigrations core 0015
```

---

## Production Best Practices & Pitfalls

1. **Commit Migration Files to Version Control**: Migration files are codebase source code.
2. **Zero-Downtime Multi-Stage Deployments**:
   - **Adding NOT NULL Column**:
     1. Add field as `null=True`. Deploy code & migrate schema.
     2. Run data migration to populate default values for existing rows.
     3. Update model field to `null=False` (or add constraint). Deploy & migrate schema.
   - **Renaming Column**:
     1. Add new column. Dual-write in application layer.
     2. Backfill historical data.
     3. Switch reads to new column.
     4. Deprecate and drop old column in subsequent release.
3. **PostgreSQL Concurrent Indexing**:
   - Standard index creation acquires an `SHARE` lock, blocking writes during index build.
   - Use `AddIndexConcurrently` from `django.contrib.postgres.operations` inside non-atomic
migrations.

---

## References & Authoritative Sources
- [Django Docs: Migrations
  Overview](https://docs.djangoproject.com/en/stable/topics/migrations/)
- [Django Docs: Migration Operations
  Reference](https://docs.djangoproject.com/en/stable/ref/schema-editor/)
- [Django Docs: Writing Database
  Migrations](https://docs.djangoproject.com/en/stable/howto/writing-migrations/)

---

## Interview Questions & Answers (5 YOE Senior Level)

### Q1: How does Django track applied migrations, and why is using `apps.get_model()` mandatory
    inside data migrations instead of importing model classes directly?
**Answer**:
Django tracks executed migrations in the `django_migrations` table stored inside the database.
When `manage.py migrate` is executed, Django builds a Directed Acyclic Graph (DAG) of local
migration files and compares them against rows in `django_migrations` to determine which
migrations remain unapplied.

Inside data migrations (`RunPython`), using `apps.get_model('app_name', 'ModelName')` fetches a
**historical model state** representing how the model was defined at that specific point in the
migration timeline.

Directly importing a model (`from core.models import User`) uses the **current live Python
code** state. If a developer later removes a field or renames a method on `User`, running
historic migration history from scratch (e.g. in CI pipelines or new environment setups) will
crash with `AttributeError` or `FieldError` because the current code no longer matches
historical schema expectations.

**Follow-up Question**: What happens if `apps.get_model()` is called for a model that has custom
methods defined in `models.py`?
*Answer*: Historical models generated by `apps.get_model()` do not carry custom model instance
methods or signals defined on the live class; only fields, managers, and database meta
properties are preserved.

---

### Q2: You need to add a `NOT NULL` column with no default value to a table with 50 million
    rows in a live production PostgreSQL database. How do you execute this with zero downtime?
**Answer**:
Executing `ALTER TABLE recipes ADD COLUMN status VARCHAR(20) NOT NULL;` directly on a
50-million-row table in PostgreSQL requires a table rewrite or table lock (`ACCESS EXCLUSIVE`),
blocking all reads and writes and causing application downtime or query timeouts.

To achieve zero-downtime execution:
1. **Stage 1 (Schema Addition)**: Add the field to Django model as `null=True, blank=True`. Run
   `makemigrations` and `migrate`. Adding a nullable column in PostgreSQL (v11+) is an instant
   metadata-only operation acquiring a brief lock.
2. **Stage 2 (Application Dual-Write / Defaulting)**: Update application code so all newly
   created/updated rows explicitly populate the new field value.
3. **Stage 3 (Batch Data Migration)**: Execute a background task or script to backfill existing
   NULL rows in small batches (e.g. 5,000 rows per batch using `LIMIT/OFFSET` or primary key
   ranges) to prevent long transaction locks and replication lag.
4. **Stage 4 (Add Check Constraint / NOT NULL)**: Add `NOT NULL` constraint using `RunSQL`:
   - In PostgreSQL, add constraint as `NOT VALID` (`ALTER TABLE recipes ADD CONSTRAINT
check_status_not_null CHECK (status IS NOT NULL) NOT VALID;`), which acquires a minimal lock
without validating existing data.
   - Run `ALTER TABLE recipes VALIDATE CONSTRAINT check_status_not_null;`, which scans table
without blocking concurrent writes.
   - Optionally update Django model definition to `null=False` with
`separate_database_inside=True` or `state_operations`.

**Follow-up Question**: How does PostgreSQL 11+ handle adding non-null columns with a constant
default value differently than older versions?
*Answer*: PostgreSQL 11+ stores constant default values in table metadata without updating
existing rows on disk, making `ADD COLUMN ... DEFAULT 'val' NOT NULL` an O(1) instant operation.

---

### Q3: Write a production-ready Django data migration script (`RunPython`) to split a single
    `full_name` column into `first_name` and `last_name` columns with full rollback support.
**Answer**:

```python
from django.db import migrations, models


def forward_split_names(apps, schema_editor):
    User = apps.get_model("core", "User")
    # Use iterator() to process in chunks and save RAM on large datasets
    users_to_update = []
    for user in User.objects.filter(first_name="").iterator(chunk_size=2000):
        parts = (user.full_name or "").strip().split(" ", 1)
        user.first_name = parts[0] if parts else ""
        user.last_name = parts[1] if len(parts) > 1 else ""
        users_to_update.append(user)

        if len(users_to_update) >= 2000:
            User.objects.bulk_update(
                users_to_update, ["first_name", "last_name"]
            )
            users_to_update.clear()

    if users_to_update:
        User.objects.bulk_update(users_to_update, ["first_name", "last_name"])


def reverse_combine_names(apps, schema_editor):
    User = apps.get_model("core", "User")
    users_to_update = []
    for user in User.objects.iterator(chunk_size=2000):
        user.full_name = f"{user.first_name} {user.last_name}".strip()
        users_to_update.append(user)

        if len(users_to_update) >= 2000:
            User.objects.bulk_update(users_to_update, ["full_name"])
            users_to_update.clear()

    if users_to_update:
        User.objects.bulk_update(users_to_update, ["full_name"])


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_add_first_last_name_fields"),
    ]

    operations = [
        migrations.RunPython(
            code=forward_split_names,
            reverse_code=reverse_combine_names,
            elidable=False,
        ),
    ]
```

**Follow-up Question**: What does `elidable=False` mean on `RunPython`?  
*Answer*: `elidable=False` ensures that when migrations are squashed using `squashmigrations`,
Django will not omit/discard this `RunPython` operation from the squashed output file.

---

### Q4: Two engineers on different git branches created separate migrations named
    `0003_add_bio.py` and `0003_add_avatar.py`. When merging branches, Django throws a command
    error about multiple leaf nodes. How do you resolve this?
**Answer**:
When two developers create migrations off the same parent migration (`0002_initial.py`), Django
detects a split branch (multiple leaf nodes) in the dependency DAG.

Resolution Workflow:
1. **Interactive Merge (`makemigrations --merge`)**:
   Run `uv run python manage.py makemigrations --merge`. Django prompts to generate a new merge
migration file (e.g. `0004_merge_20260809_1200.py`) whose `dependencies` list both leaf
migrations:
   ```python
   dependencies = [
       ("core", "0003_add_bio"),
       ("core", "0003_add_avatar"),
   ]
   ```
2. **Sequential Renaming (Clean Git History Alternative)**:
   If the branch has not been merged to main/production yet, one developer can rename their
migration file to `0004_add_avatar.py` and update its `dependencies` pointer from `0002` to
`0003_add_bio`.
3. **Verification**:
   Run `uv run python manage.py showmigrations` to ensure a clean linear execution graph without
multiple unmerged heads.

**Follow-up Question**: What risk occurs if one developer has already applied their `0003`
migration locally and then renames it?
*Answer*: Django's local `django_migrations` table records `0003_add_avatar`. Renaming the file
without unapplying it first (`migrate app 0002`) causes Django to consider the renamed file
unapplied while leaving orphan rows in `django_migrations`, requiring `--fake` or database
cleanup.

---

### Q5: How do you create a PostgreSQL index on a live Django production database without
    locking the table against writes, and why does standard Django `models.Index` lock tables?
**Answer**:
By default, when Django applies `migrations.AddIndex` or `models.Index`, it generates a standard
SQL `CREATE INDEX` statement. PostgreSQL acquires a `SHARE` lock during standard index creation,
which allows `SELECT` reads but blocks all concurrent `INSERT`, `UPDATE`, and `DELETE` queries
until index building completes.

To create an index concurrently without blocking writes:
1. Use `django.contrib.postgres.operations.AddIndexConcurrently` instead of standard `AddIndex`.
2. Disable atomic transaction wrapper on the migration class by setting `atomic = False`.
   PostgreSQL prohibits `CREATE INDEX CONCURRENTLY` inside a transaction block.

```python
from django.contrib.postgres.operations import AddIndexConcurrently
from django.db import migrations, models


class Migration(migrations.Migration):
    atomic = False  # Mandatory for concurrent index operations in Postgres

    dependencies = [
        ("core", "0005_previous_migration"),
    ]

    operations = [
        AddIndexConcurrently(
            model_name="recipe",
            index=models.Index(
                fields=["title"], name="recipe_title_concurrent_idx"
            ),
        ),
    ]
```

**Follow-up Question**: What happens if index creation fails mid-way during
`AddIndexConcurrently`?
*Answer*: PostgreSQL leaves an invalid index marked `INVALID`. Django's migration engine fails,
and the invalid index must be dropped manually (`DROP INDEX CONCURRENTLY`) before re-running the
migration.
