#!/usr/bin/env python3
"""
Простое приложение для управления задачами (To-Do List)
Функциональность:
- Добавление задач
- Просмотр всех задач
- Отметка задач как выполненных
- Удаление задач
- Сохранение в файл
"""

import json
import os
from datetime import datetime


class TodoApp:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        """Загрузка задач из файла"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    self.tasks = json.load(f)
                print(f"✓ Загружено {len(self.tasks)} задач(и)")
            except (json.JSONDecodeError, IOError):
                print("⚠ Не удалось загрузить файл задач, начинаем с пустого списка")
                self.tasks = []
        else:
            print("ℹ Новый список задач создан")

    def save_tasks(self):
        """Сохранение задач в файл"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.tasks, f, ensure_ascii=False, indent=2)
            print("✓ Задачи сохранены")
        except IOError as e:
            print(f"✗ Ошибка сохранения: {e}")

    def add_task(self, title, description=""):
        """Добавление новой задачи"""
        task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "description": description,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "completed": False
        }
        self.tasks.append(task)
        print(f"✓ Задача #{task['id']} добавлена: {title}")
        return task

    def view_tasks(self, show_completed=True):
        """Просмотр задач"""
        if not self.tasks:
            print("ℹ Список задач пуст")
            return

        filtered_tasks = self.tasks if show_completed else [t for t in self.tasks if not t['completed']]
        
        if not filtered_tasks:
            print("ℹ Нет задач для отображения")
            return

        print("\n" + "=" * 60)
        print(f"{'ID':<5} {'Статус':<8} {'Название':<30} {'Дата создания':<20}")
        print("=" * 60)
        
        for task in filtered_tasks:
            status = "✓" if task['completed'] else "○"
            title = task['title'][:28] + ".." if len(task['title']) > 30 else task['title']
            print(f"{task['id']:<5} {status:<8} {title:<30} {task['created_at']:<20}")
        
        print("=" * 60)
        print(f"Всего задач: {len(filtered_tasks)}")
        if not show_completed:
            print(f"(скрыто выполненных: {len(self.tasks) - len(filtered_tasks)})")
        print()

    def complete_task(self, task_id):
        """Отметка задачи как выполненной"""
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = True
                task['completed_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"✓ Задача #{task_id} отмечена как выполненная")
                return True
        print(f"✗ Задача #{task_id} не найдена")
        return False

    def delete_task(self, task_id):
        """Удаление задачи"""
        for i, task in enumerate(self.tasks):
            if task['id'] == task_id:
                deleted = self.tasks.pop(i)
                # Перенумеруем оставшиеся задачи
                for j, t in enumerate(self.tasks, 1):
                    t['id'] = j
                print(f"✓ Задача #{task_id} удалена: {deleted['title']}")
                return True
        print(f"✗ Задача #{task_id} не найдена")
        return False

    def clear_completed(self):
        """Удаление всех выполненных задач"""
        completed_count = sum(1 for t in self.tasks if t['completed'])
        self.tasks = [t for t in self.tasks if not t['completed']]
        # Перенумеруем оставшиеся задачи
        for i, t in enumerate(self.tasks, 1):
            t['id'] = i
        print(f"✓ Удалено {completed_count} выполненных задач(и)")

    def menu(self):
        """Отображение меню"""
        print("\n" + "=" * 40)
        print("       МЕНЕДЖЕР ЗАДАЧ")
        print("=" * 40)
        print("1. Добавить задачу")
        print("2. Показать все задачи")
        print("3. Показать активные задачи")
        print("4. Отметить задачу выполненной")
        print("5. Удалить задачу")
        print("6. Очистить выполненные задачи")
        print("7. Сохранить и выйти")
        print("8. Выход без сохранения")
        print("=" * 40)

    def run(self):
        """Основной цикл приложения"""
        print("\n🎯 Добро пожаловать в Менеджер Задач!")
        
        while True:
            self.menu()
            choice = input("\nВыберите действие (1-8): ").strip()

            if choice == '1':
                title = input("Введите название задачи: ").strip()
                if title:
                    description = input("Введите описание (необязательно): ").strip()
                    self.add_task(title, description)
                else:
                    print("✗ Название задачи не может быть пустым")

            elif choice == '2':
                self.view_tasks(show_completed=True)

            elif choice == '3':
                self.view_tasks(show_completed=False)

            elif choice == '4':
                try:
                    task_id = int(input("Введите ID задачи для завершения: "))
                    self.complete_task(task_id)
                except ValueError:
                    print("✗ Введите корректный номер")

            elif choice == '5':
                try:
                    task_id = int(input("Введите ID задачи для удаления: "))
                    self.delete_task(task_id)
                except ValueError:
                    print("✗ Введите корректный номер")

            elif choice == '6':
                confirm = input("Вы уверены? (y/n): ").strip().lower()
                if confirm == 'y':
                    self.clear_completed()

            elif choice == '7':
                self.save_tasks()
                print("👋 До свидания!")
                break

            elif choice == '8':
                confirm = input("Изменения не будут сохранены. Выйти? (y/n): ").strip().lower()
                if confirm == 'y':
                    print("👋 До свидания!")
                    break

            else:
                print("✗ Неверный выбор, попробуйте снова")


if __name__ == "__main__":
    app = TodoApp()
    app.run()
