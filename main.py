import flet as ft
from db.main_db import main_db  # Исправленный импорт

PRIORITY_COLORS = {
    'high':   ft.Colors.RED_400,
    'medium': ft.Colors.AMBER_400,
    'low':    ft.Colors.GREEN_400,
}

PRIORITY_LABELS = {
    'high':   'High',
    'medium': 'Medium',
    'low':    'Low',
}


def priority_options():
    return [
        ft.DropdownOption(
            key=key,
            text=PRIORITY_LABELS[key],
            content=ft.Text(PRIORITY_LABELS[key], color=PRIORITY_COLORS[key], weight=ft.FontWeight.BOLD),
        )
        for key in ('high', 'medium', 'low')
    ]


def main_page(page: ft.Page):
    page.title = 'ToDo List'
    page.theme_mode = ft.ThemeMode.LIGHT

    task_list = ft.Column(spacing=20, scroll=ft.ScrollMode.AUTO, expand=True)
    filter_type = 'all'

    def load_tasks():
        task_list.controls.clear()
        for task_id, task, completed, priority in main_db.get_tasks(filter_type):
            task_list.controls.append(
                view_task(task_id=task_id, task_text=task, completed=completed, priority=priority)
            )
        page.update()

    def view_task(task_id, task_text, completed=None, priority='medium'):
        task_field = ft.TextField(value=task_text, expand=True, read_only=True)

        checkbox = ft.Checkbox(
            value=bool(completed),
            on_change=lambda e: toggle_task(task_id, e.control.value),
        )

        priority_dropdown = ft.Dropdown(
            value=priority,
            width=140,
            options=priority_options(),
            on_select=lambda e: change_priority(task_id, e.control.value),
        )

        def change_priority(t_id, new_priority):
            main_db.update_task(task_id=t_id, priority=new_priority)
            page.update()

        def save_edit(_):
            main_db.update_task(task_id=task_id, new_task=task_field.value)
            task_field.read_only = True
            page.update()

        def enable_edit(_):
            task_field.read_only = not task_field.read_only
            page.update()

        save_button = ft.IconButton(icon=ft.Icons.SAVE, on_click=save_edit)
        edit_button = ft.IconButton(icon=ft.Icons.EDIT, on_click=enable_edit)

        return ft.Row([
            checkbox,
            priority_dropdown,
            task_field,
            edit_button,
            save_button,
        ])

    def toggle_task(task_id, is_completed):
        main_db.update_task(task_id=task_id, completed=int(is_completed))
        page.update()

    def add_task_flet(_):
        if task_input.value:
            task_text = task_input.value.strip()
            selected_priority = priority_select.value or 'medium'
            task_id = main_db.add_task(task=task_text, priority=selected_priority)
            task_input.value = None
            task_list.controls.append(
                view_task(task_id=task_id, task_text=task_text, priority=selected_priority)
            )
            page.update()

    # Логика для кнопки очистки
    def clear_completed_flet(_):
        main_db.delete_completed_tasks()
        load_tasks()

    task_input = ft.TextField(label='Введите задачу', on_submit=add_task_flet, expand=True)

    priority_select = ft.Dropdown(
        value='medium',
        width=150,
        options=priority_options(),
    )

    add_button = ft.IconButton(icon=ft.Icons.ADD_CIRCLE, on_click=add_task_flet)

    input_row = ft.Row([task_input, priority_select, add_button])

    def set_filter(filter_value):
        nonlocal filter_type
        filter_type = filter_value
        load_tasks()

    # Кнопки фильтрации + кнопка очистки выполненных
    filter_buttons = ft.Row([
        ft.ElevatedButton('Все задачи',  on_click=lambda e: set_filter('all')),
        ft.ElevatedButton('В работе',    on_click=lambda e: set_filter('uncompleted')),
        ft.ElevatedButton('Готово ✅',   on_click=lambda e: set_filter('completed')),
        ft.OutlinedButton('Очистить выполненные 🗑️', on_click=clear_completed_flet, icon=ft.Icons.DELETE_OUTLINE),
    ], alignment=ft.MainAxisAlignment.SPACE_AROUND)

    page.add(input_row, filter_buttons, task_list)
    load_tasks()


if __name__ == '__main__':
    main_db.init_db()
    ft.app(main_page)