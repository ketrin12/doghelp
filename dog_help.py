import streamlit as st

st.set_page_config(
    page_title="Ketrin Plase | Главная",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed"  # Сворачиваем меню по умолчанию
)

# Полностью убираем боковое меню и жестко задаем цвет кнопок
st.markdown(
    """
    <style>
    /* Полностью скрываем боковую панель, кнопку открытия и всю верхнюю техническую шапку */
    [data-testid="stSidebar"], 
    [data-testid="collapsedControl"], 
    [data-testid="stHeader"] {
        display: none !important;
    }
    
    /* Фиксируем темный цвет кнопок с золотой рамкой */
    .stButton > button {
        background-color: #046307 !important;
        color: #046307 !important;
        border: 1px solid #bc987e !important;
        transition: all 0.3s ease;
    }
    
    /* Эффект при наведении мышки на ПК */
    .stButton > button:hover {
        background-color: #bc987e !important;
        color: #140f0d !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("""
<style>
/* Фиксируем красивый темный фон */
.stApp, .main, [data-testid="stAppViewContainer"] { 
    background-image: linear-gradient(rgba(20, 15, 13, 0.8), rgba(20, 15, 13, 0.8)), url("https://ibb.co") !important;
    background-size: cover !important;
    background-position: center !important;
    background-attachment: fixed !important;
    background-color: #ffffff !important;
} 

}
[data-testid="stSidebarCollapseButton"] button::after {
    content: "•" !important; /* Ставим аккуратную точку */
    font-size: 28px !important;
    color: #dfba9d !important; /* Красим в золото */
    display: block !important;
    line-height: 1 !important;
}

/* Элегантные шрифты для текста */
h1, h2, h3, h4, h5, h6, p, span, label, li, div, b { 
    color: #f5ebe6 !important; 
    font-family: 'Georgia', serif !important; 
}

/* Шоколадное боковое меню */
[data-testid="stSidebar"], [data-testid="stSidebarNav"] {
    background-color: #2d2320 !important;
}

/* Золотые вкладки в меню */
[data-testid="stSidebarNav"] span, [data-testid="stSidebarNav"] a {
    color: #dfba9d !important;
    font-size: 18px !important;
}

/* Полностью стираем текст внутри кнопки на любых экранах */
[data-testid="stSidebarCollapseButton"] div, 
[data-testid="stSidebarCollapseButton"] span,
[data-testid="stSidebarCollapseButton"] svg {
    display: none !important;
    font-size: 0 !important;
    color: transparent !important;
    width: 0 !important;
    height: 0 !important;
}
[data-testid="stSidebarCollapseButton"] button {
    display: none !important;
}

</style>
""", unsafe_allow_html=True)

# Шапка сайта
st.markdown(
    "<div style='background-color: rgba(25, 20, 18, 0.9); padding: 30px; border-radius: 12px; text-align: center; border: 1px solid #4a3b32;'>"
    "<h1 style='color: #dfba9d !important; margin: 0; font-size: 42px; letter-spacing: 2px;'>Ketrin Plase</h1>"
    "<p style='margin: 10px 0 0 0; color: #b3b3b3 !important; font-size: 16px; letter-spacing: 3px; text-transform: uppercase;'>Премиум СПА-салон в Гомеле</p>"
    "</div>", 
    unsafe_allow_html=True
)

st.write("") 

col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown("<h4 style='color: #bc987e !important; text-transform: uppercase; letter-spacing: 2px;'>Эстетика релакса</h4>", unsafe_allow_html=True)
st.title("Добро пожаловать в Ketrin Plase")
st.write("Выберите интересующий вас раздел в боковом меню слева, чтобы посмотреть цены или открыть галерею нашего салона.")

# Добавляем крупные и понятные кнопки для мобильных пользователей прямо по центру
st.markdown("### 📱 Быстрый переход по разделам:")
col_menu1, col_menu2 = st.columns(2)

with col_menu1:
    if st.button("💰 Посмотреть ЦЕНЫ", use_container_width=True):
        st.switch_page("pages/1_Цены.py") # Проверь, чтобы имя файла в скобках совпадало с твоим в папке pages

with col_menu2:
    if st.button("🖼️ Открыть ГАЛЕРЕЮ", use_container_width=True):
        st.switch_page("pages/2_Галерея.py") # Проверь, чтобы имя файла в скобках совпадало с твоим в папке pages

st.divider()

# Форма онлайн-записи
st.markdown("<h2>📩 Онлайн-резервирование визита</h2>", unsafe_allow_html=True)
FORMSPREE_URL = "https://formspree.io" 

form_html = f"""
<form action="{FORMSPREE_URL}" method="POST" style="background-color: rgba(25, 20, 18, 0.9); padding: 30px; border-radius: 12px; border: 1px solid #4a3b32;">
    <div style="margin-bottom: 20px;"><label style="color: #dfba9d !important; font-weight: bold;">Ваше имя:</label><br><input type="text" name="name" required style="width: 100%; padding: 12px; background-color: #140f0d; border: 1px solid #bc987e; border-radius: 6px; color: white;"></div>
    <div style="margin-bottom: 20px;"><label style="color: #dfba9d !important; font-weight: bold;">Телефон или Email:</label><br><input type="email" name="_replyto" required style="width: 100%; padding: 12px; background-color: #140f0d; border: 1px solid #bc987e; border-radius: 6px; color: white;"></div>
    <div style="margin-bottom: 20px;"><label style="color: #dfba9d !important; font-weight: bold;">Пожелания к визиту:</label><br><textarea name="message" required style="width: 100%; height: 100px; background-color: #140f0d; border: 1px solid #bc987e; border-radius: 6px; color: white; resize: none;"></textarea></div>
    <button type="submit" style="background-color: #bc987e; color: #231f20; padding: 14px 28px; border: none; border-radius: 6px; cursor: pointer; font-size: 16px; font-weight: bold; width: 100%; text-transform: uppercase;">Забронировать визит</button>
</form>
"""
st.markdown(form_html, unsafe_allow_html=True)

st.divider()
st.caption("© 2026 Ketrin Plase. Режим работы: с 9:00 до 23:00 ежедневно. Разработано будущим топовым ИТ-специалистом.")
