import paramiko
import CustomSpeech as winspeech
import WriteToFile as WTF

onceConnectionDone = False

def ExecuteLinuxScript(hostname,username,password,cmd):
    hostname = hostname
    username = username
    password = password

    cmd = cmd
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname,username=username,password=password)
        print("Connected to %s" % hostname)
        global onceConnectionDone
        if onceConnectionDone == False:
            winspeech.say_wait("Connection with server is successful")
            WTF.ChangeLogOnly(f"Connection to {hostname} is successful")
            onceConnectionDone = True
    except paramiko.AuthenticationException:
        print("Failed to connect to %s due to wrong username/password" %hostname)
        winspeech.say_wait("Failed to connect to %s due to wrong username/password" %hostname)
        exit(1)
    except Exception as e:
        print("error in ExecuteLinuxScript"+str(e))    
        exit(2)

    try:
        stdin, stdout, stderr = ssh.exec_command(cmd)
    except Exception as e:
        print("error in ExecuteLinuxScript"+str(e))    

    err = ''.join(stderr.readlines())
    out = ''.join(stdout.readlines())
    final_output = str(out)+str(err)
    #print(final_output)
    
    WTF.AppendStringToFile(final_output+"\n","ScriptOutputLog.txt")
    return final_output

#ExecuteLinuxScript("52.170.81.217","Buddy","Walnutbird1$","dir")