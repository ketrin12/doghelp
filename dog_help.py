import streamlit as st
import requests
import json
import os
import base64

# 1. Настройка страницы и темы
st.set_page_config(
    page_title="Помощь хвостикам — Передержка и ОСВВ",
    page_icon="🐾",
    layout="wide"
)

# Кастомные стили (Палитра Татьяны)
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"], .stApp {
        color-scheme: light !important;
        background-color: #F7F4F0 !important;
    }
    .stApp {
        background-color: #F7F4F0 !important;
    }
    h1, h2, h3, p, span, label, li, .stMarkdown, [data-testid="stWidgetLabel"] p, [data-testid="stMarkdownContainer"] p {
        color: #000000 !important;
    }
    .stButton>button, .stLinkButton>a {
        background-color: #7FA998 !important;
        color: #F7F4F0 !important; 
        border-radius: 10px;
        border: 1px solid #000000;
        font-weight: bold;
        transition: 0.3s;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        justify-content: center;
    }
    .stButton>button:hover, .stLinkButton>a:hover {
        background-color: #638A7A !important;
        color: white !important;
        border-color: #000000;
    }
    code, pre, [data-testid="stCodeBlock"] pre {
        background-color: #E2F0D9 !important; 
        color: #000000 !important;          
        border: 1px solid #7FA998 !important;
        border-radius: 8px !important;
        font-weight: bold !important;
    }
    .stTextInput input, .stSelectbox div, .stTextArea textarea {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #7FA998 !important;
    }
    [data-testid="stSidebar"] {
        background-color: #EFEBE4 !important; 
    }
    [data-testid="stSidebar"] * {
        color: #000000 !important;
    }
    .status-badge {
        padding: 4px 10px;
        border-radius: 5px;
        font-size: 14px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 10px;
    }
    .status-otlov { background-color: #FFD2D2 !important; color: #D32F2F !important; border: 1px solid #D32F2F; }
    .status-perederzhka { background-color: #E2F0D9 !important; color: #385723 !important; border: 1px solid #385723; }
    .status-street { background-color: #FFF2CC !important; color: #7F6000 !important; border: 1px solid #7F6000; }
    </style>
""", unsafe_allow_html=True)


# ================= НАСТРОЙКИ ОБЛАКА JSONBIN =================
# Иван, обязательно проверь эти ключи! Сюда нужно вставить валидный Master Key и ID твоей корзины (bin)
BIN_KEY = "$2b$10$VvXwcc4/bInixOKdxGfgPOv64nA89l1ksvAiQJptNBGiERzIz5uOi"
BIN_ID = "64d3679affd5d16053736a4f"
BIN_URL = f"https://api.jsonbin.v3/b/{BIN_ID}"


def file_to_base64(uploaded_file):
    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        encoded = base64.b64encode(file_bytes).decode("utf-8")
        return f"data:image/jpeg;base64,{encoded}"
    return "https://unsplash.com"


# ============== ОБНОВЛЕННЫЕ ФУНКЦИИ ЗАГРУЗКИ И СОХРАНЕНИЯ ==============
def load_animals():
    """Загружает список питомцев из облака JSONBin"""
    headers = {
        "X-Master-Key": BIN_KEY
    }
    try:
        response = requests.get(BIN_URL, headers=headers)
        if response.status_code == 200:
            # JSONBin возвращает структуру вида {"record": [...] или {"record": {"animals": [...]}}}
            res_data = response.json()
            return res_data.get("record", [])
    except Exception as e:
        st.error(f"Ошибка загрузки из облака: {e}")
    return []


def save_animals(data):
    """Сохраняет список питомцев в облако JSONBin (не сотрется при перезапуске сервера)"""
    headers = {
        "Content-Type": "application/json",
        "X-Master-Key": BIN_KEY
    }
    try:
        # Отправляем обновленный список обратно в корзину методом PUT
        response = requests.put(BIN_URL, json=data, headers=headers)
        if response.status_code == 200:
            return True
    except Exception as e:
        st.error(f"Ошибка сохранения в облако: {e}")
    return False


# ИНИЦИАЛИЗАЦИЯ: данные берутся из интернета один раз при запуске сессии
if 'animals_list' not in st.session_state:
    st.session_state.animals_list = load_animals()


# ================= МУЛЬТИЯЗЫЧНОСТЬ =================
LANG_DICT = {
    "Русский": {
        "nav": ["Главная (Питомцы)", "Помочь хвостикам", "Панель управления", "О нас"],
        "lang_label": "🌐 Выберите язык / Language",
        "title_main": "🐾 Помощь животным: Передержка и спасение",
        "subtitle_main": "Здесь собраны подопечные, которым нужна помощь прямо сейчас.",
        "no_animals": "Сейчас на сайте нет объявлений. Добавьте первого хвостика через Панель управления! 🥰",
        "type": "Тип",
        "age_cat": "Категория возраста",
        "age": "Точный возраст",
        "desc": "Описание",
        "needs": "Актуально",
        "btn_help": "Помочь / Забрать",
        "alert_help": "Спасибо за отклик! Свяжитесь с куратором во вкладке 'О нас' или перейдите в раздел 'Помочь хвостикам'.",
        "age_cats": ["Щенок / Котенок", "Взрослый питомец"],
        "donate_title": "❤️ Поддержать наш проект",
        "donate_desc": "Все собранные средства идут на покупку корма, лекарств и оплату передержек для хвостиков.",
        "donate_btn": "Перейти на сайт для пожертвований 💳"
    },
    "English": {
        "nav": ["Home (Pets)", "Donate & Help", "Admin Panel", "About Us"],
        "lang_label": "🌐 Choose Language",
        "title_main": "🐾 Animal Help: Foster & Rescue",
        "subtitle_main": "Here are the pets who need your help right now.",
        "no_animals": "No pets listed at the moment. Admin can add them in the Admin Panel! 🥰",
        "type": "Type",
        "age_cat": "Age Category",
        "age": "Exact Age",
        "desc": "Description",
        "needs": "Urgent Needs",
        "btn_help": "Help / Adopt",
        "alert_help": "Thank you! Please contact the curator in the 'About Us' tab or proceed to 'Donate & Help'.",
        "age_cats": ["Puppy / Kitten", "Adult Pet"],
        "donate_title": "❤️ Support Our Project",
        "donate_desc": "All funds raised go towards food, medicine, and foster care for our pets.",
        "donate_btn": "Go to Donation Website 💳"
    },
    "Deutsch": {
        "nav": ["Startseite (Tiere)", "Spenden & Helfen", "Admin-Bereich", "Über uns"],
        "lang_label": "🌐 Sprache wählen",
        "title_main": "🐾 Tierhilfe: Pflegestelle & Rettung",
        "subtitle_main": "Hier sind die Tiere, die jetzt Ihre Hilfe brauchen.",
        "no_animals": "Im Moment gibt es keine Tiere auf der Website. Der Admin kann welche hinzufügen! 🥰",
        "type": "Tierart",
        "age_cat": "Alterskategorie",
        "age": "Genaues Alter",
        "desc": "Beschreibung",
        "needs": "Aktuelle Bedürfnisse",
        "btn_help": "Helfen / Adoptieren",
        "alert_help": "Vielen Dank für Ihre Antwort! Kontaktieren Sie uns im Bereich 'Über uns' или 'Spenden & Helfen'.",
        "age_cats": ["Welpe / Kätzchen", "Erwachsenes Tier"],
        "donate_title": "❤️ Unterstützen Sie unser Projekt",
        "donate_desc": "Alle Spenden werden für Futter, Medizin und die Pflege der Tiere verwendet.",
        "donate_btn": "Zur Spenden-Website gehen 💳"
    }
}

selected_lang = st.sidebar.selectbox("", ["Русский", "English", "Deutsch"], label_visibility="visible", index=0)
t = LANG_DICT[selected_lang]

menu_options = t["nav"]
menu_choice = st.sidebar.radio(t["lang_label"], menu_options)
menu_idx = menu_options.index(menu_choice)

# === СТРАНИЦА 0: ГЛАВНАЯ ===
if menu_idx == 0:
    st.title(t["title_main"])
    st.write(t["subtitle_main"])

    if selected_lang == "Русский":
        filter_options = ["Все", "Щенки / Котята (0-1 год)", "Взрослые питомцы (1+ лет)"]
    elif selected_lang == "English":
        filter_options = ["All", "Puppies / Kittens (0-1 year)", "Adult Pets (1+ years)"]
    else:
        filter_options = ["Alle", "Welpen / Kätzchen (0-1 Jahr)", "Erwachsene Tiere (1+ Jahre)"]

    selected_filter = st.segmented_control(
        "", 
        options=filter_options, 
        default=filter_options[0]
    )

    filtered_animals = []
    for pet in st.session_state.animals_list:
        pet_cat = pet.get("age_category", "Взрослый питомец")
        if selected_filter == filter_options[0] or selected_filter is None:
            filtered_animals.append(pet)
        elif selected_filter == filter_options[1] and pet_cat == "Щенок / Котенок":
            filtered_animals.append(pet)
        elif selected_filter == filter_options[2] and pet_cat == "Взрослый питомец":
            filtered_animals.append(pet)

    # Дальше идет твой код отображения filtered_animals карточек...
    # (Допиши или вставь сюда свою логику рендеринга карточек)


# === СТРАНИЦА 1: ПОМОЧЬ ХВОСТИКАМ (КНОПКА ДЛЯ ТАТЬЯНЫ) ===
elif menu_idx == 1:
    st.title(t["donate_title"])
    st.write(t["donate_desc"])
    
    # Ссылка, которую дала Татьяна. Замени "https://example.com" на реальный адрес (например, ЮMoney или сайт фонда)
    donation_url = "https://example.com" 
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.link_button(t["donate_btn"], donation_url, use_container_width=True)
