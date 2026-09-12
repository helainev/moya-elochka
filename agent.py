import os
import subprocess
import ollama

# 1. ИНСТРУМЕНТЫ (Функции, которые агент выполняет на вашем ПК)

def rewrite_html_code(new_html_content):
    """Инструмент для полной перезаписи файла index.html"""
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(new_html_content)
    return "Файл index.html успешно обновлен локально."

def get_current_html():
    """Инструмент для чтения текущего кода сайта"""
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    return "Файл index.html не найден."

def run_git_push(commit_message):
    """Инструмент для автоматической отправки изменений на GitHub Pages"""
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        return "Изменения успешно закоммичены и отправлены на GitHub Pages!"
    except subprocess.CalledProcessError as e:
        return f"Ошибка при работе с Git: {str(e)}"

# 2. ГЛАВНАЯ ЛОГИКА АГЕНТА

def ask_agent(user_command):
    print(f"\n[Вы]: {user_command}")
    print("[Агент думает и выполняет задачу...]\n")
    
    current_code = get_current_html()
    
    system_prompt = f"""
    Ты — автономный ИИ-агент, управляющий кодом сайта ватных игрушек "Моя Ёлочка".
    Ты должен изменить HTML-код по требованию пользователя и вернуть ПОЛНЫЙ обновленный HTML-код.
    
    Текущий код сайта index.html:
    {current_code}
    
    ПРАВИЛА ИЗМЕНЕНИЯ КОДА:
    1. Всегда возвращай ПОЛНЫЙ код страницы, начиная с <!DOCTYPE html> и до самого конца. Не используй сокращения вроде '// ... остальной код'.
    2. Обязательно сохраняй весь новогодний стиль, Tailwind CSS, анимацию падающего снега и комментарий-инструкцию в самом начале файла.
    3. Твой ответ должен содержать только один блок кода в формате ```html ... ```. Без лишней болтовни на английском.
    """

    # Вызываем локальную модель через установленную библиотеку
    response = ollama.chat(
        model='qwen2.5-coder:7b',
        messages=[
            { 'role': 'system', 'content': system_prompt },
            { 'role': 'user', 'content': user_command }
        ]
    )
    
    text_response = response['message']['content']
    
    # Автоматически извлекаем сгенерированный код из ответа модели
    if "```html" in text_response:
        try:
            # Вырезаем код из разметки
            new_code = text_response.split("```html")[1].split("```")[0].strip()
            
            # Перезаписываем файл на диске
            rewrite_status = rewrite_html_code(new_code)
            print(f"[Система]: {rewrite_status}")
            
            # Автоматически отправляем на живой сайт в интернет!
            git_status = run_git_push(f"ИИ-Агент: {user_command[:50]}")
            print(f"[Система]: {git_status}")
            
        except Exception as e:
            print(f"[Ошибка агента]: Не удалось корректно сохранить код. {str(e)}")
    else:
        print("[Внимание]: Модель не вернула блок кода ```html. Файл не изменен.")
        print(f"[Ответ модели]: {text_response}")

# Пример запуска команды для агента:
if __name__ == "__main__":
    # Сюда пишите любую команду для вашего сайта на русском языке!
    # Например, давайте проверим, как он изменит ссылку на ВКонтакте:
    text_command = "Измени в контактах ссылку на ВКонтакте, поставь туда адрес: https://vk.com"
    
    ask_agent(text_command)
