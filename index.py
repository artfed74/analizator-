import tkinter as tk
from tkinter import filedialog
import speech_recognition as sr
from pydub import AudioSegment
from PIL import Image, ImageTk, ImageDraw, ImageOps
import patterns  # Импортируем наш файл с паттернами

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

                # Проверка на паттерны
                missing_keywords, found_unwanted_words = patterns.check_keywords_presence(text, patterns.keywords, patterns.unwanted_words)
                structure_valid = patterns.check_text_structure(text, patterns.pattern)

                # Очистка текстовых виджетов перед добавлением нового текста
                converted_text.delete(1.0, tk.END)
                result_text.delete(1.0, tk.END)

                # Добавление конвертированного текста и выделение нежелательных слов
                converted_text.insert(tk.END, "Конвертированный текст:\n")
                for word in text.split():
                    if word in found_unwanted_words:
                        converted_text.insert(tk.END, word + " ", "unwanted")
                    else:
                        converted_text.insert(tk.END, word + " ")
                converted_text.insert(tk.END, "\n\n")

                # Проверка на ключевые слова и структуру
                if found_unwanted_words:
                    result_text.insert(tk.END, f"Найдено нежелательное слово: {', '.join(found_unwanted_words)}\n", "unwanted")
                else:
                    result_text.insert(tk.END, "Нежелательные слова не найдены.\n", "normal")
                
                if missing_keywords:
                    result_text.insert(tk.END, f"Ключевые слова не найдены: {', '.join(missing_keywords)}\n", "missing")
                if structure_valid:
                    result_text.insert(tk.END, "Текст соответствует ожидаемой структуре.\n", "valid")
                else:
                    result_text.insert(tk.END, "Текст не соответствует ожидаемой структуре.\n", "invalid")

                # Обновление текста метки с количеством нарушений
                violations_label.config(text="Нарушения в данном аудио:", fg=label_color)
            except sr.UnknownValueError:
                print("Google Speech Recognition не смог распознать аудио")
                result_text.insert(tk.END, "Google Speech Recognition не смог распознать аудио\n", "error")
            except sr.RequestError as e:
                print("Ошибка при запросе к Google Speech Recognition:", e)
                result_text.insert(tk.END, f"Ошибка при запросе к Google Speech Recognition: {e}\n", "error")
        except Exception as e:
            print("Ошибка при конвертации аудио:", e)
            result_text.insert(tk.END, f"Ошибка при конвертации аудио: {e}\n", "error")

# Создание главного окна
root = tk.Tk()
root.title("Анализатор переговоров РЖД")  # Обновленный заголовок

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

# Установка цветовой схемы РЖД
bg_color = "#e9eaed"  # Приглушенный серый цвет фона
fg_color = "#ffffff"  # Белый цвет текста
button_color = "#d52b1e"  # Красный цвет кнопки РЖД
button_hover_color = "#ba2419"  # Более темный красный для hover
text_color = "#ffffff"  # Белый цвет текста
text_color_src = "#767d89"  # Серый цвет для отображения пути файла
label_color = "#000000"  # Белый цвет текста для меток РЖД

root.configure(bg=bg_color)

# Путь к логотипу РЖД
logo_path = "rzd_logo.png"  # Добавил эту строку

# Создание блока для логотипа и названия приложения
header_block = tk.Frame(root, bg="#ffffff", width=window_width, height=100)
header_block.pack(side="top", fill="x")

# Загрузка изображения логотипа без скругления
logo_image = Image.open(logo_path).resize((100, 100), Image.LANCZOS)
logo = ImageTk.PhotoImage(logo_image)

# Создание метки для отображения логотипа
logo_label = tk.Label(root, image=logo, bg=bg_color)
logo_label.place(x=-0.7, y=-0.7)  # Размещение логотипа в верхнем левом углу

# Создание метки с дополнительным текстом в верхнем правом углу
additional_label = tk.Label(root, text="Анализатор переговоров РЖД", font=("Helvetica", 28), bg=fg_color, fg=label_color)
additional_label.place(relx=1.0, x=-30, y=30, anchor="ne")  # небольшой сдвиг на -30 по оси x

# Создание метки для отображения количества нарушений
violations_label = tk.Label(root, text="", font=("Helvetica", 12), bg=bg_color, fg=label_color)
violations_label.pack(pady=10)

# Создание кнопки для загрузки аудио-сообщения
button = tk.Button(root, text="Загрузить аудио-сообщение", command=load_audio, bg="#e31b1a", fg="white", font=("Helvetica", 12, "bold"), padx=15, pady=15, bd=0, relief=tk.FLAT)
button.pack(side="top", pady=(0, 10))
button.bind("<Enter>", on_enter)
button.bind("<Leave>", on_leave)

# Создание метку для отображения пути к загруженному файлу
file_label = tk.Label(root, text="", font=("Helvetica", 10), bg=bg_color, fg=text_color_src)
file_label.pack(side="top", pady=(0, 10))

# Создание рамки для обоих текстовых виджетов
text_frame = tk.Frame(root, bg=bg_color)
text_frame.pack(pady=10)

# Создание текстового виджета для отображения конвертированного текста
converted_text = tk.Text(text_frame, font=("Helvetica", 12), bg="white", fg="black", wrap="word", height=10, width=35)
converted_text.tag_config("unwanted", foreground="red")
converted_text.grid(row=0, column=0, padx=5)

# Создание текстового виджета для отображения результатов проверки
result_text = tk.Text(text_frame, font=("Helvetica", 12), bg="white", wrap="word", height=10, width=35)
result_text.tag_config("unwanted", foreground="red")
result_text.tag_config("missing", foreground="blue")
result_text.tag_config("valid", foreground="green")
result_text.tag_config("invalid", foreground="orange")
result_text.tag_config("error", foreground="purple")
result_text.grid(row=0, column=1, padx=5)

# Запуск главного цикла обработки событий
root.mainloop()
