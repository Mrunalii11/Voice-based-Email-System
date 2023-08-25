import speech_recognition as sr
import easyimap as e
import pyttsx3
import smtplib

r=sr.Recognizer()
engine=pyttsx3.init()
voices=engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)
engine.setProperty('rate', 150)

def speak(str):
    print(str)
    engine.say(str)
    engine.runAndWait()

def listen():
    while True:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            # speak('Speak Now')
            aud=r.listen(source)
            try:
                text=r.recognize_google(aud)
                return text
                break
            except Exception as e:
                print(e)
                speak('Sorry could not recognize what you said!')
                continue       
speak('WELCOME TO THE VOICE-BASED E-MAIL SYSTEM')


def  your_mail():
    speak("Your E-mail ID please")
    email=listen()
    email="".join(email.split())
    if('attherate'in email):
        email=email.replace('attherate', '@')
        email=email.lower()
    if '@' in email:
        speak(email)
    else:
        speak('Wrong E-mail')
        return your_mail()       
    
    speak('Is this E-mail ID correct?')
    ans=listen()
    if ans=='no':
        return your_mail()
    else:
        return email

def psswd(): 
    speak("Password Please")
    pwd=listen()
    pwd="".join(pwd.split())
    if('attherate'in pwd):
        pwd=pwd.replace('attherate', '@')
        pwd=pwd.lower()
    speak(pwd)
    speak('Is this Password Correct?')
    ans=listen()
    if ans=='no':
        return psswd()
    else:
        return pwd

sender_email=your_mail()    
pwd=psswd()

def send_mail():
    def recv_mail():   
        speak("Say Receiver's E-mail ID")
        mail=listen()
        email="".join(mail.split())
        if('attherate'in email or 'at the rate' in email):
            email=email.replace('attherate','@')
            email=email.lower()
        speak("You said "+email)
        speak('Is this E-mail ID correct?')
        ans=listen()
        if ans == 'no':
            return recv_mail()
        else:
            return email
    recv=recv_mail()
    print(recv)
    
    speak('Please Convey your Messege')
    msg=listen()
    speak(msg)
    speak('You have Conveyed your Messege,should I send it ?')
    ans=listen()
    if 'YES' in ans or 'yes' in ans:
        server=smtplib.SMTP_SSL('smtp.gmail.com',465)    
        server.login(sender_email,pwd)
        server.sendmail(sender_email, recv, msg)
        server.quit()
        speak('Your Mail has been sent!')

def read_mail():
    server=e.connect('imap.gmail.com',sender_email,pwd,read_only=False)
    server.listids()
    def mails():
        speak('Say the Serial Number of E-mail you wanna read')
        a=listen()
        if(a=='Tu' or a=='two'):
            a='2'
        if (a=='free' or a=='re' or a=='tree'):
            a='3'
        if a.isdigit==False:
            a=listen()
        b=int(a)-1
        email=server.mail(server.listids()[b])
        speak('The E-mail is from:')
        speak(email.from_addr)
        speak('Sent on Date:')
        speak(email.date)
        speak('The Subject of E-mail is:')
        speak(email.title)
        speak("The Body of E-mail is:")
        speak(email.body)
    
        speak('Do you want to read more mails?')
        ans=listen()
        if ans=='yes':
            return mails()
        server.quit()
        
    mails()
while 1:   
    speak('What do you want to do?')
    speak('Say Send to Send a Mail      Read to Read inbox       Exit to Logout')
    ans=listen()

    if(ans=='send'):
        send_mail()
    elif (ans=='read'):
        read_mail()
    elif (ans=='exit'):
        exit(1)  