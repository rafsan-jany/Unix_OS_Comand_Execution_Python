#from __future__ import print_function
import os
import subprocess
import commands
import serial
import serial.tools.list_ports
import crypt # Interface to crypt(3), to encrypt passwords.
#import getpass # To get a password from user input.
import spwd # Shadow password database (to read /etc/shadow).
import json
import time
from subprocess import Popen, PIPE, check_call

print(time.time())
up = ["user","admin","su"]
#a = {}
#password_hint = ""

def super_user(user_name_su, password_su, su_hint, new=False):      
    print ('Register as superuser: ')
    
    check_call(['useradd',user_name_su])
        
    proc = Popen(['passwd', user_name_su], stdin=PIPE,stderr=PIPE)
    proc.stdin.write(password_su + '\n')
    proc.stdin.write(password_su)
    proc.stdin.flush()
    stdout,stderr = proc.communicate() 
                
    if new:
        a = {} # primary dictionary for user
    else:
        with open('cp.txt') as json_file:
            a = json.load(json_file)
                
    user = user_name_su
    date_gen = time.time()
    hint = su_hint
    user_details = {} # secondary dictionary for user details
    user_details["up"] = up[2]
    user_details["date_gen"] = date_gen
    user_details["hint"] = su_hint
                
    a[user] = user_details #inserted data to primary dictionary  

    z_su = {}
    z_su[user_name_su] = 'su'
    y_su = json.dumps(z_su)
    with open('dp.txt','a+') as su:
        su.write(y_su)
        
    b = json.dumps(a)
    f.write(b)    
    ArduinoSerial.write('IG100> {} registered as a super user. Thank You.\r\n'.format(str(user_name_su)))
    
    
def check_super_user_name_password(super_password):
    with open('dp.txt','r') as fsu:
        z_su = json.loads(fsu.read())
        
    super_user_name = z_su.keys()[0]
    #print super_user_name
    test_su_pass = login(super_user_name, super_password)
    #print test_su_pass
    return test_su_pass

    
'''def reset_superuser(reset_super_user_name, reset_super_user_password):
    with open('dp.txt','r+') as fff:
        dp = json.loads(fff.read())
        
    with open('cp.txt','r+') as aaa:
        ap = json.loads(aaa.read())
    
    pass'''
    
        
def u_p():
    ArduinoSerial.write('IG100> enter username: ')
    uname = ArduinoSerial.readline().strip()
    
    ArduinoSerial.write('IG100> enter password: ')
    password_1 = ArduinoSerial.readline().strip()
    
    ArduinoSerial.write('IG100> re-type password: ')
    password_2 = ArduinoSerial.readline().strip()
    password = password_2
    
    while password_1 != password_2:
        ArduinoSerial.write = ('IG100> re-type password: ')
        password_2 = ArduinoSerial.readline().strip()
        password = password_2
        
    ArduinoSerial.write('IG100> password hint: ')
    password_hint = ArduinoSerial.readline().strip()
    
    return uname, password, password_hint
    
def find_serial():
    list = serial.tools.list_ports.comports()
    device_info = {}
    valid_hwid = ['0403:6001','067b:2303']
    for element in list:
        #connected.append(element[0])
        device_info[element[0]] = {}
        try:
            hwid = element[2][element[2].find('VID:PID=')+len('VID:PID='):element[2].find('VID:PID=')+len('VID:PID=')+9]
        except:
            hwid = 'n/a'
        if(hwid != 'n/a' and hwid in valid_hwid):
            #print element[0]
            device_info[element[0]]['port'] = element[0]
            device_info[element[0]]['desc'] = element[1]
            device_info[element[0]]['hwid'] = hwid #element[2]
            #ArduinoSerial = serial.Serial(element[0],9600) 
        else:
            device_info.pop(element[0])
    return device_info
#print("Connected COM ports: " + str(connected))
#print(device_info)

def register(uname_reg1, password_reg1, password_hint_reg1):
    #ArduinoSerial = serial.Serial(usb_device_name,9600)
    user_details = {} # secondary dictionary for user details
    
    with open('cp.txt','r') as f:
        a = json.loads(f.read())

    while uname_reg1 in a:
        ArduinoSerial.write('IG100> {} already exists. Please Try a differnt one.\r\n'.format(str(uname_reg1)))
        username_reg3, password_reg3, password_hint_reg3 = u_p()   
        uname_reg1 = username_reg3
        password_reg1 = password_reg3
        password_hint_reg1 = password_hint_reg3
    
    ArduinoSerial.write('IG100> choose admin privilege\r\n\t super user\r\n\t admin\r\n\t user')
    admin_priv = ArduinoSerial.readline().strip()

    user_details["up"] = admin_priv
    
    ArduinoSerial.write('IG100> enter your super user password: ')
    super_password = ArduinoSerial.readline().strip()

    test_su_pass = check_super_user_name_password(super_password) # verify super user name and password 
    #print test_su_pass
    
    if test_su_pass == True:
        check_call(['useradd',uname_reg1])
        print 'Hello'
        proc = Popen(['passwd', uname_reg1], stdin=PIPE,stderr=PIPE)
        proc.stdin.write(password_reg1 + '\n')
        proc.stdin.write(password_reg1)
        proc.stdin.flush() 
        stdout,stderr = proc.communicate()    
    
        ArduinoSerial.write('IG100> {} is successfully registered! \r\n'.format(str(uname_reg1)))
        user = uname_reg1
        date_gen = time.time()
        hint = password_hint_reg1
        #user_details = {} 
        #user_details["up"] = up[admin_priv]
        user_details["date_gen"] = date_gen
        user_details["hint"] = password_hint_reg1
                
        a[user] = user_details #inserted data to primary dictionary 

        b = json.dumps(a)
        
        with open('cp.txt','w') as f:
            f.write(b)
    else:
        ArduinoSerial.write('IG100> {} is not registered! \r\n'.format(str(uname_reg1)))
    
    return 1
    
def login(user, password):
    try:
        enc_pwd = spwd.getspnam(user)[1]
        if crypt.crypt(password, enc_pwd) == enc_pwd:
            print "password matched"
            return True
        else:
            return "incorrect password"
    except KeyError:
        return "user '%s' not found" % user
    return "unknown error"
    
    
def delete(user):
    #ArduinoSerial = serial.Serial(usb_device_name,9600)
    
    with open('cp.txt','r') as fdel:
        a = json.loads(fdel.read())
        #print a
        
    #print a[user]
    with open('dp.txt','r') as fsu:
        z_su = json.loads(fsu.read())
        
    if user not in z_su:
        if user in a:
            super_user_name = z_su.keys()[0]
            #print super_user_name
                
            ArduinoSerial.write('IG100> enter super user password: ')
            super_password = ArduinoSerial.readline().strip()
            
            del_user_pass = login(super_user_name, super_password) # verify super user name and password
            #print del_user_pass
            
            if del_user_pass == True:
                with open("/etc/passwd","r+") as f:
                    new_f = f.readlines()
                    f.seek(0)
                    for line in new_f:
                        if user not in line:
                            f.write(line)
                    f.truncate()

                with open("/etc/shadow","r+") as f:
                    new_f = f.readlines()
                    f.seek(0)
                    for line in new_f:
                        if user not in line:
                            f.write(line)
                    f.truncate()
                
                with open("/etc/group","r+") as f:
                    new_f = f.readlines()
                    f.seek(0)
                    for line in new_f:
                        if user not in line:
                            f.write(line)
                    f.truncate()
                
                del a[user]
                
                a_del = json.dumps(a) 
                with open('cp.txt','w') as fa_del:
                    fa_del.write(a_del)
                
                ArduinoSerial.write('IG100> {} deleted \r\n'.format(str(user)))
        else:
            ArduinoSerial.write('IG100> {} not registered \r\n'.format(str(user)))
    else:
        ArduinoSerial.write('IG100> super user {} can not be deleted \r\n'.format(str(user)))
    return 1
    
def logout(): ########################################################################################LOGOUT
    ArduinoSerial.write('IG100>you are logged out. please type login or register!')
    log_out = ArduinoSerial.readline().strip()
    
    if log_out == 'login':
        ArduinoSerial.write('IG100> username ')
        username_log = ArduinoSerial.readline().strip()
        ArduinoSerial.write('IG100> password ')
        password_log = ArduinoSerial.readline().strip()
        lp_out = login(username_log, password_log)
    elif log_out == 'register':
        lp_reg = register()
        
    return 1

while True:
    #Check if serial module for CLI is present or not
    devices = find_serial()
    #print(devices.items())
    try:
        devices_len = len(devices.items())
        devices = devices.items()
        ArduinoSerial = serial.Serial(devices[0][0],9600)
    except:
        print("Failed to connect CLI")

    t = 0
    x = 0
    y = 0
    
    with open('cp.txt','a+') as f:
        first = f.read(1)
        if not first:
            ArduinoSerial.write('IG100> Register a Super user account first. \r\n')
            username_su, password_su, password_hint_su = u_p()
            #super_user(True)
            super_user(username_su, password_su, password_hint_su, True)
    
    ArduinoSerial.write('IG100> please type to proceed \r\n\t login\r\n\t register\r\n\t delete\r\n\t exit \0')
    choice = ArduinoSerial.readline().strip()
    while choice not in ['login','register','delete','exit']: 
        ArduinoSerial.write('IG100> please type betwwen "login", "register", "delete", "exit"')
        choice = ArduinoSerial.readline().strip()
        
    if choice == 'login': ################################LOGIN#################
        #username_password()
        ArduinoSerial.write('IG100> username ')
        username = ArduinoSerial.readline().strip()
        ArduinoSerial.write('IG100> password ')
        password = ArduinoSerial.readline().strip()
        status = login(username, password)
        if status == True:
            print("Logged in!")
            t = 1
        else:
            print("Login failed, %s." % status)
            t = 0
        
    elif choice == 'register': ##########################REGISTER####################
        username_reg, password_reg, password_hint_reg = u_p()
        x = register(username_reg, password_reg, password_hint_reg)
        #x = register()
        
    elif choice == 'delete': ##########################DELETE####################
        ArduinoSerial.write('IG100> username ')
        username = ArduinoSerial.readline().strip()
        y = delete(username)
    
    elif choice == 'exit':
        #saveData()
        quit()
        
    if (t == 1 or x == 1 or y == 1):
        print "Welcome NS-OS"
        while True:
            ArduinoSerial.write('IG100>')
            #command = ArduinoSerial.readline().strip()
            command = ArduinoSerial.readline().strip()
            #while command in ['register','delete','logout']:
            if command == 'register':
                username_reg2, password_reg2, password_hint_reg2 = u_p()
                x = register(username_reg2, password_reg2, password_hint_reg2)
            elif command == 'delete':
                ArduinoSerial.write('IG100> username ')
                username_1 = ArduinoSerial.readline().strip()
                y = delete(username_1)
            elif command == 'logout':
                logout()
            else:       
                #print command
                com_output = commands.getoutput(command) #commands : For linux commands output
                #ArduinoSerial.writelines(com_output.strip())
                #print com_output
                a = []
                for i in com_output.split('\n'):
                    a.append(i)
                    a.append('\r') #add carriage 
                    a.append('\n') #add newline
                ArduinoSerial.writelines(a)
                #print device, '-->', info
    else:
        ArduinoSerial.write('IG100> invalid\r\n')
    