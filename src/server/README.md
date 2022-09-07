## Инициализация проекта

### Alembic

Инициализация (асинхронный драйвер):

```sh
poetry run alembic init -t async alembic
```

В файле `env.py`:

```python
from src.db_conf.models import Base
from src.shared.settings import settings
config.set_main_option("sqlalchemy.url", settings.db_conf_url)
target_metadata = Base.metadata # edit
```