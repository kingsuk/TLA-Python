import ScriptExecutionHelper as SEHelper

hostname = "104.41.150.81"
username = "acn_root"
password = "Acn_root1234"
cmd = "sudo sh -x /usr/local/scripts/unix_04_automation_local/lvcreatelinux.sh oradata"

returnValue = SEHelper.ExecuteLinuxScript(hostname,username,password,cmd)
print(returnValue)