import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Налаштування сторінки
st.set_page_config(page_title="Lab 5: Data Analysis", layout="wide")


# --- 1. Завантаження даних ---
@st.cache_data
def load_data():
    all_data = []
    current_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(current_dir, "vhi_data")
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            region_id = filename.split('_')[2]
            
            try:
                # Жорстко задаємо імена колонок. 
                # skipinitialspace=True ігнорує зайві пробіли після ком
                # header=1 пропускає перший рядок, де часто буває тег <tt><pre>
                df = pd.read_csv(
                    file_path, 
                    header=1, 
                    names=['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'Empty'], 
                    skipinitialspace=True
                )
                
                # Видаляємо сміття (наприклад, рядки з тегами </pre></tt> внизу файлу)
                df = df[~df['Year'].astype(str).str.contains('<', na=False)]
                
                # Конвертуємо колонки в числа. Якщо десь залишився текст, він перетвориться на порожнечу (NaN)
                for col in ['Year', 'Week', 'VCI', 'TCI', 'VHI']:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                
                # Додаємо область
                df['Region'] = f"Область {region_id}"
                
                # Залишаємо тільки потрібне і видаляємо рядки з порожнечею
                df = df[['Region', 'Year', 'Week', 'VCI', 'TCI', 'VHI']].dropna()
                
                all_data.append(df)
            except Exception as e:
                print(f"Помилка у {filename}: {e}")
                
    # Заглушка, щоб програма не "падала", якщо файли все ж не прочитались
    if not all_data:
        st.error("Критична помилка: Не вдалося прочитати жоден файл. Перевірте папку vhi_data.")
        return pd.DataFrame({'Region': ['Область 1'], 'Year': [2000], 'Week': [1], 'VCI': [0], 'TCI': [0], 'VHI': [0]})
        
    full_df = pd.concat(all_data, ignore_index=True)
    
    # Видаляємо помилкові значення VHI (які іноді позначаються як -1)
    full_df = full_df[full_df['VHI'] > 0]
    
    # Робимо рік і тиждень цілими числами
    full_df['Year'] = full_df['Year'].astype(int)
    full_df['Week'] = full_df['Week'].astype(int)
    
    return full_df

df = load_data()

# --- 2. Ініціалізація стану для кнопки Reset ---
# Це потрібно для того, щоб кнопка дійсно повертала інтерактивні елементи до початкових значень
if 'region' not in st.session_state:
    st.session_state.region = df['Region'].unique()[0]
if 'index' not in st.session_state:
    st.session_state.index = 'VHI'
if 'weeks' not in st.session_state:
    st.session_state.weeks = (1, 52)
if 'years' not in st.session_state:
    st.session_state.years = (int(df['Year'].min()), int(df['Year'].max()))
if 'sort_asc' not in st.session_state:
    st.session_state.sort_asc = False
if 'sort_desc' not in st.session_state:
    st.session_state.sort_desc = False

def reset_filters():
    st.session_state.region = df['Region'].unique()[0]
    st.session_state.index = 'VHI'
    st.session_state.weeks = (1, 52)
    st.session_state.years = (int(df['Year'].min()), int(df['Year'].max()))
    st.session_state.sort_asc = False
    st.session_state.sort_desc = False

# --- 3. Інтерактивні елементи (Бокова панель) ---
st.sidebar.header("Фільтри даних")

index_choice = st.sidebar.selectbox("Оберіть часовий ряд", ['VCI', 'TCI', 'VHI'], key='index')
region_choice = st.sidebar.selectbox("Оберіть область", df['Region'].unique(), key='region')
week_range = st.sidebar.slider("Інтервал тижнів", 1, 52, key='weeks')
year_range = st.sidebar.slider("Інтервал років", int(df['Year'].min()), int(df['Year'].max()), key='years')

st.sidebar.write("Сортування даних:")
sort_asc = st.sidebar.checkbox("За зростанням", key='sort_asc')
sort_desc = st.sidebar.checkbox("За спаданням", key='sort_desc')

st.sidebar.button("Reset (Скинути фільтри)", on_click=reset_filters)

# --- 4. Фільтрація та обробка даних ---
filtered_df = df[
    (df['Region'] == region_choice) &
    (df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1]) &
    (df['Week'] >= week_range[0]) & (df['Week'] <= week_range[1])
]

# Реакція на чекбокси сортування
if sort_asc and sort_desc:
    st.warning("Увага: обрано одночасно сортування за зростанням та спаданням! Дані залишено в оригінальному порядку.")
elif sort_asc:
    filtered_df = filtered_df.sort_values(by=index_choice, ascending=True)
elif sort_desc:
    filtered_df = filtered_df.sort_values(by=index_choice, ascending=False)

# --- 5. Основна частина: Таблиця та Графіки ---
st.title("Аналіз вегетаційних індексів (Lab 5)")

# Створюємо 3 вкладки
tab1, tab2, tab3 = st.tabs(["Таблиця даних", "Графік відфільтрованих даних", "Порівняння по областях"])

with tab1:
    st.subheader(f"Дані: {region_choice}")
    st.dataframe(filtered_df, width="stretch")

with tab2:
    st.subheader(f"Динаміка {index_choice} для {region_choice}")
    if not filtered_df.empty:
        fig, ax = plt.subplots(figsize=(10, 4))
        # Для коректного графіку сортуємо за часом
        plot_df = filtered_df.sort_values(by=['Year', 'Week'])
        x_labels = plot_df['Year'].astype(str) + "-W" + plot_df['Week'].astype(str)
        
        ax.plot(x_labels.values, plot_df[index_choice].values, marker='o', color='green', linewidth=2)
        ax.set_xlabel("Час (Рік-Тиждень)")
        ax.set_ylabel(index_choice)
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Відображаємо лише кожен 5-й підпис на осі X, щоб не було накладання тексту
        n = max(1, len(x_labels) // 10)
        ax.set_xticks(ax.get_xticks()[::n])
        ax.tick_params(axis='x', rotation=45)
        
        st.pyplot(fig)
    else:
        st.info("Немає даних для побудови графіка.")

with tab3:
    st.subheader(f"Порівняння середнього {index_choice} за обраний період")
    
    # Фільтруємо дані по часу для всіх областей
    compare_df = df[
        (df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1]) &
        (df['Week'] >= week_range[0]) & (df['Week'] <= week_range[1])
    ]
    
    if not compare_df.empty:
        avg_data = compare_df.groupby('Region')[index_choice].mean().reset_index()
        
        # Виділяємо обрану область червоним кольором, інші - синім
        colors = ['tomato' if r == region_choice else 'steelblue' for r in avg_data['Region']]
        
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        ax2.bar(avg_data['Region'], avg_data[index_choice], color=colors)
        ax2.set_xlabel("Область")
        ax2.set_ylabel(f"Середнє значення {index_choice}")
        ax2.tick_params(axis='x', rotation=90)
        ax2.grid(axis='y', linestyle='--', alpha=0.7)
        
        st.pyplot(fig2)
    else:
        st.info("Немає даних для порівняння.")