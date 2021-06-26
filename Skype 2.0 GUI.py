import tkinter, json, os.path, socket, threading, sys, os

def Add_Contact(Name, Address):
    Close_Window()
    if os.path.exists("Contacts.json"):
        Contacts = json.load(open("Contacts.json"))
        Contacts.append({"Name":Name, "Address":Address})
    else: Contacts = [{"Name":Name, "Address":Address}]
    Contacts_JSON = json.dumps(Contacts, indent=4, sort_keys=True)
    with open("Contacts.json", 'w') as File:
        File.write(Contacts_JSON)
    ContactList.delete(0, tkinter.END)
    for Contact in sorted(json.load(open("Contacts.json")), key=lambda k: k['Name']):
        ContactList.insert(tkinter.END, Contact['Name'])
    ContactList.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    ContactScroll.config(command=ContactList.yview)

def Add_Contact_Window():
    global Popup
    Popup = tkinter.Tk()
    Popup.title("Add Contact")
    Popup.iconbitmap("Icon 128.ico")
    Frame_1 = tkinter.Frame(Popup)
    Frame_1.pack(fill=tkinter.X)
    Frame_2 = tkinter.Frame(Popup)
    Frame_2.pack(fill=tkinter.X)
    Frame_3 = tkinter.Frame(Popup)
    Frame_3.pack(fill=tkinter.X)
    Name_Text = tkinter.Label(Frame_1, text="Name")
    Name_Text.pack(side=tkinter.LEFT)
    Name_Input = tkinter.Entry(Frame_1)
    Name_Input.pack(side=tkinter.RIGHT)
    Name_Input.focus_set()
    Address_Text = tkinter.Label(Frame_3, text="I.P Address")
    Address_Text.pack(side=tkinter.LEFT)
    Address_Input = tkinter.Entry(Frame_3)
    Address_Input.pack(side=tkinter.RIGHT)
    Add = tkinter.Button(Popup, text="Add", command= lambda: Add_Contact(Name_Input.get(), Address_Input.get()))
    Add.pack()

def Add_To_Contact_List_Window(Address):
    global Popup
    Popup = tkinter.Tk()
    Popup.title("Add To Contact List")
    Popup.iconbitmap("Icon 128.ico")
    Frame_1 = tkinter.Frame(Popup)
    Frame_1.pack(fill=tkinter.X)
    Frame_2 = tkinter.Frame(Popup)
    Frame_2.pack(fill=tkinter.X)
    Frame_3 = tkinter.Frame(Popup)
    Frame_3.pack(fill=tkinter.X)
    Name_Text = tkinter.Label(Frame_1, text="Name")
    Name_Text.pack(side=tkinter.LEFT)
    Name_Input = tkinter.Entry(Frame_1)
    Name_Input.pack(side=tkinter.RIGHT)
    Name_Input.focus_set()
    Add = tkinter.Button(Popup, text="Add", command= lambda: Add_Contact(Name_Input.get(), Address))
    Add.pack()

def Edit_Contact(Name, Address):
    Close_Window()
    if os.path.exists("Contacts.json"):
        Contacts = json.load(open("Contacts.json"))
        Contacts[Contacts.index(ContactSelected)] = {"Name":Name, "Address":Address}
    else: Contacts = [{"Name":Name, "Address":Address}]
    Contacts_JSON = json.dumps(Contacts, indent=4, sort_keys=True)
    with open("Contacts.json", 'w') as File:
        File.write(Contacts_JSON)
    ContactList.delete(0, tkinter.END)
    for Contact in sorted(json.load(open("Contacts.json")), key=lambda k: k['Name']):
        ContactList.insert(tkinter.END, Contact['Name'])
    ContactList.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    ContactScroll.config(command=ContactList.yview)

def Edit_Contact_Window():
    global Popup
    Popup = tkinter.Tk()
    Popup.title("Edit Contact")
    Popup.iconbitmap("Icon 128.ico")
    Frame_1 = tkinter.Frame(Popup)
    Frame_1.pack(fill=tkinter.X)
    Frame_2 = tkinter.Frame(Popup)
    Frame_2.pack(fill=tkinter.X)
    Frame_3 = tkinter.Frame(Popup)
    Frame_3.pack(fill=tkinter.X)
    Name_Text = tkinter.Label(Frame_1, text="Name")
    Name_Text.pack(side=tkinter.LEFT)
    Name_Input = tkinter.Entry(Frame_1)
    Name_Input.pack(side=tkinter.RIGHT)
    Name_Input.focus_set()
    Name_Input.insert(0, ContactSelected['Name'])
    Address_Text = tkinter.Label(Frame_3, text="I.P Address")
    Address_Text.pack(side=tkinter.LEFT)
    Address_Input = tkinter.Entry(Frame_3)
    Address_Input.pack(side=tkinter.RIGHT)
    Address_Input.insert(0, ContactSelected['Address'])
    Add = tkinter.Button(Popup, text="Edit", command= lambda: Edit_Contact(Name_Input.get(), Address_Input.get()))
    Add.pack()

def Remove_Contact():
    Close_Window()
    Contacts = json.load(open("Contacts.json"))
    for Contact in Contacts:
        if Contact['Name'] == ContactSelected['Name']:
            #Contacts.pop(Contact['Name'])
            Contacts.remove(Contact)
    Contacts_JSON = json.dumps(Contacts, indent=4, sort_keys=True)
    with open("Contacts.json", 'w') as File:
        File.write(Contacts_JSON)
    ContactList.delete(0, tkinter.END)
    for Contact in sorted(json.load(open("Contacts.json")), key=lambda k: k['Name']):
        ContactList.insert(tkinter.END, Contact['Name'])
    ContactList.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    ContactScroll.config(command=ContactList.yview)

def Remove_Contact_Window():
    global Popup
    Popup = tkinter.Tk()
    Popup.title("Remove Contact")
    Popup.iconbitmap("Icon 128.ico")
    Remove = tkinter.Button(Popup, text="Remove", command=Remove_Contact)
    Remove.pack(side=tkinter.LEFT)
    Cancel = tkinter.Button(Popup, text="Cancel", command=Close_Window)
    Cancel.pack(side=tkinter.RIGHT)

def Send_File():
    with open(Directory, 'rb') as File:
        File_Bytes = File.read()
    Header = "-FILE START-"
    Send(Header)
    #Send(File_Bytes)

def Send_Open():
    global Directory
    if Directory == "":
        Directory = Listbox.get(tkinter.ACTIVE) + ":/"
    else:
        Directory += "/" + Listbox.get(tkinter.ACTIVE)
    if os.path.isfile(Directory):
        Send_File()
        print("Is file.")
    elif os.path.isdir(Directory):
        Listbox.delete(0, tkinter.END)
        for Name in os.listdir(Directory):
            if os.path.isdir(Directory + "/" + Name):
                Listbox.insert(tkinter.END, Name)
                print(Directory + "/" + Name)
        for Name in os.listdir(Directory):
            if os.path.isfile(Directory + "/" + Name):
                Listbox.insert(tkinter.END, Name)
                print(Directory + "/" + Name)
    print()
            
def Send_File_Window():
    global Popup, Listbox, Directory
    Popup = tkinter.Tk()
    Popup.title("Open File")
    Popup.iconbitmap("Icon 128.ico")
    Frame_1 = tkinter.Frame(Popup)
    Frame_1.pack(fill=tkinter.X)
    Frame_2 = tkinter.Frame(Popup)
    Frame_2.pack(fill=tkinter.X)
    Frame_3 = tkinter.Frame(Popup)
    Frame_3.pack(fill=tkinter.X)
    Cancel = tkinter.Button(Frame_3, text="Cancel", command=Close_Window)
    Cancel.pack(side=tkinter.RIGHT)
    Open = tkinter.Button(Frame_3, text="Open", command=Send_Open)
    Open.pack(side=tkinter.RIGHT)
    Scroll = tkinter.Scrollbar(Frame_2)
    Scroll.pack(side=tkinter.RIGHT, fill=tkinter.BOTH)
    Listbox = tkinter.Listbox(Frame_2)
    Listbox.pack(side=tkinter.TOP, fill=tkinter.BOTH)
    Back = tkinter.Button(Frame_1, text="Back")
    Back.pack(side=tkinter.RIGHT)
    Drive_Letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    Directory = ""
    if Directory == "":
        for Letter in Drive_Letters:
            if os.path.exists(Letter + ":/"):
                Listbox.insert(tkinter.END, Letter)
                
def Settings_Window():
    global Popup
    Popup = tkinter.Tk()
    Popup.title("Settings")
    Popup.iconbitmap("Icon 128.ico")
    Frame_1 = tkinter.Frame(Popup)
    Frame_1.pack(fill=tkinter.X)
    Frame_2 = tkinter.Frame(Popup)
    Frame_2.pack(fill=tkinter.X)
    Frame_3 = tkinter.Frame(Popup)
    Frame_3.pack(fill=tkinter.X)
    Name_Text = tkinter.Label(Frame_1, text="Name")
    Name_Text.pack(side=tkinter.LEFT)
    Name_Input = tkinter.Entry(Frame_1)
    Name_Input.pack(side=tkinter.RIGHT)
    Name_Input.focus_set()
    Address_Text = tkinter.Label(Frame_3, text="I.P Address")
    Address_Text.pack(side=tkinter.LEFT)
    Address_Input = tkinter.Entry(Frame_3)
    Address_Input.pack(side=tkinter.RIGHT)
    Add = tkinter.Button(Popup, text="Ok", command= lambda: Add_Contact(Name_Input.get(), Computer_Input.get(), Address_Input.get()))
    Add.pack()
    #Popup.mainloop()

def Close_Window():
    Popup.destroy()

#Quit Callback
def Quit():
    quit() 

#Send Callback
def Send(*args):
    global ContactSelected
    if args[0] == "-FILE START-":
        SendSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        SendSocket.sendto(args[0].encode(), (ContactSelected['Address'], 443))
        SendSocket.sendto(args[1].encode(), (ContactSelected['Address'], 443))
        
    elif ChatEntry.get().strip() != '':
        ChatLogs[ContactSelected['Address']].append("You: " + ChatEntry.get())
        SendSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        SendSocket.sendto(ChatEntry.get().encode(), (ContactSelected['Address'], 443))
        ChatEntry.delete(0, tkinter.END)

#Receive Worker
def ReceiveWorker():
    global Received, ReceivedAddress
    ReceiveSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ReceiveSocket.bind((socket.gethostbyname(socket.gethostname()), 443))
    while True:
        (Message, Address) = ReceiveSocket.recvfrom(64)
        Received = Message.decode()
        ReceivedAddress = Address[0]
    ReceiveSocket.close()
    

#Init Window
Window = tkinter.Tk()
Window.title("Skype 2.0 GUI")
Window.iconbitmap("Icon 128.ico")
Window.geometry("800x800")
Window.configure(bg='white')

#Init Menu
MenuBar = tkinter.Menu(Window)
Skype2 = tkinter.Menu(MenuBar, tearoff=0)
Skype2.add_command(label="Quit", command=Quit)
MenuBar.add_cascade(label="Skype 2.0", menu=Skype2)
Contacts = tkinter.Menu(MenuBar, tearoff=0)
Contacts.add_command(label="Add Contact", command=Add_Contact_Window)
MenuBar.add_cascade(label="Contacts", menu=Contacts)
Window.config(menu=MenuBar)

#Contact Scrollbar
ContactFrame = tkinter.Frame(Window)
ContactFrame.pack(side=tkinter.LEFT, fill=tkinter.Y)
ContactTitle = tkinter.Label(ContactFrame, text="Contact List", bg="red")
ContactTitle.pack(side=tkinter.TOP, fill=tkinter.X)
ContactScroll = tkinter.Scrollbar(ContactFrame)
ContactScroll.pack(side=tkinter.RIGHT, fill=tkinter.BOTH)
ContactList = tkinter.Listbox(ContactFrame, yscrollcommand=ContactScroll.set, activestyle='none', selectbackground='red', selectforeground='black', background='white', highlightcolor='white', highlightbackground='white')
if os.path.exists("Contacts.json"):
    for Contact in sorted(json.load(open("Contacts.json")), key=lambda k: k['Name']):
        ContactList.insert(tkinter.END, Contact['Name'])
ContactList.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
ContactScroll.config(command=ContactList.yview)

def Context_Menu(event):
    ContextMenu.post(event.x_root, event.y_root)
    
ContextMenu = tkinter.Menu(Window, tearoff=0)
ContextMenu.add_command(label='Add', command=Add_Contact_Window)
ContextMenu.add_command(label='Edit', command=Edit_Contact_Window)
ContextMenu.add_command(label='Remove', command=Remove_Contact_Window)
ContactList.bind("<Button-3>", Context_Menu)

#Chat Box
Chat_File_Icon = tkinter.PhotoImage(file="File Icon.png")

ChatFrame = tkinter.Frame(Window)
ChatFrame.pack(side=tkinter.BOTTOM, fill=tkinter.X)
ChatSend = tkinter.Button(ChatFrame, text="Send", command=Send, bg='red', activebackground='orange')
ChatSend.pack(side=tkinter.RIGHT, fill=tkinter.Y)
ChatEntry = tkinter.Entry(ChatFrame)
ChatEntry.pack(side=tkinter.BOTTOM, fill=tkinter.X)
ChatEntry.bind('<Return>', Send)
ChatFile = tkinter.Button(ChatFrame, image=Chat_File_Icon, command=Send_File_Window)
ChatFile.pack(side=tkinter.RIGHT)
ChatScroll = tkinter.Scrollbar(ChatFrame)
ChatScroll.pack(side=tkinter.RIGHT, fill=tkinter.BOTH)
ChatBoxTitle = tkinter.Label(ChatFrame, text="Chat Box", bg="red")
ChatBoxTitle.pack(side=tkinter.TOP, fill=tkinter.X)
ChatBox = tkinter.Listbox(ChatFrame, yscrollcommand=ChatScroll.set, highlightcolor='white', highlightbackground='white', activestyle='none', selectforeground='black', background='white')
ChatBox.pack(side=tkinter.BOTTOM, fill=tkinter.BOTH)
ChatScroll.config(command=ChatBox.yview)

#Contact Information
ContactFrame = tkinter.Frame(Window, bg='white')
ContactFrame.pack(side=tkinter.TOP, fill=tkinter.X)
ContactSelected = sorted(json.load(open("Contacts.json")), key=lambda k: k['Name'])[ContactList.index(tkinter.ACTIVE)]
ContactInformationTitle = tkinter.Label(ContactFrame, text="Contact Information", bg="red")
ContactInformationTitle.pack(side=tkinter.TOP, fill=tkinter.X)
ContactName = tkinter.Label(ContactFrame, text=ContactSelected['Name'], background='white')
ContactName.pack()
ContactAddress = tkinter.Label(ContactFrame, text=ContactSelected['Address'], background='white')
ContactAddress.pack()

#Receive Socket
ChatLogs = {}
ReceivedAddress = ''
ReceivedName = ''
Received = 0
ReceiveThread = threading.Thread(target=ReceiveWorker, args=())
ReceiveThread.start()

while True:
    if Received != 0:
        for Contact in sorted(json.load(open("Contacts.json")), key=lambda k: k['Name']):
            if Contact['Address'] == ReceivedAddress:
                ReceivedName = Contact['Name']
        if ReceivedAddress not in ChatLogs:
            ChatLogs[ReceivedAddress] = []
        if ReceivedName != '':
            ChatLogs[ReceivedAddress].append(ReceivedName + ": " + Received)
        else:
            Add_To_Contact_List_Window(ReceivedAddress)
            ChatLogs[ReceivedAddress].append("Unknown: " + Received)
        RecievedName = ''
        ReceivedAddress = ''
        ReceivedName = ''
        Received = 0
    ContactSelected = sorted(json.load(open("Contacts.json")), key=lambda k: k['Name'])[ContactList.index(tkinter.ACTIVE)]
    ContactName.config(text=ContactSelected['Name'])
    ContactAddress.config(text=ContactSelected['Address'])
    ChatBox.delete(0, tkinter.END)
    if ContactSelected['Address'] not in ChatLogs:
            ChatLogs[ContactSelected['Address']] = []
    for Line in ChatLogs[ContactSelected['Address']]:
        ChatBox.insert(tkinter.END, Line)
    Window.update()
