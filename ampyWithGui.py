#!/usr/bin/python3
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os, subprocess, json

class ampyWithGui(object):
    def __init__(self):
        try:
            subprocess.check_output("ampy --version")
        except:
            raise(Exception("pls install ampy and add to env_path"))
        self.window = tk.Tk()
        self.window.title('ESP File Manager')  

        self.frame = tk.Frame(self.window)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=2)
        self.frame.rowconfigure(8, weight=1)
        self.frame.pack(fill = "both", expand = True)

        self.port_notify = tk.Label(self.frame, text='Port:')
        self.port_notify.grid(row = 0, column = 0, sticky=tk.NW, padx=5)
        self.port_entry = tk.Entry(self.frame)
        self.port_entry.grid(row = 1, column = 0, sticky=tk.N + tk.W +tk.E, padx=5)

        self.path_notify = tk.Label(self.frame, text='Local path:')
        self.path_notify.grid(row = 4, column = 0, sticky=tk.NW, padx=5)
        self.path_entry = tk.Entry(self.frame)
        self.path_entry.bind("<Return>", self.parseLocalPath)
        self.path_entry.grid(row = 5, column = 0, sticky=tk.N + tk.W +tk.E, padx=5)

        self.btn_frame = tk.Frame(self.frame)
        self.btn_frame.grid(row = 6, column = 0, sticky=tk.W, pady=10)
        self.path_btn = tk.Button(self.btn_frame, text="open", command=self.onPathBtnClick)
        self.readRemote_btn = tk.Button(self.btn_frame, text="Read remote", command=self.onReadRemoteBtnClick)
        self.upload_btn = tk.Button(self.btn_frame, text="Upload")
        self.uploadAll_btn = tk.Button(self.btn_frame, text="UploadAll")
        self.download_btn = tk.Button(self.btn_frame, text="Download")
        self.downloadAll_btn = tk.Button(self.btn_frame, text="DownloadAll")

        self.path_btn.grid(row = 0, column = 0, padx=5)
        self.readRemote_btn.grid(row = 0, column = 1, padx=5)
        self.upload_btn.grid(row = 0, column = 2, padx=5)
        self.uploadAll_btn.grid(row = 0, column = 3, padx=5)
        self.download_btn.grid(row = 0, column = 4, padx=5)
        self.downloadAll_btn.grid(row = 0, column = 5, padx=5)

        self.localTree_notify = tk.Label(self.frame, text='Local dir content:')
        self.localTree_notify.grid(row = 7, column = 0, sticky=tk.NW, padx=5)
        self.localTree = ttk.Treeview(self.frame) 
        self.localTree.grid(row = 8,column = 0, sticky=tk.N+tk.S+tk.W+tk.E, padx=5, pady=10)

        self.remoteTree_notify = tk.Label(self.frame, text='Remote dir content:')
        self.remoteTree_notify.grid(row = 7, column = 1, sticky=tk.NW, padx=5)
        self.remoteTree = ttk.Treeview(self.frame) 
        self.remoteTree.grid(row = 8,column = 1, sticky=tk.N+tk.S+tk.W+tk.E, padx=5, pady=10)

        self.window.mainloop()
    
    def cleanTreeView(self, treeView):
        x = treeView.get_children()
        for item in x:
            treeView.delete(item)

    def parseLocalPath(self, event=None):
        self.cleanTreeView(self.localTree)
        path = self.path_entry.get()
        if not os.path.exists(path):
            return
        else:
            if path[-1] == os.sep:
                path = path[0:-1]
                self.path_entry.delete(0, 'end')
                self.path_entry.insert(0, path)
            path_iid = path.replace('/', '\\')
            if (not self.localTree.exists(path_iid)):
                self.localTree.insert("", 'end', path_iid, text=path_iid)
            
            for root, dirs, files in os.walk(path):
                files = [f for f in files if not f[0] == '.']
                dirs[:] = [d for d in dirs if not d[0] == '.']

                dir_iid = root.replace('/', '\\')
                if (dir_iid != path_iid) and (not self.localTree.exists(dir_iid)):
                    self.localTree.insert(os.path.dirname(dir_iid).replace('/', '\\'), 'end', dir_iid, text=os.path.split(dir_iid)[1])
                
                for name in files:
                    file_iid = os.path.join(root, name).replace('/', '\\')
                    if(not self.localTree.exists(file_iid)):
                        self.localTree.insert(os.path.dirname(file_iid), 'end', file_iid, text=os.path.split(file_iid)[1])    


    def onPathBtnClick(self):
        self.path_entry.delete(0, 'end')
        self.path_entry.insert(0, filedialog.askdirectory().replace('/', '\\'))
        self.parseLocalPath()

    def onReadRemoteBtnClick(self):
        self.cleanTreeView(self.remoteTree)
        port = self.port_entry.get()
        output = subprocess.check_output("ampy -p {} run getDeviceFileTree.py".format(port)).decode().split("\r\r\n")
        if len(output) != 3:
            return
        else:
            dirs = json.loads(output[0])
            files = json.loads(output[1])
            
            self.remoteTree.insert("", 'end', '/', text='/')
            for dir in dirs:
                if(not self.remoteTree.exists(dir)):
                    self.remoteTree.insert(os.path.dirname(dir), 'end', dir, text=dir)

            for file in files:
                if(not self.remoteTree.exists(file)):
                    self.remoteTree.insert(os.path.dirname(file), 'end', file, text=os.path.split(file)[1])

a = ampyWithGui()
