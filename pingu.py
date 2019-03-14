#!/usr/bin/python
from Tkinter import *
from multiprocessing.dummy import Pool as ThreadPool
import subprocess
import socket

app=Tk()
app.title("Pingu - ping subnet")

listbox = Listbox(app)
listbox.pack(fill="both", expand=True)

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

    ip = getip()
    subnet = '.'.join(ip.split('.')[:3]) + '.'

    for i in range(255):
      hosts.append(subnet + str(i))

    pool = ThreadPool(255)
    results = pool.map(ping, hosts)

    livehosts.sort(key=lambda x:tuple(map(int, x.split('.'))))
    
    for host in livehosts:
        try:
            hostname = subprocess.check_output("host -i " + host,shell=True)
            hostname = hostname.split()[-1]
        except:
            hostname = ''
        listbox.insert(END,host + "    " + hostname)

button=Button(app,text="Rescan",command=rescan)
button.pack()

rescan()
mainloop()
