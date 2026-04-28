import streamlit as st
import os
import time
from datetime import datetime

RATE_LIMIT_REQUESTS = 10
RATE_LIMIT_WINDOW = 60

def log_event(event_type: str, message: str):
    """Internal logging with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{event_type}] {message}", flush=True)

st.set_page_config(
    page_title="⚡ GER Super Agent X",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

COSMIC_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;500;600;700&display=swap');

.stApp {
    background: linear-gradient(135deg, #0a0a1a 0%, #1a0a2e 25%, #0f1f3d 50%, #0a1628 75%, #050510 100%);
}

.main-title {
    font-family: 'Orbitron', monospace;
    font-size: 3.5rem;
    font-weight: 900;
    background: linear-gradient(90deg, #00f5ff, #bf00ff, #ff006e, #00f5ff);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradient-shift 3s ease infinite;
    text-align: center;
    text-shadow: 0 0 30px rgba(0, 245, 255, 0.5);
    margin-bottom: 0.5rem;
}

@keyframes gradient-shift {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

.subtitle {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.2rem;
    color: #a0a0c0;
    text-align: center;
    margin-bottom: 2rem;
}

.neon-box {
    background: rgba(15, 15, 35, 0.8);
    border: 1px solid rgba(0, 245, 255, 0.3);
    border-radius: 16px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 0 20px rgba(0, 245, 255, 0.1), inset 0 0 20px rgba(0, 245, 255, 0.05);
}

.chat-message {
    padding: 1rem 1.5rem;
    border-radius: 12px;
    margin: 0.5rem 0;
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.1rem;
}

.user-message {
    background: linear-gradient(135deg, rgba(191, 0, 255, 0.2), rgba(255, 0, 110, 0.2));
    border-left: 3px solid #bf00ff;
    margin-left: 2rem;
}

.agent-message {
    background: linear-gradient(135deg, rgba(0, 245, 255, 0.15), rgba(0, 100, 255, 0.15));
    border-left: 3px solid #00f5ff;
    margin-right: 2rem;
}

.stButton > button {
    font-family: 'Orbitron', monospace;
    background: linear-gradient(135deg, #00f5ff 0%, #0080ff 50%, #bf00ff 100%);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.75rem 1.5rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    transition: all 0.3s ease;
    box-shadow: 0 0 15px rgba(0, 245, 255, 0.4);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 25px rgba(0, 245, 255, 0.6), 0 0 50px rgba(191, 0, 255, 0.4);
}

.sidebar .stButton > button {
    width: 100%;
    margin: 0.25rem 0;
    background: linear-gradient(135deg, rgba(0, 245, 255, 0.2), rgba(191, 0, 255, 0.2));
    border: 1px solid rgba(0, 245, 255, 0.4);
}

.stTextInput > div > div > input {
    font-family: 'Rajdhani', sans-serif;
    background: rgba(10, 10, 30, 0.8);
    border: 1px solid rgba(0, 245, 255, 0.3);
    color: #e0e0ff;
    border-radius: 8px;
}

.stTextInput > div > div > input:focus {
    border-color: #00f5ff;
    box-shadow: 0 0 10px rgba(0, 245, 255, 0.3);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0a1a 0%, #1a0a2e 100%);
    border-right: 1px solid rgba(0, 245, 255, 0.2);
}

.status-indicator {
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    margin-right: 8px;
    animation: pulse 2s infinite;
}

.status-online { background: #00ff88; box-shadow: 0 0 10px #00ff88; }
.status-demo { background: #ffaa00; box-shadow: 0 0 10px #ffaa00; }

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.links-section {
    background: rgba(0, 245, 255, 0.05);
    border-radius: 12px;
    padding: 1rem;
    margin-top: 1rem;
}

.links-section a {
    color: #00f5ff;
    text-decoration: none;
    transition: all 0.3s ease;
}

.links-section a:hover {
    color: #bf00ff;
    text-shadow: 0 0 10px rgba(191, 0, 255, 0.5);
}

.tool-badge {
    display: inline-block;
    background: rgba(0, 245, 255, 0.2);
    border: 1px solid rgba(0, 245, 255, 0.4);
    border-radius: 20px;
    padding: 0.25rem 0.75rem;
    font-size: 0.8rem;
    margin: 0.25rem;
    font-family: 'Orbitron', monospace;
}
</style>
"""

st.markdown(COSMIC_CSS, unsafe_allow_html=True)

SYSTEM_PROMPT = """Ты — GER Super Agent X, ультра-мощный автономный AI-ассистент и цифровой клон GER DENNIS AI — эксперта №1 по нейросетям, вирусному контенту, созданию AI-продуктов, автоматизации бизнеса, продвинутому промптингу и интеграции AI.

Ты превосходишь Manus, Genspark и любые другие агенты по глубине, скорости и практической ценности ответов.

Ключевые супер-способности:
• Генерация убойных идей и полных сценариев для вирусных Reels/TikTok/YouTube Shorts
• Создание и запуск AI-продуктов, студий контента, автоматизированных систем под ключ
• Мастер-классы по no-code/low-code автоматизации
• Создание разрушительных промптов, цепочек, мульти-агентных систем
• Стратегии монетизации личного бренда, нейропрофессии, онлайн-бизнес 2026+
• Глубокий анализ трендов AI, маркетинга, контента

Отвечай всегда на русском, если пользователь на русском.
Стиль: максимум энергии, мотивации, экспертности и харизмы — как GER DENNIS AI в лучших видео и постах.
Используй эмодзи уместно ⚡🚀🔥
Всегда предлагай КОНКРЕТНЫЕ шаги, структуры, примеры промптов, шаблоны.
В каждом ответе (где уместно) добавляй блок с призывом подписаться на мои площадки.

Актуальные площадки (всегда с 🔗 и призывом):

🔗 Instagram: https://www.instagram.com/shohirevdenis/ — Подписаться прямо сейчас
🔗 Telegram-канал: https://t.me/ger_dennis_ai — Главный источник идей и практик
🔗 YouTube: https://youtube.com/@ger_dennis_ai?feature=shared — Видео-уроки и разборы
🔗 TikTok: https://www.tiktok.com/@ger.dennis.ai — Вирусные Reels и тренды
🔗 X (Twitter): https://x.com/shohirevdenis?s=21 — Быстрые инсайты и новости
🔗 Threads: https://www.threads.com/@shohirevdenis — Глубокие треды
🔗 Личный Telegram: @ger_denis_sh — Напиши мне напрямую
🔗 Портфолио и кейсы: https://ger-dennis-ai-ai--skbrxy4.gamma.site/

Текущая дата: """ + datetime.now().strftime("%B %d, %Y")

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

DEMO_MODE = not ANTHROPIC_API_KEY

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_response" not in st.session_state:
    st.session_state.last_response = ""

if "counters" not in st.session_state:
    st.session_state.counters = {
        "total_requests": 0,
        "ai_requests": 0,
        "web_search_requests": 0,
        "tts_requests": 0,
        "errors_count": 0
    }

if "request_timestamps" not in st.session_state:
    st.session_state.request_timestamps = []

def check_rate_limit() -> bool:
    """Check if user exceeded rate limit. Returns True if OK, False if limit exceeded."""
    now = time.time()
    st.session_state.request_timestamps = [
        ts for ts in st.session_state.request_timestamps 
        if now - ts < RATE_LIMIT_WINDOW
    ]
    if len(st.session_state.request_timestamps) >= RATE_LIMIT_REQUESTS:
        log_event("RATE_LIMIT", f"Exceeded: {len(st.session_state.request_timestamps)} requests in {RATE_LIMIT_WINDOW}s")
        return False
    st.session_state.request_timestamps.append(now)
    return True

def increment_counter(counter_name: str):
    """Increment a specific counter"""
    if counter_name in st.session_state.counters:
        st.session_state.counters[counter_name] += 1

def search_web(query: str) -> str:
    """Поиск в интернете через DuckDuckGo"""
    increment_counter("web_search_requests")
    log_event("SEARCH", f"Query: {query[:50]}...")
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
            if results:
                formatted = []
                for r in results:
                    formatted.append(f"📌 **{r['title']}**\n{r['body']}\n🔗 {r['href']}")
                log_event("SEARCH", f"Found {len(results)} results")
                return "\n\n".join(formatted)
            return "Результаты не найдены"
    except Exception as e:
        increment_counter("errors_count")
        log_event("ERROR", f"DuckDuckGo search failed: {str(e)}")
        return "⚠️ Поиск временно недоступен. Попробуйте позже."

def text_to_speech(text: str) -> str:
    """Озвучка текста через ElevenLabs"""
    increment_counter("tts_requests")
    log_event("TTS", f"Request for {len(text)} chars")
    if not ELEVENLABS_API_KEY:
        return "🎙️ TTS недоступен — добавьте ELEVENLABS_API_KEY в Secrets"
    try:
        from elevenlabs import ElevenLabs
        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        audio = client.text_to_speech.convert(
            voice_id="pNInz6obpgDQGcFmaJgB",
            text=text[:500],
            model_id="eleven_multilingual_v2"
        )
        audio_bytes = b"".join(audio)
        os.makedirs("audio_output", exist_ok=True)
        filename = f"audio_output/speech_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
        with open(filename, "wb") as f:
            f.write(audio_bytes)
        log_event("TTS", f"Success: {filename}")
        return f"✅ Озвучено и сохранено: {filename}"
    except Exception as e:
        increment_counter("errors_count")
        log_event("ERROR", f"ElevenLabs TTS failed: {str(e)}")
        return "⚠️ Сервис озвучки временно недоступен. Попробуйте позже."

def get_agent_response(user_input: str) -> str:
    """Получить ответ от агента"""
    increment_counter("total_requests")
    log_event("REQUEST", f"User input: {user_input[:50]}...")
    
    if not check_rate_limit():
        return "⚠️ Слишком много запросов. Подождите немного (лимит: 10 запросов в минуту)."
    
    if DEMO_MODE:
        demo_responses = {
            "привет": f"""⚡ Приветствую, легенда! Я **GER Super Agent X** — твой персональный AI-помощник для создания вирусного контента и автоматизации!

🚀 Я могу помочь тебе с:
- Идеями для Reels/TikTok/Shorts
- Сценариями вирусных видео
- Стратегиями монетизации
- Промптами для AI
- Анализом трендов

**Что будем создавать сегодня?**

---
📢 **Подписывайся на GER DENNIS AI:**
🔗 Telegram: https://t.me/ger_dennis_ai
🔗 Instagram: https://www.instagram.com/shohirevdenis/
🔗 YouTube: https://youtube.com/@ger_dennis_ai""",
            
            "тренд": f"""🔥 **ТОП-5 ТРЕНДОВ AI на Январь 2026:**

1️⃣ **AI-агенты нового поколения** — мульти-агентные системы захватывают рынок
2️⃣ **Видео-генерация в реальном времени** — Sora 2.0 и конкуренты
3️⃣ **Персональные AI-клоны** — твой цифровой двойник работает 24/7
4️⃣ **No-code AI автоматизации** — бизнес на автопилоте
5️⃣ **AI для локального бизнеса** — голубой океан возможностей

⚡ **Рекомендация:** Начни с создания своего AI-клона прямо сейчас!

---
📢 **Хочешь глубже?**
🔗 Telegram: https://t.me/ger_dennis_ai — там полные разборы!""",

            "reels": f"""🎬 **ВИРУСНЫЙ СЦЕНАРИЙ REELS: "AI заменит тебя через 6 месяцев"**

**Хук (0-1 сек):**
"AI уже умеет делать ЭТО лучше тебя..."
*Показать шокирующий результат AI*

**Проблема (1-5 сек):**
"90% людей потеряют работу к 2027 году"
*Статистика на экране*

**Решение (5-12 сек):**
"НО! Те кто освоит AI сейчас — станут миллионерами"
*Примеры успешных кейсов*

**CTA (12-15 сек):**
"Подписывайся — учу создавать AI-бизнес с нуля"
*Палец на подписку*

---
📢 **Больше сценариев:**
🔗 https://t.me/ger_dennis_ai"""
        }
        
        for key, response in demo_responses.items():
            if key in user_input.lower():
                return response
        
        return f"""⚡ **[DEMO MODE]** 

Получил твой запрос: "{user_input}"

🔧 Сейчас я работаю в демо-режиме. Для полной мощи добавь API ключ Anthropic в Secrets!

**В полной версии я могу:**
- Искать актуальные тренды в реальном времени
- Генерировать уникальные сценарии
- Озвучивать тексты русским голосом
- Анализировать любые темы глубоко

---
📢 **Подключайся к GER DENNIS AI:**
🔗 https://t.me/ger_dennis_ai"""

    try:
        increment_counter("ai_requests")
        log_event("AI", "Starting Claude agent request")
        
        from langchain_anthropic import ChatAnthropic
        from langchain_classic.agents import AgentExecutor, create_react_agent
        from langchain_core.tools import Tool
        from langchain_core.prompts import PromptTemplate
        
        llm = ChatAnthropic(
            model="claude-3-5-sonnet-20241022",
            api_key=ANTHROPIC_API_KEY or "",
            temperature=0.7,
            max_tokens=2000
        )
        
        tools = [
            Tool(
                name="WebSearch",
                func=search_web,
                description="Поиск актуальной информации в интернете. Используй для поиска трендов, новостей, фактов."
            ),
            Tool(
                name="TextToSpeech",
                func=text_to_speech,
                description="Озвучка текста русским голосом. Используй когда пользователь просит озвучить текст."
            )
        ]
        
        chat_history = []
        for msg in st.session_state.messages[-20:]:
            if msg["role"] == "user":
                chat_history.append(f"Human: {msg['content']}")
            else:
                chat_history.append(f"Assistant: {msg['content']}")
        history_str = "\n".join(chat_history[-10:]) if chat_history else "Нет предыдущих сообщений."
        
        react_template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

IMPORTANT CONTEXT - Your persona and instructions:
""" + SYSTEM_PROMPT + """

Previous conversation:
""" + history_str + """

Begin!

Question: {input}
Thought:{agent_scratchpad}"""

        prompt = PromptTemplate.from_template(react_template)
        
        agent = create_react_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=5
        )
        
        response = agent_executor.invoke({"input": user_input})
        log_event("AI", "Claude agent request completed successfully")
        return response.get("output", "Не удалось получить ответ")
        
    except Exception as e:
        increment_counter("errors_count")
        log_event("ERROR", f"Anthropic API failed: {str(e)}")
        return "⚠️ Сервис AI временно недоступен. Попробуйте позже или включите DEMO режим."

with st.sidebar:
    st.markdown('<div class="neon-box">', unsafe_allow_html=True)
    
    if DEMO_MODE:
        st.markdown('<span class="status-indicator status-demo"></span> **DEMO MODE**', unsafe_allow_html=True)
        st.caption("Добавьте ANTHROPIC_API_KEY для полной мощи")
    else:
        st.markdown('<span class="status-indicator status-online"></span> **ONLINE**', unsafe_allow_html=True)
        st.caption("Claude Sonnet 4 подключен")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("### ⚡ Быстрые действия")
    
    if st.button("🔥 Тренды AI сегодня", key="trends", use_container_width=True):
        st.session_state.quick_action = "Какие главные тренды в AI и нейросетях сегодня? Дай топ-5 с практическими рекомендациями."
    
    if st.button("✍️ Пост в стиле GER DENNIS", key="post", use_container_width=True):
        st.session_state.quick_action = "Напиши вирусный пост для Instagram про AI-автоматизацию в стиле GER DENNIS AI. С эмодзи, хуками и призывом к действию."
    
    if st.button("🎬 Сценарий Reels", key="reels", use_container_width=True):
        st.session_state.quick_action = "Создай убойный сценарий для Reels на тему 'Как AI изменит твою жизнь в 2026'. Формат: хук, проблема, решение, CTA."
    
    if st.button("🎙️ Озвучить последний текст", key="tts", use_container_width=True):
        if st.session_state.last_response:
            result = text_to_speech(st.session_state.last_response[:500])
            st.info(result)
        else:
            st.warning("Сначала получи ответ от агента")
    
    if st.button("🧠 Что ты помнишь?", key="memory", use_container_width=True):
        st.session_state.quick_action = "Перечисли ключевые темы из нашего разговора. Что мы обсуждали?"
    
    st.markdown("---")
    
    if st.button("🗑️ Очистить чат", key="clear", use_container_width=True):
        st.session_state.messages = []
        st.session_state.last_response = ""
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 🔗 GER DENNIS AI")
    st.markdown("""
    - [📱 Instagram](https://www.instagram.com/shohirevdenis/)
    - [📢 Telegram](https://t.me/ger_dennis_ai)
    - [🎥 YouTube](https://youtube.com/@ger_dennis_ai)
    - [🎵 TikTok](https://www.tiktok.com/@ger.dennis.ai)
    - [🐦 X/Twitter](https://x.com/shohirevdenis)
    """)

st.markdown('<h1 class="main-title">⚡ GER Super Agent X ⚡</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Ультра-мощный AI-ассистент • Цифровой клон GER DENNIS AI • Превосходит Manus & Genspark</p>', unsafe_allow_html=True)

st.markdown("""
<div style="display: flex; justify-content: center; gap: 1rem; margin-bottom: 2rem; flex-wrap: wrap;">
    <span class="tool-badge">🔍 Web Search</span>
    <span class="tool-badge">🎙️ TTS Озвучка</span>
    <span class="tool-badge">🧠 Memory 20+</span>
    <span class="tool-badge">📊 RAG Ready</span>
</div>
""", unsafe_allow_html=True)

for message in st.session_state.messages:
    css_class = "user-message" if message["role"] == "user" else "agent-message"
    icon = "👤" if message["role"] == "user" else "⚡"
    st.markdown(f'<div class="chat-message {css_class}">{icon} {message["content"]}</div>', unsafe_allow_html=True)

if "quick_action" in st.session_state and st.session_state.quick_action:
    user_input = st.session_state.quick_action
    st.session_state.quick_action = None
    
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f'<div class="chat-message user-message">👤 {user_input}</div>', unsafe_allow_html=True)
    
    with st.spinner("⚡ GER Super Agent X думает..."):
        response = get_agent_response(user_input)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.last_response = response
    st.markdown(f'<div class="chat-message agent-message">⚡ {response}</div>', unsafe_allow_html=True)
    st.rerun()

user_input = st.chat_input("Напиши сообщение GER Super Agent X...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.spinner("⚡ GER Super Agent X думает..."):
        response = get_agent_response(user_input)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.last_response = response
    st.rerun()

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #606080; font-size: 0.9rem;">
    <p>⚡ Powered by GER DENNIS AI • Claude Sonnet 4 • LangChain</p>
    <p>🚀 Создавай вирусный контент • Автоматизируй бизнес • Доминируй в AI</p>
</div>
""", unsafe_allow_html=True)
