import tkinter as tk
from tkinter import filedialog
import speech_recognition as sr
from pydub import AudioSegment

# Создание главного окна
root = tk.Tk()
root.title("Анализатор переговоров")

# Получение размеров экрана
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Определение размеров окна и его положения по середине экрана
window_width = 800
window_height = 800  # Увеличено для размещения нового текста
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

# Установка размеров и положения окна
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Установка цветовой схемы
bg_color = "#ffffff"  # Белый фон
fg_color = "#d52b1e"  # Красный цвет текста
button_color = "#d52b1e"  # Красный цвет кнопки
button_hover_color = "#ba2419"  # Более темный красный для hover
text_color = "#000000"  # Черный цвет текста
label_color = "#58595b"  # Серый цвет текста для меток

root.configure(bg=bg_color)

# Функция для изменения цвета кнопки при наведении
def on_enter(e):
    button['background'] = button_hover_color

def on_leave(e):
    button['background'] = button_color

def load_audio():
    # Открыть диалоговое окно для выбора файла
    file_path = filedialog.askopenfilename(
        title="Выберите аудио-сообщение",
        filetypes=[("Audio Files", "*.mp3 *.wav *.ogg"), ("All Files", "*.*")]
    )
    if file_path:
        # Обновление текста метки
        file_label.config(text=f"Аудио-сообщение загружено: {file_path}")
        print(f"Аудио-сообщение загружено: {file_path}")

        # Конвертация аудиофайла в формат WAV
        try:
            audio = AudioSegment.from_file(file_path)
            wav_file_path = "converted_audio.wav"
            audio.export(wav_file_path, format="wav")

            # Создание объекта Recognizer
            recognizer = sr.Recognizer()

            # Загрузка аудиофайла
            with sr.AudioFile(wav_file_path) as source:
                # Слушаем аудиофайл до его окончания
                audio_data = recognizer.listen(source)

            # Распознавание текста из аудиофайла
            try:
                text = recognizer.recognize_google(audio_data, language="ru-RU")
                print("Текст из аудио:", text)
                # Обновление текста метки с распознанным текстом
                result_label.config(text=f"Распознанный текст: {text}")
            except sr.UnknownValueError:
                print("Google Speech Recognition не смог распознать аудио")
                result_label.config(text="Google Speech Recognition не смог распознать аудио")
            except sr.RequestError as e:
                print("Ошибка при запросе к Google Speech Recognition:", e)
                result_label.config(text=f"Ошибка при запросе к Google Speech Recognition: {e}")
        except Exception as e:
            print("Ошибка при конвертации аудио:", e)
            result_label.config(text=f"Ошибка при конвертации аудио: {e}")

        # Обновление текста метки с количеством нарушений
        violations_label.config(text="Количество нарушений", fg=label_color)

# Создание метки для отображения количества нарушений
violations_label = tk.Label(root, text="Количество нарушений", font=("Helvetica", 12), bg=bg_color, fg=label_color)
violations_label.pack(pady=10)

# Создание кнопки для загрузки аудио-сообщения
button = tk.Button(root, text="Загрузить аудио-сообщение", command=load_audio, bg=button_color, fg="white", font=("Helvetica", 12, "bold"), activebackground=button_hover_color, activeforeground="white")
button.pack(pady=10)
button.bind("<Enter>", on_enter)
button.bind("<Leave>", on_leave)

# Создание метки для отображения пути к загруженному файлу
file_label = tk.Label(root, text="", font=("Helvetica", 10), bg=bg_color, fg=label_color)
file_label.pack(pady=10)

# Создание метки для отображения распознанного текста
result_label = tk.Label(root, text="", font=("Helvetica", 12), bg=bg_color, fg=text_color, wraplength=350)
result_label.pack(pady=10)

# Создание метки с


# Создание метки с дополнительным текстом
additional_label = tk.Label(root, text="Анализатор переговоров РЖД", font=("Helvetica", 14), bg=bg_color, fg=text_color)
additional_label.pack(pady=5)

# Создание рамки для визуального элемента
visual_frame = tk.Frame(root, bg=bg_color)
visual_frame.pack(pady=5)

# Создание визуального элемента (может быть графиком, изображением и т. д.)
# В данном случае просто прямоугольник для демон

# Создание визуального элемента (может быть графиком, изображением и т. д.)
# В данном случае просто прямоугольник для демонстрации
visual_element = tk.Canvas(visual_frame, bg="lightgray", width=200, height=50)
visual_element.pack()

# Запуск главного цикла обработки событий
root.mainloop()
