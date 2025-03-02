import pytest
from src.task_manager import TaskManager
from src.task import Task
from database.DB import create_connection
'''
ПОСЛЕ ИСПОЛЬЗОВАНИЯ ВСЯ БД БУДЕТ ОЧИЩЕНА
'''
@pytest.fixture(scope="function")
def setup_database():
    conn = create_connection()
    conn.execute("DELETE FROM taskdb")  # ОЧИСТКА БД
    conn.commit()
    yield conn
    conn.close()
@pytest.fixture
def task_manager():
    return TaskManager()
def test_create_task(task_manager, setup_database):
    task = task_manager.create_task("Тестовая задача", "Это тестовая задача", "2025-12-31 12:00:00", "низкий", "работа")
    assert task.id is not None
    assert task.title == "Тестовая задача" # Проверка что название задачи корректно

def test_update_task(task_manager, setup_database):
    task = task_manager.create_task("Задача для обновления", "Данная задача будет обновлена", "2025-12-31 12:00:00", "средний", "учеба")
    task_manager.update_task(task.id, title="Обновленная задача", description="Обновленное описание")

    updated_task = task_manager.tasks_dict[task.id]  # Получаем обновку задачу
    assert updated_task.title == "Обновленная задача"  # Проверка что название обновлено
    assert updated_task.description == "Обновленное описание"  # Проверкв что описание обновлено

def test_delete_task(task_manager, setup_database):
    task = task_manager.create_task("Задача для удаления", "Данная задача будет удалена", "2025-12-31 12:00:00", "высокий", "личное")
    task_manager.delete_task(task.id)
    assert task_manager.tasks_dict.get(task.id) is None  # Ghjdthrf что задача удалена

def test_load_tasks(task_manager, setup_database):
    task_manager.create_task("Задача 1", "Описание 1", "2025-12-31 12:00:00", "низкий", "работа")
    task_manager.create_task("Задача 2", "Описание 2", "2025-12-31 12:00:00", "средний", "учеба")

    tasks = task_manager.get_all_tasks()
    assert len(tasks) == 2

def test_search_tasks(task_manager, setup_database):
    task_manager.create_task("Искомая задача", "Данная задача будет найдена", "2025-12-31 12:00:00", "низкий", "работа")
    task_manager.create_task("Другая задача", "Эта не подходит", "2025-12-31 12:00:00", "высокий", "личное")

    results = task_manager.search_task("Искомая")
    assert len(results) == 1
    assert results[0].title == "Искомая задача"  # Проверка что это правильная задача

def test_search_task_cp(task_manager, setup_database):

    task_manager.create_task("Задача с высоким приоритетом", "Почему не низкий??", "2025-12-31 12:00:00", "высокий", "работа")
    task_manager.create_task("Задача с низким приорит.", "ыфвывыфвычяс", "2025-12-31 12:00:00", "низкий", "учеба")

    results = task_manager.search_task_cp("высокий")
    assert len(results) == 1
    assert results[0].title == "Задача с высоким приоритетом"  # Проверка что это правильная задача