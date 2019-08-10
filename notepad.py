# -*- coding: utf-8 -*-
# @Time    : 2019/5/1
# @Author  : water66
# @Site    :
# @File    : notepad.py
# @Version : 1.0
# @Python Version : 3.6
# @Software: PyCharm


from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter import scrolledtext
import os

filename=''


def author():
    showinfo(title="作者", message="water66")


def power():
    showinfo(title="版权信息", message="water66")


def new_file(*args):
    global top, filename, textPad
    top.title("未命名文件")
    filename = None
    textPad.delete(1.0, END)


def open_file(*args):
    global filename
    filename = askopenfilename(defaultextension=".txt")
    if filename == "":
        filename = None
    else:
        top.title(""+os.path.basename(filename))
        textPad.delete(1.0, END)
        f = open(filename, 'r', encoding="utf-8")
        textPad.insert(1.0, f.read())
        f.close()


def click_open(event):
    global filename
    top.title("" + os.path.basename(filename))
    textPad.delete(1.0, END)
    f = open(filename, 'r', encoding="utf-8")
    textPad.insert(1.0, f.read())
    f.close()


def save(*args):
    global filename
    try:
        f=open(filename, 'w', encoding="utf-8")
        msg=textPad.get(1.0, 'end')
        f.write(msg)
        f.close()
    except:
        save_as()


def save_as(*args):
    global filename
    f = asksaveasfilename(initialfile="未命名.txt", defaultextension=".txt")
    filename = f
    fh = open(f, 'w', encoding="utf-8")
    msg = textPad.get(1.0, END)
    fh.write(msg)
    fh.close()
    top.title(""+os.path.basename(f))


def rename(newname):
    global filename
    name = os.path.basename(os.path.splitext(filename)[0])
    oldpath = filename
    newpath = os.path.dirname(oldpath)+'/'+newname+'.txt'
    os.rename(oldpath, newpath)
    filename = newpath
    refresh()
        
        
def rename_file(*args):
    global filename
    t = Toplevel()
    t.geometry("260x80+200+250")
    t.title('重命名')
    frame = Frame(t)
    frame.pack(fill=X)
    lable = Label(frame, text="文件名")
    lable.pack(side=LEFT, padx=5)
    var = StringVar()
    e1 = Entry(frame, textvariable=var)
    e1.pack(expand=YES, fill=X, side=RIGHT)
    botton = Button(t, text="确定", command=lambda: rename(var.get()))
    botton.pack(side=BOTTOM, pady=10)


def delete(*args):
    global filename, top
    choice = askokcancel('提示', '要执行此操作吗')
    if choice:
        if os.path.exists(filename):
            os.remove(filename)
            textPad.delete(1.0, END)
            top.title("记事本")
            filename = ''


def cut():
    global textPad
    textPad.event_generate("<<Cut>>")


def copy():
    global textPad
    textPad.event_generate("<<Copy>>")


def paste():
    global textPad
    textPad.event_generate("<<Paste>>")


def undo():
    global textPad
    textPad.event_generate("<<Undo>>")


def redo():
    global textPad
    textPad.event_generate("<<Redo>>")


def select_all():
    global textPad
    textPad.tag_add("sel", "1.0", "end")


def find(*agrs):
    global textPad
    t = Toplevel(top)
    t.title("查找")
    t.geometry("260x60+200+250")
    t.transient(top)
    Label(t, text="查找：").grid(row=0, column=0, sticky="e")
    v = StringVar()
    e = Entry(t, width=20, textvariable=v)
    e.grid(row=0, column=1, padx=2, pady=2, sticky="we")
    e.focus_set()
    c = IntVar()
    Checkbutton(t, text="不区分大小写", variable=c).grid(row=1, column=1, sticky='e')
    Button(t, text="查找所有", command=lambda: search(v.get(), c.get(), textPad, t, e)).grid\
        (row=0, column=2, sticky="e"+"w", padx=2, pady=2)
    
    def close_search():
        textPad.tag_remove("match", "1.0", END)
        t.destroy()
    t.protocol("WM_DELETE_WINDOW", close_search)


def mypopup(event):
    global editmenu
    editmenu.tk_popup(event.x_root, event.y_root)


def search(needle, cssnstv, textPad, t, e):
    textPad.tag_remove("match", "1.0", END)
    count = 0
    if needle:
        start = 1.0
        while True:
            pos = textPad.search(needle, start, nocase=cssnstv, stopindex=END)
            if not pos:
                break
            strlist = pos.split('.')
            left = strlist[0]
            right = str(int(strlist[1])+len(needle))
            lastpos = left+'.'+right
            textPad.tag_add("match", pos, lastpos)
            count += 1
            start = lastpos
            textPad.tag_config('match', background="yellow")
        e.focus_set()
        t.title(str(count)+"个被匹配")


def refresh():
    global top, filename
    if filename:
        top.title(os.path.basename(filename))
    else:
        top.title("记事本")


top = Tk()
top.title("记事本")
top.geometry("640x480+100+50")

menubar = Menu(top)

# 文件功能
filemenu = Menu(top)
filemenu.add_command(label="新建", accelerator="Ctrl+N", command=new_file)
filemenu.add_command(label="打开", accelerator="Ctrl+O", command=open_file)
filemenu.add_command(label="保存", accelerator="Ctrl+S", command=save)
filemenu.add_command(label="另存为", accelerator="Ctrl+shift+s", command=save_as)
filemenu.add_command(label="重命名", accelerator="Ctrl+R", command=rename_file)
filemenu.add_command(label="删除", accelerator="Ctrl+D", command=delete)
menubar.add_cascade(label="文件", menu=filemenu)

# 编辑功能
editmenu = Menu(top)
editmenu.add_command(label="撤销", accelerator="Ctrl+Z", command=undo)
editmenu.add_command(label="重做", accelerator="Ctrl+Y", command=redo)
editmenu.add_separator()
editmenu.add_command(label="剪切", accelerator="Ctrl+X", command=cut)
editmenu.add_command(label="复制", accelerator="Ctrl+C", command=copy)
editmenu.add_command(label="粘贴", accelerator="Ctrl+V", command=paste)
editmenu.add_separator()
editmenu.add_command(label="查找", accelerator="Ctrl+F", command=find)
editmenu.add_command(label="全选", accelerator="Ctrl+A", command=select_all)
menubar.add_cascade(label="编辑", menu=editmenu)

# 关于 功能
aboutmenu = Menu(top)
aboutmenu.add_command(label="作者", command=author)
aboutmenu.add_command(label="版权", command=power)
menubar.add_cascade(label="关于", menu=aboutmenu)

top['menu'] = menubar

shortcutbar = Frame(top, height=25, bg='Silver')
shortcutbar.pack(expand=NO, fill=X)

textPad=Text(top, undo=True)
textPad.pack(expand=YES, fill=BOTH)
scroll=Scrollbar(textPad)
textPad.config(yscrollcommand=scroll.set)
scroll.config(command=textPad.yview)
scroll.pack(side=RIGHT, fill=Y)

# 热键绑定
textPad.bind("<Control-N>", new_file)
textPad.bind("<Control-n>", new_file)
textPad.bind("<Control-O>", open_file)
textPad.bind("<Control-o>", open_file)
textPad.bind("<Control-S>", save)
textPad.bind("<Control-s>", save)
textPad.bind("<Control-D>", delete)
textPad.bind("<Control-d>", delete)
textPad.bind("<Control-R>", rename_file)
textPad.bind("<Control-r>", rename_file)
textPad.bind("<Control-A>", select_all)
textPad.bind("<Control-a>", select_all)
textPad.bind("<Control-F>", find)
textPad.bind("<Control-f>", find)

textPad.bind("<Button-3>", mypopup)
top.mainloop()
