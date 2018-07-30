#!/usr/bin/env python3

from tkinter import *
from tkinter import messagebox, ttk
from PIL import ImageTk, Image

from queue import Queue
from threading import Thread

from minervaboto import utils

import minervaboto

import os

mb = messagebox

default_font = ('verdana', 14)
default_pad = 5
default_relief = FLAT


class App:
    def __init__(self):
        self.queue = Queue()

        self.root = Tk()
        self.root.title('Renovação Minerva')
        self.root.resizable(False, False)
        self.root.bind('<Escape>', self.close)

        self.var_save_credentials = IntVar()

        main_frame = Frame(self.root)
        main_frame.pack(expand=True, fill=BOTH)

        logo_img = ImageTk.PhotoImage(Image.open('logo.png'))
        logo = Label(main_frame, image=logo_img, pady=default_pad)
        logo.pack()

        first_row = Frame(main_frame)
        first_row.pack(fill=X)

        id_label = Label(first_row, text='Id:', relief=default_relief)
        id_label.config(font=default_font)
        id_label.pack(side=LEFT, padx=default_pad, pady=default_pad)

        self.id_entry = Entry(first_row, validate='key')
        self.id_entry['validatecommand'] = (self.id_entry.register(
            self.validate_id),'%P','%d')
        self.id_entry.config(width=11, font=default_font)
        self.id_entry.pack(side=RIGHT, padx=default_pad)


        second_row = Frame(main_frame)
        second_row.pack(fill=X)

        pass_label = Label(second_row, text='Senha:', relief=default_relief)
        pass_label.config(font=default_font)
        pass_label.pack(side=LEFT, padx=default_pad, pady=default_pad)

        self.pass_entry = Entry(second_row)
        self.pass_entry.config(width=11, font=default_font, show="*")
        self.pass_entry.pack(side=RIGHT, padx=default_pad)
        self.pass_entry.bind('<Return>', self.renew_callback)

        third_row = Frame(main_frame)
        third_row.pack(fill=X)

        save_checkbox = Checkbutton(third_row, text='Salvar dados',
                                    variable=self.var_save_credentials)
        save_checkbox.config(font=default_font)
        save_checkbox.pack(side=LEFT, padx=default_pad, pady=default_pad)


        fourth_row = Frame(main_frame)
        fourth_row.pack(fill=X)

        self.renew_button = Button(fourth_row, text='Renovar',
                                   command=self.renew_callback)
        self.renew_button.config(font=default_font)
        self.renew_button.pack(side=RIGHT, padx=default_pad, pady=default_pad)
        self.renew_button.bind('<Return>', self.renew_callback)

        self.progress_row = Frame(main_frame)

        progressbar = ttk.Progressbar(self.progress_row, orient='horizontal',
                                      mode='indeterminate')
        progressbar.pack(expand=True, fill=X)
        progressbar.start(15)

        self.progress_status = Label(self.progress_row, relief=SUNKEN)
        self.progress_status.config(font=default_font)
        self.progress_status.pack(expand=True, fill=X)
        self.progress_status['text'] = ' '


        has_credentials = self.fill_credentials()
        self.var_save_credentials.set(has_credentials)

        if has_credentials:
            self.renew_button.focus_set()
        else:
            self.id_entry.focus_set()

        self.root.mainloop()

    def renew_callback(self, event=None):
        self.progress_row.pack(fill=X)

        RenewTask(self.queue, self.id_entry.get(), self.pass_entry.get()).start()
        self.root.after(15, self.wait_for_renewal)

    def wait_for_renewal(self):
        # NOTE(erick): Spin baby, spin!
        if self.queue.empty():
            self.root.after(15, self.wait_for_renewal)
            return

        self.renewal_done(self.queue.get(0))

    def renewal_done(self, renewed):
        self.progress_row.pack_forget()

        if renewed['result']:
            mb.showinfo('Renovação', minervaboto.renewed_to_string(renewed))
            self.save_credentials()
        else:
            if renewed['response']['code'] == 200:
                mb.showwarning('Renovação', minervaboto.renewed_to_string(renewed))
                self.save_credentials()
            else:
                mb.showerror('Renovação', minervaboto.renewed_to_string(renewed))


    def validate_id(self, input_str, action_type):
        if action_type == '1': #insert
            return input_str.isdigit()

        return True

    def fill_credentials(self):
        config_file = utils.get_default_config_file('minervaboto', 'boto.conf')
        if not os.path.exists(config_file): return False

        config = utils.read_config_file(config_file)
        user_id, user_pass = utils.get_info_from_config(config)

        if not (user_id and user_pass): return False

        self.id_entry.insert(0, user_id)
        self.pass_entry.insert(0, user_pass)

        return True
    def save_credentials(self):
        if not self.var_save_credentials.get(): return
        config_file = utils.get_default_config_file('minervaboto', 'boto.conf')
        config = utils.read_config_file(config_file)

        config['LOGIN']['MINERVA_ID'] = self.id_entry.get()
        config['LOGIN']['MINERVA_PASS'] = self.pass_entry.get()
        utils.write_config_file(config, config_file)

    def close(self, event=None):
        self.root.destroy()

class RenewTask(Thread):
    def __init__(self, queue, user_id, user_password):
        Thread.__init__(self)

        self.queue = queue
        self.user_id = user_id
        self.user_password = user_password
    def run(self):
        renewed = minervaboto.renew_books(self.user_id, self.user_password)
        self.queue.put(renewed)

app = App()
