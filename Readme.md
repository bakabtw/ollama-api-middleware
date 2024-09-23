# ollama-api-middleware

API сервис предназначенный для генерации и последующей обработки текста разными нейросетями.

# Запуск
## Требования
- docker
- docker-compose
- nvidia toolkit

## Установка
- Установка зависимостей
```bash
apt install docker.io docker-compose-v2 apparmor-utils
```

- Копирование репозитория
```bash
git clone https://github.com/bakabtw/ollama-api-middleware
```

- Переходим в скопированную директорию
```bash
cd ollama-api-middleware
```

- Запускаем контейнеры
```bash
docker compose up -d
```

Сервис почти готов к использованию, осталось добавить модели.

# Установка моделей
По-умолчанию, ollama будет запущена без доступных моделей.

## Импорт моделей
- Модель для генерации текста
```bash
docker compose exec ollama ollama create generator -f ./Modelfile-step1
```

- Модель для генерации текста
```bash
docker compose exec ollama ollama create processor -f ./Modelfile-step2
```

## Настройка API
Все настройки меняются через `docker-compose.yml`:

```docker
environment:
    - OLLAMA_HOST=http://ollama:11434 # Адрес ollama
    - STEP1_MODEL=generator # Название модели для генерации текста
    - STEP2_MODEL=processor # Название модели для обработки текста
```

После внесения изменений, перезапустите сервис:
```bash
docker compose up -d app
```