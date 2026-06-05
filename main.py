import flet as ft 

def main_page(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.title = 'Мое первое приложение'

    text_hello = ft.Text(value='Hello world')

    greeting_history = []
    history_text = ft.Text(value='История приветствий:')


    def on_button_click(_):
        # print(name_input.value)

        if name_input.value:
            name = name_input.value.strip()
            text_hello.value = f'Hello {name}'
            name_input.value = None
            text_hello.color = None

            greeting_history.append(name)
            print(greeting_history)
            history_text.value = "История приветсвий:\n" + "\n".join(greeting_history)
        else: 
            text_hello.value = 'Введите имя!'
            text_hello.color = ft.Colors.RED

    name_input = ft.TextField(on_submit=on_button_click)
    button_elevated = ft.ElevatedButton('send', icon=ft.Icons.SEND, on_click=on_button_click)

    def clear_history(_):
        greeting_history.clear()
        history_text.value = "История приветсвий:"

    clear_button = ft.IconButton(icon=ft.Icons.DELETE, on_click=clear_history)

    page.add(text_hello, name_input, button_elevated, clear_button, history_text)

ft.run(main_page)