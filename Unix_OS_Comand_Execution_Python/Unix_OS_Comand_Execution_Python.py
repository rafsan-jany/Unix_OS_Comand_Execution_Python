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

def super_user(user_name_su, password_su, su_hint, new=False):      
    print ('Register as superuser: ')
    privilege = 'su' 
    
    a = dictionary_formation(user_name_su, password_su, su_hint, privilege, new)
    print a
    print user_name_su
    z_su = {}
    z_su[user_name_su] = 'su'
    y_su = json.dumps(z_su)
    
    with open('dp.txt','w') as su:
        su.write(y_su)
        
    b = json.dumps(a)
    with open('cp.txt','w') as f:
        f.write(b)    
    ArduinoSerial.write('IG100> {} registered as a super user. Thank You.\r\n'.format(str(user_name_su)))

def dictionary_formation(user_name_dict, password_dict, hint_dict, privilege, new):
    if new:
        a = {} # primary dictionary for user
    else:
        with open('cp.txt') as json_file:
            a = json.load(json_file)

    check_call(['useradd',user_name_dict])
        
    proc = Popen(['passwd', user_name_dict], stdin=PIPE,stderr=PIPE)
    proc.stdin.write(password_dict + '\n')
    proc.stdin.write(password_dict)
    proc.stdin.flush()
    stdout,stderr = proc.communicate() 
    
    user = user_name_dict
    date_gen = time.time()
    hint = hint_dict
    user_details = {} # secondary dictionary for user details
    user_details["up"] = privilege
    user_details["date_gen"] = date_gen
    user_details["hint"] = hint_dict
                
    a[user] = user_details #inserted data to primary dictionary 
    
    return a   
    
def reset_super_user_name_password():
    #global super_user_name
    ArduinoSerial.write('IG100> enter super user password to register as a new super user: ')
    #ArduinoSerial.write('IG100> register as super user: \r\n')
    reset_super_password = ArduinoSerial.readline().strip() 
    
    a, z_su, test_su_pass = check_super_user_name_password(reset_super_password)
    print a
    print z_su
    print test_su_pass
    
    super_user_name = z_su.keys()[0]
    #del a[super_user_name]
    
    #a_del = json.dumps(a) 
    #with open('cp.txt','w') as fa_del:
        #fa_del.write(a_del)
    
    username_su, password_su, password_hint_su = get_username_passsword_hint() ###
    print username_su
    print password_su
    
    super_user_name = z_su.keys()[0]
    print super_user_name
    
    if test_su_pass == True:
        del a[super_user_name]
        a_del = json.dumps(a)
        with open('cp.txt','w') as fa_del:
            fa_del.write(a_del)
        
        #del z_su[super_user_name]  
        #z_su_del = json.dumps(z_su)
        #with open('dp.txt','w') as fz_su_del:
            #fz_su_del.write(z_su_del)
        
        #delete(super_user_name, reset_super_password)
        
        super_user(username_su, password_su, password_hint_su, False)
        #ArduinoSerial.write('IG100> super user reset: \r\n')      
    else:
        ArduinoSerial.write('IG100> super user reset is not possible: \r\n')
        
    return 1

def check_super_user_name_password(super_password):
    with open('cp.txt','r') as fdel:
        a = json.loads(fdel.read()) 

    with open('dp.txt','r') as fsu:
        z_su = json.loads(fsu.read())
        
    super_user_name = z_su.keys()[0]
    #print super_user_name
    test_su_pass = login(super_user_name, super_password)
    #print test_su_pass
    return a, z_su, test_su_pass  
        
def get_username_passsword_hint():
    ArduinoSerial.write('IG100> enter username: ')
    uname = ArduinoSerial.readline().strip()
    
    ArduinoSerial.write('IG100> enter password: ')
    password_1 = ArduinoSerial.readline().strip()
    
    ArduinoSerial.write('IG100> re-type password: ')
    password_2 = ArduinoSerial.readline().strip()
    password = password_2
    
    while password_1 != password_2:
        ArduinoSerial.write("IG100> re-type password: ")
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
    
    ArduinoSerial.write('IG100> enter super user password: ')
    super_password = ArduinoSerial.readline().strip()  
    
    # verify super user name and password
    a, z_su, test_su_pass = check_super_user_name_password(super_password) 
    #print test_su_pass    
    
    while uname_reg1 in a:
        ArduinoSerial.write('IG100> {} already exists. please try a differnt one.\r\n'.format(str(uname_reg1)))
        username_reg3, password_reg3, password_hint_reg3 = get_username_passsword_hint() ### If user exists, take all input again 
        uname_reg1 = username_reg3
        password_reg1 = password_reg3
        password_hint_reg1 = password_hint_reg3
    
    #ArduinoSerial.write('IG100> choose privilege: "super user", "admin" or "user" ')
    ArduinoSerial.write('IG100> choose privilege: "admin" or "user" ')
    admin_priv = ArduinoSerial.readline().strip() 
    
    while admin_priv not in ['super user','admin','user']: 
        ArduinoSerial.write('IG100> please type between "admin" or "user"')
        admin_priv = ArduinoSerial.readline().strip()    
    
    if test_su_pass == True:
        new = False
        a = dictionary_formation(uname_reg1, password_reg1, password_hint_reg1, admin_priv, new)
    
        ArduinoSerial.write('IG100> {} is successfully registered \r\n'.format(str(uname_reg1)))

        b = json.dumps(a)
        with open('cp.txt','w') as f:
            f.write(b)
    else:
        ArduinoSerial.write('IG100> {} is not registered \r\n'.format(str(uname_reg1)))
    
    return 1
    
def login(user, password):
    global current_user, super_user_prevelige_flag
    try:
        enc_pwd = spwd.getspnam(user)[1]
        if crypt.crypt(password, enc_pwd) == enc_pwd:
            current_user = user
            super_user_prevelige_flag = True
            print "password matched"
            return True
        else:
            return "incorrect password"
    except KeyError:
        return "user '%s' not found" % user
    return "unknown error"
    
    
def delete(user, super_password):
    #ArduinoSerial = serial.Serial(usb_device_name,9600)

    #ArduinoSerial.write('IG100> enter super user password: ')
    #super_password = ArduinoSerial.readline().strip() 

    a, z_su, del_user_pass = check_super_user_name_password(super_password) # verify super user name and password
        
    if user not in z_su:
        if user in a:
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
                ArduinoSerial.write('IG100> wrong super user password \r\n')
        else:
            ArduinoSerial.write('IG100> {} not registered \r\n'.format(str(user)))
    else:
        ArduinoSerial.write('IG100> super user {} can not be deleted \r\n'.format(str(user)))
    return 1
    
def logout():
    ArduinoSerial.write('IG100> logged out. please type "login" or "register" ')
    log_out = ArduinoSerial.readline().strip()
    
    while log_out not in ['login','register']: 
        ArduinoSerial.write('IG100> please type between "login" or "register" ')
        log_out = ArduinoSerial.readline().strip()    
    
    if log_out == 'login':
        ArduinoSerial.write('IG100> enter username: ')
        username_log = ArduinoSerial.readline().strip()
        ArduinoSerial.write('IG100> enter password: ')
        password_log = ArduinoSerial.readline().strip()
        lp_out = login(username_log, password_log)
        
        while lp_out != True:
            ArduinoSerial.write('IG100> please type valid username and password \r\n')
            ArduinoSerial.write('IG100> enter username: ')
            username_log = ArduinoSerial.readline().strip()
            ArduinoSerial.write('IG100> enter password: ')
            password_log = ArduinoSerial.readline().strip()
            lp_out = login(username_log, password_log)
        
    elif log_out == 'register':
        username_reg, password_reg, password_hint_reg = get_username_passsword_hint()
        lp_reg = register(username_reg, password_reg, password_hint_reg)
        
    return 1

#while True:
while find_serial() == {}:
#while find_serial() == {'/dev/ttyUSB0': {'hwid': '0403:6001', 'port': '/dev/ttyUSB0', 'desc': 'FTDI FT232R USB UART 00000000'}}:
    #Check if serial module for CLI is present or not
    devices = find_serial()
    print devices
    #print(devices.items())
    try:
        devices_len = len(devices.items())
        devices = devices.items()
        ArduinoSerial = serial.Serial(devices[0][0],9600)
        print ArduinoSerial
    except:
        print("Failed to connect CLI")
    time.sleep (1)
    if find_serial() != {}:
        devices = find_serial()
        devices_len = len(devices.items())
        devices = devices.items()
        ArduinoSerial = serial.Serial(devices[0][0],9600)
        print 'After if '
    
        login_flag_t = 0
        register_flag_x = 0
        delete_flag_y = 0
        reset_flag_s = 0
        super_user_prevelige_flag = False
      
        with open('cp.txt','a+') as f:
        #with open('dp.txt','a+') as f:
            first = f.read(1)
            if not first:
                ArduinoSerial.write('IG100> register a super user account first. \r\n')
                username_su, password_su, password_hint_su = get_username_passsword_hint() ###
                #super_user(True)
                super_user(username_su, password_su, password_hint_su, True)
                #first_user = True
        #with open('cp.txt','a+') as file_json:
            #d = json.load(file_json)
        
        #ArduinoSerial.write('IG100> please type to proceed \r\n\t login\r\n\t register\r\n\t delete\r\n\t exit \0')
        ArduinoSerial.write('IG100> please type "login" or "register" ')    
        choice = ArduinoSerial.readline().strip()
        while choice not in ['login','register']: 
            ArduinoSerial.write('IG100> please type between "login" or "register" ')
            choice = ArduinoSerial.readline().strip()
            
        if choice == 'login': ################################LOGIN#################
            #username_password()
            ArduinoSerial.write('IG100> enter username: ')
            username = ArduinoSerial.readline().strip()
            ArduinoSerial.write('IG100> enter password: ')
            password = ArduinoSerial.readline().strip()
            status = login(username, password)
            print status
            if status == True:
                login_flag_t = 1
            else:
                login_flag_t = 0
           
            while status != True: 
                ArduinoSerial.write('IG100> please enter valid username and password \r\n')
                ArduinoSerial.write('IG100> enter valid username: ')
                username = ArduinoSerial.readline().strip()
                ArduinoSerial.write('IG100> enter valid password: ')
                password = ArduinoSerial.readline().strip()
                status = login(username, password)
                login_flag_t = 1
            
        elif choice == 'register': ##########################REGISTER####################
            username_reg, password_reg, password_hint_reg = get_username_passsword_hint() 
            register_flag_x = register(username_reg, password_reg, password_hint_reg)
            
        #elif choice == 'delete': ##########################DELETE####################
            #ArduinoSerial.write('IG100> username ')
            #username = ArduinoSerial.readline().strip()
            #delete_flag_y = delete(username)
        
        #elif choice == 'exit':
            #saveData()
            #quit()
            
        ########################USER_PREVELEGE#############################################   
        #print current_user + " Current User" 
        #with open('cp.txt','r') as fpre:
            #a = json.loads(fpre.read()) 
            
        #print super_user_prevelige_flag    
        #if super_user_prevelige_flag == True:
            #u_pre = a[current_user]['up']
            #print a[current_user]['up']
        #else:
            #print "please enter valid user name and password"
            #ArduinoSerial.write('IG100> please type valid username and password \r\n')
        #if u_pre == 'su':
            #console_sign = "IG100(config)#"
        #elif u_pre == 'admin':
            #console_sign = "IG100#"
        #else:
           # console_sign = "IG100>"
            
        if (login_flag_t == 1 or register_flag_x == 1):
            print "Welcome NS-OS"
            while True:
            #while ArduinoSerial:
                ArduinoSerial.write('IG100>')
                #ArduinoSerial.write(console_sign)
                #command = ArduinoSerial.readline().strip()
                command = ArduinoSerial.readline().strip()
                #while command in ['register','delete','logout']:
                if command == 'register':
                    try:
                        username_reg2, password_reg2, password_hint_reg2 = get_username_passsword_hint() ###
                        register_flag_x = register(username_reg2, password_reg2, password_hint_reg2)
                    except:
                        print 'port is closed'
                        break
                elif command == 'delete':
                    try:
                        ArduinoSerial.write('IG100> type username to be deleted: ')
                        username_1 = ArduinoSerial.readline().strip()
                        ArduinoSerial.write('IG100> enter super user password: ')
                        super_password = ArduinoSerial.readline().strip() 
                        delete_flag_y = delete(username_1, super_password)
                    except:
                        print 'port is closed : exception from inner delete'
                        break
                elif command == 'logout':
                    try:
                        #print current_user + " Current User" 
                        lop = logout()
                        #a[current_user]['up']
                        #print a[current_user]['up']
                        
                        #if u_pre == 'su':
                            #console_sign = "IG100(config)#"
                        #elif u_pre == 'admin':
                            #console_sign = "IG100#"
                        #else:
                            #console_sign = "IG100>" 
                    except:
                        print 'port is closed : exception from inner logout'
                        break
                elif command == 'reset':
                    try:
                        reset_flag_s = reset_super_user_name_password()
                    except:
                        print 'port is closed : exception from inner reset'
                        break
                elif command == 'help':
                    try:                   
                        ArduinoSerial.write('IG100> type "logout", "register", "delete", "reset" or "valid commands" \r\n')
                    except:
                        print 'port is closed : exception from inner help'
                else:
                    try:
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
                    except:
                        print 'port is closed : exception from inner command'
                        break
        else:
            ArduinoSerial.write('IG100> invalid user name or password \r\n')
    else: 
        print 'port not found!!!'