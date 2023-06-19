from tkinter import messagebox
import customtkinter as ctk
import tkinter as tk

from cryptography.fernet import Fernet
from PIL import Image

import cryptography.fernet
import webbrowser
import random
import time

APPEARANCE_MODE = 'light'
ctk.set_appearance_mode(APPEARANCE_MODE)
ctk.set_default_color_theme('blue')

PROJECT_NAME = 'Cryptography'
PROJECT_VERSION = '1.1.1'
SUBTEXTS = ['Free', 'Fast', 'Simple', 'Safe', 'Secure', 'Reliable', 'Efficient']


def changeMode(mode):
    global APPEARANCE_MODE
    ctk.set_appearance_mode(mode)
    APPEARANCE_MODE = mode


# noinspection PyTypeChecker,PyMethodMayBeStatic
class Client(ctk.CTkToplevel):
    def __init__(self, parent):
        ctk.CTkToplevel.__init__(self, parent)
        self.after(250, lambda: [self.lift(), self.iconbitmap('assets\\icon\\icon.ico')])

        self.title(f'{PROJECT_NAME} {PROJECT_VERSION}')
        self.resizable(False, False)

        # HEADER FRAME
        self.headerFrame = ctk.CTkFrame(self, corner_radius=0, fg_color='transparent')
        self.headerFrame.grid(row=0, column=3, sticky='nsew')

        self.sidebarToggleButton = ctk.CTkButton(self, text='', width=0, fg_color='transparent', hover=False,
                                                 image=ctk.CTkImage(
                                                     light_image=Image.open('assets\\textures\\menu_light.png'),
                                                     dark_image=Image.open('assets\\textures\\menu_dark.png')),
                                                 cursor='hand2', command=self.sidebar_event)
        self.sidebarToggleButton.grid(row=0, column=3, sticky='nw', padx=25, pady=5)

        self.sidebarFrame = ctk.CTkFrame(self, corner_radius=0)
        self.in_sidebarButton = ctk.CTkButton(self.sidebarFrame, text='', width=0, fg_color='transparent', hover=False,
                                              image=ctk.CTkImage(
                                                  light_image=Image.open('assets\\textures\\menu_light.png'),
                                                  dark_image=Image.open('assets\\textures\\menu_dark.png')),
                                              cursor='hand2',
                                              command=self.sidebar_event)

        self.homeButton = ctk.CTkButton(self.sidebarFrame, text='', width=0, fg_color='transparent', hover=False,
                                        image=ctk.CTkImage(
                                            light_image=Image.open('assets\\textures\\home_light.png'),
                                            dark_image=Image.open('assets\\textures\\home_dark.png')),
                                        cursor='hand2',
                                        command=self.returnHome)

        self.settingButton = ctk.CTkButton(self.sidebarFrame, text='', width=0, fg_color='transparent', hover=False,
                                           image=ctk.CTkImage(
                                               light_image=Image.open('assets\\textures\\setting_light.png'),
                                               dark_image=Image.open('assets\\textures\\setting_dark.png')),
                                           cursor='hand2')

        self.changeModeButton = ctk.CTkButton(self.sidebarFrame, text='', width=0, fg_color='transparent', hover=False,
                                              image=ctk.CTkImage(
                                                  light_image=Image.open('assets\\textures\\mode_light.png'),
                                                  dark_image=Image.open('assets\\textures\\mode_dark.png')),
                                              cursor='hand2', command=lambda: changeMode('dark' if APPEARANCE_MODE != 'dark' else 'light'))

        # HEADER FRAME
        self.headerFrame.grid_columnconfigure(5, weight=1)
        self.headerText = ctk.CTkLabel(self.headerFrame, text=f'{PROJECT_NAME}')
        self.headerText.cget('font').configure(weight='bold', size=25)
        self.headerText.grid(row=1, column=5, sticky='nsew', pady=15)

        # TAB-VIEW STUFF
        self.mainTabview = ctk.CTkTabview(self, corner_radius=10, width=500, command=self.focus)
        self.mainTabview.grid(row=5, column=3, padx=25, pady=25)

        self.encryptFrame = self.mainTabview.add('Encrypt')
        self.decryptFrame = self.mainTabview.add('Decrypt')

        self.encryptFrame.grid_columnconfigure((3, 4), weight=1)
        self.decryptFrame.grid_columnconfigure((3, 4), weight=1)

        # ENCRYPT FRAME
        ctk.CTkLabel(self.encryptFrame, text='Message:').grid(row=3, column=3, sticky='e', padx=(0, 15), pady=15)
        self.encryptEntry = ctk.CTkEntry(self.encryptFrame, placeholder_text='Your message...', width=375)
        self.encryptEntry.grid(row=3, column=4, pady=15, sticky='w')

        self.encryptButton = ctk.CTkButton(self.encryptFrame, text='Encrypt', cursor='hand2', command=self.encrypt)
        self.encryptButton.cget('font').configure(weight='bold')
        self.encryptButton.grid(row=5, column=3, columnspan=2)

        self.encryptedTokenMenu = tk.Menu(tearoff=0)
        self.encryptedTokenMenu.add_command(label='Copy token',
                                            command=lambda: self.copy_clipboard(self.encryptedTokenEntry.get()))

        self.encryptedMenu = tk.Menu(tearoff=0)
        self.encryptedMenu.add_command(label='Copy message',
                                       command=lambda: self.copy_clipboard(self.encryptedEntry.get()))

        ctk.CTkLabel(self.encryptFrame, text='Token:').grid(row=7, column=3, sticky='e', padx=(0, 15), pady=(30, 5))
        self.encryptedTokenEntry = ctk.CTkEntry(self.encryptFrame, fg_color=('gray90', '#343638'), state='disabled',
                                                width=375)
        self.encryptedTokenEntry.grid(row=7, column=4, sticky='w', pady=(30, 5))

        ctk.CTkLabel(self.encryptFrame, text='Message:').grid(row=9, column=3, sticky='e', padx=(0, 15))
        self.encryptedEntry = ctk.CTkEntry(self.encryptFrame, fg_color=('gray90', '#343638'), state='disabled',
                                           width=375)
        self.encryptedEntry.grid(row=9, column=4, sticky='w')

        # DECRYPT FRAME
        ctk.CTkLabel(self.decryptFrame, text='Message:').grid(row=3, column=3, pady=(15, 5), sticky='e', padx=(0, 15))
        self.decryptEntry = ctk.CTkEntry(self.decryptFrame, placeholder_text='Your encrypted message...', width=375)
        self.decryptEntry.grid(row=3, column=4, pady=(15, 3), sticky='w')

        ctk.CTkLabel(self.decryptFrame, text='Token:').grid(row=5, column=3, pady=(5, 15), sticky='e', padx=15)
        self.decryptKeyEntry = ctk.CTkEntry(self.decryptFrame, placeholder_text='Your token...', width=375)
        self.decryptKeyEntry.grid(row=5, column=4, pady=(5, 15), sticky='w')

        self.dencryptButton = ctk.CTkButton(self.decryptFrame, text='Decrypt', cursor='hand2', command=self.decrypt)
        self.dencryptButton.cget('font').configure(weight='bold')
        self.dencryptButton.grid(row=7, column=3, columnspan=2)

        ctk.CTkLabel(self.decryptFrame, text='Message:').grid(row=9, column=3, sticky='e', padx=(0, 15), pady=(30, 5))
        self.decryptedEntry = ctk.CTkEntry(self.decryptFrame, fg_color=('gray90', '#343638'), state='disabled',
                                           width=375)
        self.decryptedEntry.grid(row=9, column=4, sticky='w', pady=(30, 5))

        # BIND
        self.encryptedTokenEntry.bind('<Button-3>',
                                      lambda event: self.encryptedTokenMenu.tk_popup(event.x_root, event.y_root))
        self.encryptedEntry.bind('<Button-3>', lambda event: self.encryptedMenu.tk_popup(event.x_root, event.y_root))

        self.protocol('WM_DELETE_WINDOW', self.close)

    def close(self):
        askClose = messagebox.askyesnocancel('Warning',
                                             f'You\'re trying to close {PROJECT_NAME}. Would you like to return to the main hub instead?',
                                             icon='warning')
        if askClose:
            client.tryButton.configure(state='normal')
            client.deiconify()
            self.destroy()
        elif askClose is None:
            return
        else:
            client.destroy()
            quit()

    def returnHome(self):
        if messagebox.askyesno(f'{PROJECT_NAME} {PROJECT_VERSION}', 'Do you want to return back to the main hub?'):
            client.tryButton.configure(state='normal')
            client.deiconify()
            self.destroy()

    def sidebar_event(self):
        if self.sidebarFrame.winfo_viewable():
            # DISAPPEAR
            self.sidebarFrame.grid_forget()
            self.sidebarToggleButton.grid(row=0, column=3, sticky='nw', padx=25, pady=5)
        else:
            # APPEAR
            self.sidebarFrame.grid(row=0, rowspan=100, column=0, sticky='nsew')
            self.sidebarToggleButton.grid_forget()
            self.in_sidebarButton.grid(row=0, column=10)
            self.homeButton.grid(row=2, column=10, pady=5)
            ctk.CTkFrame(self.sidebarFrame, fg_color=['black', 'gray'], corner_radius=10, height=3, width=0).grid(row=3,
                                                                                                                  column=10,
                                                                                                                  sticky='ew',
                                                                                                                  pady=3,
                                                                                                                  padx=3)
            self.sidebarFrame.grid_rowconfigure(99, weight=1)
            self.changeModeButton.grid(row=100, column=10, sticky='s')
            self.settingButton.grid(row=101, column=10, sticky='s', pady=(5, 10))

    def copy_clipboard(self, item: str):
        self.clipboard_clear()
        self.clipboard_append(item)

    def encrypt(self):
        if self.encryptEntry.get().strip() == '':
            messagebox.showwarning('Warning', 'There\'s nothing to encrypt.\nPerhaps you forgot to add something?')
            return

        key = Fernet.generate_key()
        encrypted = Fernet(key).encrypt(bytes(self.encryptEntry.get(), 'utf-8')).decode('utf-8')

        self.encryptedTokenEntry.configure(state='normal')
        self.encryptedTokenEntry.delete(0, 'end')
        self.encryptedTokenEntry.insert(0, f'k&' + key.decode('utf-8'))
        self.encryptedTokenEntry.configure(state='disabled')

        self.encryptedEntry.configure(state='normal')
        self.encryptedEntry.delete(0, 'end')
        self.encryptedEntry.insert(0, f'm&' + encrypted)
        self.encryptedEntry.configure(state='disabled')

    def decrypt(self):
        if self.decryptKeyEntry.get().strip() != self.decryptEntry.get().strip() == '':
            messagebox.showwarning('Warning', 'Missing a message to decrypt.\nPerhaps you forgot to add it?')
            return
        elif self.decryptEntry.get().strip() != self.decryptKeyEntry.get().strip() == '':
            messagebox.showwarning('Warning', 'Missing a token (key) to decrypt.\nPerhaps you forgot to add it?')
            return
        elif self.decryptEntry.get().strip() == self.decryptKeyEntry.get().strip() == '':
            messagebox.showwarning('Warning',
                                   'Missing both message and token. Unable to decrypt.\nPerhaps you forgot to add it?')
            return

        key = self.decryptKeyEntry.get()
        message = self.decryptEntry.get()
        if key.startswith('k&'):
            key = key[2:]
        if message.startswith('m&'):
            message = message[2:]

        try:
            decrypted = Fernet(bytes(key, 'utf-8')).decrypt(bytes(message, 'utf-8'))
        except cryptography.fernet.InvalidToken:
            messagebox.showwarning('Warning',
                                   'Invalid decrypted message. Please make sure that your message is correct and valid.')
            return
        except ValueError:
            messagebox.showwarning('Warning', 'Invalid token. Please make sure that your token is correct and valid.')
            return

        self.decryptedEntry.configure(state='normal')
        self.decryptedEntry.delete(0, 'end')
        self.decryptedEntry.insert(0, decrypted)
        self.decryptedEntry.configure(state='disabled')


class Load(ctk.CTkToplevel):
    def __init__(self, parent):
        ctk.CTkToplevel.__init__(self, parent)
        self.after(250, lambda: [self.lift(), self.iconbitmap('assets\\textures\\transparent.ico')])

        self.title('Initialization')
        self.resizable(False, False)

        self.grid_columnconfigure(3, weight=1)

        self.mainProgressbar = ctk.CTkProgressBar(self, orientation='horizontal', mode='indeterminate', width=350)

        self.loadingText = ctk.CTkLabel(self, text='Initializing...')
        self.loadingText.grid(row=2, column=3, sticky='s', pady=(15, 5))
        self.loadingText.cget('font').configure(size=20, weight='bold')

        self.mainProgressbar.grid(row=3, column=3, sticky='ew', padx=15, pady=(0, 25))
        self.mainProgressbar.start()

        self.after(random.randint(3000, 7500), self.done)
        self.protocol('WM_DELETE_WINDOW', lambda: [self.destroy(), client.tryButton.configure(state='normal')])

    # noinspection PyMethodMayBeStatic
    def done(self):
        self.mainProgressbar.stop()
        self.mainProgressbar.configure(mode='determinate')
        self.mainProgressbar.set(1)
        self.after(random.randint(1000, 3000), lambda: [self.destroy(), client.withdraw(), Client(client)])


def tryit():
    Load(client)


# noinspection PyTypeChecker
class Application(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(f'{PROJECT_NAME} {PROJECT_VERSION}')
        # self.configure(background=ctk.CTkImage(Image.open('menu_light.png')))
        self.geometry('700x400')
        self.resizable(False, False)

        self.iconbitmap('assets\\icon\\icon.ico')

        self.changeModeHubButton = ctk.CTkButton(self, text='', width=0, fg_color='transparent',
                                                 hover=False,
                                                 image=ctk.CTkImage(
                                                     light_image=Image.open('assets\\textures\\mode_light.png'),
                                                     dark_image=Image.open('assets\\textures\\mode_dark.png')),
                                                 cursor='hand2', command=lambda: changeMode('dark' if APPEARANCE_MODE != 'dark' else 'light'))
        self.changeModeHubButton.grid(row=1, column=3, sticky='w', padx=5, pady=(3, 0))

        self.grid_columnconfigure(3, weight=1)
        self.headerText = ctk.CTkLabel(self, text=f'{PROJECT_NAME}', font=('Calibri', 50, 'bold'))
        self.headerText.grid(row=3, column=3, sticky='n', pady=(80, 0))

        self.subtitleMoveFrame = ctk.CTkFrame(self, fg_color='transparent')
        self.subtitleMoveFrame.grid(row=5, column=3, sticky='n')

        ctk.CTkLabel(self.subtitleMoveFrame, text='The', font=('Calibri', 30)).grid(row=3, column=3, padx=10, pady=10)
        ctk.CTkLabel(self.subtitleMoveFrame, text='encryption application', font=('Calibri', 30)).grid(row=3, column=5,
                                                                                                       padx=10, pady=10)

        self.current_subtext = 0
        self.current_index = 0
        self.subtitleText = ctk.CTkLabel(self.subtitleMoveFrame, text=SUBTEXTS[self.current_subtext],
                                         font=('Calibri', 30, 'bold'))
        self.subtitleText.grid(row=3, column=4, pady=10)
        self.after(1000, self.delete_subtitle_movement_event)

        self.tryButton = ctk.CTkButton(self, text='Try it now', cursor='hand2',
                                       command=lambda: [self.tryButton.configure(state='disabled'), tryit()])
        self.tryButton.cget('font').configure(size=20, weight='bold')
        self.tryButton.grid(row=7, column=3, ipadx=15, ipady=3, pady=20)

        self.grid_rowconfigure(99, weight=1)
        self.bottomFrame = ctk.CTkFrame(self, corner_radius=0, height=80)
        self.bottomFrame.grid(row=100, column=3, sticky='sew')

        self.bottomFrame.grid_columnconfigure(3, weight=1)
        self.authorLabel = ctk.CTkLabel(self.bottomFrame, text=f'{PROJECT_NAME} {time.strftime("%Y")}', cursor='hand2')
        self.authorLabel.cget('font').configure(weight='bold', size=17)

        self.authorLabel.bind('<Button-1>', lambda _: webbrowser.open('https://github.com/ItsHungg'))
        self.authorLabel.bind('<Button-2>',
                              lambda _: messagebox.showinfo('Hyperlink', 'Link: https://github.com/ItsHungg'))
        self.authorLabel.bind('<Enter>', lambda _: self.authorLabel.cget('font').configure(underline=True))
        self.authorLabel.bind('<Leave>', lambda _: self.authorLabel.cget('font').configure(underline=False))
        self.authorLabel.grid(row=3, column=3, pady=5)

    def add_subtitle_movement_event(self):
        if self.current_subtext >= len(SUBTEXTS):
            self.current_subtext = 0
        if len(self.subtitleText.cget('text')) == len(SUBTEXTS[self.current_subtext]):
            self.after(1000, self.delete_subtitle_movement_event)
            self.current_index = 0
            return
        self.current_index += 1
        self.subtitleText.configure(text=SUBTEXTS[self.current_subtext][:self.current_index])
        self.after(75, self.add_subtitle_movement_event)

    def delete_subtitle_movement_event(self):
        if self.subtitleText.cget('text').strip() == '':
            self.current_subtext += 1
            self.after(1000, self.add_subtitle_movement_event)
        else:
            self.subtitleText.configure(text=self.subtitleText.cget('text')[:-1])
            self.after(80, self.delete_subtitle_movement_event)


client = Application()
client.mainloop()
