import paramiko
import select
import re

interesting_line_pattern = re.compile('xxx')

def do_tail():
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    from os.path import expanduser
    home = expanduser("~")
    client.connect('104.41.150.81',
                   username='acn_root',
                   password='Acn_root1234')

    log_file = '/usr/local/scripts/unix_04_automation_local/logs/unix04_main.sh.log'
    grep_pattern = "grep_filter"
    #remote_command = 'tail -50f %s | grep --line-buffered "%s" ' % (log_file, grep_pattern)
    remote_command = "tail -50f /usr/local/scripts/unix_04_automation_local/logs/unix04_main.sh.log"
    print(remote_command)

    transport = client.get_transport()
    channel = transport.open_session()
    channel.exec_command(remote_command)

    while 1:
        try:
            rl, _, _ = select.select([channel], [], [], 0.0)
            if len(rl) > 0:
                print ("ready to read")
                for line in linesplit(channel):
                    print (line)

        except (KeyboardInterrupt, SystemExit):
            print ('got ctrl+c')
            break

    client.close()
    print ('client closed')

def linesplit(socket):
    buffer_string = socket.recv(4048)
    done = False
    while not done:
        if str.encode("\n") in buffer_string:
            (line, buffer_string) = buffer_string.split(str.encode("\n"), 1)
            yield line + str.encode("\n")
        else:
            more = socket.recv(4048)
            if not more:
                done = True
            else:
                buffer_string = buffer_string + more
    if buffer_string:
        yield buffer_string


if __name__ == '__main__':

    do_tail()
