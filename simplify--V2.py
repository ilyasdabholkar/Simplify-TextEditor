import tkinter as tk 
from tkinter import ttk 
from tkinter import font, colorchooser, filedialog, messagebox
import os 

master = tk.Tk()
master.geometry('1000x600')
master.iconbitmap('icon.ico')
master.title("Simplify -- Untitled")

################################ Right-Click-Menubar ###################################################

m = tk.Menu(master,tearoff=0)
m.add_command(label ="Cut",command=lambda:text_editor.event_generate("<Control x>"))
m.add_command(label ="Copy",command=lambda:text_editor.event_generate("<Control c>"))
m.add_command(label ="Paste",command=lambda:text_editor.event_generate("<Control v>"))
def do_popup(event):
    try:
        m.tk_popup(event.x_root,event.y_root)
    finally:
        m.grab_release()

master.bind("<Button-3>",do_popup)
############################################# MENUBAR ###################################################

font_properties = ('calibri',12)        
menubar = tk.Menu(master,font=font_properties)
master.config(menu=menubar)

#VARIABLE==============================================================
path = ""

file_data = [("All Files" , "*.*"),
                         ("Text Files" , "*.txt"),
                         ("Python Scripts" , "*.py"),
                         ("Markdown Documents" , "*.md"),
                         ("Javascripts Files" , "*.js"),
                         ("Html Document" , "*.html"),
                         ("CSS Document" , "*.css")]

def clear_text(*args):
        text_editor.delete(1.0 ,tk.END)

def set_window_title(name=None):
        if name:
            master.title(name + "      -- Simplify")
        else:
            master.title("Simplify -- Untitled")

#====File===================================================================
File = tk.Menu(menubar,font=font_properties ,tearoff=0)

#New File
def new_file():
    global path
    path = ""
    clear_text()
    set_window_title()

File.add_command(label="New",accelerator="Ctrl+N",command=new_file)

#Open File
def open_file(*args):
    global path
    path = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select File', filetypes=(file_data))
    try:
        with open(path, 'r') as fr:
            text_editor.delete(1.0, tk.END)
            text_editor.insert(1.0, fr.read())
    except FileNotFoundError:
        return 
    except:
        return 
    set_window_title(path)

File.add_command(label="Open" ,accelerator="Ctrl+O",command=open_file)

#Save file
def Save_file(event=None):
    global path 
    try:
        if path:
            content = str(text_editor.get(1.0, tk.END))
            with open(path, 'w', encoding='utf-8') as fw:
                fw.write(content)
            set_window_title(path)
        else:
            path = filedialog.asksaveasfile(mode = 'w', defaultextension='.txt', filetypes=(file_data))
            content2 = text_editor.get(1.0, tk.END)
            path.write(content2)
            path.close()
            set_window_title(path)
    except:
        return 

File.add_command(label="Save" ,accelerator="Ctrl+S",command=Save_file)

#SaveAs file
def Save_as(*args):
    global path 
    try:
        content = text_editor.get(1.0, tk.END)
        path = filedialog.asksaveasfile(mode = 'w', defaultextension='.txt', filetypes=(file_data))
        path.write(content)
        path.close()
        set_window_title(path)
    except:
        return 

File.add_command(label="Save as",accelerator="Ctrl+Shift+S",command=Save_as)

#Exit function
def exit_function(event=None):
    global path, text_modified
    try:
        if text_modified:
            mbox = messagebox.askyesno('Warning', 'Do you want to save the file ?')
            if mbox is True:
                if path:
                    content = text_editor.get(1.0, tk.END)
                    with open(path, 'w', encoding='utf-8') as fw:
                        fw.write(content)
                        master.destroy()
                else:
                    content2 = str(text_editor.get(1.0, tk.END))
                    path = filedialog.asksaveasfile(mode = 'w', defaultextension='.txt', filetypes=(file_data))
                    path.write(content2)
                    path.close()
                    master.destroy()
            elif mbox is False:
                master.destroy()
        else:
            master.destroy()
    except:
        return 
File.add_command(label="Exit" ,command=exit_function)

#====Edit===================================================================

#find function
def find_functionality(*args):
    def find():
        word_to_find = find_input.get()
        text_editor.tag_remove('match','1.0',tk.END)
        matches = 0
        if word_to_find:
            start_position = '1.0'
            while True:
                start_position = text_editor.search(word_to_find, start_position, stopindex=tk.END)
                if not start_position:
                    break
                end_position = f"{start_position}+{len(word_to_find)}c"
                text_editor.tag_add('match', start_position, end_position)
                matches += 1
                start_position = end_position
                text_editor.tag_config('match', foreground='red', background='yellow')
    
    def replace():
        word_to_find = find_input.get()
        word_to_replace = replace_input.get()
        content = text_editor.get(1.0, tk.END)
        new_content = content.replace(word_to_find,word_to_replace)
        text_editor.delete(1.0, tk.END)
        text_editor.insert(1.0, new_content)

    find_window = tk.Toplevel()
    find_window.title('Find')
    find_window.geometry('300x160+300+200')
    find_window.resizable(0,0)
    photo = tk.PhotoImage(file = 'icons/search.png')
    find_window.iconphoto(True,photo)
    ## frame 
    find_frame = ttk.LabelFrame(find_window, text='Find/Replace')
    find_frame.pack(pady=20)
    ## labels
    text_find_label = ttk.Label(find_frame, text='Find : ')
    text_replace_label = ttk.Label(find_frame, text= 'Replace')
    ## entry 
    find_input = ttk.Entry(find_frame, width=30)
    replace_input = ttk.Entry(find_frame, width=30)
    ## button 
    find_button = ttk.Button(find_window, text='Find',command=find)
    replace_button = ttk.Button(find_window, text= 'Replace',command=replace)
    ## label grid 
    text_find_label.grid(row=0, column=0, padx=4, pady=4)
    text_replace_label.grid(row=1, column=0, padx=4, pady=4)
    ## entry grid 
    find_input.grid(row=0, column=1, padx=4, pady=4)
    replace_input.grid(row=1, column=1, padx=4, pady=4)
    ## button grid 
    find_button.pack(pady=2,padx=50,side=tk.LEFT)
    replace_button.pack(side=tk.LEFT)
    #find_button.grid(row=2, column=0, padx=8, pady=4)
    #replace_button.grid(row=2, column=1, padx=8, pady=4)
    
    find_window.mainloop()
master.bind("<Control-f>", find_functionality)

Edit = tk.Menu(menubar,font=font_properties ,tearoff=0)
Edit.add_command(label="Copy" ,accelerator="Ctrl+C" ,command=lambda:text_editor.event_generate("<Control c>"))
Edit.add_command(label="Paste" ,accelerator="Ctrl+V" ,command=lambda:text_editor.event_generate("<Control v>"))
Edit.add_command(label="Cut" ,accelerator="Ctrl+X" ,command=lambda:text_editor.event_generate("<Control x>"))
Edit.add_command(label="Clear All" ,accelerator="Ctrl+Shift+X" ,command=clear_text)
Edit.add_command(label="Find" ,accelerator="Ctrl+F" ,command=find_functionality)

#====View===================================================================

show_toolbar = tk.BooleanVar()
show_toolbar.set(True)

def hide_toolbar():
    global show_toolbar
    if show_toolbar:
        toolbar.pack_forget()
        show_toolbar = False 
    else :
        text_editor.pack_forget()
        statusbar.pack_forget()
        toolbar.pack(side=tk.TOP, fill=tk.X)
        text_editor.pack(fill=tk.BOTH, expand=True)
        statusbar.pack(side=tk.BOTTOM)
        show_toolbar = True

View = tk.Menu(menubar,font=font_properties ,tearoff=0)
View.add_checkbutton(label='Hide Tool Bar',command=hide_toolbar)
        
#====Colour-Theme===========================================================
        
Theme = tk.Menu(menubar,font=font_properties ,tearoff=0)
theme_choice = tk.StringVar()
theme_dict = {
    'Light Default' : ('#000000','#ffffff'),
    'Dark' : ('#c4c4c4', '#2d2d2d'),
    'Blue' : ('#ededed','#6b9dc2')}
def change_theme():
    chosen_theme = theme_choice.get()
    color_tuple = theme_dict.get(chosen_theme)
    fg_color, bg_color = color_tuple[0], color_tuple[1]
    text_editor.config(background=bg_color, fg=fg_color) 
count = 0 
for i in theme_dict:
    Theme.add_radiobutton(label = i,variable=theme_choice,command=change_theme)
    count += 1 
#========Cascade================================================================

menubar.add_cascade(label="File", menu=File)
menubar.add_cascade(label="Edit", menu=Edit)
menubar.add_cascade(label="View", menu=View)
menubar.add_cascade(label="Theme", menu=Theme)

############################################## toolbar  #################################################

toolbar = tk.Label(master,bg='#f7f1e3')
toolbar.pack(side=tk.TOP,fill=tk.X)

## font box 
font_tuple = tk.font.families()
font_family = tk.StringVar()
font_box = ttk.Combobox(toolbar, width=30, textvariable=font_family, state='readonly')
font_box['values'] = font_tuple
font_box.current(font_tuple.index('Arial'))
font_box.grid(row=0, column=0, padx=5)

current_font_family = 'Arial'

def change_font(event=None):
    global current_font_family
    current_font_family = font_family.get()
    text_editor.configure(font=(current_font_family, current_font_size))

font_box.bind("<<ComboboxSelected>>", change_font)


## size box 
size_var = tk.IntVar()
font_size = ttk.Combobox(toolbar, width=14, textvariable = size_var, state='readonly')
font_size['values'] = tuple(range(8,81))
font_size.current(4)
font_size.grid(row=0, column=1, padx=5)

current_font_size = 12

def change_fontsize(event=None):
    global current_font_size
    current_font_size = size_var.get()
    text_editor.configure(font=(current_font_family, current_font_size))

font_size.bind("<<ComboboxSelected>>", change_fontsize)

#bold button
bold_icon = tk.PhotoImage(file='icons/font_bold.png')
bold_btn = ttk.Button(toolbar, image=bold_icon)
bold_btn.grid(row=0, column=2, padx=5)

def bold_function():
    current_text_properties = tk.font.Font(font=text_editor['font'])
    #print(tk.font.Font(font=text_editor['font']).actual())
    if current_text_properties.actual()['weight'] == 'normal':
        text_editor.configure(font=(current_font_family,current_font_size,'bold'))
    if current_text_properties.actual()['weight'] == 'bold':
        text_editor.configure(font=(current_font_family,current_font_size,'normal'))

bold_btn.configure(command=bold_function)

## italic button 
italic_icon = tk.PhotoImage(file='icons/font_italic.png')
italic_btn = ttk.Button(toolbar, image=italic_icon)
italic_btn.grid(row=0, column=3, padx=5)

def italic_function():
    current_text_properties = tk.font.Font(font=text_editor['font'])
    if current_text_properties.actual()['slant'] == 'roman':
        text_editor.configure(font=(current_font_family,current_font_size,'italic'))
    if current_text_properties.actual()['slant'] == 'italic':
        text_editor.configure(font=(current_font_family,current_font_size,'roman'))

italic_btn.configure(command=italic_function)

## underline button 
underline_icon = tk.PhotoImage(file='icons/font_underlined.png')
underline_btn = ttk.Button(toolbar, image = underline_icon)
underline_btn.grid(row = 0, column=4, padx=5)

def underline_function():
    current_text_properties = tk.font.Font(font=text_editor['font'])
    if current_text_properties.actual()['underline'] == 0:
        text_editor.configure(font=(current_font_family,current_font_size,'underline'))
    if current_text_properties.actual()['underline'] == 1:
        text_editor.configure(font=(current_font_family,current_font_size,'normal'))  

underline_btn.configure(command=underline_function)

## font color button 
font_color_icon = tk.PhotoImage(file='icons/font_color.png')
font_color_btn = ttk.Button(toolbar, image=font_color_icon)
font_color_btn.grid(row=0, column=5,padx=5)

def font_colour_function():
    colour_var = tk.colorchooser.askcolor()
    #print(colour_var)
    text_editor.configure(fg=colour_var[1])

font_color_btn.configure(command=font_colour_function)

## align left
align_left_icon = tk.PhotoImage(file='icons/align_left.png')
align_left_btn = ttk.Button(toolbar, image=align_left_icon)
align_left_btn.grid(row=0, column=6, padx=5)

def align_left_function():
    contents = text_editor.get(1.0,'end')
    text_editor.tag_config('left', justify=tk.LEFT)
    text_editor.delete(1.0, tk.END)
    text_editor.insert(tk.INSERT, contents , 'left')

align_left_btn.configure(command=align_left_function)

## align center 
align_center_icon = tk.PhotoImage(file='icons/align_justify.png')
align_center_btn = ttk.Button(toolbar, image=align_center_icon)
align_center_btn.grid(row=0, column=7, padx=5)

def align_center_function():
    contents = text_editor.get(1.0,'end')
    text_editor.tag_config('center', justify=tk.CENTER)
    text_editor.delete(1.0, tk.END)
    text_editor.insert(tk.INSERT, contents , 'center')

align_center_btn.configure(command=align_center_function)

## align right 
align_right_icon = tk.PhotoImage(file='icons/align_right.png')
align_right_btn = ttk.Button(toolbar, image=align_right_icon)
align_right_btn.grid(row=0, column=8, padx=5)

def align_right_function():
    contents = text_editor.get(1.0,'end')
    text_editor.tag_config('right', justify=tk.RIGHT)
    text_editor.delete(1.0, tk.END)
    text_editor.insert(tk.INSERT, contents , 'right')

align_right_btn.configure(command=align_right_function)
############################################## text editor #################################################

text_editor = tk.Text(master)
text_editor.config(wrap='word', relief=tk.FLAT)

#======setting_up_scrollbar_to_texteditor===================================================================

scroll_bar = tk.Scrollbar(master)
text_editor.focus_set()
scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
text_editor.pack(fill=tk.BOTH, expand=True)
scroll_bar.config(command=text_editor.yview)
text_editor.config(yscrollcommand=scroll_bar.set)

############################################## status bar ##################################################

statusbar = ttk.Label(master,text="STATUS BAR")
statusbar.pack(side=tk.BOTTOM)

text_modified = False
def status(*args):
    global text_modified
    #edit_modified method is used to look for changes
    if text_editor.edit_modified():
        text_modified = True
        words = len(text_editor.get(1.0,'end-1c').split())
        characters = len(text_editor.get(1.0,'end-1c'))
        statusbar.config(text=f"CHARACTERS : {characters} WORDS : {words}")
    text_editor.edit_modified(False)

#important bindings
text_editor.bind('<<Modified>>',status)
text_editor.bind('<Control-X>',clear_text)

master.mainloop()