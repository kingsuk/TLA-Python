import paramiko
import winspeech

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
        #winspeech.say_wait("Connected to %s" % hostname)
    except paramiko.AuthenticationException:
        return "Failed to connect to %s due to wrong username/password" %hostname
        exit(1)
    except Exception as e:
        print(e.message)    
        exit(2)

    try:
        stdin, stdout, stderr = ssh.exec_command(cmd)
    except Exception as e:
        print(e.message)

    err = ''.join(stderr.readlines())
    out = ''.join(stdout.readlines())
    final_output = str(out)+str(err)
    #print(final_output)
    return final_output