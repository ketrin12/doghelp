import streamlit as st
import json
import os
import base64

# 1. Настройка страницы и темы
st.set_page_config(
    page_title="Помощь хвостикам — Передержка и ОСВВ",
    page_icon="🐾",
    layout="wide"
)

# Кастомные стили с контрастным тёмно-серым текстом для читаемости
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"], .stApp {
        color-scheme: light !important;
        background-color: #F7F4F0 !important;
    }
    
    /* 1. Главный фон сайта */
    .stApp {
        background-color: #F7F4F0 !important;
    }
    
    /* 2. Цвет текста — Делаем глубоким тёмно-серым (#2B2B2B) для максимального контраста */
    h1, h2, h3, p, span, label, li, .stMarkdown, [data-testid="stWidgetLabel"] p {
        color: #2B2B2B !important;
    }
    
    /* 3. Кнопки (Приглушенный шалфейный) */
    .stButton>button {
        background-color: #7FA998 !important;
        color: #F7F4F0 !important; 
        border-radius: 10px;
        border: 1px solid #2B2B2B;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #638A7A !important;
        color: white !important;
        border-color: #2B2B2B;
    }
    
    /* 4. Поля ввода (Белый фон, тёмно-серый текст внутри) */
    .stTextInput input, .stSelectbox div, .stTextArea textarea {
        background-color: #FFFFFF !important;
        color: #2B2B2B !important;
        border: 1px solid #7FA998 !important;
    }
    
    /* 5. Боковое меню */
    [data-testid="stSidebar"] {
        background-color: #EFEBE4 !important; 
    }
    [data-testid="stSidebar"] * {
        color: #2B2B2B !important;
    }
    
    /* Стили для статусов животных */
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

DB_FILE = "animals.json"

# Конвертация загруженного через «Обзор» файла в формат для сохранения
def file_to_base64(uploaded_file):
    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        encoded = base64.b64encode(file_bytes).decode("utf-8")
        return f"data:image/jpeg;base64,{encoded}"
    return "https://unsplash.com"

# Безопасная загрузка базы данных
def load_animals():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Если в базе остались старые локальные пути, очищаем её для защиты от вылетов
                for item in data:
                    if "pagesdog2/" in item["img"] or "images/" in item["img"]:
                        return []
                return data
        except:
            return []
    return []

def save_animals(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Инициализация списка животных
if 'animals_list' not in st.session_state:
    st.session_state.animals_list = load_animals()

# Меню навигации
menu = st.sidebar.radio("Навигация по сайту", ["Главная (Питомцы)", "Помочь хвостикам", "Панель управления", "О нас"])

# === СТРАНИЦА 1: ГЛАВНАЯ ===
if menu == "Главная (Питомцы)":
    st.title("🐾 Помощь животным: Передержка и спасение")
    st.write("Здесь собраны подопечные, которым нужна помощь прямо сейчас.")

    animals = st.session_state.animals_list

    if not animals:
        st.info("Сейчас на сайте нет объявлений. Добавьте первого хвостика через Панель управления! 🥰")
    else:
        for i in range(0, len(animals), 3):
            cols = st.columns(3)
            for j in range(3):
                idx = i + j
                if idx < len(animals):
                    with cols[j]:
                        item = animals[idx]
                        
                        # Защищенный вывод картинки
                        try:
                            st.image(item["img"], use_container_width=True)
                        except Exception:
                            st.warning("⚠️ Не удалось загрузить фото этого питомца")
                        
                        status = item.get("status", "На временной передержке")
                        if "отлове" in status:
                            st.markdown(f'<div class="status-badge status-otlov">🚨 {status}</div>', unsafe_allow_html=True)
                        elif "улице" in status:
                            st.markdown(f'<div class="status-badge status-street">🏡 {status}</div>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<div class="status-badge status-perederzhka">🐾 {status}</div>', unsafe_allow_html=True)

                        st.subheader(f"{item['name']} ({item['age']})")
                        st.caption(f"Тип: {item['type']}")
                        st.write(f"**Описание:** {item['desc']}")
                        
                        if item.get("needs"):
                            st.warning(f"⚠️ **Актуально:** {item['needs']}")

                        if st.button(f"Помочь / Забрать {item['name']}", key=f"btn_{idx}"):
                            st.success(f"Спасибо за отклик! Свяжитесь с куратором во вкладке 'О нас' или перейдите в раздел 'Помочь хвостикам'.")
                        st.markdown("---")

# === СТРАНИЦА 2: ПОМОЩЬ ===
elif menu == "Помочь хвостикам":
    st.title("💚 Поддержать подопечных и передержку")
    st.write("Все средства идут точечно на спасение животных из отлова, оплату временных передержек и лечение.")
    
    st.info("ℹ️ Все поступающие средства идут напрямую на покупку корма, лекарств и оплату ветеринаров.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("💳 Банковская карта / ЕРИП")
        st.code("Благотворительный счет в Беларусбанке:\nBYXX AKBB XXXX XXXX XXXX XXXX XXXX")
        st.code("Код ЕРИП: 1234567 (Благотворительность -> Помощь животным)")
    with col2:
        st.subheader("📞 Другие способы помощи")
        st.write("Вы можете помочь руками, передать корм, лекарства или помочь с автопомощью.")
        st.write("**Телефон куратора:** +375 (29) XXX-XX-XX (Татьяна)")

# === СТРАНИЦА 3: ПАНЕЛЬ УПРАВЛЕНИЯ ===
elif menu == "Панель управления":
    st.title("🔒 Вход в панель управления")
    
    password = st.text_input("Введите пароль администратора", type="password")
    
    if password == "admin123":
        st.success("Доступ разрешен!")
        
        tab1, tab2 = st.tabs(["➕ Добавить питомца", "🗑️ Управление / Удаление"])
        
        with tab1:
            with st.form("add_animal_form", clear_on_submit=True):
                st.subheader("Добавление нового подопечного")
                
                new_name = st.text_input("Кличка животного")
                new_type = st.selectbox("Кто это?", ["Собака", "Кошка", "Другое"])
                new_status = st.selectbox("Текущий статус / Где находится?", [
                    "В отлове (Срочный вывоз!)", 
                    "На временной передержке", 
                    "Живет на улице (Нужна помощь)"
                ])
                new_age = st.text_input("Примерный возраст")
                new_needs = st.text_input("В чем нуждается? (например: Сбор на корм, Нужен дом)")
                new_desc = st.text_area("Описание ситуации / Характер")
                
                # Кнопка ОБЗОР для загрузки картинок с ПК/телефона
                uploaded_file = st.file_uploader("Выберите фото питомца", type=["jpg", "jpeg", "png"])
                
                submit = st.form_submit_button("Добавить на сайт")
                
                if submit:
                    if new_name and new_desc:
                        img_data = file_to_base64(uploaded_file)
                        
                        new_pet = {
                            "name": new_name,
                            "type": new_type,
                            "status": new_status,
                            "age": new_age,
                            "needs": new_needs,
                            "desc": new_desc,
                            "img": img_data
                        }
                        st.session_state.animals_list.append(new_pet)
                        save_animals(st.session_state.animals_list)
                        st.success(f"🎉 {new_name} успешно добавлен на сайт!")
                        st.rerun()
                    else:
                        st.error("Пожалуйста, введите кличку и описание.")
        
        with tab2:
            st.subheader("Удаление питомцев с сайта")
            animals = st.session_state.animals_list
            
            if not animals:
                st.info("На сайте пока нет добавленных животных.")
            else:
                animal_options = [f"{pet['name']} ({pet['type']}) — {pet['status']}" for pet in animals]
                selected_animal_str = st.selectbox("Выберите животное для удаления:", animal_options)
                
                selected_idx = animal_options.index(selected_animal_str)
                selected_pet = animals[selected_idx]
                
                st.warning(f"Вы собираетесь удалить подопечного: **{selected_pet['name']}**.")
                
                if st.button(f"❌ Подтвердить удаление {selected_pet['name']}", key="delete_pet_btn"):
                    st.session_state.animals_list.pop(selected_idx)
                    save_animals(st.session_state.animals_list)
                    st.success("Успешно удалено!")
                    st.rerun()
                    
    elif password:
        st.error("Неверный пароль!")

# === СТРАНИЦА 4: О НАС ===
elif menu == "О нас":
    st.title("🏢 О нашей волонтерской группе")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🌟 Наша миссия")
        st.write("Мы — объединение волонтеров, которые спасают животных из пунктов отлова и организуют передержки.")
    with col2:
        st.subheader("📍 Контакты")
        st.markdown("📞 **Телефон для связи:** +375 (29) XXX-XX-XX (Татьяна)")
        st.markdown("💬 **Telegram / Viber:** @tatyana_khvost_up")
