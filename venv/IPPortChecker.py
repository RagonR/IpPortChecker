import pyautogui
import socket
import time
from tkinter import *
from tkinter import messagebox, font

class dataStorage():
    IPValue = ""
    PortValue = 0
    GivenByFileCheck = 2
    GivenByGuiCheck = 1

class IpCheckerInterface(Frame):
    def __init__(self):
        Frame.__init__(self)
        frame = Frame()
        self.master.title('Port Checker')
        self.master.geometry("280x160")
        self.master.configure(bg="#2A2A2E")
        self.master.resizable(0, 0)
        self.master.attributes("-topmost", True)
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
        def click_start(event):
            try:
                dataStorage.PortValue = int(self.PortEntry.get())
                dataStorage.IPValue = self.IPEntry.get()
                if dataStorage.IPValue == '':
                    messagebox.showerror("Error", "IP entry is empty")
                else:
                    number = 0
                    run_check()
            except ValueError:
                messagebox.showerror("Error", "Port entry is empty")

        self.StartButton = Button(frame, text="Check", font=fontForLabels)
        self.StartButton.bind("<ButtonRelease-1>", click_start)
        self.StartButton.grid(row=3, column=2)

        def run_check():
            try:
                self.checkResultLaber.destroy()
            except:
                pass
            result = check_port(dataStorage.IPValue, dataStorage.PortValue, dataStorage.GivenByGuiCheck)
            print(result)
            if result == 0:
                self.checkResultLaber = Label(frame, text="%s is Open" % dataStorage.PortValue, bg="#2A2A2E", fg="#00ff00", font=fontForScanner)
                self.checkResultLaber.grid(row=3, column=0, columnspan=2)
            elif result == -2:
                pass
            else:
                self.checkResultLaber = Label(frame, text="%s is Closed" % dataStorage.PortValue, bg="#2A2A2E", fg="#e60000", font=fontForScanner)
                self.checkResultLaber.grid(row=3, column=0, columnspan=2)

        #button for reading file
        def click_scan_from_list(event):
            scan_file();

        self.ScanFileButton = Button(frame, text="Scan from list", font=fontForLabels)
        self.ScanFileButton.bind("<ButtonRelease-1>", click_scan_from_list)
        self.ScanFileButton.grid(row=4, column=0, columnspan=2)


def scan_file():
    try:
        with open("IPsAndPorts.txt", "r") as read:
            with open("Results.txt", "a+") as save:
                for line in read:
                    wordNumber = 1
                    for word in line.split():
                        if wordNumber == 1:
                            dataStorage.IPValue = str(word)
                            wordNumber += 1
                        else:
                            dataStorage.PortValue = int(word)
                            writeToFile(save)
            save.close()
        read.close()
        messagebox.showinfo("Successful", "The results are saved in a Results.txt")
    except:
        messagebox.showerror("Error", "IPsAndPorts.txt file does not exsit")


def write_to_file(save):
    result = check_port(dataStorage.IPValue, dataStorage.PortValue, dataStorage.GivenByFileCheck)
    if result == 0:
            save.write(textToWrite ("OPEN"))
    elif result == -2:
        save.write(textToWrite ("FAILED"))
    else:
        save.write(textToWrite ("CLOSED"))

def check_port(IPAddress, Port, Check):
    if Port < 0 or Port > 65535:
        if Check == 1:
            messagebox.showerror("Error", "Port is out of range (0 to 65535)")
            return -2
        else:
            return -2
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.4)
    location = (IPAddress, Port)
    try:
        result_of_check = s.connect_ex(location)
        return result_of_check
    except:
        if Check == 1:
            messagebox.showerror("Error", "Failed to find IP/URL with given port")
            return -2
        else:
            return -2

def text_to_write (status):
    return "%s : %s %s \n" %(dataStorage.IPValue, dataStorage.PortValue, status)

def gui():
    IpCheckerInterface().mainloop()

def main():
    gui()

main()