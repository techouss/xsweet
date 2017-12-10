from core.xsweet_process_cmd import ProcessCmd
from core.xsweet_logging import *

def process_command(data, transport, attacker_username, ip, fake_workingdir):
    printlinebreak = 0
    cmd = ''
    params = ''
    data = data.strip()
    message = "COMMAND: " + data+"\n"
    writetosession(ip,message)
    transport.write('\r\n')
    data=data.split()
    if len(data)>0:
        cmd = data[0]
    if len(data)>1:
        params=data[1:len(data)]
    cmd_processor = ProcessCmd(cmd, params, transport, attacker_username, ip, fake_workingdir)
    (fake_workingdir, attacker_username) = cmd_processor.get_values()
    # return some values so they remain dynamic        
    return (printlinebreak, fake_workingdir, attacker_username)

