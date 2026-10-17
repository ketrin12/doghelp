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

DB_FILE = "animals.json"

def file_to_base64(uploaded_file):
    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        encoded = base64.b64encode(file_bytes).decode("utf-8")
        return f"data:image/jpeg;base64,{encoded}"
    return "https://unsplash.com"

DB_FILE = "animals.json"

# Вставь сюда свой скопированный Master Key с сайта JSONBin
DIN_KEY = "$2a$10$VxXWcC4/bInixOKdXgfpgOv64nA89l1ksvAiQJptNBg1eRzIzSuOi"
# Ссылка на твою личную корзину (создастся автоматически при первом сохранении)
DIN_URL = "https://api.jsonbin.v3/b/67110901e41b4d34e444bc30" # Эту ссылку мы обновим после первого теста

DB_FILE = "animals.json"

# ================= НАСТРОЙКИ ОБЛАКА JSONBIN =================
DIN_KEY = "$2a$10$VxXWcC4/bInixOKdXgfpgOv64nA89l1ksvAiQJptNBg1eRzIzSuOi"
DIN_ID = "64d3679affd5d16053736a4f"
DIN_URL = f"https://api.jsonbin.v3/b/{DIN_ID}"

def load_animals():
    """Загружает список питомцев из облака JSONBin"""
    headers = {
        "X-Master-Key": DIN_KEY  # Используем строго DIN_KEY
    }
    try:
        # Делаем запрос к актуальной версии данных
        response = requests.get(f"{DIN_URL}/latest", headers=headers)
        if response.status_code == 200:
            res_data = response.json()
            record_data = res_data.get("record", [])
            
            # Если это список (как на твоем скриншоте), отдаем его
            if isinstance(record_data, list):
                return record_data
            # Если это одиночный объект, оборачиваем в список
            elif isinstance(record_data, dict):
                return [record_data]
        
        # Если сервер лег, берем локальный файл для резерва
        with open("animals.json", "r", encoding="utf-8") as f:
            local_data = json.load(f)
            return local_data if isinstance(local_data, list) else []
    except:
        return []

def save_animals(data):
    """Сохраняет список питомцев в облако JSONBin"""
    # 1. Резервное сохранение в локальный файл
    try:
        with open("animals.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except:
        pass

    # 2. Основное сохранение в JSONBin
    headers = {
        "Content-Type": "application/json",
        "X-Master-Key": DIN_KEY  # Используем строго DIN_KEY
    }
    try:
        response = requests.put(DIN_URL, json=data, headers=headers)
        if response.status_code == 200:
            return True
    except:
        pass
    return False

    # ИНИЦИАЛИЗАЦИЯ: Если списка еще нет в памяти, мы загружаем его из наших Secrets
if 'animals_list' not in st.session_state:
    st.session_state.animals_list = load_animals()

# 1. Сначала идет сам словарь со всеми переводами (строка 108+)
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
        "age_cats": ["Щенок / Котенок", "Взрослый питомец"]
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
        "age_cats": ["Puppy / Kitten", "Adult Pet"]
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
        "alert_help": "Vielen Dank für Ihre Antwort! Kontaktieren Sie uns im Bereich 'Über uns' oder 'Spenden & Helfen'.",
        "age_cats": ["Welpe / Kätzchen", "Erwachsenes Tier"]
    }
}

# СЮДА ВСТАВЛЯЕМ ЭТИ СТРОЧКИ (ПОСЛЕ ЗАКРЫТИЯ СЛОВАРЯ!):
selected_lang = st.sidebar.selectbox("", ["Русский", "English", "Deutsch"], label_visibility="visible", index=0)
t = LANG_DICT[selected_lang]

menu_options = t["nav"]
menu_choice = st.sidebar.radio(t["lang_label"], menu_options)
menu_idx = menu_options.index(menu_choice)

# === СТРАНИЦА 0: ГЛАВНАЯ ===
if menu_idx == 0:
    st.title(t["title_main"])
    st.write(t["subtitle_main"])

    # Добавляем переводы для фильтра в зависимости от выбранного языка
    if selected_lang == "Русский":
        filter_options = ["Все", "Щенки / Котята (0-1 год)", "Взрослые питомцы (1+ лет)"]
    elif selected_lang == "English":
        filter_options = ["All", "Puppies / Kittens (0-1 year)", "Adult Pets (1+ years)"]
    else:
        filter_options = ["Alle", "Welpen / Kätzchen (0-1 Jahr)", "Erwachsene Tiere (1+ Jahre)"]

    # Кнопки-переключатели на самом верху страницы
        # Кнопки-переключатели на самом верху страницы
    selected_filter = st.segmented_control(
        "", 
        options=filter_options, 
        default=filter_options[0]  # По умолчанию выбрано "Все"
    )

    # Фильтруем список
    filtered_animals = []
    for pet in "animals":
        pet_cat = pet.get("age_category", "Взрослый питомец")
        
        # Если выбрано "Все" или фильтр сброшен
        if selected_filter == filter_options[0] or selected_filter is None:
            filtered_animals.append(pet)
        # Если выбрана вкладка Щенки
        elif selected_filter == filter_options[1]:
            if pet_cat == "Щенок / Котенок":
                filtered_animals.append(pet)
        # Если выбрана вкладка Взрослые
        elif selected_filter == filter_options[2]:
            if pet_cat == "Взрослый питомец":
                filtered_animals.append(pet)

            if pet_cat == "Щенок / Котенок":
                filtered_animals.append(pet)
        else: # Выбрано "Взрослые"
            if pet_cat == "Взрослый питомец":
                filtered_animals.append(pet)

    # Выводим на экран уже отфильтрованных животных
    if not filtered_animals:
        st.info("В этой категории сейчас нет подопечных. Посмотрите другие вкладки! 🥰")
    else:
        for i in range(0, len(filtered_animals), 3):
            cols = st.columns(3)
            for j in range(3):
                idx = i + j
                if idx < len(filtered_animals):
                    with cols[j]:
                        item = filtered_animals[idx]
                        
                        try:
                            st.image(item["img"], use_container_width=True)
                        except:
                            st.warning("⚠️ Photo error")
                        
                        status = item.get("status", "На временной передержке")
                        if "отлове" in status or "rescue" in status or "Tötung" in status:
                            st.markdown(f'<div class="status-badge status-otlov">🚨 {status}</div>', unsafe_allow_html=True)
                        elif "улице" in status or "street" in status or "Straße" in status:
                            st.markdown(f'<div class="status-badge status-street">🏡 {status}</div>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<div class="status-badge status-perederzhka">🐾 {status}</div>', unsafe_allow_html=True)

                        st.subheader(f"{item['name']} ({item.get('age', '')})")
                        st.write(f"**{t['type']}:** {item.get('type', '')} | **{t['age_cat']}:** {item.get('age_category', 'Взрослый питомец')}")
                        st.write(f"**{t['desc']}:** {item['desc']}")
                        
                        if item.get("needs"):
                            st.warning(f"⚠️ **{t['needs']}:** {item['needs']}")

                        if st.button(f"{t['btn_help']} {item['name']}", key=f"btn_{idx}"):
                            st.success(t["alert_help"])
                        st.markdown("---")

# === СТРАНИЦА 1: ПОМОЩЬ ===
elif menu_idx == 1:
    if selected_lang == "Русский":
        st.title("💚 Поддержать подопечных и передержку")
        st.write("Все средства идут точечно на спасение животных из отлова, оплату передержек и лечение.")
        st.info("ℹ️ Все поступающие средства идут напрямую на корм, лекарства и клиники.")
    elif selected_lang == "English":
        st.title("💚 Support Foster Care & Rescue")
        st.write("All funds go directly towards rescuing animals from pounds, paying for foster homes, and medical treatment.")
    else:
        st.title("💚 Pflegestelle & Rettung unterstützen")
        st.write("Alle Spenden fließen direkt in die Rettung von Tieren aus Tötungsstationen, die Bezahlung von Pflegestellen und medizinische Behandlungen.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("💳 Банковская карта / ЕРИП")
        st.code("Благотворительный счет в Беларусбанке:\nBYXX AKBB XXXX XXXX XXXX XXXX XXXX")
        st.code("Код ЕРИП: 1234567 (Благотворительность -> Помощь животным)")
    
    with col2:
        st.subheader("📦 Пункты сбора помощи и выдачи")
        st.write("Если вы хотите передать хвостикам **корма, теплые вещи, поводки или лекарства**, вы можете привезти их по адресам:")
        
        # Оформляем адреса в виде красивых блоков-цитат
        st.info("📍 **г. Речица, ул. Советская, 37** (Пункт Ozon)")
        st.info("📍 **г. Речица, ул. Чапаева, 8** (Пункт ВБ)")
        st.warning("🚨 **г. Речица, ул. Пролетарская, 118** — Пункт временного содержания (Сюда особенно необходима помощь теплыми вещами на подстилки и сухими кормами!)")
        
        st.markdown("---")
        st.write("**Телефон куратора:** +375 (29) XXX-XX-XX (Татьяна)")

# === СТРАНИЦА 2: ПОМОЩЬ ===
elif menu_idx == 1:
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

# === СТРАНИЦА 2: ПАНЕЛЬ УПРАВЛЕНИЯ ===
elif menu_idx == 2:
    st.title("🔒 Вход в панель управления")
    password = st.text_input("Введите пароль администратора / Enter admin password", type="password")
    
    if password == "admin123":
        st.success("Доступ разрешен!")
        tab1, tab2, tab3 = st.tabs(["➕ Добавить", "✏️ Редактировать", "🗑️ Удалить"])
        
        with tab1:
            # Создаем форму для добавления питомца
            with st.form("add_animal_form", clear_on_submit=True):
                st.subheader("Добавление нового подопечного")
                
                new_name = st.text_input("Кличка животного")
                new_type = st.selectbox("Кто это?", ["Собака", "Кошка", "Другое"])
                new_age_cat = st.selectbox("Категория возраста", ["Щенок / Котенок", "Взрослый питомец"])
                new_status = st.selectbox("Текущий статус / Где находится?", [
                    "В отлове (Срочный вывоз!)", 
                    "На временной передержке", 
                    "Живет на улице (Нужна помощь)"
                ])
                new_age = st.text_input("Примерный возраст")
                new_needs = st.text_input("В чем нуждается? (например: Сбор на корм, Нужен дом)")
                new_desc = st.text_area("Описание ситуации / Характер")
                
                uploaded_file = st.file_uploader("Выберите фото питомца", type=["jpg", "jpeg", "png"], key="add_upload")
                
                # ВОТ ЭТА СТРОКА ОБЯЗАТЕЛЬНО ДОЛЖНА БЫТЬ ТУТ:
                submit = st.form_submit_button("Добавить на сайт")
                
                if submit:
                    if new_name and new_desc:
                        img_data = file_to_base64(uploaded_file)
                        
                        new_pet = {
                            "name": new_name,
                            "type": new_type,
                            "age_category": new_age_cat,
                            "status": new_status,
                            "age": new_age,
                            "needs": new_needs,
                            "desc": new_desc,
                            "img": img_data
                        }
                        st.session_state.animals_list.append(new_pet)
                        
                        # Сохраняем локально и в облако, затем обновляем
                        save_animals(st.session_state.animals_list)
                        st.rerun()
                    else:
                        st.error("Пожалуйста, введите кличку и описание.")

        with tab2:
            st.subheader("📝 Редактирование")
            animals = st.session_state.animals_list
            if not animals: st.info("Пусто")
            else:
                animal_options = [f"{pet['name']} ({pet['type']})" for pet in animals]
                selected_edit_str = st.selectbox("Выберите питомца:", animal_options)
                edit_idx = animal_options.index(selected_edit_str)
                current_pet = animals[edit_idx]
                
                with st.form("edit_form"):
                    edit_name = st.text_input("Кличка", value=current_pet.get("name", ""))
                    edit_type = st.selectbox("Кто это?", ["Собака", "Кошка", "Другое"], index=["Собака", "Кошка", "Другое"].index(current_pet.get("type", "Собака")))
                    
                    cat_list = ["Щенок / Котенок", "Взрослый питомец"]
                    cat_idx = cat_list.index(current_pet.get("age_category", "Взрослый питомец")) if current_pet.get("age_category") in cat_list else 1
                    edit_age_cat = st.selectbox("Категория возраста", cat_list, index=cat_idx)
                    
                    edit_status = st.selectbox("Статус", ["В отлове (Срочный вывоз!)", "На временной передержке", "Живет на улице (Нужна помощь)"], index=0)
                    edit_age = st.text_input("Точный возраст", value=current_pet.get("age", ""))
                    edit_needs = st.text_input("Нужды", value=current_pet.get("needs", ""))
                    edit_desc = st.text_area("Описание", value=current_pet.get("desc", ""))
                    edit_file = st.file_uploader("Загрузить новую фотографию", type=["jpg", "jpeg", "png"])
                    
                    if st.form_submit_button("Сохранить изменения"):
                        final_img = file_to_base64(edit_file) if edit_file is not None else current_pet.get("img")
                        st.session_state.animals_list[edit_idx] = {
                            "name": edit_name, "type": edit_type, "age_category": edit_age_cat,
                            "status": edit_status, "age": edit_age, "needs": edit_needs, "desc": edit_desc, "img": final_img
                        }
                        save_animals(st.session_state.animals_list)
                        st.success("Обновлено!")
                        st.rerun()
        
        with tab3:
            st.subheader("Удаление")
            animals = st.session_state.animals_list
            if not animals: st.info("Пусто")
            else:
                animal_options_del = [f"{pet['name']} ({pet['type']})" for pet in animals]
                selected_animal_str = st.selectbox("Выберите для удаления:", animal_options_del)
                selected_idx = animal_options_del.index(selected_animal_str)
                if st.button(f"❌ Подтвердить удаление {animals[selected_idx]['name']}"):
                    st.session_state.animals_list.pop(selected_idx)
                    save_animals(st.session_state.animals_list)
                    st.success("Удалено!")
                    st.rerun()

# === СТРАНИЦА 3: О НАС ===
elif menu_idx == 3:
    if selected_lang == "Русский":
        st.title("🏢 О нашей инициативе «Хвост-Ап»")
        
        st.subheader("🌟 Кто мы такие?")
        st.write(
            "«Хвост-Ап» — это не классический приют со стационарными вольерами и госбюджетом. Мы — независимое объединение "
            "волонтеров и неравнодушных людей, которые взяли на себя задачу спасать тех, у кого нет шансов выжить в одиночку. "
            "Все наши подопечные живут либо на временных домашних передержках у волонтеров, либо находятся под опекой кураторов прямо на улице."
        )
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🎯 Направления нашей работы:")
            st.markdown("""
            * **Спасение из отлова:** Мы экстренно выкупаем и вывозим собак и кошек из пунктов временного содержания (отлова), где им грозит усыпление.
            * **Временный дом (Передержка):** Мы обеспечиваем хвостикам безопасную жизнь в семьях наших волонтеров, лечим их, адаптируем и социализируем.
            * **Уличная опека и ОСВВ:** Мы подкармливаем бездомных животных, строим утепленные будки во дворах, организуем стерилизацию и вакцинацию, чтобы гуманно контролировать их численность.
            """)
        with col2:
            st.subheader("📍 Как с нами связаться?")
            st.markdown("📞 **Телефон куратора:** +375 (29) XXX-XX-XX (Татьяна)")
            st.markdown("💬 **Telegram / Viber:** @tatyana_khvost_up")
            st.markdown("📌 *Вы можете помочь руками, кормом или автопомощью. Каждый шаг важен!*")
            
    elif selected_lang == "English":
        st.title("🏢 About Our Initiative 'Khvost-Up'")
        st.subheader("🌟 Who We Are")
        st.write(
            "We are an independent volunteer rescue group. We do not have a centralized shelter building. "
            "All animals under our care stay either in temporary volunteer foster homes or are supported directly on the streets by local curators."
        )
        st.subheader("🎯 Our Key Mission")
        st.markdown("""
        * **Pound Rescue:** Saving animals from death row in city pounds.
        * **Foster Network:** Providing safe temporary housing, socialization, and medical care.
        * **Street Care & TNR:** Feeding stray animals, providing shelter boxes, and organizing Trap-Neuter-Return programs.
        """)
        st.write("📞 **Contact Curator:** +375 (29) XXX-XX-XX (Tatyana)")
        
    else:  # Deutsch
        st.title("🏢 Über unsere Initiative 'Chwost-Up'")
        st.subheader("🌟 Wer wir sind")
        st.write(
            "Wir sind eine unabhängige Tierschutz-Freiwilligengruppe. Wir haben kein stationäres Tierheimgebäude. "
            "Alle Tiere leben entweder in temporären Pflegefamilien unserer Freiwilligen oder werden direkt auf der Straße von Betreuern versorgt."
        )
        st.subheader("🎯 Unsere Hauptaufgaben")
        st.markdown("""
        * **Rettung aus Tötungsstationen:** Dringende Evakuierung von Tieren vor der Einschläferung.
        * **Pflegestellennetzwerk:** Sicherstellung eines sicheren Lebens in Familien, medizinische Versorgung und Sozialisierung.
        * **Straßenbetreuung:** Fütterung, Kastration und Impfung von Straßenhunden und -katzen.
        """)
        st.write("📞 **Kontakt:** +375 (29) XXX-XX-XX (Tatyana)")
