from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import pywinauto.application, pywinauto.findwindows
f_app = Flask(__name__)
ask = Ask(f_app, '/System_Control')

def startApplication(application):
    app = pywinauto.application.Application().start(application)
    return app

def closeApplication(application):
    search_str = ".*" + application + ".*"
    if(len(pywinauto.findwindows.find_elements(title_re=search_str))!= 1):
        print("Not specific enough, sorry")
        print("Applicable values:")
        for i in pywinauto.findwindows.find_elements(title_re=search_str):
            print(i.name)
    else:
        app = pywinauto.application.Application()
        app.connect(title_re=search_str)
        app.Kill_()
    return

def keyInputtoApplication(application, inp):
    searchAppString = ".*" + application
    app = pywinauto.application.Application()
    if(len(pywinauto.findwindows.find_elements(title_re=searchAppString))!= 1):
        print("Not specific enough, sorry")
        print("Applicable values:")
        for i in pywinauto.findwindows.find_elements(title_re=searchAppString):
            print(i.name)
    else:
        app.connect(title_re=searchAppString)
        try:
            for window in app.windows_():
                if(window.IsVisible()):
                    window.TypeKeys(inp, with_spaces=True)
        except:
            print("Error")
        
    return


def stringFormat(string):
    reference = {
        "find":"^f",
        "enter":"~",
        "alt":"%",
        "save":"^s",
        "delete":"{DELETE}",
        "control":"^"
    }
    words = string.split()
    for index, value in enumerate(words):
        words[index] = reference.get(value.lower(), value)
    return " ".join(words)



def runningApplications(search=0):
    if(search != 0):
        search_str = ".*" + search
    else:
        search_str = ""
    out = []
    for i in pywinauto.findwindows.find_elements(title_re=search_str):
        if i.name != "":
            out.append(i.name + " ... ")
    return "".join(out)






@ask.launch
def launchMessage():
    start_message = "System Control system successfully intialized. You can now enter commands."
    return statement(start_message).simple_card('Started system', start_message)


@ask.intent("RunningApplications")
def ReturnRunningApps():
    applist = runningApplications()
    return statement(applist)

@ask.intent("RunningApplicationsNamed")
def ReturnRunningAppswName(appname):
    applist = runningApplications(appname)
    return statement(applist)

@ask.intent("StartApplications")
def RespondStartApplication(appname):
    startApplication(appname)
    return_msg = appname + " has been successfully started."
    return statement(return_msg).simple_card('Started application', appname)

@ask.intent("StopApplication")
def RespondStopApplication(appname):
    closeApplication(appname)
    return_msg = appname + " has been successfully stopped."
    return statement(return_msg).simple_card('Stopped application', appname)

@ask.intent("InputTextApplication")
def RespondInputTexttoApplication(appname, inp):
    keyInputtoApplication(appname, stringFormat(inp))
    return_msg = "Sent message " + inp + " to application " + appname + "."
    return statement(return_msg).simple_card('Sent Message to Application', appname)




if __name__ == '__main__':
    f_app.run(debug=True)










