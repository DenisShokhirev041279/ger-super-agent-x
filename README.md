# ⚡ GER Super Agent X

> Ультра-мощный AI-ассистент для русскоязычных контент-мейкеров  
> Цифровой клон **GER DENNIS AI** · Превосходит Manus & Genspark

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.52+-red?logo=streamlit)](https://streamlit.io)
[![Claude](https://img.shields.io/badge/Claude-3.5%20Sonnet-orange?logo=anthropic)](https://anthropic.com)
[![LangChain](https://img.shields.io/badge/LangChain-ReAct%20Agent-green)](https://langchain.com)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## 🚀 О проекте

**GER Super Agent X** — это Streamlit-приложение с ReAct-агентом на базе Claude 3.5 Sonnet и LangChain. Создан специально для русскоязычных контент-мейкеров, помогает с:

- 🎬 Созданием сценариев для Reels / TikTok / YouTube Shorts
- 🔥 Поиском актуальных трендов в реальном времени (DuckDuckGo)
- 🎙️ Озвучкой текстов русским голосом (ElevenLabs)
- 🤖 Промптингом, AI-продуктами и автоматизацией бизнеса
- 💰 Стратегиями монетизации личного бренда

---

## ✅ Чеклист возможностей

### Ядро агента
- [x] Claude 3.5 Sonnet (`claude-3-5-sonnet-20241022`) через `langchain-anthropic`
- [x] ReAct-агент (`create_react_agent`) из `langchain_classic`
- [x] Контекстная память — последние 20 сообщений чата
- [x] Максимум 5 итераций рассуждений на запрос
- [x] Обработка ошибок парсинга (`handle_parsing_errors=True`)

### Инструменты
- [x] 🔍 **Web Search** — поиск в DuckDuckGo (до 5 результатов)
- [x] 🎙️ **Text-to-Speech** — озвучка русским голосом ElevenLabs (`eleven_multilingual_v2`)
- [ ] 📄 RAG (работа с документами) — в разработке
- [ ] 🖼️ Генерация изображений — запланировано
- [ ] 🐍 Code Interpreter — запланировано

### UI / UX
- [x] Космический неоновый дизайн (тёмный градиент, neon cyan/purple)
- [x] Шрифты Orbitron + Rajdhani (Google Fonts)
- [x] Анимированный заголовок с градиентом
- [x] Боковая панель с быстрыми действиями
- [x] Индикатор статуса (ONLINE / DEMO MODE)
- [x] Отображение истории чата со стилями

### Безопасность & надёжность
- [x] Rate limiting: 10 запросов / 60 секунд на сессию
- [x] Счётчики использования (всего, AI, поиск, TTS, ошибки)
- [x] try/except обёртки вокруг всех внешних API
- [x] DEMO-режим при отсутствии `ANTHROPIC_API_KEY`
- [x] Логирование событий с временными метками

### Быстрые действия (сайдбар)
- [x] 🔥 Тренды AI сегодня
- [x] ✍️ Пост в стиле GER DENNIS
- [x] 🎬 Сценарий Reels
- [x] 🎙️ Озвучить последний текст
- [x] 🧠 Что ты помнишь?
- [x] 🗑️ Очистить чат

---

## 🛠️ Установка и запуск

### Требования
- Python 3.11+
- API ключ Anthropic (Claude)
- API ключ ElevenLabs (опционально, для TTS)

### Быстрый старт

```bash
# 1. Клонируй репозиторий
git clone https://github.com/DenisShokhirev041279/ger-super-agent-x.git
cd ger-super-agent-x

# 2. Установи зависимости
pip install -r requirements.txt

# 3. Задай переменные окружения
export ANTHROPIC_API_KEY="sk-ant-..."
export ELEVENLABS_API_KEY="sk_..."   # опционально

# 4. Запусти приложение
streamlit run app.py
```

### Запуск через uv (рекомендуется)

```bash
uv sync
uv run streamlit run app.py
```

### Через Replit
Просто форкни этот репозиторий на [Replit](https://replit.com) и добавь ключи в **Secrets**.

---

## ⚙️ Конфигурация

| Переменная окружения | Обязательно | Описание |
|---|---|---|
| `ANTHROPIC_API_KEY` | ✅ Да | Claude API ключ. Без него — DEMO режим |
| `ELEVENLABS_API_KEY` | ❌ Нет | ElevenLabs TTS. Без него — озвучка отключена |

---

## 📦 Зависимости

```
streamlit>=1.52
langchain>=1.2.0
langchain-anthropic>=1.3.1
langchain-community>=0.4.1
langchain-classic (ReAct агент)
anthropic>=0.75.0
duckduckgo-search>=8.1.1
elevenlabs>=2.28.0
faiss-cpu>=1.13.2
beautifulsoup4>=4.14.3
requests>=2.32.5
```

---

## 🏗️ Структура проекта

```
ger-super-agent-x/
├── app.py                  # Главный файл — вся логика и UI
├── .streamlit/
│   └── config.toml         # Тема и настройки сервера Streamlit
├── pyproject.toml          # Зависимости Python (uv/pip)
├── requirements.txt        # Зависимости для pip install
├── audio_output/           # Сохранённые TTS-аудиофайлы (авто)
└── README.md
```

---

## 🎯 Архитектура агента

```
Пользователь → Streamlit UI
                    ↓
            get_agent_response()
                    ↓
         Rate Limit Check (10/60s)
                    ↓
         LangChain ReAct Agent
         (Claude 3.5 Sonnet)
              ↙          ↘
     WebSearch Tool    TextToSpeech Tool
    (DuckDuckGo)       (ElevenLabs)
```

---

## 🔗 GER DENNIS AI — Площадки

| Платформа | Ссылка |
|---|---|
| 📢 Telegram | [t.me/ger_dennis_ai](https://t.me/ger_dennis_ai) |
| 📱 Instagram | [instagram.com/shohirevdenis](https://www.instagram.com/shohirevdenis/) |
| 🎥 YouTube | [youtube.com/@ger_dennis_ai](https://youtube.com/@ger_dennis_ai) |
| 🎵 TikTok | [tiktok.com/@ger.dennis.ai](https://www.tiktok.com/@ger.dennis.ai) |
| 🐦 X/Twitter | [x.com/shohirevdenis](https://x.com/shohirevdenis) |
| 🧵 Threads | [threads.com/@shohirevdenis](https://www.threads.com/@shohirevdenis) |
| 💼 Портфолио | [Кейсы и проекты](https://ger-dennis-ai-ai--skbrxy4.gamma.site/) |

---

## 📄 Лицензия

MIT License — используй свободно, делай форки, улучшай!

---

<div align="center">
⚡ Powered by <strong>GER DENNIS AI</strong> · Claude 3.5 Sonnet · LangChain · Streamlit<br>
🚀 Создавай вирусный контент · Автоматизируй бизнес · Доминируй в AI
</div>
