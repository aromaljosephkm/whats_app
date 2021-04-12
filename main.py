import csv
from datetime import datetime
import time
import webbrowser as web
import pyautogui as pg
from urllib.parse import quote
import tkinter as tk
from tkinter import *
import _thread
from tkinter.filedialog import askopenfilename

sleeptm = "None, You can use this function to print the remaining time in seconds."
filename = ''


class CountryCodeException(Exception):
    pass


class CallTimeException(Exception):
    pass


def prnt_sleeptm():
    return sleeptm


def sendwhatmsg(phone_no, message, time_hour, time_min, wait_time=15, print_waitTime=True):
    global sleeptm
    if "+" not in phone_no:
        raise CountryCodeException("Country code missing from phone_no")
    timehr = time_hour

    if time_hour not in range(0, 25) or time_min not in range(0, 60):
        print("Invalid time format")

    if time_hour == 0:
        time_hour = 24
    callsec = (time_hour * 3600) + (time_min * 60)

    curr = time.localtime()
    currhr = curr.tm_hour
    currmin = curr.tm_min
    # currsec = curr.tm_sec
    currsec = 45

    if currhr == 0:
        currhr = 24

    currtotsec = (currhr * 3600) + (currmin * 60) + currsec
    lefttm = callsec - currtotsec

    if lefttm <= 0:
        lefttm = 86400 + lefttm

    if lefttm < wait_time:
        raise CallTimeException("Call time must be greater than wait_time as web.whatsapp.com takes some time to load")

    sleeptm = lefttm - wait_time
    if print_waitTime:
        print(
            f"In {prnt_sleeptm()} seconds web.whatsapp.com will open and after {wait_time} seconds message will be "
            f"delivered")
    time.sleep(sleeptm)
    parsedMessage = quote(message)
    web.open('https://web.whatsapp.com/send?phone=' + phone_no + '&text=' + parsedMessage)
    time.sleep(2)
    width, height = pg.size()
    pg.click(width / 2, height / 2)
    time.sleep(wait_time - 2)
    pg.press('enter')
    pg.hotkey('ctrl', 'w')
    pg.press('enter')


def browseFiles():
    global filename
    filename = askopenfilename(initialdir="/", title="Select a File", filetypes=(("CSV files", "*.csv*")))
    MultiMessage.button_explore.configure(text=filename)



class TimeTableApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.title(self, "Bulk Whatsapp Messenger")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, Developer, MultiMessage, SingleMessage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def destroy_frame(self):
        self.destroy()

    @staticmethod
    def configurationRun():
        web.open('https://web.whatsapp.com/')
        time.sleep(30)
        pg.hotkey('ctrl', 'w')

    @staticmethod
    def messanger(message, csvfile):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        list = current_time.split(':')
        h = int(list[0])
        m = int(list[1])
        m = m + 1
        if m > 59:
            m = 0
            h = h + 1
            if h > 23:
                h = 0
        with open(csvfile, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                try:
                    # _thread.start_new_thread(sendwhatmsg, ('+91' + str(row[1]), message, h, m))
                    sendwhatmsg('+91' + str(row[1]), message, h, m)
                    print("Message sent to " + str(row[0]))
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    list = current_time.split(':')
                    h = int(list[0])
                    m = int(list[1])
                    m = m + 1
                    if m > 59:
                        m = 0
                        h = h + 1
                        if h > 23:
                            h = 0
                except:
                    print('\nMessage Not Sent to ' + str(row[0]) + '\n')
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    list = current_time.split(':')
                    h = int(list[0])
                    m = int(list[1])
                    m = m + 1
                    if m > 59:
                        m = 0
                        h = h + 1
                        if h > 23:
                            h = 0

    @staticmethod
    def unknownNumber(message, phone):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        list = current_time.split(':')
        h = int(list[0])
        m = int(list[1])
        m = m + 1
        if m > 59:
            m = 0
            h = h + 1
            if h > 23:
                h = 0
        try:
            _thread.start_new_thread(sendwhatmsg, ('+91' + str(phone), message, h, m))
        except:
            print("Error: unable to start thread")
        # sendwhatmsg('+91' + str(phone), message, h, m)


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label1 = tk.Label(self, text="Bulk Whatsapp Messenger", foreground="red", font=("Times New Roman", 15))
        label1.pack(padx=50, pady=10)

        label2 = tk.Label(self, text="Don't Use PC during the process", foreground="red", font=("Times New Roman", 12))
        label2.pack(padx=50, pady=5)

        btn1 = tk.Button(self, text='Configuration Run', bd='5', command=lambda: controller.configurationRun())
        btn1.pack(padx=10, pady=10)

        btn2 = tk.Button(self, text='Message to Unknown Number', bd='5',
                         command=lambda: controller.show_frame(SingleMessage))
        btn2.pack(padx=10, pady=10)

        btn3 = tk.Button(self, text='Message to Multiple Numbers', bd='5',
                         command=lambda: controller.show_frame(MultiMessage))
        btn3.pack(padx=10, pady=10)

        btn4 = tk.Button(self, text="Developers", command=lambda: controller.show_frame(Developer))
        btn4.pack(pady=5)

        btn5 = tk.Button(self, text="Exit", command=lambda: controller.destroy_frame())
        btn5.pack(pady=5)


class Developer(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label1 = tk.Label(self, text="Bulk Whatsapp Messenger", foreground="red", font=("Times New Roman", 15))
        label1.pack(padx=50, pady=10)

        label3 = tk.Label(self, text="Aromal Joseph K M\n(S7 CSE)", foreground="green", font=("Times New Roman", 10))
        label3.pack()

        label4 = tk.Label(self, text="Team Ignited Minds", foreground="red", font=("Times New Roman", 10))
        label4.pack()

        button1 = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack(pady=5)

        button2 = tk.Button(self, text="Exit", command=lambda: controller.destroy_frame())
        button2.pack(pady=5)


class MultiMessage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label1 = tk.Label(self, text="Bulk Whatsapp Messenger", foreground="red", font=("Times New Roman", 15))
        label1.pack(padx=50, pady=10)

        label2 = tk.Label(self, text="Don't Use PC during the process", foreground="red", font=("Times New Roman", 12))
        label2.pack(padx=50, pady=5)

        label3 = tk.Label(self, text="Team Ignited Minds", foreground="red", font=("Times New Roman", 10))
        label3.pack()

        label4 = tk.Label(self, text="Message : ", foreground="red", font=("Times New Roman", 10), )
        label4.pack()
        entry1 = Entry(self, bd=4)
        entry1.pack()

        label5 = tk.Label(self, text="CSV file : ", foreground="red", font=("Times New Roman", 10), )
        label5.pack()

        button_explore = Button(self, text="Browse Files", command=browseFiles)
        button_explore.pack()

        global filename
        btn1 = tk.Button(self, text='Send', bd='5',
                         command=lambda: controller.messanger(entry1.get(), filename))
        btn1.pack(padx=10, pady=10)

        button1 = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack(pady=5)

        button2 = tk.Button(self, text="Exit", command=lambda: controller.destroy_frame())
        button2.pack(pady=5)


class SingleMessage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label1 = tk.Label(self, text="Bulk Whatsapp Messenger", foreground="red", font=("Times New Roman", 15))
        label1.pack(padx=50, pady=10)

        label2 = tk.Label(self, text="Don't Use PC during the process", foreground="red", font=("Times New Roman", 12))
        label2.pack(padx=50, pady=5)

        label3 = tk.Label(self, text="Team Ignited Minds", foreground="red", font=("Times New Roman", 10))
        label3.pack()

        label4 = tk.Label(self, text="Message : ", foreground="red", font=("Times New Roman", 10), )
        label4.pack()
        entry1 = Entry(self, bd=4)
        entry1.pack()

        label5 = tk.Label(self, text="Phone Number : ", foreground="red", font=("Times New Roman", 10), )
        label5.pack()
        entry2 = Entry(self, bd=4)
        entry2.pack()

        btn1 = tk.Button(self, text='Send', bd='5',
                         command=lambda: controller.unknownNumber(entry1.get(), entry2.get()))
        btn1.pack(padx=10, pady=10)

        btn2 = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        btn2.pack(pady=5)

        btn3 = tk.Button(self, text="Exit", command=lambda: controller.destroy_frame())
        btn3.pack(pady=5)


app = TimeTableApp()
app.mainloop()
