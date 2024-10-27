import ollama
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText
from PIL import Image, ImageTk
import emoji
import time
import datetime


class ollama_stream():
    def __init__(self) -> None:
        self.model = 'llama3.2:3b'
        self.config_stream = True
        self.config_format = 'json'
        self.message = []
        self.chat_history = []

    
    def clean_chat_history(self):
        self.chat_history = []
    

    def get_answer(self, content):
        this_message = {
            'role': 'user',
            'content': content
        }

        self.chat_history.append(this_message)

        self.stream = ollama.chat(
            # format=self.config_format,
            model=self.model,
            messages=self.chat_history,
            # messages=self.message,
            stream=self.config_stream
        )

        answer = ''

        for chunk in self.stream:
            answer = answer + chunk['message']['content']
        
        answer = {
            'role': 'assistant',
            'content': answer
        }

        self.chat_history.append(answer)

        return answer


class application(ttk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.master=master
        self.place()
        self.stream = ollama_stream()
        self.theme_index = 0
        self.style_obj = ttk.Style('darkly')
        self.theme_names = self.style_obj.theme_names()
        self.create_main_frame()
        self.create_nav_frame()
        self.create_chat_frame()

    
    def reload_main_frame(self):
        self.frame_nav.destroy()
        self.create_main_frame()
        self.create_nav_frame()
        self.create_chat_frame()


    def create_main_frame(self):
        self.frame_main = ttk.Frame(self.master, width=800, height=600)
        self.frame_main.place(x=0, y=0)

        # self.style_obj.theme_use('darkly')


    def change_theme(self, event):
        theme_cbo_value = self.combox_theme_selector.get()
        self.style_obj.theme_use(theme_cbo_value)
        # theme_selected.configure(text=theme_cbo_value)
        self.combox_theme_selector.selection_clear()


    def get_theme_name(self):
        theme_list = ['darkly', 'vapor', 'cyborg', 'morph']
        if self.theme_index < 3:
            self.theme_index += 1
        else:
            self.theme_index = 0
        
        if self.theme_index == 3:
            # 浅色主题设置
            self.input_box.configure(foreground='black')
        else:
            self.input_box.configure(foreground='white')
        
        return theme_list[self.theme_index]


    def change_theme_click(self):
        self.style_obj.theme_use(self.get_theme_name())
        self.reload_main_frame()


    def create_nav_frame(self):
        self.frame_nav = ttk.Frame(self.frame_main, width=200, height=600)
        self.frame_nav.place(x=0, y=0)

        self.image_object = Image.open('./img/logo.png').resize((200, 200))
        self.logo = ImageTk.PhotoImage(self.image_object)
        self.label_logo = ttk.Label(self.frame_nav, image=self.logo)
        self.label_logo.place(x=0, y=5, width=200, height=200)

        self.s = ttk.Style()
        self.s.configure('my.TButton', font=('黑体', 12, 'bold'))

        self.button_reset = ttk.Button(self.frame_nav, text='重置对话', command=self.clean_chat, style='my.TButton')
        self.button_reset.place(x=5, y=215, width=190, height=40)

        self.button_reset = ttk.Button(self.frame_nav, text='切换主题', command=self.change_theme_click, style='my.TButton')
        self.button_reset.place(x=5, y=260, width=190, height=40)

        # self.label_style_selector = ttk.Label(self.frame_nav, text="选择主题:", bootstyle='success')
        # self.label_style_selector.place(x=5, y=250, width=90, height=40)

        # self.combox_theme_selector = ttk.Combobox(
        #         master=self.frame_nav,
        #         text=self.style_obj.theme.name,
        #         values=self.theme_names
        # )
        
        # self.combox_theme_selector.place(x=95, y=250, width=100, height=40)
        # self.combox_theme_selector.bind('<<ComboboxSelected>>', self.change_theme)

        self.label_time = ttk.Label(self.frame_nav, text='current_time')
        self.label_time.place(x=5, y=530, width=200)

        self.label_date = ttk.Label(self.frame_nav, text=time.strftime('%Y年%m月%d日'))
        self.label_date.place(x=5, y=570)

        self.label_time.configure(font=('黑体', 24, 'bold'), foreground='#d0f8f8')
        self.label_date.configure(font=('黑体', 14, 'bold'), foreground='#d0f8f8')

        self.update_datetime_label()
    

    def update_datetime_label(self):
        time_str = datetime.datetime.now().strftime('%H:%M:%S')
        self.label_time.configure(text=time_str)
        self.label_time.after(1000, self.update_datetime_label)
        

# ====================================================================================================
    __PLACEHOLDER = '开始对话吧！'

    def on_focus_in(self, entry, event=None):
        # 当Entry获得焦点时，提示信息消失
        self.input_box.configure(foreground='black')
        if self.theme_index != 3:
            # 浅色主题设置
            self.input_box.configure(foreground='white')
        if entry.get() == self.__PLACEHOLDER:
            entry.delete(0, END)

 
    def on_focus_out(self, entry, event=None):
        # 当Entry失去焦点且内容为空时，显示提示信息
        self.input_box.configure(foreground='grey')
        if not entry.get():
            entry.insert(0, self.__PLACEHOLDER)


    def clean_chat(self):
        self.stream.clean_chat_history()
        self.frame_chat_history.configure(state = 'normal')
        self.frame_chat_history.delete('1.0', END)
        self.frame_chat_history.configure(state = 'disable')
    

    def create_chat_frame(self):
        self.frame_chat_board = ttk.Frame(self.frame_main, width=600, height=600, bootstyle="info")
        self.frame_chat_board.place(x=200, y=0)

        self.frame_chat_history = ttk.ScrolledText(self.frame_chat_board, font=("黑体", 14))
        self.frame_chat_history.place(x=0, y=0, width=600, height=570, bordermode='inside')

        self.input_box = ttk.Entry(self.frame_chat_board)
        self.input_box.place(x=60, y=570, width=460)
        self.on_focus_out(self.input_box, "<FocusOut>")
        self.input_box.bind('<Return>', self.button_go_event)

        # 绑定焦点事件
        self.input_box.bind("<FocusIn>", lambda event: self.on_focus_in(self.input_box, event))
        self.input_box.bind("<FocusOut>", lambda event: self.on_focus_out(self.input_box, event))

        self.label_input = ttk.Label(self.frame_chat_board, text='  >>>', font=("楷体", 12), bootstyle='success')
        self.label_input.place(x=1, y=570, width=59, height=30)
        self.button_go = ttk.Button(self.frame_chat_board, text='Go!', command=self.button_go_event, style='my.TButton')
        self.button_go.place(x=520, y=570, width=80, height=30)
        

    def button_go_event(self, event=None):
        self.frame_chat_history.configure(state = 'normal')
        message = self.input_box.get()
        if len(self.stream.chat_history) == 0:
            self.frame_chat_history.insert(END, emoji.emojize('🧑 你:'))
            # self.frame_chat_history.tag_add("red", "1.0", "1.5")
            # self.frame_chat_history.tag_config("red", foreground="red")
        else:
            self.frame_chat_history.insert(END, emoji.emojize('\n🧑 你:'))
        self.frame_chat_history.insert(END, '\n')
        self.frame_chat_history.insert(END, '\n'+message)
        self.frame_chat_history.insert(END, '\n'+'========================================================'+'\n')
        
        answer = self.stream.get_answer(content=message)
        self.frame_chat_history.insert(END, emoji.emojize('\n🐒 Ollama:'))
        self.frame_chat_history.insert(END, '\n')
        self.frame_chat_history.insert(END, '\n'+answer['content'])

        self.frame_chat_history.insert(END, '\n'+'========================================================'+'\n')
        self.frame_chat_history.configure(state = 'disabled')

        self.frame_chat_history.yview_moveto(1)
        self.input_box.delete(0, END)


if __name__=='__main__':
    root = ttk.Window(alpha=0.9, iconphoto='./img/logo.png')
    root.geometry('800x600')
    root.title('OllamaPy')
    root.resizable(False, False)
    app=application(root)
    root.mainloop()