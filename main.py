from tkinter import *
import sqlite3
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox

root = Tk()
root.title("Contact List")
width = 900  # Increased width for better spacing
height = 500  # Increased height for better spacing
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)
root.config(bg="#f0f0f0")  # Light gray background


FIRSTNAME = StringVar()
LASTNAME = StringVar()
GENDER = StringVar()
AGE = StringVar()
ADDRESS = StringVar()
CONTACT = StringVar()


def Database(order_by='lastname'):
    conn = sqlite3.connect("pythontut.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, firstname TEXT, lastname TEXT, gender TEXT, age TEXT, address TEXT, contact TEXT)")
    cursor.execute(f"SELECT * FROM `member` ORDER BY `{order_by}` ASC")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()

def SubmitData():
    if  FIRSTNAME.get() == "" or LASTNAME.get() == "" or GENDER.get() == "" or AGE.get() == "" or ADDRESS.get() == "" or CONTACT.get() == "":
        result = tkMessageBox.showwarning('', 'Please Complete The Required Field', icon="warning")
    else:
        tree.delete(*tree.get_children())
        conn = sqlite3.connect("pythontut.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO `member` (firstname, lastname, gender, age, address, contact) VALUES(?, ?, ?, ?, ?, ?)", (str(FIRSTNAME.get()), str(LASTNAME.get()), str(GENDER.get()), int(AGE.get()), str(ADDRESS.get()), str(CONTACT.get())))
        conn.commit()
        cursor.execute("SELECT * FROM `member` ORDER BY `lastname` ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()
        FIRSTNAME.set("")
        LASTNAME.set("")
        GENDER.set("")
        AGE.set("")
        ADDRESS.set("")
        CONTACT.set("")

def UpdateData():
    if GENDER.get() == "":
       result = tkMessageBox.showwarning('', 'Please Complete The Required Field', icon="warning")
    else:
        tree.delete(*tree.get_children())
        conn = sqlite3.connect("pythontut.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE `member` SET `firstname` = ?, `lastname` = ?, `gender` =?, `age` = ?,  `address` = ?, `contact` = ? WHERE `mem_id` = ?", (str(FIRSTNAME.get()), str(LASTNAME.get()), str(GENDER.get()), str(AGE.get()), str(ADDRESS.get()), str(CONTACT.get()), int(mem_id)))
        conn.commit()
        cursor.execute("SELECT * FROM `member` ORDER BY `lastname` ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()
        FIRSTNAME.set("")
        LASTNAME.set("")
        GENDER.set("")
        AGE.set("")
        ADDRESS.set("")
        CONTACT.set("")
    
def OnSelected(event):
    global mem_id, UpdateWindow
    curItem = tree.focus()
    contents =(tree.item(curItem))
    selecteditem = contents['values']
    mem_id = selecteditem[0]
    FIRSTNAME.set("")
    LASTNAME.set("")
    GENDER.set("")
    AGE.set("")
    ADDRESS.set("")
    CONTACT.set("")
    FIRSTNAME.set(selecteditem[1])
    LASTNAME.set(selecteditem[2])
    GENDER.set(selecteditem[3])
    AGE.set(selecteditem[4])
    ADDRESS.set(selecteditem[5])
    CONTACT.set(selecteditem[6])
    UpdateWindow = Toplevel()
    UpdateWindow.title("Update Contact")
    width = 400
    height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = ((screen_width/2) + 450) - (width/2)
    y = ((screen_height/2) + 20) - (height/2)
    UpdateWindow.resizable(0, 0)
    UpdateWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    if 'NewWindow' in globals():
        NewWindow.destroy()

    Label(UpdateWindow, text="Firstname:").grid(row=0, column=0, padx=10, pady=10)
    Entry(UpdateWindow, textvariable=FIRSTNAME).grid(row=0, column=1, padx=10, pady=10)
    
    Label(UpdateWindow, text="Lastname:").grid(row=1, column=0, padx=10, pady=10)
    Entry(UpdateWindow, textvariable=LASTNAME).grid(row=1, column=1, padx=10, pady=10)
    
    Label(UpdateWindow, text="Gender:").grid(row=2, column=0, padx=10, pady=10)
    Radiobutton(UpdateWindow, text="Male", variable=GENDER, value="Male").grid(row=2, column=1, padx=10, pady=5)
    Radiobutton(UpdateWindow, text="Female", variable=GENDER, value="Female").grid(row=2, column=2, padx=10, pady=5)
    Radiobutton(UpdateWindow, text="Other", variable=GENDER, value="Other").grid(row=2, column=3, padx=10, pady=5)
    
    Label(UpdateWindow, text="Age:").grid(row=3, column=0, padx=10, pady=10)
    Spinbox(UpdateWindow, from_=1, to=100, textvariable=AGE).grid(row=3, column=1, padx=10, pady=10)
    
    Label(UpdateWindow, text="Address:").grid(row=4, column=0, padx=10, pady=10)
    Entry(UpdateWindow, textvariable=ADDRESS).grid(row=4, column=1, padx=10, pady=10)
    
    Label(UpdateWindow, text="Contact:").grid(row=5, column=0, padx=10, pady=10)
    Entry(UpdateWindow, textvariable=CONTACT).grid(row=5, column=1, padx=10, pady=10)
    
    Button(UpdateWindow, text="Update", command=UpdateData).grid(row=6, columnspan=2, pady=10)

def DeleteData():
    if not tree.selection():
       result = tkMessageBox.showwarning('', 'Please Select Something First!', icon="warning")
    else:
        result = tkMessageBox.askquestion('', 'Are you sure you want to delete this record?', icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents =(tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)
            conn = sqlite3.connect("pythontut.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM `member` WHERE `mem_id` = %d" % selecteditem[0])
            conn.commit()
            cursor.close()
            conn.close()

def AddNewWindow():
    global NewWindow
    FIRSTNAME.set("")
    LASTNAME.set("")
    GENDER.set("")
    AGE.set("")
    ADDRESS.set("")
    CONTACT.set("")
    NewWindow = Toplevel()
    NewWindow.title("Add New Contact")
    width = 400
    height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = ((screen_width/2) - 455) - (width/2)
    y = ((screen_height/2) + 20) - (height/2)
    NewWindow.resizable(0, 0)
    NewWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    if 'UpdateWindow' in globals():
        UpdateWindow.destroy()

    Label(NewWindow, text="Firstname:").grid(row=0, column=0, padx=10, pady=10)
    Entry(NewWindow, textvariable=FIRSTNAME).grid(row=0, column=1, padx=10, pady=10)
    
    Label(NewWindow, text="Lastname:").grid(row=1, column=0, padx=10, pady=10)
    Entry(NewWindow, textvariable=LASTNAME).grid(row=1, column=1, padx=10, pady=10)
    
    Label(NewWindow, text="Gender:").grid(row=2, column=0, padx=10, pady=10)
    Radiobutton(NewWindow, text="Male", variable=GENDER, value="Male").grid(row=2, column=1, padx=10, pady=5)
    Radiobutton(NewWindow, text="Female", variable=GENDER, value="Female").grid(row=2, column=2, padx=10, pady=5)
    Radiobutton(NewWindow, text="Other", variable=GENDER, value="Other").grid(row=2, column=3, padx=10, pady=5)
    
    Label(NewWindow, text="Age:").grid(row=3, column=0, padx=10, pady=10)
    Spinbox(NewWindow, from_=1, to=100, textvariable=AGE).grid(row=3, column=1, padx=10, pady=10)
    
    Label(NewWindow, text="Address:").grid(row=4, column=0, padx=10, pady=10)
    Entry(NewWindow, textvariable=ADDRESS).grid(row=4, column=1, padx=10, pady=10)
    
    Label(NewWindow, text="Contact:").grid(row=5, column=0, padx=10, pady=10)
    Entry(NewWindow, textvariable=CONTACT).grid(row=5, column=1, padx=10, pady=10)
    
    Button(NewWindow, text="Save", command=SubmitData).grid(row=6, columnspan=2, pady=10)

def Chatbot():
    tkMessageBox.showinfo("Chatbot", "This is where the chatbot functionality will be implemented.")

def CountContacts():
    conn = sqlite3.connect("pythontut.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM `member`")
    count = cursor.fetchone()[0]
    tkMessageBox.showinfo("Count Contacts", f"Total contacts: {count}")
    cursor.close()
    conn.close()

def SortByAgeAsc():
    tree.delete(*tree.get_children())
    Database(order_by='age')

Top = Frame(root, width=900, bd=1, relief=SOLID)
Top.pack(side=TOP)
Mid = Frame(root, width=900,  bg="#f0f0f0")
Mid.pack(side=TOP)
MidLeft = Frame(Mid, width=900, bg="#f0f0f0")  # Adjusted width and background color
MidLeft.pack(side=TOP, pady=10)
TableMargin = Frame(root, width=900)
TableMargin.pack(side=TOP)

lbl_title = Label(Top, width=900, font=('arial', 18), text="Contact Management System")
lbl_title.pack()

btn_add = Button(MidLeft, text="+ ADD NEW", command=AddNewWindow, bg="#b3e6ff", font=('arial', 12))
btn_add.pack(side=LEFT, padx=10, pady=10)
btn_delete = Button(MidLeft, text="DELETE", command=DeleteData, bg="#ff9999", font=('arial', 12))
btn_delete.pack(side=LEFT, padx=10, pady=10)
btn_count = Button(MidLeft, text="Count Contacts", command=CountContacts, bg="#ffcc99", font=('arial', 12))
btn_count.pack(side=LEFT, padx=10, pady=10)
btn_chatbot = Button(MidLeft, text="Chatbot", command=Chatbot, bg="#ffffcc", font=('arial', 12))
btn_chatbot.pack(side=LEFT, padx=10, pady=10)
btn_sort = Button(MidLeft, text="Sort by Age Asc", command=SortByAgeAsc, bg="#cce5ff", font=('arial', 12))
btn_sort.pack(side=LEFT, padx=10, pady=10)


scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
tree = ttk.Treeview(TableMargin, columns=("MemberID", "Firstname", "Lastname", "Gender", "Age", "Address", "Contact"), height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)
tree.heading('MemberID', text="MemberID", anchor=W)
tree.heading('Firstname', text="Firstname", anchor=W)
tree.heading('Lastname', text="Lastname", anchor=W)
tree.heading('Gender', text="Gender", anchor=W)
tree.heading('Age', text="Age", anchor=W)
tree.heading('Address', text="Address", anchor=W)
tree.heading('Contact', text="Contact", anchor=W)
tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=80)
tree.column('#2', stretch=NO, minwidth=0, width=120)
tree.column('#3', stretch=NO, minwidth=0, width=120)
tree.column('#4', stretch=NO, minwidth=0, width=90)
tree.column('#5', stretch=NO, minwidth=0, width=40)
tree.column('#6', stretch=NO, minwidth=0, width=150)
tree.column('#7', stretch=NO, minwidth=0, width=120)
tree.pack()
tree.bind('<Double-Button-1>', OnSelected)


if __name__ == '__main__':
    Database()
    root.mainloop()
