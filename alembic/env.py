from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from api.database import Base  # استيراد Base من database

# هذا هو ملف إعدادات Alembic الذي يتيح الوصول إلى القيم من ملف ini
config = context.config

# تكوين السجلات (loggers)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# تحديد الـ target_metadata
target_metadata = Base.metadata  # هذا هو المطلوب لكي يتمكن Alembic من عمل الميجريشن بشكل صحيح

def run_migrations_offline() -> None:
    """تشغيل الميجريشن في وضع 'off-line'"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """تشغيل الميجريشن في وضع 'online'"""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

# تشغيل الميجريشن بناءً على وضع الاتصال
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
