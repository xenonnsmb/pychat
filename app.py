import web
import re
import uuid
def sanitizeHTML(raw): # strip html tags from messages
        html_filter = re.compile('<.*?>')
        cleaned = re.sub(html_filter, '', raw)
        return cleaned
def make_text(string):
    return sanitizeHTML(string)

urls = ('/', 'login', '/chat', 'chat')
render = web.template.render('templates/')
global chatlog
chatlog = "Welcome to pychat 1.0, \"it sucks but not too much\" edition"
app = web.application(urls, globals())
my_form = web.form.Form(
                web.form.Textbox('', class_='textfield', id='textfield'),
                )
class ChatUser():
    def __init__(self):
        self.nick = "undefined"
        self.userid = "undefined"
    def printData(self):
        print(self.nick)
        print(self.userid)
    def searchId(self, userid):
        if (userid == self.userid):
            return True
        else:
            return False

global users
users = {}
class login:
    def GET(self): # this function is used to load the initial page
        global chatlog
        form = my_form()
        return render.login(form, "Welcome to pychat. Please type in a username and press enter or send.")

    def POST(self): # this function logs in the user
        global users
        global chatlog
        form = my_form()
        form.validates()
        s = form.value['textfield']
        requestKind = web.input().request_kind
        print(s)
        currentId = str(uuid.uuid4())
        users[currentId] = ChatUser()
        users[currentId].nick = s
        users[currentId].userid = currentId
        idToReturn = users[currentId].userid
        return idToReturn


class chat:
    def GET(self): # this function is used to load the initial page
        global chatlog
        form = my_form()
        return render.chat(form, "Connecting...")

    def POST(self): # this function is used to update the chatlog and post messages
        global chatlog
        global users
        nameForId = ""
        form = my_form()
        form.validates()
        s = form.value['textfield']
        requestKind = web.input().request_kind
        chatid = web.input().chatid
        #print(requestKind)
        #print(chatid)
        if (requestKind == "update"):
            #print("sending log to client: " + chatlog) This is only for debugging
            return chatlog
        elif (requestKind == "send"):
            nameForId = users[chatid].nick
            chatlog = chatlog + " <br> " + nameForId + ": " + make_text(s)
            #print("New chatlog: " + chatlog) This is only for debugging
            return chatlog
        else:
            return "Unknown request type"

if __name__ == '__main__':
    app.run()
