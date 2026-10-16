import streamlit as st
import json
import os

# 1. Настройка страницы и темы (Белый фон, зеленые элементы)
st.set_page_config(
    page_title="Помощь хвостикам — Передержка и ОСВВ",
    page_icon="🐾",
    layout="wide"
)

# Кастомные стили для изменения цвета кнопок и шрифтов на зеленый
st.markdown("""
    <style>
    /* 1. Основной фон сайта (60%) — Мягкий кремово-бежевый */
    .stApp {
        background-color: #F7F4F0 !important;
    }
    
    /* 2. Цвет главного текста и заголовков (30%) — Глубокий хвойно-зеленый */
    h1, h2, h3, p, span, label, .stMarkdown {
        color: #2F3E36 !important;
    }
    
    /* 3. Главные кнопки (10%) — Приглушенный шалфейный */
    .stButton>button {
        background-color: #7FA998 !important;
        color: #F7F4F0 !important; 
        border-radius: 10px;
        border: 1px solid #2F3E36;
        font-weight: bold;
        transition: 0.3s;
    }
    
    /* 4. Эффект при наведении на кнопку (Ховер) */
    .stButton>button:hover {
        background-color: #638A7A !important;
        color: white !important;
        border-color: #2F3E36;
    }
    
    /* Подправка стиля бокового меню */
    .stSidebar {
        background-color: #EFEBE4 !important; 
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
    .status-otlov { background-color: #FFD2D2; color: #D32F2F; border: 1px solid #D32F2F; }
    .status-perederzhka { background-color: #E2F0D9; color: #385723; border: 1px solid #385723; }
    .status-street { background-color: #FFF2CC; color: #7F6000; border: 1px solid #7F6000; }
    </style>
""", unsafe_allow_html=True)

# 2. База данных во временном файле JSON
DB_FILE = "animals.json"

def load_animals():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    
    # Стартовые данные с локальным фото с компьютера
    return [
        {
            "name": "Чебурашка",
            "type": "Собака",
            "status": "Живет на улице (Нужна помощь)",
            "age": "2 года",
            "needs": "Запланирована стерилизация, очень нужен дом или передержка!",
            "desc": "Девочка, среднего размера. Живёт на улице, где каждый день грозит опасность. Очень ласковая и ждет свою семью.",
            "img": "images/cheburashka.jpg"  # Путь к файлу в твоей папке проекта
        }
    ]

def save_animals(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Загружаем текущий список животных
if 'animals_list' not in st.session_state:
    st.session_state.animals_list = load_animals()

# 3. Боковое меню (Sidebar) для навигации
menu = st.sidebar.radio("Навигация по сайту", ["Главная (Питомцы)", "Помочь хвостикам", "Панель управления", "О нас"])

if menu == "Главная (Питомцы)":
    st.title("🐾 Помощь животным: Передержка и спасение")
    st.write("Здесь собраны подопечные, которым нужна помощь прямо сейчас: кто-то находится в отлове, кто-то на временных домашних передержках, а кто-то всё еще выживает на улице.")

    animals = st.session_state.animals_list

    if not animals:
        st.info("Сейчас все животные под надежной защитой или нашли свой дом! 🥰")
    else:
        for i in range(0, len(animals), 3):
            cols = st.columns(3)
            for j in range(3):
                idx = i + j
                if idx < len(animals):
                    with cols[j]:
                        item = animals[idx]
                        st.image(item["img"], use_container_width=True)
                        
                        # Отображение статуса животного с красивым стилем
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
                            st.success(f"Спасибо за отклик! Перейдите во вкладку 'Помочь хвостикам' для перевода средств или в 'О нас', чтобы связаться с куратором Татьяной.")
                        st.markdown("---")

# === СТРАНИЦА 2: ПОМОЩЬ ===
elif menu == "Помочь хвостикам":
    st.title("💚 Поддержать подопечных и передержку")
    st.write("У нас нет стационарного здания приюта. Все средства идут точечно на спасение животных из отлова, оплату временных домашних передержек, лечение уличных хвостиков и покупку корма.")
    
    st.info("ℹ️ Все поступающие средства идут напрямую на покупку корма, лекарств и оплату ветеринаров.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("💳 Банковская карта / ЕРИП")
        st.code("Благотворительный счет в Беларусбанке:\nBYXX AKBB XXXX XXXX XXXX XXXX XXXX")
        st.code("Код ЕРИП: 1234567 (Благотворительность -> Помощь животным)")
    with col2:
        st.subheader("📞 Другие способы помощи")
        st.write("Вы можете помочь руками, передать корм, лекарства (обработчики от клещей/глистов) или помочь с автопомощью (отвезти хвостика в клинику).")
        st.write("**Телефон куратора:** +375 (29) XXX-XX-XX (Татьяна)")

# === СТРАНИЦА 3: ПАНЕЛЬ УПРАВЛЕНИЯ ===
elif menu == "Панель управления":
    st.title("🔒 Вход в панель управления")
    
    password = st.text_input("Введите пароль администратора", type="password")
    
    if password == "admin123":
        st.success("Доступ разрешен!")
        
        # Создаем две вкладки внутри админки для удобства
        tab1, tab2 = st.tabs(["➕ Добавить питомца", "🗑️ Управление / Удаление"])
        
        # ВКЛАДКА 1: ДОБАВЛЕНИЕ
        with tab1:
            with st.form("add_animal_form", clear_on_submit=True):
                st.subheader("Добавление нового подопечного")
                
                new_name = st.text_input("Кличка животного (или описание, если нет имени)")
                new_type = st.selectbox("Кто это?", ["Собака", "Кошка", "Другое"])
                new_status = st.selectbox("Текущий статус / Где находится?", [
                    "В отлове (Срочный вывоз!)", 
                    "На временной передержке", 
                    "Живет на улице (Нужна помощь)"
                ])
                new_age = st.text_input("Примерный возраст (например: 5 месяцев, 1-2 года)")
                new_needs = st.text_input("В чем нуждается? (например: Сбор на операцию, Ищет дом, Нужен корм)")
                new_desc = st.text_area("Описание ситуации / Характер")
                
                new_img = st.text_input("Ссылка на фотографию (URL)", 
                                        value="https://unsplash.com")
                
                submit = st.form_submit_button("Добавить на сайт")
                
                if submit:
                    if new_name and new_desc:
                        new_pet = {
                            "name": new_name,
                            "type": new_type,
                            "status": new_status,
                            "age": new_age,
                            "needs": new_needs,
                            "desc": new_desc,
                            "img": new_img
                        }
                        st.session_state.animals_list.append(new_pet)
                        save_animals(st.session_state.animals_list)
                        st.success(f"🎉 {new_name} успешно добавлен на сайт!")
                        st.rerun()  # Перезагружаем страницу, чтобы обновить списки везде
                    else:
                        st.error("Пожалуйста, введите кличку и описание.")
        
        # ВКЛАДКА 2: УДАЛЕНИЕ / АРХИВАЦИЯ
        with tab2:
            st.subheader("Удаление питомцев с сайта")
            st.write("Если животное нашло дом или ситуация разрешилась, выберите его из списка ниже и нажмите кнопку удаления.")
            
            animals = st.session_state.animals_list
            
            if not animals:
                st.info("На сайте пока нет добавленных животных.")
            else:
                # Создаем список понятных названий для выпадающего списка: "Кличка (Тип) - Статус"
                animal_options = [f"{pet['name']} ({pet['type']}) — {pet['status']}" for pet in animals]
                
                # Выбор животного для удаления
                selected_animal_str = st.selectbox("Выберите животное для удаления:", animal_options)
                
                # Находим индекс выбранного животного
                selected_idx = animal_options.index(selected_animal_str)
                selected_pet = animals[selected_idx]
                
                st.warning(f"Вы собираетесь удалить подопечного: **{selected_pet['name']}**. Это действие нельзя отменить.")
                
                # Кнопка подтверждения удаления
                if st.button(f"❌ Подтвердить удаление {selected_pet['name']}", key="delete_pet_btn"):
                    # Удаляем из session_state и перезаписываем JSON
                    removed_name = st.session_state.animals_list.pop(selected_idx)['name']
                    save_animals(st.session_state.animals_list)
                    
                    st.success(f"🐾 {removed_name} успешно удален(а) с сайта!")
                    st.rerun()  # Мгновенно обновляем интерфейс
                    
    elif password:
        st.error("Неверный пароль!")

# === СТРАНИЦА 4: О НАС ===
elif menu == "О нас":
    st.title("🏢 О нашей волонтерской группе")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🌟 Наша миссия")
        st.write(
            "Мы не являемся государственным или классическим частным приютом. Мы — объединение волонтеров, "
            "которые спасают животных из пунктов отлова, организуют временные домашние передержки, "
            "занимаются лечением и социализацией уличных животных, а также реализуют программу гуманного регулирования "
            "численности (ОСВВ: Отлов-Стерилизация-Вакцинация-Возврат)."
        )
    with col2:
        st.subheader("📍 Контакты")
        st.markdown("🌐 **Название:** Инициативная группа помощи животным")
        st.markdown("📞 **Телефон для связи:** +375 (29) XXX-XX-XX (Татьяна)")
        st.markdown("💬 **Telegram / Viber:** @tatyana_khvost_up")
