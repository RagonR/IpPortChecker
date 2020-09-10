from builtins import print

import pyautogui
import socket
import time
from tkinter import *
from tkinter import messagebox, font

class GivenInfoFromFile():
    IPValue = ""
    PortValue = 0
    GivenByFileCheck = 2

class GivenInfoInGui():
    IPValue = ""
    PortValue = 0
    GivenByGuiCheck = 1


class IpCheckerInterface(Frame):
    def __init__(self):
        Frame.__init__(self)
        frame = Frame()
        self.master.title('Port Checker')
        self.master.geometry("260x160")
        self.master.configure(bg="#2A2A2E")
        frame.grid()
        fontForLabels = font.Font(family="Yu Gothic", size=12, weight='bold')
        emptyLabelFont = font.Font(size=4, weight='bold')
        fontForEntry = font.Font(family="Yu Gothic", size=12)
        fontForScanner = font.Font(family="Yu Gothic", size=14, weight='bold')
        frame.configure(bg="#2A2A2E")
        #Empty
        self.labMargin = Label(frame, text="", bg="#2A2A2E", fg="#CFCFD1", font=emptyLabelFont)
        self.labMargin.grid(row=0, column=0, sticky=W)
        # Ip address
        self.labIP = Label(frame, text="IP/URL:", bg="#2A2A2E", fg="#CFCFD1", font=fontForLabels)
        self.labIP.grid(row=1, column=0, sticky=E)
        self.IPEntry = Entry(frame, width=20, bg="white", font=fontForEntry)
        self.IPEntry.grid(row=1, column=1, columnspan=2, sticky=SE)
        # Port number
        self.labPort= Label(frame, text="Port:", bg="#2A2A2E", fg="#CFCFD1", font=fontForLabels)
        self.labPort.grid(row=2, column=0)
        self.PortEntry = Entry(frame, width=8, bg="white", font=fontForEntry)
        self.PortEntry.grid(row=2, column=1, sticky=SW)
        # Button to check
        def clickStart(event):
            try:
                GivenInfoInGui.PortValue = int(self.PortEntry.get())
                GivenInfoInGui.IPValue = self.IPEntry.get()
                if GivenInfoInGui.IPValue == '':
                    messagebox.showerror("Error", "IP entry is empty")
                else:
                    number = 0
                    RunCheck()
            except ValueError:
                messagebox.showerror("Error", "Port entry is empty")

        self.StartButton = Button(frame, text="Check", font=fontForLabels)
        self.StartButton.bind("<ButtonRelease-1>", clickStart)
        self.StartButton.grid(row=3, column=2)

        def RunCheck():
            try:
                self.checkResultLaber.destroy()
            except:
                pass
            if CheckPort(GivenInfoInGui.IPValue, GivenInfoInGui.PortValue, GivenInfoInGui.GivenByGuiCheck) == 0:
                self.checkResultLaber = Label(frame, text="%s is Open" % GivenInfoInGui.PortValue, bg="#2A2A2E", fg="#00ff00", font=fontForScanner)
                self.checkResultLaber.grid(row=3, column=0, columnspan=2)
            else:
                self.checkResultLaber = Label(frame, text="%s is Closed" % GivenInfoInGui.PortValue, bg="#2A2A2E", fg="#e60000", font=fontForScanner)
                self.checkResultLaber.grid(row=3, column=0, columnspan=2)

        #button for reading file
        def clickScanFromList(event):
            ScanFile();

        self.ScanFileButton = Button(frame, text="Scan from list", font=fontForLabels)
        self.ScanFileButton.bind("<ButtonRelease-1>", clickScanFromList)
        self.ScanFileButton.grid(row=4, column=0, columnspan=2)



def ScanFile():
    with open("IPs.txt", "r") as f:
        for line in f:
            wordNumber = 1
            for word in line.split():
                if wordNumber == 1:
                    GivenInfoFromFile.IPValue = str(word)
                    wordNumber+=1
                else:
                    GivenInfoFromFile.PortValue = int(word)
                    writeToFile()
    f.close()

def CheckPort(IPAddress, Port, Check):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    location = (IPAddress, Port)
    try:
        result_of_check = s.connect_ex(location)
        return result_of_check
    except:
        if Check == 1:
            messagebox.showerror("Error", "Failed to find IP/URL with given port")
        else:
            return Check

def textToWrite (status):
    return "%s : %s %s \n" %(GivenInfoFromFile.IPValue, GivenInfoFromFile.PortValue, status)

def writeToFile():
    save_file = open("save.txt", "a+")
    if CheckPort(GivenInfoFromFile.IPValue, GivenInfoFromFile.PortValue, GivenInfoFromFile.GivenByFileCheck) == 0:
            save_file.write(textToWrite ("OPEN"))
    elif CheckPort(GivenInfoFromFile.IPValue, GivenInfoFromFile.PortValue, GivenInfoFromFile.GivenByFileCheck) == 2:
        save_file.write(textToWrite ("FAILED"))
    else:
        save_file.write(textToWrite ("CLOSED"))
    save_file.close()

def Gui():
    IpCheckerInterface().mainloop()

def main():
    Gui()

main()