#!/usr/bin/python
from Tkinter import *
from multiprocessing.dummy import Pool as ThreadPool
import subprocess
import socket

app=Tk()
app.minsize(250,30)
app.title("Pingu - ping subnet")

label = Label(app, text="Current IP:").pack(anchor=W)

textbox = Entry(app)
textbox.pack(anchor=W)

button=Button(app,text="Rescan")
button.pack(side=BOTTOM,fill=X)

scrollbar = Scrollbar(app)
scrollbar.pack(side=RIGHT, fill=Y)

listbox = Listbox(app, yscrollcommand=scrollbar.set)
listbox.pack(side=LEFT, fill=BOTH, expand=True)

scrollbar.config(command=listbox.yview)

def ping(host):

    response = subprocess.call("ping -c 1 -w 1 " + host + " >/dev/null 2>&1",shell=True)
    if (response == 0):
            livehosts.append(host)
            
def getip():

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))
    return s.getsockname()[0]

def rescan():

    global livehosts

    livehosts = []
    hosts = []

    listbox.delete(0,END)
    textbox.delete(0,END)

    ip = getip()
    textbox.insert(0,ip)

    subnet = '.'.join(ip.split('.')[:3]) + '.'

    for i in range(255):
      hosts.append(subnet + str(i))

    pool = ThreadPool(100)
    results = pool.map(ping, hosts)

    livehosts.sort(key=lambda x:tuple(map(int, x.split('.'))))
    
    for host in livehosts:
        try:
            hostname = subprocess.check_output("host -i " + host,shell=True)
            hostname = hostname.split()[-1]
        except:
            hostname = ''
        listbox.insert(END,host + "    " + hostname)

button.config(command=rescan)

rescan()
mainloop()
