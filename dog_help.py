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

# Кастомные стили с перекраской реквизитов и БЕЛОЙ кнопкой меню на телефонах
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
    
    /* 2. Цвет текста на сайте (четкий черный) */
    h1, h2, h3, p, span, label, li, .stMarkdown, [data-testid="stWidgetLabel"] p, [data-testid="stMarkdownContainer"] p {
        color: #000000 !important;
    }
    
    /* 3. Кнопки (Приглушенный шалфейный) */
    .stButton>button {
        background-color: #7FA998 !important;
        color: #F7F4F0 !important; 
        border-radius: 10px;
        border: 1px solid #000000;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #638A7A !important;
        color: white !important;
        border-color: #000000;
    }
    
    /* 4. Квадратик с пожертвованием (st.code) — светло-зеленый */
    code, pre, [data-testid="stCodeBlock"] pre {
        background-color: #E2F0D9 !important; 
        color: #000000 !important;          
        border: 1px solid #7FA998 !important;
        border-radius: 8px !important;
        font-weight: bold !important;
    }
    
    /* 5. ПОЛНАЯ ПЕРЕКРАСКА КНОПКИ МЕНЮ НА ТЕЛЕФОНЕ (Рычаг >>) */
    /* Делаем сам круг полностью БЕЛЫМ, чтобы убрать черный цвет */
    [data-testid="stSidebarCollapseButton"] button {
        background-color: #FFFFFF !important; /* Белый круг кнопки */
        color: #7FA998 !important;            /* Цвет контура стрелочки */
        border: 2px solid #7FA998 !important; /* Красивый шалфейный ободок вокруг кнопки */
        box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.15) !important; /* Легкая тень, чтобы кнопка парила */
    }
    
    /* Красим саму иконку стрелочки (>> или >) внутри круга в шалфейный цвет */
    [data-testid="stSidebarCollapseButton"] svg {
        fill: #7FA998 !important;             
        color: #7FA998 !important;
    }
    
    /* 6. Поля ввода (Белый фон, черный text) */
    .stTextInput input, .stSelectbox div, .stTextArea textarea {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #7FA998 !important;
    }
    
    /* 7. Боковое меню */
    [data-testid="stSidebar"] {
        background-color: #EFEBE4 !important; 
    }
    [data-testid="stSidebar"] * {
        color: #000000 !important;
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
        
        # Создаем три вкладки: Добавление, Редактирование и Удаление
        tab1, tab2, tab3 = st.tabs(["➕ Добавить питомца", "✏️ Редактировать", "🗑️ Удалить с сайта"])
        
        # --- ВКЛАДКА 1: ДОБАВЛЕНИЕ ---
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
                
                uploaded_file = st.file_uploader("Выберите фото питомца", type=["jpg", "jpeg", "png"], key="add_upload")
                
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
        
        # --- ВКЛАДКА 2: РЕДАКТИРОВАНИЕ (НОВАЯ ФУНКЦИЯ) ---
        with tab2:
            st.subheader("📝 Редактирование карточки животного")
            animals = st.session_state.animals_list
            
            if not animals:
                st.info("На сайте пока нет животных для редактирования.")
            else:
                # 1. Выбираем, кого именно хотим изменить
                animal_options = [f"{pet['name']} ({pet['type']})" for pet in animals]
                selected_edit_str = st.selectbox("Выберите питомца для изменения данных:", animal_options, key="select_edit")
                
                edit_idx = animal_options.index(selected_edit_str)
                current_pet = animals[edit_idx]
                
                st.write(f"✍️ Вы редактируете профиль подопечного: **{current_pet['name']}**")
                
                # 2. Создаем форму, куда ЗАРАНЕЕ подставляем текущие значения из базы (через value)
                with st.form("edit_animal_form"):
                    edit_name = st.text_input("Кличка животного", value=current_pet.get("name", ""))
                    
                    # Находим индекс старого типа в списке, чтобы он выбрался по умолчанию
                    type_list = ["Собака", "Кошка", "Другое"]
                    try: type_idx = type_list.index(current_pet.get("type", "Собака"))
                    except: type_idx = 0
                    edit_type = st.selectbox("Кто это?", type_list, index=type_idx)
                    
                    status_list = ["В отлове (Срочный вывоз!)", "На временной передержке", "Живет на улице (Нужна помощь)"]
                    try: status_idx = status_list.index(current_pet.get("status", "На временной передержке"))
                    except: status_idx = 1
                    edit_status = st.selectbox("Текущий статус / Где находится?", status_list, index=status_idx)
                    
                    edit_age = st.text_input("Примерный возраст", value=current_pet.get("age", ""))
                    edit_needs = st.text_input("В чем нуждается?", value=current_pet.get("needs", ""))
                    edit_desc = st.text_area("Описание ситуации / Характер", value=current_pet.get("desc", ""))
                    
                    st.info("💡 Если хотите поменять фотографию — загрузите новую ниже. Если оставите поле пустым, сохранится старое фото.")
                    edit_file = st.file_uploader("Загрузить новую фотографию (необязательно)", type=["jpg", "jpeg", "png"], key="edit_upload")
                    
                    save_changes = st.form_submit_button("💾 Сохранить изменения")
                    
                    if save_changes:
                        if edit_name and edit_desc:
                            # Если загрузили новую фотку — конвертируем её. Если нет — берем старую из базы
                            if edit_file is not None:
                                final_img = file_to_base64(edit_file)
                            else:
                                final_img = current_pet.get("img")
                                
                            # Перезаписываем данные в списке
                            st.session_state.animals_list[edit_idx] = {
                                "name": edit_name,
                                "type": edit_type,
                                "status": edit_status,
                                "age": edit_age,
                                "needs": edit_needs,
                                "desc": edit_desc,
                                "img": final_img
                            }
                            
                            save_animals(st.session_state.animals_list)
                            st.success(f"📈 Данные для {edit_name} успешно обновлены!")
                            st.rerun()
                        else:
                            st.error("Кличка и описание не могут быть пустыми.")
        
        # --- ВКЛАДКА 3: УДАЛЕНИЕ ---
        with tab3:
            st.subheader("Удаление питомцев с сайта")
            animals = st.session_state.animals_list
            
            if not animals:
                st.info("На сайте пока нет добавленных животных.")
            else:
                animal_options_del = [f"{pet['name']} ({pet['type']}) — {pet['status']}" for pet in animals]
                selected_animal_str = st.selectbox("Выберите животное для удаления:", animal_options_del, key="select_del")
                
                selected_idx = animal_options_del.index(selected_animal_str)
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
