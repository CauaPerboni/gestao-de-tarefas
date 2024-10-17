import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.core.text import LabelBase

LabelBase.register(name='Poppins', fn_regular='fonts/Poppins-Regular.ttf', fn_bold='fonts/Poppins-Bold.ttf')

Window.size = (400, 600)

class TaskManager(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.task_input = TextInput(
            hint_text="Digite uma tarefa", 
            size_hint=(0.8, None), 
            height=40, 
            pos_hint={'center_x': 0.5, 'top': 1},
            font_name='Poppins', 
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1) 
        )
        self.add_widget(self.task_input)

        self.priority_spinner = Spinner(
            text='Prioridade',
            values=('Baixa', 'Média', 'Alta'),
            size_hint=(0.3, None),
            height=40,
            pos_hint={'center_x': 0.5, 'top': 0.95},
            font_name='Poppins',
            background_color=(1, 1, 1, 1),
            color=(0, 0, 0, 1)
        )
        self.add_widget(self.priority_spinner)

        self.add_task_button = Button(
            text="Adicionar Tarefa", 
            size_hint=(0.8, None), 
            height=40, 
            pos_hint={'center_x': 0.5, 'top': 0.9},
            font_name='Poppins', 
            background_color=(0.2, 0.6, 0.2, 1),
            color=(1, 1, 1, 1) 
        )
        self.add_task_button.bind(on_press=self.add_task)
        self.add_widget(self.add_task_button)

        self.tasks_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.tasks_layout.bind(minimum_height=self.tasks_layout.setter('height'))

        self.scroll_view = ScrollView(size_hint=(1, 0.6), pos_hint={'center_x': 0.5, 'top': 0.75}) 
        self.scroll_view.add_widget(self.tasks_layout)
        self.add_widget(self.scroll_view)

        self.feedback_label = Label(size_hint_y=None, height=30, pos_hint={'center_x': 0.5, 'top': 0.7}, font_name='Poppins')
        self.add_widget(self.feedback_label)

        self.load_tasks()

    def priority_order(self, priority):
        if priority == 'Alta':
            return 3
        elif priority == 'Média':
            return 2
        elif priority == 'Baixa':
            return 1
        return 0

    def add_task(self, instance):
        task_text = self.task_input.text
        priority = self.priority_spinner.text
        if task_text and priority != 'Prioridade':
            task_layout = BoxLayout(size_hint_y=None, height=30, padding=(10, 5), spacing=10)

            task_checkbox = CheckBox(size_hint=(0.1, 1)) 
            task_layout.add_widget(task_checkbox)

            task_label = Label(text=f"{task_text} [{priority}]", size_hint=(0.7, None), height=30, font_name='Poppins', halign='left')
            task_label.bind(size=task_label.setter('text_size')) 
            task_layout.add_widget(task_label)

            
            remove_button = Button(text="Remover", size_hint=(0.2, None), height=30, font_name='Poppins') 
            remove_button.bind(on_press=lambda x: self.remove_task(task_layout))
            task_layout.add_widget(remove_button)

            
            self.tasks_layout.add_widget(task_layout)
            self.task_input.text = ""
            self.priority_spinner.text = 'Prioridade'
            self.save_tasks()

            self.sort_tasks()

    def sort_tasks(self):
        tasks = list(self.tasks_layout.children)
        
        tasks.sort(key=lambda x: self.priority_order(x.children[1].text.split('[')[-1].strip(']')), reverse=True)

        self.tasks_layout.clear_widgets()
        for task in tasks:
            self.tasks_layout.add_widget(task)

    def remove_task(self, task_layout):
        self.tasks_layout.remove_widget(task_layout)
        self.save_tasks()
        self.sort_tasks() 

    def save_tasks(self):
        tasks = []
        for task_layout in self.tasks_layout.children:
            task_label = task_layout.children[1].text 
            tasks.append(task_label)
        with open('tasks.json', 'w') as f:
            json.dump(tasks, f)

    def load_tasks(self):
        try:
            with open('tasks.json', 'r') as f:
                tasks = json.load(f)
                for task in tasks:
                    task_layout = BoxLayout(size_hint_y=None, height=30, padding=(10, 5), spacing=10)
                    task_checkbox = CheckBox(size_hint=(0.1, 1)) 
                    task_layout.add_widget(task_checkbox)
                    task_label = Label(text=task, size_hint=(0.7, None), height=30, font_name='Poppins', halign='left')
                    task_label.bind(size=task_label.setter('text_size'))
                    task_layout.add_widget(task_label)
                    remove_button = Button(text="Remover", size_hint=(0.2, None), height=30, font_name='Poppins') 
                    remove_button.bind(on_press=lambda x: self.remove_task(task_layout))
                    task_layout.add_widget(remove_button)
                    self.tasks_layout.add_widget(task_layout)
                self.sort_tasks()
        except FileNotFoundError:
            pass 


class TaskApp(App):
    def build(self):
        return TaskManager()


if __name__ == '__main__':
    TaskApp().run()
