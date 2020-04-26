import subprocess
import os
'''
bashCommand = "sudo apt-get install openvpn; sudo openvpn --config ./config.ovpn"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE, shell=True)
output, error = process.communicate()
'''

# subprocess.call(["sudo", "apt-get", "install", "openvpn"])
# subprocess.call(["sudo", "openvpn", "--config", "./config.ovpn"])
os.system('start /wait cmd /k "cd C:\Program Files\OpenVPN\easy-rsa"')
