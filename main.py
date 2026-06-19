import flet as ft
from config import WINDOW_TITLE
from db.main_db import init_db
from db.queries import add_item, get_all_items, update_item_status, delete_item

def main(page: ft.Page):
    page.title = WINDOW_TITLE
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO

    init_db()

    item_input = ft.TextField(hint_text="Что нужно купить?", expand=True)
    quantity_input = ft.TextField(hint_text="Кол-во", value="1", width=80, text_align=ft.TextAlign.CENTER)
    
    items_list_view = ft.ListView(expand=1, spacing=10, padding=20)

    def load_items():
        """Загружает элементы из БД и обновляет интерфейс"""
        items_list_view.controls.clear()
        
        for item_id, name, quantity, is_bought in get_all_items():
         
            text_style = ft.TextStyle(decoration=ft.TextDecoration.LINE_THROUGH) if is_bought else None
            
            item_row = ft.Row(
                controls=[
                    ft.Checkbox(
                        value=bool(is_bought),
                        on_change=lambda e, i_id=item_id: toggle_bought(e, i_id)
                    ),
                    ft.Container(
                        content=ft.Text(f"{name} ({quantity} шт.)", style=text_style, size=16),
                        expand=True
                    ),
                 
                    ft.Container(
                        content=ft.Text("❌", size=16),
                        on_click=lambda e, i_id=item_id: remove_item(e, i_id),
                        padding=10
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
            items_list_view.controls.append(item_row)
        
        page.update()

    def add_clicked(e):
        """Обработчик добавления нового товара"""
        if not item_input.value.strip():
            item_input.error_text = "Введите название"
            page.update()
            return
        
        try:
            qty = int(quantity_input.value)
            if qty <= 0:
                raise ValueError
        except ValueError:
            quantity_input.error_text = "Ошибка"
            page.update()
            return

        item_input.error_text = None
        quantity_input.error_text = None
        
        add_item(item_input.value, qty)
        
        item_input.value = ""
        quantity_input.value = "1"
        
        load_items()

    def toggle_bought(e, item_id):
        update_item_status(item_id, e.control.value)
        load_items()

    def remove_item(e, item_id):
        delete_item(item_id)
        load_items()

    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(WINDOW_TITLE, size=30, weight=ft.FontWeight.BOLD),
                    ft.Row(
                        controls=[
                            item_input,
                            quantity_input,
                            ft.ElevatedButton("ADD", on_click=add_clicked, bgcolor="blue500", color="white")
                        ]
                    ),
                    ft.Divider(),
                    items_list_view
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            width=500,
            padding=20
        )
    )

    load_items()

if __name__ == "__main__":
    ft.app(target=main)