from tkinter import messagebox, filedialog
import customtkinter as ctk
import tkinter as tk

from cryptography.fernet import Fernet
from PIL import Image

import cryptography.fernet
import webbrowser
import platform
import random
import time

PROJECT_NAME = 'Cryptography'
PROJECT_VERSION = __version__ = '1.2.1'

if platform.system().strip().lower() != 'windows' or not any(k in platform.release().strip().lower() for k in ['10', '11']):
    if not messagebox.askyesno('Important Warning',
                               f'Many features here might be broken because your current Operating System is not supported, or outdated.\n\nInfo:\n - Operating System: {platform.system()}\n - Release: {platform.release()}\n - Version: {platform.version()}\n\nConfiguration required:\n - Operating System: Windows\n - Version/Release: 10 or above\n\nWould you like to continue using {PROJECT_NAME}?',
                               icon='warning', default='no'):
        quit()

with open('profile\\mode_config.txt', 'r') as md:
    APPEARANCE_MODE = md.read().strip()
with open('profile\\theme_config.txt', 'r') as th:
    THEME = th.read().strip()
with open('profile\\configs.txt', 'r') as cf:
    CONFIGS = cf.readlines()
ASK_RETURN = int(CONFIGS[0])

ctk.set_appearance_mode(APPEARANCE_MODE)
ctk.set_default_color_theme(THEME)

SUBTEXTS = ['Free', 'Fast', 'Simple', 'Safe', 'Secure', 'Reliable', 'Efficient']

client = False
main = False
settings = False


def changeMode(mode, save=False):
    global APPEARANCE_MODE
    ctk.set_appearance_mode(mode)
    APPEARANCE_MODE = mode
    if save:
        with open('profile\\mode_config.txt', 'w') as saveMode:
            saveMode.write(APPEARANCE_MODE.strip())
    if settings:
        settings.chooseModeMenu.set(APPEARANCE_MODE.capitalize())


# noinspection PyBroadException
def restart():
    global client
    client.destroy()

    time.sleep(1)
    client = Application()
    client.mainloop()


def askReturnHubConfig():
    global ASK_RETURN
    ASK_RETURN = 0 if ASK_RETURN else 1
    with open('profile\\configs.txt', 'r+') as cfread:
        config_lines = cfread.readlines()
        config_lines[0] = f'{ASK_RETURN}'
        cfread.seek(0)
        cfread.write('\n'.join(config_lines))


class CreateToolTip(object):
    def __init__(self, widget, text: str):
        self.waittime = 500  # miliseconds
        self.wraplength = 200  # pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, _):
        self.schedule()

    def leave(self, _):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self):
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                         background="#ffffff", relief='solid', borderwidth=1,
                         wraplength=self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()


# noinspection PyTypeChecker, PyMethodMayBeStatic
class Settings(ctk.CTkToplevel):
    def __init__(self, parent):
        global settings
        if settings:
            return
        settings = True

        ctk.CTkToplevel.__init__(self, parent)
        self.after(250, lambda: [self.lift(), self.iconbitmap('assets\\icon\\icon.ico')])

        self.title(f'Settings')
        self.resizable(False, False)

        # HEADER FRAME
        self.headerFrame = ctk.CTkFrame(self, corner_radius=0, fg_color='transparent')
        self.headerFrame.grid(row=3, column=3, sticky='nsew')

        self.headerFrame.grid_columnconfigure(3, weight=1)
        self.headerText = ctk.CTkLabel(self.headerFrame, text=f'Settings')
        self.headerText.cget('font').configure(weight='bold', size=23)
        self.headerText.grid(row=3, column=3, sticky='nsew', pady=(15, 10))

        ctk.CTkFrame(self.headerFrame, fg_color=('black', 'gray'), corner_radius=25, height=3, width=0).grid(row=5,
                                                                                                             column=3,
                                                                                                             sticky='ew',
                                                                                                             padx=5)

        self.themeFrame = ctk.CTkFrame(self, fg_color='transparent')
        self.themeFrame.grid(row=5, column=3, sticky='nsew', padx=15, pady=15)

        self.isThemeEditorOpened = False

        ctk.CTkLabel(self.themeFrame, text='Themes', font=('Calibri', 20, 'bold')).grid(row=1, column=3, pady=(0, 5),
                                                                                        columnspan=2)

        self.themeFrame.grid_columnconfigure((3, 4), weight=1)
        ctk.CTkLabel(self.themeFrame, text='Edit your theme:').grid(row=3, column=3, padx=10)
        self.chooseThemeButton = ctk.CTkButton(self.themeFrame, text='Theme Editor', width=100, cursor='hand2',
                                               command=self.themeEditor)
        self.chooseThemeButton.grid(row=3, column=4, padx=(0, 10))

        self.modeFrame = ctk.CTkFrame(self, fg_color='transparent')
        self.modeFrame.grid(row=7, column=3, sticky='nsew', padx=15, pady=(0, 15))

        ctk.CTkLabel(self.modeFrame, text='Mode', font=('Calibri', 20, 'bold')).grid(row=1, column=3, pady=(0, 5),
                                                                                     columnspan=2)

        self.modeFrame.grid_columnconfigure((3, 4), weight=1)
        ctk.CTkLabel(self.modeFrame, text='Choose your mode:').grid(row=3, column=3, padx=10)
        self.chooseModeMenu = ctk.CTkOptionMenu(self.modeFrame, values=['Light', 'Dark', 'System'], width=100,
                                                command=lambda _: changeMode(self.chooseModeMenu.get().lower(), True))
        self.chooseModeMenu.set(APPEARANCE_MODE.capitalize())
        self.chooseModeMenu.grid(row=3, column=4, padx=(0, 10))

        self.miscFrame = ctk.CTkFrame(self, fg_color='transparent')
        self.miscFrame.grid(row=11, column=3, sticky='nsew', padx=15, pady=(0, 15))

        self.miscFrame.grid_columnconfigure(3, weight=1)
        ctk.CTkLabel(self.miscFrame, text='Miscellaneous', font=('Calibri', 20, 'bold')).grid(row=1, column=3,
                                                                                              pady=(0, 5))
        self.askReturnMainHubSwitch = ctk.CTkSwitch(self.miscFrame, text='Return main hub', command=askReturnHubConfig)
        self.askReturnMainHubSwitch.select() if ASK_RETURN else None
        CreateToolTip(self.askReturnMainHubSwitch, text='Ask to return back to the main hub after closing the main window.')
        self.askReturnMainHubSwitch.grid(row=3, column=3)

        self.protocol('WM_DELETE_WINDOW', self.on_exit)

    def on_exit(self):
        global settings
        self.destroy()

        settings = False

    def themeEditor(self):
        if self.isThemeEditorOpened:
            return
        self.isThemeEditorOpened = True

        themeEditWindow = ctk.CTkToplevel(self)
        themeEditWindow.title('Theme Editor 1.0')
        themeEditWindow.resizable(False, False)

        self.after(100, themeEditWindow.lift)
        ctk.CTkLabel(themeEditWindow, text='Theme Editor', font=('Calibri', 25, 'bold')).grid(row=1, column=3,
                                                                                              columnspan=3, pady=15)

        # EDIT FRAME
        editFrame = ctk.CTkFrame(themeEditWindow)
        editFrame.grid(row=3, column=3, padx=(15, 7), pady=(5, 10), rowspan=5)

        ctk.CTkLabel(editFrame, text='Viewer:').grid(row=1, column=3, sticky='ew', pady=5)
        editValue = ctk.CTkTextbox(editFrame, height=250, wrap='word')
        editValue.insert('0.0', f'Welcome to Theme Editor!')
        editValue.grid(row=3, column=3, sticky='nsew', padx=15, pady=(0, 15))

        # PATH FRAME
        def validator(item):
            savePathButton.configure(state='normal', cursor='hand2')
            if item.strip() == '':
                savePathButton.configure(state='disabled', cursor='')
                return True
            elif item.count(':') > 1:
                return False
            elif any(k in item for k in '<>\"|?*'):
                return False
            return True

        def load_path():
            try:
                editValue.delete('0.0', 'end')
                if pathEntry.get().strip() != THEME:
                    saveThemeButton.configure(state='normal', cursor='hand2')
                else:
                    saveThemeButton.configure(state='disabled', cursor='')
                if pathEntry.get() in ['blue', 'dark-blue', 'green']:
                    editValue.insert('0.0', f'Default theme: {pathEntry.get()}')
                    return
                with open(pathEntry.get(), 'r') as json_data:
                    editValue.insert('0.0', json_data.read().strip())
            except FileNotFoundError:
                editValue.insert('0.0', 'Error: FileNotFound')
                saveThemeButton.configure(state='disabled', cursor='')
                messagebox.showerror('Error', f'Invalid theme path: \"{pathEntry.get()}\"')

        def openfile():
            # noinspection PyRedundantParentheses
            filename = filedialog.askopenfilename(title='Choose a theme', initialdir='\\',
                                                  filetypes=[('JSON files', '*.json')])
            if filename != '':
                pathEntry.delete(0, 'end')
                pathEntry.insert(0, filename)
                load_path()

        def saveTheme():
            # noinspection PyBroadException
            try:
                global THEME
                new_theme = pathEntry.get().strip()
                ctk.set_default_color_theme(new_theme)
                THEME = new_theme

                with open('profile\\theme_config.txt', 'w') as save_theme:
                    save_theme.write(new_theme)
            except:
                messagebox.showerror('Error', f'Something went wrong. Please try again.')
                return

            askRestart = messagebox.askyesnocancel('Warning',
                                                   f'You need to restart {PROJECT_NAME} to see the changes.\nDo you want to auto-restart now?\n\nWarning: An auto-restart may cause a lot of bugs. It\'s recommended to restart manually by reopening {PROJECT_NAME}.',
                                                   icon='warning')
            if askRestart:
                themeEditWindow.destroy()
                self.after(500, restart)
                return
            elif askRestart is None:
                return

            for child in [editValue, pathEntry, savePathButton, openPathButton, cancelButton]:
                child.configure(state='disabled')
            cancelButton.configure(fg_color='gray70')
            saveThemeButton.configure(text='Saved Theme', state='disabled', cursor='')
            self.after(1000, self.on_exit)

        pathFrame = ctk.CTkFrame(themeEditWindow)
        pathFrame.grid(row=3, column=5, sticky='n', padx=(7, 15), pady=10)

        savePathButton = ctk.CTkButton(pathFrame, text='Load', width=75, height=25, cursor='hand2', command=load_path)
        savePathButton.configure(state='disabled')
        savePathButton.grid(row=5, column=3, pady=(0, 15), padx=7, sticky='e')

        openPathButton = ctk.CTkButton(pathFrame, text='Open', width=75, height=25, cursor='hand2', command=openfile)
        openPathButton.grid(row=5, column=4, pady=(0, 15), padx=7, sticky='w')

        ctk.CTkLabel(pathFrame, text='Path (.json):').grid(row=1, column=3, sticky='ew', pady=5, columnspan=2)
        pathEntry = ctk.CTkEntry(pathFrame, width=175, validate='key', validatecommand=(self.register(validator), '%P'))
        pathEntry.insert(0, THEME)
        pathEntry.grid(row=3, column=3, sticky='nsew', padx=15, pady=(0, 10), columnspan=2)

        saveFrame = ctk.CTkFrame(themeEditWindow)
        saveFrame.grid(row=7, column=5, sticky='sew', padx=(7, 15), pady=10)

        saveThemeButton = ctk.CTkButton(saveFrame, text='Save Theme', width=125, state='disabled', command=saveTheme)
        saveThemeButton.grid(row=3, column=3, padx=(15, 5), pady=15)

        cancelButton = ctk.CTkButton(saveFrame, text='',
                                     image=ctk.CTkImage(Image.open('assets\\textures\\trashbin.png')), width=40,
                                     fg_color='#f52f2f', hover_color='#d62929', cursor='hand2',
                                     command=lambda: [saveThemeButton.configure(state='disabled', cursor=''),
                                                      editValue.delete('0.0', 'end'),
                                                      savePathButton.configure(state='disabled', cursor=''),
                                                      pathEntry.delete(0, 'end'), pathEntry.focus()])
        cancelButton.grid(row=3, column=5, sticky='e', pady=15, padx=(5, 15))

        def exitEditor():
            themeEditWindow.destroy()
            self.isThemeEditorOpened = False

        themeEditWindow.protocol('WM_DELETE_WINDOW', exitEditor)


# noinspection PyTypeChecker, PyMethodMayBeStatic
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
                                           cursor='hand2', command=self.settings)

        self.changeModeButton = ctk.CTkButton(self.sidebarFrame, text='', width=0, fg_color='transparent', hover=False,
                                              image=ctk.CTkImage(
                                                  light_image=Image.open('assets\\textures\\mode_light.png'),
                                                  dark_image=Image.open('assets\\textures\\mode_dark.png')),
                                              cursor='hand2', command=lambda: changeMode(
                'dark' if APPEARANCE_MODE != 'dark' else 'light'))

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
        self.encryptedTokenMenu.add_command(label='Clear token', command=lambda: [self.encryptedTokenEntry.configure(state='normal'), self.encryptedTokenEntry.delete(0, 'end'), self.encryptedTokenEntry.configure(state='disabled')])

        self.encryptedMenu = tk.Menu(tearoff=0)
        self.encryptedMenu.add_command(label='Copy message',
                                       command=lambda: self.copy_clipboard(self.encryptedEntry.get()))
        self.encryptedMenu.add_command(label='Clear message', command=lambda: [self.encryptedEntry.configure(state='normal'), self.encryptedEntry.delete(0, 'end'), self.encryptedEntry.configure(state='disabled')])

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
        if ASK_RETURN:
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
        else:
            client.destroy()
            quit()

    def returnHome(self):
        if messagebox.askyesno(f'{PROJECT_NAME} {PROJECT_VERSION}', 'Do you want to return back to the main hub?'):
            client.tryButton.configure(state='normal')
            client.deiconify()

            self.destroy()

    def settings(self):
        global settings
        settings = Settings(self)

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
            ctk.CTkFrame(self.sidebarFrame, fg_color=('black', 'gray'), corner_radius=10, height=3, width=0).grid(row=3,
                                                                                                                  column=10,
                                                                                                                  sticky='ew',
                                                                                                                  pady=3,
                                                                                                                  padx=3)
            self.sidebarFrame.grid_rowconfigure(99, weight=1)
            self.changeModeButton.grid(row=100, column=10, sticky='s')
            self.settingButton.grid(row=101, column=10, sticky='s', pady=(5, 10))

    def copy_clipboard(self, item: str):
        if item.strip() == '':
            if not messagebox.askyesno('Warning', 'The text you\'re about to copy is empty. Would you still like to copy?', icon='warning', default='no'):
                return
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

    def command(self):
        global main
        self.destroy()
        client.withdraw()
        main = Client(client)

    def done(self):
        self.mainProgressbar.stop()
        self.mainProgressbar.configure(mode='determinate')
        self.mainProgressbar.set(1)
        self.after(random.randint(1000, 3000), self.command)


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

        self.after_objects = set()

        self.iconbitmap('assets\\icon\\icon.ico')

        self.changeModeHubButton = ctk.CTkButton(self, text='', width=0, fg_color='transparent',
                                                 hover=False,
                                                 image=ctk.CTkImage(
                                                     light_image=Image.open('assets\\textures\\mode_light.png'),
                                                     dark_image=Image.open('assets\\textures\\mode_dark.png')),
                                                 cursor='hand2', command=lambda: changeMode(
                'dark' if APPEARANCE_MODE != 'dark' else 'light'))
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

        self.authorLabel.bind('<Button-1>', lambda _: webbrowser.open('https://sites.google.com/view/py-cryptography'))
        self.authorLabel.bind('<Button-2>',
                              lambda _: messagebox.showinfo('Hyperlink', 'Link: https://sites.google.com/view/py-cryptography'))
        self.authorLabel.bind('<Enter>', lambda _: self.authorLabel.cget('font').configure(underline=True))
        self.authorLabel.bind('<Leave>', lambda _: self.authorLabel.cget('font').configure(underline=False))
        self.authorLabel.grid(row=3, column=3, pady=5)

    def add_subtitle_movement_event(self):
        if self.current_subtext >= len(SUBTEXTS):
            self.current_subtext = 0
        if len(self.subtitleText.cget('text')) == len(SUBTEXTS[self.current_subtext]):
            self.after(1000, self.delete_subtitle_movement_event)
            # self.after_objects.add(self.after(1000, self.delete_subtitle_movement_event))
            self.current_index = 0
            return
        self.current_index += 1
        self.subtitleText.configure(text=SUBTEXTS[self.current_subtext][:self.current_index])
        self.after(75, self.add_subtitle_movement_event)
        # self.after_objects.add(self.after(75, self.add_subtitle_movement_event))

    def delete_subtitle_movement_event(self):
        if self.subtitleText.cget('text').strip() == '':
            self.current_subtext += 1
            self.after(1000, self.add_subtitle_movement_event)
            # self.after_objects.add(self.after(1000, self.add_subtitle_movement_event))
        else:
            self.subtitleText.configure(text=self.subtitleText.cget('text')[:-1])
            self.after(75, self.delete_subtitle_movement_event)
            # self.after_objects.add(self.after(75, self.delete_subtitle_movement_event))


client = Application()
client.mainloop()
