from Tkinter import *
import threading
import time
import random

class App:

    def __init__(self, master):

        frame1 = LabelFrame(master, text="Group", padx=5, pady=5)
        frame1.pack(fill=X)

        self.button = Button(frame1, text="QUIT", fg="red", command=frame1.quit)
        self.button.pack(side=LEFT)

        self.hi_there = Button(frame1, text="Hello", command=self.say_hi)
        self.hi_there.pack(side=LEFT)

        frame2 = LabelFrame(master, text="Group", padx=5, pady=5)
        frame2.pack(fill=X)

        self.button = Button(frame2, text="QUIT", fg="red", command=frame2.quit)
        self.button.pack(side=LEFT)

        self.hi_there = Button(frame2, text="Hello", command=self.say_hi)
        self.hi_there.pack(side=LEFT)
 
        self.var = IntVar()

        frame3 = LabelFrame(master, text="switch", padx=5, pady=5)
        frame3.pack(fill=X)
        c = Checkbutton(frame3, text="Expand", variable=self.var)
        c.pack(side=LEFT)

        frame4 = LabelFrame(master, text="state", padx=5, pady=5)
        frame4.pack(fill=X)
        self.v = StringVar()
        self.v.set("STATE")
        w = Label(frame4, textvariable=self.v)
        w.pack(side=LEFT)

        logFrame = LabelFrame(master, text="events", padx=5, pady=5)
        logFrame.pack(fill=X)
        scrollb  = Scrollbar(logFrame, orient=VERTICAL)
        #self.log = Text(logFrame, wrap=NONE, setgrid=True)
        self.log = Text(logFrame, wrap=NONE)
        self.log.pack(fill=X)
        self.log.config(yscrollcommand = scrollb.set)
        self.log.pack(side=LEFT, fill=BOTH, expand=True)
        scrollb.config(command = self.log.yview) 
        scrollb.pack(side=RIGHT, fill=Y)


        frame5 = LabelFrame(master, text="reader", padx=5, pady=5)
        frame5.pack(fill=X)
        self.e = Entry(frame5)
        self.e.pack(side=LEFT)
        b = Button(frame5, text="read", width=10, command=self.read)
        b.pack(side=LEFT)


    def say_hi(self):
        print "hi there, everyone: " + str(self.var.get())
        self.v.set("New Text!" + str(self.var.get()))
        self.log.insert('end', "An event" + "\n")

    def read(self):
        print "hi there, everyone: " + str(self.var.get())
        self.log.insert('end', self.e.get() + "\n")

class ThreadedClient:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """
    def __init__(self, master):
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI as well. We spawn a new thread for the worker (I/O).
        """
        self.master = master
        self.rand = random.Random()

        # Set up the GUI part
        frame4 = LabelFrame(master, text="state", padx=5, pady=5)
        frame4.pack(fill=X)
        self.v = StringVar()
        self.v.set("STATE")
        w = Label(frame4, textvariable=self.v)
        w.pack(side=LEFT)

    def startThread(self):
        # Set up the thread to do asynchronous I/O
        # More threads can also be created and used, if necessary
        self.running = 1
        self.thread1 = threading.Thread(target=self.workerThread1)
        self.thread1.setDaemon(True)
        self.thread1.start(  )


    def workerThread1(self):
        """
        This is where we handle the asynchronous I/O. For example, it may be
        a 'select(  )'. One important thing to remember is that the thread has
        to yield control pretty regularly, by select or otherwise.
        """
        while True:
            # To simulate asynchronous I/O, we create a random number at
            # random intervals. Replace the following two lines with the real
            # thing.
            time.sleep(self.rand.random(  ) * 1.5)
            msg = self.rand.random(  )
            self.v.set("Random: " + str(msg))
            print("Random: " + str(msg))

class GUIThread:

    def __init__(self, master):
        self.root = master

    def startThread(self):
        # Set up the thread to do asynchronous I/O
        # More threads can also be created and used, if necessary
        self.running = 1
        self.thread1 = threading.Thread(target=self.workerThread1)
        self.thread1.setDaemon(True)
        self.thread1.start(  )

    def workerThread1(self):
        self.root.mainloop()

root = Tk()

app = App(root)

client = ThreadedClient(root)
client.startThread()

#gui = GUIThread(root)
#gui.startThread()
root.mainloop()
root.destroy() # optional; see description below
time.sleep(15)
