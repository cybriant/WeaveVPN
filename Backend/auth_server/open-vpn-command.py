import subprocess
import os
# Some commands to install OpenVPN on Linux
'''
bashCommand = "sudo apt-get install openvpn; sudo openvpn --config ./config.ovpn"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE, shell=True)
output, error = process.communicate()

subprocess.call(["sudo", "apt-get", "install", "openvpn"])
subprocess.call(["sudo", "openvpn", "--config", "./config.ovpn"])
'''


''' 
Commands to generate certificate and keys 
Must be in the OpenVPN\easy-rsa folder to run commands
Must have the cmd in admin mode
All of this was runned on Windows
'''

#os.system('start /wait cmd /k "cd C:\Program Files\OpenVPN\easy-rsa"')

subprocess.call("init-config", shell=True)
#subprocess.call("vars.bat", shell=True)
subprocess.call("clean-all", shell=True)
subprocess.call("build-dh", shell=True)
subprocess.call("build-ca", shell=True)
subprocess.call("build-key-server ServerVPN", shell=True)
subprocess.call("build-key ClientVPN", shell=True)
subprocess.call("openvpn --genkey --secret keys/ta.key", shell=True)
