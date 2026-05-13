import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
from scipy.signal import butter, filtfilt

# --- 1. Початкові параметри ---
init_amplitude = 1.0
init_frequency = 1.0  # Це наша омега (ω)
init_phase = 0.0
init_noise_mean = 0.0
init_noise_covariance = 0.1
init_cutoff = 2.0  # Частота зрізу для фільтра

# Часова вісь
t = np.linspace(0, 10, 1000)

# Базовий шум (генерується ОДИН раз, щоб при зміні гармоніки шум не стрибав)
base_noise = np.random.normal(0, 1, len(t))

# --- 2. Функції для розрахунків ---
def get_harmonic(amp, freq, phase):
    """Повертає чисту гармоніку y(t) = A * sin(ωt + φ)"""
    return amp * np.sin(freq * t + phase)

def get_noise(mean, covariance):
    """Масштабує базовий шум відповідно до середнього та дисперсії (коваріації)"""
    # covariance - це дисперсія (sigma^2), тому стандартне відхилення - це корінь з неї
    std_dev = np.sqrt(covariance) if covariance > 0 else 0
    return (base_noise * std_dev) + mean

def apply_filter(data, cutoff_freq):
    """Фільтрує сигнал за допомогою фільтра Баттерворта низьких частот"""
    # Якщо частота зрізу занадто мала, фільтр не працюватиме коректно, тому ставимо ліміт
    if cutoff_freq <= 0.1:
        return data
    b, a = butter(N=3, Wn=cutoff_freq, fs=100, btype='low') # fs - частота дискретизації
    return filtfilt(b, a, data)

# --- 3. Налаштування вікна Matplotlib ---
fig, ax = plt.subplots(figsize=(10, 7))
plt.subplots_adjust(left=0.1, bottom=0.4) # Залишаємо місце знизу для слайдерів

# Малюємо початкові графіки
clean_y = get_harmonic(init_amplitude, init_frequency, init_phase)
current_noise = get_noise(init_noise_mean, init_noise_covariance)
noisy_y = clean_y + current_noise
filtered_y = apply_filter(noisy_y, init_cutoff)

# Лінії на графіку
line_clean, = ax.plot(t, clean_y, label='Чиста гармоніка', color='green', lw=2)
line_noisy, = ax.plot(t, noisy_y, label='Зашумлений сигнал', color='orange', alpha=0.7)
line_filtered, = ax.plot(t, filtered_y, label='Відфільтрована', color='blue', linestyle='--', lw=2)

ax.set_title("Гармоніка з шумом та фільтрацією")
ax.set_xlabel("Час (t)")
ax.set_ylabel("Амплітуда (y)")
ax.legend(loc='upper right')
ax.grid(True)

# --- 4. Інтерфейс (Слайдери, Кнопки, Чекбокси) ---
axcolor = 'lightgoldenrodyellow'

# Розташування слайдерів (x, y, ширина, висота)
ax_amp = plt.axes([0.15, 0.30, 0.65, 0.03], facecolor=axcolor)
ax_freq = plt.axes([0.15, 0.25, 0.65, 0.03], facecolor=axcolor)
ax_phase = plt.axes([0.15, 0.20, 0.65, 0.03], facecolor=axcolor)
ax_noise_mean = plt.axes([0.15, 0.15, 0.65, 0.03], facecolor=axcolor)
ax_noise_cov = plt.axes([0.15, 0.10, 0.65, 0.03], facecolor=axcolor)
ax_cutoff = plt.axes([0.15, 0.05, 0.65, 0.03], facecolor=axcolor)

# Створення слайдерів
sl_amp = Slider(ax_amp, 'Amplitude', 0.1, 5.0, valinit=init_amplitude)
sl_freq = Slider(ax_freq, 'Frequency (ω)', 0.1, 10.0, valinit=init_frequency)
sl_phase = Slider(ax_phase, 'Phase (φ)', 0.0, 2*np.pi, valinit=init_phase)
sl_noise_mean = Slider(ax_noise_mean, 'Noise Mean', -2.0, 2.0, valinit=init_noise_mean)
sl_noise_cov = Slider(ax_noise_cov, 'Noise Covariance', 0.0, 2.0, valinit=init_noise_covariance)
sl_cutoff = Slider(ax_cutoff, 'Cutoff Freq', 0.1, 20.0, valinit=init_cutoff)

# Чекбокс для шуму
ax_check = plt.axes([0.85, 0.15, 0.12, 0.1])
check = CheckButtons(ax_check, ['Show Noise'], [True])

# Кнопка Reset
ax_reset = plt.axes([0.85, 0.05, 0.1, 0.04])
btn_reset = Button(ax_reset, 'Reset', hovercolor='0.975')

# --- 5. Логіка оновлення (Що відбувається при русі повзунків) ---
def update(val):
    # Отримуємо нові значення зі слайдерів
    amp = sl_amp.val
    freq = sl_freq.val
    phase = sl_phase.val
    n_mean = sl_noise_mean.val
    n_cov = sl_noise_cov.val
    cutoff = sl_cutoff.val
    
    # 1. Оновлюємо чисту гармоніку
    new_clean_y = get_harmonic(amp, freq, phase)
    line_clean.set_ydata(new_clean_y)
    
    # 2. Оновлюємо шум. (Базовий шум не міняється, міняється лише масштаб)
    new_noise = get_noise(n_mean, n_cov)
    new_noisy_y = new_clean_y + new_noise
    
    # Показувати чи ховати шум залежно від чекбоксу
    if check.get_status()[0]:
        line_noisy.set_ydata(new_noisy_y)
        line_noisy.set_visible(True)
    else:
        line_noisy.set_visible(False)
        
    # 3. Оновлюємо відфільтровану лінію
    new_filtered_y = apply_filter(new_noisy_y, cutoff)
    line_filtered.set_ydata(new_filtered_y)
    
    # Перемальовуємо графік
    fig.canvas.draw_idle()

# Прив'язуємо функцію оновлення до кожного слайдера та чекбоксу
sl_amp.on_changed(update)
sl_freq.on_changed(update)
sl_phase.on_changed(update)
sl_noise_mean.on_changed(update)
sl_noise_cov.on_changed(update)
sl_cutoff.on_changed(update)
check.on_clicked(update)

def reset(event):
    sl_amp.reset()
    sl_freq.reset()
    sl_phase.reset()
    sl_noise_mean.reset()
    sl_noise_cov.reset()
    sl_cutoff.reset()
btn_reset.on_clicked(reset)

# Запуск програми
plt.show()