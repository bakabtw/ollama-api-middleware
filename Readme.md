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
apt install docker.io docker-compose-v2 apparmor-utils git
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
- Используемые модели
    - Генерация текста: `LLama3-Lexi-Aura-3Some-SLERP-SLERP.f16.gguf`
    - Обработка текста: `T-lite-instruct-0.1-abliterated.f16.gguf`

- Cкачивание моделей (все модели должны находиться в папке `./ollama`)
    - Lama3-Lexi-Aura-3Some-SLERP-SLERP.f16.gguf
    ```bash
    wget https://huggingface.co/mradermacher/LLama3-Lexi-Aura-3Some-SLERP-SLERP-GGUF/resolve/main/LLama3-Lexi-Aura-3Some-SLERP-SLERP.f16.gguf -O ollama/LLama3-Lexi-Aura-3Some-SLERP-SLERP.f16.gguf
    ```

    - T-lite-instruct-0.1-abliterated.f16.gguf
    ```bash
    wget https://huggingface.co/mradermacher/T-lite-instruct-0.1-abliterated-GGUF/resolve/main/T-lite-instruct-0.1-abliterated.f16.gguf -O ollama/T-lite-instruct-0.1-abliterated.f16.gguf
    ```

- Создаем модель для генерации текста
```bash
docker compose exec ollama ollama create generator -f /root/.ollama/Modelfile-step1
```

- Создаем модель для обработки текста
```bash
docker compose exec ollama ollama create processor -f /root/.ollama/Modelfile-step2
```

## Настройка API
Все настройки меняются через `app.py`:

```python
OLLAMA_HOST = os.environ.get('OLLAMA_HOST', 'http://localhost:11434')  # API endpoint for Ollama
STEP1_MODEL = "generator"  # Step1 model name
STEP2_MODEL = "processor"  # Step2 model name
STEP1_PROMPT = ""  # SYSTEM prompt for step1 model
STEP2_PROMPT = ""  # SYSTEM prompt for step1 model
```

После внесения изменений, перезапустите сервис:
```bash
docker compose up -d app
```