# Import system modules for path manipulation
import sys
import os
# Добавляем путь к модулю
module_path = os.path.join(os.path.dirname(__file__), 'Generate_instruction', 'GenAI-1-39')
sys.path.append(module_path)
from using_ollama import ask_ollama

def generate_video_script(topic):
    """
    Генерирует сценарий видео по заданной теме
    
    1. Получает тему видео
    2. Генерирует сценарий: вступление, обзор, заключение  
    3. Добавляет реплики ведущего
    4. Ограничивает 300 слов
    5. Сохраняет как markdown
    """
    
    prompt = f"""
Создай подробный сценарий для YouTube видео на тему: "{topic}"
Структура сценария:
1.Вступление
2.Обзор  
3.Заключение

Строгие требования:
- Разбей фразу на реплики
- Все реплики в формате: **Ведущий**: "Текст реплики"
- Не добавляй пояснений или описаний действий между репликами.
- Общий объем: менее 300 слов.
- Стиль: дружелюбный, профессиональный.

"""
    
    # Генерация через Ollama
    try:
        print("Пытаюсь сгенерировать через Ollama...")
        script = ask_ollama(prompt)
        if(len(script.split()) > 350):
            script = ask_ollama(prompt)
        return format_as_markdown(script, topic)
        
    except Exception as e:
        print(f"Ollama не доступен: {e}")
        exit()

def is_script_quality_good(script):
    """Проверяет качество сгенерированного сценария"""
    if not script or len(script.strip()) < 100:
        return False
    
    # Проверяем наличие ключевых разделов
    required_elements = ["вступление", "обзор", "заключение", "ведущий"]
    found_elements = sum(1 for element in required_elements if element.lower() in script.lower())
    
    return found_elements >= 3

def format_as_markdown(script, topic):
    """Форматирует сценарий в markdown"""
    markdown_content = f"""# Сценарий видео: {topic}

{script}

---
*Сгенерировано автоматически*
*Примерный объем: {count_words(script)} слов*
"""
    return markdown_content

def count_words(text):
    """Подсчитывает количество слов в тексте"""
    return len(text.split())


def save_markdown_file(content, topic):
    """Сохраняет сценарий в markdown файл"""
    filename = f"{topic.replace(' ', '_').lower()}_сценарий.md"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        return filename
    except Exception as e:
        print(f"Ошибка сохранения: {e}")
        return None

def main():
    """Основная функция программы"""
    print("=== Генератор сценариев для видео ===")
    
    # Получаем тему видео
    topic = input("Введите тему видео (например: 'обзор смартфона', 'рецепт пиццы'): ").strip()
    while not topic:
        print("Тема не может быть пустой!")
        topic = input("Введите тему видео: ").strip()
    
    print(f"\nГенерирую сценарий для темы: '{topic}'")
    print("Это может занять некоторое время...")
    
    # Генерируем сценарий
    script = generate_video_script(topic)

    print("\n" + "="*50)
    print("ГОТОВЫЙ СЦЕНАРИЙ:")
    print("="*50)
    print(script)
    
    # Сохраняем в файл
    filename = save_markdown_file(script, topic)
    if filename:
        print(f"\nСценарий сохранен в файл: {filename}")

if __name__ == "__main__":
    main()