#!/usr/bin/python3
from tkinter import *
from tkinter import simpledialog
from multiprocessing.dummy import Pool as ThreadPool
import subprocess
import socket

app=Tk()
app.minsize(250,30)

def ping(host):

    response = subprocess.call("ping -c 1 -w 1 " + host + " >/dev/null 2>&1",shell=True)
    if (response == 0):
            livehosts.append(host)
            
def getip():

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))
    return s.getsockname()[0]

def onDouble(event):
        widget = event.widget
        selection=widget.curselection()
        ip = widget.get(selection[0])
        user = simpledialog.askstring("Username", "Enter username:")
        response = subprocess.call("ssh " + user + "@" + ip ,shell=True)

def rescan():

    global livehosts

    livehosts = []
    hosts = []

    listbox.delete(0,END)

    ip = getip()
    app.title("Pingu - " + ip)

    subnet = '.'.join(ip.split('.')[:3]) + '.'

    for i in range(255):
      hosts.append(subnet + str(i))

    pool = ThreadPool(255)
    results = pool.map(ping, hosts)

    livehosts.sort(key=lambda x:tuple(map(int, x.split('.'))))
    
    for host in livehosts:
        try:
            hostname = subprocess.check_output("host -i " + host,text=True,shell=True)
            hostname = hostname.split()[-1]
        except:
            hostname = ''
        listbox.insert(END,host + "    " + str(hostname))

button=Button(app,text="Rescan")
button.config(command=rescan)
button.pack(side=BOTTOM,fill=X)

scrollbar = Scrollbar(app)
scrollbar.pack(side=RIGHT, fill=Y)

listbox = Listbox(app, yscrollcommand=scrollbar.set)
listbox.bind("<Double-Button-1>", onDouble)
listbox.pack(side=LEFT, fill=BOTH, expand=True)

scrollbar.config(command=listbox.yview)

rescan()
mainloop()
