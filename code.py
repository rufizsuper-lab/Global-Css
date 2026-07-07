import json
import os
from datetime import datetime

FILE_NAME = "tasks.json"


class Task:
    def __init__(self, title, priority, completed=False, created=None):
        self.title = title
        self.priority = priority
        self.completed = completed
        self.created = created or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "title": self.title,
            "priority": self.priority,
            "completed": self.completed,
            "created": self.created,
        }

    @staticmethod
    def from_dict(data):
        return Task(
            data["title"],
            data["priority"],
            data["completed"],
            data["created"],
        )


class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load()

    def load(self):
        if not os.path.exists(FILE_NAME):
            return

        try:
            with open(FILE_NAME, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(x) for x in data]
        except Exception:
            self.tasks = []

    def save(self):
        with open(FILE_NAME, "w", encoding="utf-8") as f:
            json.dump(
                [t.to_dict() for t in self.tasks],
                f,
                ensure_ascii=False,
                indent=4,
            )

    def add_task(self):
        print("\nДобавление задачи")

        title = input("Название: ").strip()

        if not title:
            print("Название не может быть пустым.")
            return

        while True:
            priority = input("Приоритет (1-5): ").strip()

            if priority.isdigit():
                priority = int(priority)

                if 1 <= priority <= 5:
                    break

            print("Введите число от 1 до 5.")

        self.tasks.append(Task(title, priority))
        self.save()

        print("Задача добавлена.")

    def show_tasks(self):
        if not self.tasks:
            print("\nСписок пуст.")
            return

        print("\nСписок задач")

        for i, task in enumerate(self.tasks, start=1):
            status = "✓" if task.completed else " "
            print(
                f"{i:2}. [{status}] "
                f"{task.title} "
                f"(P:{task.priority}) "
                f"{task.created}"
            )

    def complete_task(self):
        self.show_tasks()

        if not self.tasks:
            return

        try:
            index = int(input("\nНомер задачи: ")) - 1

            if index < 0 or index >= len(self.tasks):
                raise ValueError

            self.tasks[index].completed = True
            self.save()

            print("Готово.")

        except ValueError:
            print("Некорректный номер.")

    def delete_task(self):
        self.show_tasks()

        if not self.tasks:
            return

        try:
            index = int(input("\nУдалить номер: ")) - 1

            if index < 0 or index >= len(self.tasks):
                raise ValueError

            removed = self.tasks.pop(index)

            self.save()

            print(f'Удалено: "{removed.title}"')

        except ValueError:
            print("Некорректный номер.")

    def search(self):
        text = input("\nПоиск: ").lower().strip()

        found = []

        for task in self.tasks:
            if text in task.title.lower():
                found.append(task)

        if not found:
            print("Ничего не найдено.")
            return

        print()

        for task in found:
            status = "✓" if task.completed else " "
            print(
                f"[{status}] "
                f"{task.title} "
                f"(P:{task.priority})"
            )

    def sort_priority(self):
        self.tasks.sort(key=lambda x: x.priority)
        self.save()

    def statistics(self):
        total = len(self.tasks)

        completed = len(
            [x for x in self.tasks if x.completed]
        )

        active = total - completed

        print("\nСтатистика")
        print("-" * 25)
        print(f"Всего задач : {total}") 

        if total:
            percent = completed / total * 100
            print(f"Прогресс    : {percent:.1f}%")

        priorities = {}

        for task in self.tasks:
            priorities.setdefault(task.priority, 0)
            priorities[task.priority] += 1

        print()

        for p in sorted(priorities):
            print(
                f"Приоритет {p}: "
                f"{priorities[p]}"
            )

    def clear_completed(self):
        before = len(self.tasks)

        self.tasks = [
            x
            for x in self.tasks
            if not x.completed
        ]

        removed = before - len(self.tasks)

        self.save()

        print(f"Удалено {removed} задач.")

    def menu(self):
        while True:
            print("\n" + "=" * 40)
            print("Менеджер задач")
            print("=" * 40)
            print("1. Показать задачи")
            print("2. Добавить задачу")
            print("3. Выполнить задачу")
            print("4. Удалить задачу")
            print("5. Поиск")
            print("6. Сортировка")
            print("7. Статистика")
            print("8. Очистить выполненные")
            print("0. Выход")

            choice = input("\nВыберите пункт: ").strip()

            if choice == "1":
                self.show_tasks()

            elif choice == "2":
                self.add_task()

            elif choice == "3":
                self.complete_task()

            elif choice == "4":
                self.delete_task()

            elif choice == "5":
                self.search()

            elif choice == "6":
                self.sort_priority()

            elif choice == "7":
                self.statistics()

            elif choice == "8":
                self.clear_completed()

            elif choice == "0":
                print("До свидания!")
                break

            else:
                print("Неизвестная команда.")


def main():
    manager = TaskManager()
    manager.menu()


if __name__ == "__main__":
    main()