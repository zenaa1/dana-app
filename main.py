from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import json, os

FILE_NAME = "data_dana.json"

def load_data():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(FILE_NAME, "w") as f:
        json.dump(data, f)

class MainLayout(BoxLayout):
    selected_index = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = load_data()
        self.refresh_list()

    def refresh_list(self):
        self.ids.list_container.clear_widgets()
        from kivy.uix.button import Button
        for i, item in enumerate(self.data):
            btn = Button(text=f"{item['nama']} - {item['nomor']}", size_hint_y=None, height=60)
            btn.bind(on_press=lambda x, idx=i: self.select_item(idx))
            self.ids.list_container.add_widget(btn)

    def select_item(self, index):
        self.selected_index = index
        item = self.data[index]
        self.ids.nama.text = item["nama"]
        self.ids.nomor.text = item["nomor"]

    def tambah(self):
        nama = self.ids.nama.text
        nomor = self.ids.nomor.text

        if not nama or not nomor:
            return

        self.data.append({"nama": nama, "nomor": nomor})
        save_data(self.data)
        self.refresh_list()

    def edit(self):
        if self.selected_index is None:
            return

        self.data[self.selected_index] = {
            "nama": self.ids.nama.text,
            "nomor": self.ids.nomor.text
        }
        save_data(self.data)
        self.refresh_list()

    def hapus(self):
        if self.selected_index is None:
            return

        self.data.pop(self.selected_index)
        save_data(self.data)
        self.refresh_list()

    def copy_nomor(self):
        if self.selected_index is None:
            return

        from kivy.core.clipboard import Clipboard
        Clipboard.copy(self.data[self.selected_index]["nomor"])


class DanaApp(App):
    def build(self):
        return MainLayout()

DanaApp().run()
