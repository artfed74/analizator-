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

                # Очистка текстового виджета перед добавлением нового текста
                result_text.delete(1.0, tk.END)
                
                # Добавление распознанного текста
                result_text.insert(tk.END, f"Распознанный текст: {text}\n\n")
                
                # Выделение найденных нежелательных слов
                if found_unwanted_words:
                    for word in found_unwanted_words:
                        start_index = result_text.search(word, 1.0, tk.END)
                        while start_index:
                            end_index = f"{start_index}+{len(word)}c"
                            result_text.tag_add("unwanted", start_index, end_index)
                            start_index = result_text.search(word, end_index, tk.END)

                # Проверка на ключевые слова и структуру
                if missing_keywords:
                    result_text.insert(tk.END, f"Ключевые слова не найдены: {', '.join(missing_keywords)}\n")
                if found_unwanted_words:
                    result_text.insert(tk.END, f"Найдены нежелательные слова: {', '.join(found_unwanted_words)}\n")
                if structure_valid:
                    result_text.insert(tk.END, "Текст соответствует ожидаемой структуре.")
                else:
                    result_text.insert(tk.END, "Текст не соответствует ожидаемой структуре.")
                    
                # Обновление текста метки с количеством нарушений
                violations_label.config(text="Нарушения в данном аудио:", fg=label_color)
            except sr.UnknownValueError:
                print("Google Speech Recognition не смог распознать аудио")
                result_text.insert(tk.END, "Google Speech Recognition не смог распознать аудио\n")
            except sr.RequestError as e:
                print("Ошибка при запросе к Google Speech Recognition:", e)
                result_text.insert(tk.END, f"Ошибка при запросе к Google Speech Recognition: {e}\n")
        except Exception as e:
            print("Ошибка при конвертации аудио:", e)
            result_text.insert(tk.END, f"Ошибка при конвертации аудио: {e}\n")

def create_rounded_image(image_path, size, radius):
    # Загрузка изображения
    img = Image.open(image_path).resize(size, Image.Resampling.LANCZOS)

    # Создание маски с закругленными углами
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, size[0], size[1]), radius=radius, fill=255)

    # Применение маски к изображению
    rounded_img = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
    rounded_img.putalpha(mask)

    return rounded_img

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
bg_color = "#78909C"  # Приглушенный синий цвет фона
fg_color = "#ffffff"  # Белый цвет текста
button_color = "#d52b1e"  # Красный цвет кнопки РЖД
button_hover_color = "#ba2419"  # Более темный красный для hover
text_color = "#ffffff"  # Белый цвет текста
label_color = "#ffffff"  # Белый цвет текста для меток РЖД

root.configure(bg=bg_color)

# Путь к логотипу РЖД
logo_path = "rzd_logo.png"

# Создание изображения с закругленными углами
rounded_logo_image = create_rounded_image(logo_path, (100, 100), 100)
logo = ImageTk.PhotoImage(rounded_logo_image)

# Создание метки для отображения логотипа
logo_label = tk.Label(root, image=logo, bg=bg_color)
logo_label.place(x=10, y=10)  # Размещение логотипа в верхнем левом углу

# Создание метки для отображения количества нарушений
violations_label = tk.Label(root, text="", font=("Helvetica", 12), bg=bg_color, fg=label_color)
violations_label.pack(pady=10)

# Создание кнопки для загрузки аудио-сообщения
button = tk.Button(root, text="Загрузить аудио-сообщение", command=load_audio, bg=button_color, fg="white", font=("Helvetica", 12, "bold"), activebackground=button_hover_color, activeforeground="white")
button.pack(pady=10)
button.bind("<Enter>", on_enter)
button.bind("<Leave>", on_leave)

# Создание метки для отображения пути к загруженному файлу
file_label = tk.Label(root, text="", font=("Helvetica", 10), bg=bg_color, fg=label_color)
file_label.pack(pady=10)

# Создание текстового виджета для отображения распознанного текста
result_text = tk.Text(root, font=("Helvetica", 12), bg=bg_color, fg=text_color, wrap="word", height=20, width=70)
result_text.pack(pady=10)

# Добавление тегов для выделения
result_text.tag_config("unwanted", foreground="red")

# Создание метки с дополнительным текстом
additional_label = tk.Label(root, text="Анализатор переговоров РЖД", font=("Helvetica", 14), bg=bg_color, fg=text_color)
additional_label.pack(pady=5)

# Создание рамки для визуального элемента
visual_frame = tk.Frame(root, bg=bg_color)
visual_frame.pack(pady=5)

# Запуск главного цикла обработки событий
root.mainloop()
