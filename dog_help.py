import streamlit as st
import json
import os

# 1. Настройка страницы и темы (Белый фон, зеленые элементы)
st.set_page_config(
    page_title="Приют для животных - Подари дом",
    page_icon="🐾",
    layout="wide"
)

# Кастомные стили для изменения цвета кнопок и шрифтов на зеленый
st.markdown("""
    <style>
    .stButton>button {
        background-color: #2e7d32 !important;
        color: white !important;
        border-radius: 10px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1b5e20 !important;
        color: white !important;
    }
    h1, h2, h3 {
        color: #2e7d32 !important;
    }
    </style>
""", unsafe_allow_html=True) # Оставили только этот параметр!

# 2. База данных во временном файле JSON
DB_FILE = "animals.json"

def load_animals():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    # Стартовые данные для примера, если файл еще не создан
    return [
        {
            "name": "Боня",
            "type": "Собака",
            "age": "2 года",
            "desc": "Очень добрый и игривый пес. Любит детей, приучен к поводку.",
            "img": "https://unsplash.com"
        },
        {
            "name": "Мурка",
            "type": "Кошка",
            "age": "6 месяцев",
            "desc": "Ласковая мурлыка, трехцветная (на счастье!). Ищет уютный дом.",
            "img": "https://unsplash.com"
        }
    ]

def save_animals(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Загружаем текущий список животных
if 'animals_list' not in st.session_state:
    st.session_state.animals_list = load_animals()

# 3. Боковое меню (Sidebar) для навигации
menu = st.sidebar.radio("Навигация по сайту", ["Главная (Питомцы)", "Помочь приюту", "Админка (Для Татьяны)"])

# === СТРАНИЦА 1: ГЛАВНАЯ (КАРТОЧКИ) ===
if menu == "Главная (Питомцы)":
    st.title("🐾 Подари дом пушистому другу")
    st.write("Каждое из этих животных мечтает обрести любящую семью. Посмотрите на этих красавцев!")
    
    animals = st.session_state.animals_list
    
    if not animals:
        st.info("Сейчас все животные нашли свой дом! 🥰")
    else:
        # Отображаем карточки сеткой по 3 в ряд
        for i in range(0, len(animals), 3):
            cols = st.columns(3)
            for j in range(3):
                idx = i + j
                if idx < len(animals):
                    with cols[j]:
                        item = animals[idx]
                        st.image(item["img"], use_container_width=True)
                        st.subheader(f"{item['name']} ({item['age']})")
                        st.caption(f"Тип: {item['type']}")
                        st.write(item["desc"])
                        
                        # Кнопка «Забрать» под каждой карточкой
                        if st.button(f"Хочу забрать {item['name']}", key=f"btn_{idx}"):
                            st.success(f"Прекрасный выбор! Свяжитесь с нами по телефону или в мессенджерах, чтобы познакомиться с {item['name']}.")
                        st.markdown("---")

# === СТРАНИЦА 2: ПОМОЩЬ ПРИЮТУ ===
elif menu == "Помочь приюту":
    st.title("💚 Кнопка помощи приюту")
    st.write("Если вы пока не можете взять питомца домой, вы можете помочь им финансово на корм и лечение.")
    
    st.info("ℹ️ Все поступающие средства идут напрямую на покупку корма, лекарств и оплату ветеринаров.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("💳 Банковская карта / ЕРИП")
        st.code("Благотворительный счет в Беларусбанке:\nBYXX AKBB XXXX XXXX XXXX XXXX XXXX")
        st.code("Код ЕРИП: 1234567 (Благотворительность -> Приют)")
    with col2:
        st.subheader("📞 Другие способы")
        st.write("Вы также можете привезти корм, поводки или игрушки лично. Свяжитесь с нами!")
        st.write("**Телефон:** +375 (29) XXX-XX-XX (Татьяна)")

# === СТРАНИЦА 3: АДМИНКА ДЛЯ ТАТЬЯНЫ ===
elif menu == "Админка ":
    st.title("🔒 Панель управления сайтом")
    st.write("Здесь вы можете добавлять новых животных на главную страницу.")
    
    # Простая защита паролем, чтобы обычные посетители не хулиганили
    password = st.text_input("Введите пароль администратора", type="password")
    
    if password == "admin123": # Пароль по умолчанию, потом можно сменить
        st.success("Доступ разрешен!")
        
        with st.form("add_animal_form", clear_on_submit=True):
            st.subheader("📝 Данные нового питомца")
            
            new_name = st.text_input("Кличка животного")
            new_type = st.selectbox("Кто это?", ["Собака", "Кошка", "Другое"])
            new_age = st.text_input("Возраст (например: 5 месяцев, 1 год)")
            new_desc = st.text_area("Описание характера и истории животного")
            
            # Ссылка на фото (для простоты на старте)
            new_img = st.text_input("Ссылка на фотографию животного (URL)", 
                                    value="https://unsplash.com")
            
            submit = st.form_submit_button("Добавить питомца на сайт")
            
            if submit:
                if new_name and new_desc:
                    new_pet = {
                        "name": new_name,
                        "type": new_type,
                        "age": new_age,
                        "desc": new_desc,
                        "img": new_img
                    }
                    st.session_state.animals_list.append(new_pet)
                    save_animals(st.session_state.animals_list)
                    st.success(f"🎉 {new_name} успешно добавлен на сайт!")
                else:
                    st.error("Пожалуйста, заполните как минимум кличку и описание.")
    elif password:
        st.error("Неверный пароль!")
