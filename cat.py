CAT_SCRIPT_VERSION = "1.1.3"

#                                                                                       .
#             _______   _____,,,--,-----------,                                         .
#           ,' ,'    '-/  /     |_|_,,    ,,  |                                         .
#         ,' ,'   ,';  /,'  /|   \/  /   /''''                                          .
#        /  /   ,'-'--: |  | _:   ',/   /                                               .
#       |  |   ;     |  |   '_,'\   \  |                                                .
#       ', ',   ;_ __',  ',  \   |   |  \                                               .
#         ', ',   '-_| \  ',  |  |   |   \                                              .
#           ', ',       \__/__|  |   |\   \                                             .
#             ', ',     / ___/__/   /--'   \                                            .
#               \__\___/  \__\_____/|______|                                            .
#              _________       .          ____     __________    ____                   .
#               /      /     ,'|       ,-'    ';  /    /    / ,''   '\                  .
#              /            /  |     ,'       '' /    /    / /      ,'                  .
#             /______/    ,'   |    /                /       '',_                       .
#            /      /  __/_____|_  /                /            ''-,                   .
#           /          ,'      |   |               /        ,        \                  .
#          /          /        |    \       _     /        |         |                  .
#        _/\_      _,'        _|_    ',   __,'  _/_         \______,/                   .
#         ''      '  '        '''      ''''     ''             '''                      .
#                                                                                       .

with open("header.txt", "r") as file:
    print(file.read())

import socket
import time
import keyboard
import sys

import random

import struct

from pynput.keyboard import Key, Listener

# we dont really use pyperclip for anything
#try:
#    import pyperclip
#except ImportError:
#    print("Module pyperclip not installed. Please run `pip install pyperclip`")
#    os._exit(0)

import tkinter as tk
from tkinter import filedialog

from pathlib import Path

from pyKey import pressKey, releaseKey, press, sendSequence, showKeys
import keyboard

import re

import requests

import os

# UPDATE CHECKER
update_data = requests.get("https://raw.githubusercontent.com/hi-sobe/catfacts/refs/heads/main/cat.py")
update_version = re.search("CAT_SCRIPT_VERSION = \"(\\S*)\"", update_data.text)
if update_version:
    if update_version.group(1)!=CAT_SCRIPT_VERSION:
        changelog_data = requests.get("https://raw.githubusercontent.com/hi-sobe/catfacts/refs/heads/main/CHANGELOG.md")
        changelog_log = re.search("(?s)## " + update_version.group(1) + "\n(.*?)\n\n", changelog_data.text)
        print("\aUPDATE AVAILABLE!\nCurrent version: " + CAT_SCRIPT_VERSION + "\nNew version:\t " + update_version.group(1))
        if changelog_log:
            print("Changelog:")
            print(changelog_log.group(1))
        response = input("Terminate script? [Y/N]: ")
        print("If you've made any local changes to the script, remember to back them up before you update!")
        print("Download the newest version of the script at https://github.com/hi-sobe/catfacts")
        if response.lower() == "y":
            quit()

# PROMPT GAME TYPE IF NO ARGUMENTS PROVITED
if len(sys.argv)==1:
    response = input("start in cs mode? [Y/N]: ")
    if response.lower() == "y":
        sys.argv.append("cs")
    elif response.lower() == "n" or response == "":
        sys.argv.append("tf")
game_type = ""
if sys.argv[1]=="cs": # give time to alt tab for cs for keybind
    game_type = "cs"
    time.sleep(2)
elif sys.argv[1]=="tf":
    game_type = "tf"

# set to True if another script user is detected in chat
script_conflict_disabled = False

# set to True when connecting to server, can be disabled using cat_off
allowchatprompt = False

# number of lines to display in terminal output (default: 10)
CONSOLE_MESSAGE_LIMIT = 10
# terminal output handler
serverconmessage = ""
CONSOLE_MESSAGES = [
    "Script launched",
    "Waiting for connection...",
    "======================="
]
for i in range(CONSOLE_MESSAGE_LIMIT-len(CONSOLE_MESSAGES)):
    CONSOLE_MESSAGES.insert(3,"")

# print text to specific line in terminal output, defined by pos
# lines 0-2 are reserved for connection status, prompt status, divider
def console_raw(m, pos):
    if pos < CONSOLE_MESSAGE_LIMIT:
        CONSOLE_MESSAGES[pos] = m
# print line of text to output log beneath divider
def console_log(m):
    CONSOLE_MESSAGES.insert(3,m)
    del CONSOLE_MESSAGES[CONSOLE_MESSAGE_LIMIT:]

LINE_UP = "\033[1A"
LINE_CLEAR = "\033[2K"
def clearlines(n):
    clearer=""
    for i in range(n):
        clearer+="\r"+LINE_UP+LINE_CLEAR
    print(clearer, end="")
def print_console_output():
    clearlines(CONSOLE_MESSAGE_LIMIT)
    cm=""
    for i in range(CONSOLE_MESSAGE_LIMIT):
        if i<len(CONSOLE_MESSAGES):
            cm=cm+CONSOLE_MESSAGES[i][:100]+"\n"
        else:
            cm=cm+"\n"
    print(cm,end="")
cm1=LINE_UP
for line in CONSOLE_MESSAGES:
    cm1+="\n"+line
print(cm1)

# debugmode: raw print() all tf2 console output, plus some debug info
# silent:    disable chat prompt
debugmode = False
silent = False
if len(sys.argv)>=3:
    if sys.argv[2] == "debug" or sys.argv[2] == "d":
        debugmode = True
    elif sys.argv[2] == "silent" or sys.argv[2] == "s":
        silent = True
    elif sys.argv[2] == "sd":
        silent = True
        debugmode = True

# load script settings
path_tf = ""
path_cs = ""
path_cs_cfg = ""
rconpassword = ""
try:
    with open("catsettings.txt", "r") as f:
        content = f.read()
        path_tf_temp = re.search("path_tf: (.+)", content)
        rconpassword_temp = re.search("RCON_PASSWORD: (.+)", content)
        #print(path_tf_temp)
        #print(content)
        path_cs_temp = re.search("path_cs: (.+)", content)
        path_cs_cfg_temp = re.search("path_cs_cfg: (.+)", content)
        if path_tf_temp:
            path_tf=path_tf_temp.group(1)
        if path_cs_temp:
            path_cs=path_cs_temp.group(1)
        if path_cs_cfg_temp:
            path_cs_cfg=path_cs_cfg_temp.group(1)
        if rconpassword_temp:
            rconpassword=rconpassword_temp.group(1)
except FileNotFoundError:
    with open("catsettings.txt", "a") as f:
        f.write("CAT SETTINGS\n")
# userinput for settings on first load
if sys.argv[1]=="tf":
    if rconpassword == "":
        rconpassword = input("rcon password not set! please enter your rcon password: ")
        with open("catsettings.txt", "a") as f:
            f.write("RCON_PASSWORD: " + rconpassword + "\n")
    if not Path(path_tf).exists():
        print("tf2 console.log not found! please select path to \\tf\\console.log now.")
        time.sleep(2)
        path_tf = filedialog.askopenfilename()
        print(path_tf)
        if not Path(path_tf).exists():
            raise ValueError("how did you fuck this up")
        match = re.search("/tf/console.log", path_tf)
        if not match:
            raise ValueError("that's not tf2 console.log!! do it right next time!!! dude!! come on!!!!!")
        if match.group() != "/tf/console.log":
            raise ValueError("whaahwawawawawawa aaoouuuuu")
        with open("catsettings.txt", "a") as f:
            f.write("path_tf: " + path_tf + "\n")
if sys.argv[1]=="cs":
    if debugmode==True:
        print("LAUNCHING IN CS MODE")
    if not Path(path_cs).exists():
        print("cs2 console.log not found! please select path to \\Counter-Strike Global Offensive\\game\\csgo\\console.log now.")
        time.sleep(2)
        path_cs = filedialog.askopenfilename()
        print(path_cs)
        if not Path(path_cs).exists():
            raise ValueError("how did you fuck this up")
        match = re.search("/csgo/console.log", path_cs)
        if not match:
            raise ValueError("that's not console.log!! do it right next time!!! dude!! come on!!!!!")
        if match.group() != "/csgo/console.log":
            raise ValueError("whaahwawawawawawa aaoouuuuu")
        with open("catsettings.txt", "a") as f:
            f.write("path_cs: " + path_cs + "\n")

        configdirectory = re.search("(.+)console.log", path_cs)
        path_cs_cfg = configdirectory.group(1) + "cfg/sobecatfacts.cfg"
        if not Path(path_cs_cfg).exists():
            with open(path_cs_cfg, "a") as f:
                f.write("hi!")
        with open("catsettings.txt", "a") as f:
            f.write("path_cs_cfg: " + path_cs_cfg + "\n")

currentfact="" # i dont know why i define this here lool watevere

stuffcounter = -1

# simulate this keypress for cs2, since rcon doesn't work
csmsgbind = "f13"

# timing for chat prompt in seconds
# every time chat prompt is sent, interval is set to a random value between intervalmin and intervalmax
lasttime = 0
interval = 120
intervalmin = 90
intervalmax = 180

# used to distinguish chat messages from ordinary console output
# chat messages separated by two spaces in tf2, one space in cs2
path_use = ""
commandstring = ""
if sys.argv[1]=="tf":
    path_use=path_tf
    commandstring = ":  "
    exitstring = "Shutdown function"
else:
    path_use=path_cs
    commandstring = ": "
    exitstring = "Source2Shutdown"

# fingerprint used to detect other script users, shutdown all but one
bot_ident="\x9d"
fingerprint_chars = "\x01\x02\x03\x04\x05\x06\x08\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1c\x1d\x1e\x1f"
fingerprint = ""
fingerprint_community=""
# reroll fingerprint, runs every time client connects to a server
def roll_fingerprint():
    global fingerprint
    global fingerprint_community
    fingerprint = ""
    fingerprint_community=""
    for i in range(3):
        fingerprint=fingerprint+fingerprint_chars[random.randint(0,len(fingerprint_chars)-1)]
    if debugmode == True:
        print("local fingerprint: ", end="")
        print(fingerprint.encode())
    else:
        console_log("set pub fingerprint: " + str(fingerprint.encode())[2:-1])
    fingerprint_community = "["+str(random.randint(0,999))+"] "
    if debugmode == True:
        print("local community fingerprint: ", end="")
        print(fingerprint_community)
    else:
        console_log("set community fingerprint: " + fingerprint_community)
    print_console_output()
roll_fingerprint()

# default to using community compatibility mode, set to False when client connects to a valve pub server
community_compat = True

## RCON STUFF HERE 

# generate packet structure for rcon commands
# cmdindex is arbitrary, rcon server expects an id for every packet
# if you touch anything else everything will fall apart

cmdindex = 8 # oi dpmt lmpw ;p; lol lol Watver
def msgpacket(msg, cmdtype):
    global cmdindex
    # global cmdtype
    bigness=len(msg)+10
    # print(bigness)
    packetbigness = bigness.to_bytes(4, byteorder='little', signed=True)
    packetid = cmdindex.to_bytes(4, byteorder='little', signed=True)
    cmdindex = cmdindex+1
    packettype = cmdtype.to_bytes(4, byteorder='little', signed=True)
    terminator=b"\x00"
    # fullpacket=packetbigness+packetid+packettype+msg.encode()+terminator
    fullpacket=struct.pack("<iii", bigness, cmdindex, cmdtype) + msg.encode() + b"\x00\x00"
    # print(fullpacket)
    return fullpacket
def msgpacket_id(msg, cmdtype, customid):
    global cmdindex
    # global cmdtype
    bigness=len(msg)+10
    # print(bigness)
    packetbigness = bigness.to_bytes(4, byteorder='little', signed=True)
    packetid = customid.to_bytes(4, byteorder='little', signed=True)
    cmdindex = cmdindex+1
    packettype = cmdtype.to_bytes(4, byteorder='little', signed=True)
    terminator=b"\x00"
    # fullpacket=packetbigness+packetid+packettype+msg.encode()+terminator
    fullpacket=struct.pack("<iii", bigness, cmdindex, cmdtype) + msg.encode() + b"\x00\x00"
    # print(fullpacket)
    return fullpacket

# emptyresponse = b"\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00" # for some reason this is what the protocol docs say it should be
emptyresponse = b"\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00"               # but this is what it actually is =D

# for some reason valve allows client to accept rcon commands from localhost :D
HOST = "127.0.0.1"
PORT = 27015

# execute command (m) as tf2 console command thru rcon
def command_rcon(m):
    global debugmode
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        message = msgpacket(rconpassword, 3)
        s.send(message)     # Send packet
        data = s.recv(1024)             # Receive packet
        # print(f"Received from server: {data}")

        time.sleep(.1)

        message=msgpacket(m, 2)
        s.send(message)     # Send packet
        if debugmode == True:
            print(message)
        # print(statuscommand)

        response = s.recv(4096)

        time.sleep(.1)

        message = msgpacket_id("", 0, 254)
        s.send(message)     # Send packet

        # this stuff only works on local servers
        overflowsuccess = False
        while overflowsuccess == False:
            data = s.recv(4096)
            # if debugmode == True:
                # print(f"Received from server: {data}")
            response = response+data
            if data.find(emptyresponse) != -1:
                overflowsuccess = True
                # print("whoop!")
    return data

# execute command (say "m") as tf2 console command
blockmessages = False
def message_rcon(m):
    global debugmode
    global script_conflict_disabled
    if script_conflict_disabled == False and blockmessages == False:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))

            message = msgpacket(rconpassword, 3)
            s.send(message)     # Send packet
            data = s.recv(1024)             # Receive packet
            # print(f"Received from server: {data}")

            time.sleep(.1)
            if community_compat == True:
                message=msgpacket("say \x22" + bot_ident + fingerprint_community + m + "\x22", 2)
            else:
                message=msgpacket("say \x22" + bot_ident + fingerprint + m + "\x22", 2)
            s.send(message)     # Send packet
            if debugmode == True:
                print(message)
            data = s.recv(4096)             # Receive packet
            if debugmode == True:
                print(f"Received from server: {data}")
            data = s.recv(4096)             # Receive packet
            if debugmode == True:
                print(f"Received from server: {data}")
            # print(f"Received from server: {data}")

# write command (say "m") to cs2 config "sobecatfacts" and simulate keypress to key defined by csmsgbind to execute it
def message_cs(m):
    with open(path_cs_cfg, "w") as f:
        f.write("say \"" + m + "\"")
    time.sleep(0.1)
    keyboard.press_and_release(csmsgbind)
# same thing except not say
def command_cs(m):
    with open(path_cs_cfg, "w") as f:
        f.write(m)
    time.sleep(0.1)
    keyboard.press_and_release(csmsgbind)
    if debugmode==True:
        print("EXECUTED COMMAND(s):\n"+m)

# cooldown time between chat messages, to prevent chat cooldown
message_cooldown = 1
time_last=0

# universal message handler
def cat_message(m):
    global time_last
    cur = time.time()
    if cur>time_last+message_cooldown:
        if sys.argv[1]=="tf":
            message_rcon(m)
        else:
            message_cs(m)
        console_log("MSG: " + m)
        time_last=cur
    else:
        console_log("###: (NOT SENT) " + m)
# universal command handler
def cat_command(m):
    if sys.argv[1]=="tf":
        command_rcon(m)
    else:
        command_cs(m)
    console_log("CMD: " + m)

# these dont work but i am afraid to remove them
def echo_rcon(m):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        message = msgpacket(rconpassword, 3)
        s.send(message)     # Send packet
        data = s.recv(1024)             # Receive packet
        # print(f"Received from server: {data}")

        time.sleep(.1)

        message=msgpacket("echo \x22" + m + "\x22", 2)
        print(message)
        s.send(message)     # Send packet
        data = s.recv(4096)             # Receive packet
        # print(f"Received from server: {data}")
def echo_cs(m):
    with open(path_cs_cfg, "w") as f:
        f.write("echo \"" + m + "\"")
    time.sleep(0.1)
    keyboard.press_and_release(csmsgbind)
    print("SENT MESSAGE\n"+m)
def echo_game(m):
    if sys.argv[1] == "tf":
        echo_rcon(m)
    elif sys.argv[1] == "cs":
        echo_cs(m)

# kill script
def command_killcat(a):
    console_raw("SCRIPT TERMINATED",0)
    console_raw("SCRIPT TERMINATED",1)
    print_console_output()
    os._exit(0)
    raise ValueError("KILLING CAT") # if for some reason the other exit doesn't work, which i have had issues with in the past

# run after server connection completed
# currently triggered by phrase "Redownloading all lightmaps", pretty sure this always works. 
lightmaps = "Redownloading all lightmaps"
maxplayers_over_32 = False
def connectionfinished_handler(a):
    global serverconmessage
    global blockmessages
    global lasttime
    global allowchatprompt
    global maxplayers_over_32
    output = command_rcon("status")
    blockmessages = False
    roll_fingerprint()
    lasttime = 0 # Allow script to send cat prompt immediately upon connecting to a server
    serverconmessage = "Server type not determined, assuming community server."
    community_compat=True
    if maxplayers_over_32 == False:
        allowchatprompt = False

# turn chat prompts on/off
doprompt = True
def command_prompton(a):
    global doprompt
    doprompt = True
    if debugmode==True:
        print("PROMPT ON")
    else:
        console_log("Turned prompt on.")
    # echo_game("PROMPT ON")
def command_promptoff(a):
    global doprompt
    doprompt = False
    if debugmode==True:
        print("PROMPT OFF")
    else:
        console_log("Turned prompt off.")
        console_raw("PROMPT OFF",1)

# ran by typing "listplayerids" in tf2 console, can use to get steamids of chat users
playerids = {}
def printplayers(a):
    for player, playerid in playerids.items():
        print(player + ": STEAMID " + playerid)

# turn whole thang on/off using script conflict detector
def enablescript(a):
    global script_conflict_disabled
    script_conflict_disabled = False
def disablescript(a):
    global script_conflict_disabled
    script_conflict_disabled = True

# turn community compat mode on/off (will be set automatically when status command is ran)
def forcecommunitycompat_on(c):
    global community_compat
    community_compat = True
def forcecommunitycompat_off(c):
    global community_compat
    community_compat = False

# hook commands
file_commands = {}
file_pattern_commands = {}
file_py_commands = {}
directory = Path("custom")
for file in directory.iterdir():
    if file.is_file():
        commandmatch = re.search("(.*)\\.txt", file.name)
        com = ""
        if commandmatch:
            # com = commandstring + commandmatch.group(1)
            com = commandmatch.group(1)
            file_commands[com] = {}
            if debugmode == True:
                print("registered command from file: " + com)
            numentries=0
            with open("custom/"+file.name, 'r') as file:
                for line in file:
                    file_commands[com][numentries] = line.strip()
                    if debugmode==True:
                        print(str(numentries)+": "+line.strip())
                    numentries=numentries+1
directory = Path("custom_pattern")
for file in directory.iterdir():
    if file.is_file():
        commandmatch = re.search(".*\\.txt", file.name)
        com = ""
        if commandmatch:
            # com = commandstring + commandmatch.group(1)
            numentries=-1
            with open("custom_pattern/"+file.name, 'r') as file:
                for line in file:
                    if numentries == -1:
                        com = line.strip()
                        if debugmode == True:
                            print("registered pattern command from file: " + com)
                        file_pattern_commands[com] = {}
                        numentries=numentries+1
                    else:
                        file_pattern_commands[com][numentries] = line.strip()
                        if debugmode==True:
                            print(str(numentries)+": "+line.strip())
                        numentries=numentries+1
directory = Path("custom_py")
glock_balls={}
if game_type=="tf":
    connectionpattern = "Redownloading all lightmaps"
else:
    connectionpattern = "ChangeGameUIState: CSGO_GAME_UI_STATE_LOADINGSCREEN -> CSGO_GAME_UI_STATE_INGAME"
for file in directory.iterdir():
    if file.is_file():
        commandmatch = re.search("(.*)\\.txt", file.name)
        #com = ""
        if commandmatch:
            #com = commandmatch.group(1)
            with open("custom_py/"+file.name, 'r') as file:
                for line in file:
                    com = re.sub("#CMDSTRING", commandstring, line).strip()
                    com = re.sub("#CONSTRING", connectionpattern, com)
                    cmd_text=""
                    with open("custom_py/"+commandmatch.group(1)+".py", 'r') as pyfile:
                        for pyline in pyfile:
                            cmd_text+=pyline
                    exec(cmd_text, globals=globals(), locals=glock_balls)
                    # PUSHES ALL DEFINED VARIABLES TO GLOBAL SPACE
                    # THIS CAN BREAK MAIN SCRIPT!! BE CAREFUL!!
                    globals().update(glock_balls)
                    if "PAT_CMD" in glock_balls:
                        file_py_commands[com] = glock_balls["PAT_CMD"]
                        if debugmode == True:
                            print("registered pattern python command from file: " + com)
                    else:
                        if debugmode == True:
                            print("FAILED to pattern python command \"" + com + "\", no function PAT_CMD defined in script")

def do_file_command(c,a):
    selekta = random.randint(0,len(a)-1)
    message_rcon(a[selekta])

commands = {
    "killcat": command_killcat,
    exitstring: command_killcat,
    "cat_on": command_prompton,
    "cat_off": command_promptoff,
    lightmaps: connectionfinished_handler,
    "listplayerids": printplayers,
    "script_enable": enablescript,
    "script_disable": disablescript,
    "community_on": forcecommunitycompat_on,
    "community_off": forcecommunitycompat_off
}

# detect steamids from status output, currently not used for anything
steamid_pattern = "#\\s+(\\d+)\\s+\"(.*)\"\\s+\\[(.*)\\]\\s+(\\S*)\\s+(\\d+)\\s+(\\d+)\\s+active"
def status_output_process(a, args):
    # print(a)
    if debugmode==True:
        print("STEAMID IDENTIFIED: " + args.group(3))
    playerids[args.group(2)] = args.group(3)
status_start_pattern = "players\\s+:\\s+\\d*\\s+humans,\\s+\\d*\\s+bots\\s+\\(\\d*\\s*max\\)"
# clear list on new connection
def status_start_process(a,args):
    global playerids
    playerids = {}

# script conflict handler
fingerprint_set="["+fingerprint_chars+"]"
fingerprint_pattern=bot_ident+"("+fingerprint_set+fingerprint_set+fingerprint_set+")"
fingerprint_set_community="\\d\\d\\d"
fingerprint_pattern_community=bot_ident+"[("+fingerprint_set_community+")]"
def conflict_handler(a, args):
    global script_conflict_disabled
    if community_compat == False:
        if args.group(1) != fingerprint:
            print("CONFLICT DETECTED!!!")
            if args.group(1).encode() > fingerprint.encode():
                script_conflict_disabled = True
                if debugmode == True:
                    print("#############################")
                    print("SCRIPT DISABLED")
                    print("type \'echo script_enable\' in console to reenable!")
                    print("please wait until next server before reenabling.")
                    print("#############################")
                else:
                    console_log("Please wait until next server before reenabling.")
                    console_log("type \'echo script_enable\' in console to reenable!")
                    console_log("SCRIPT DISABLED")
            else:
                if debugmode == True:
                    print("Won conflict resolution, disabling other script.")
                else:
                    console_log("Won conflict resolution, disabling other script")
def conflict_handler_community(a, args):
    global script_conflict_disabled
    if community_compat == True:
        if args.group(1) != fingerprint_community:
            print("CONFLICT DETECTED!!!")
            if args.group(1).encode() > fingerprint_community.encode():
                script_conflict_disabled = True
                if debugmode == True:
                    print("#############################")
                    print("SCRIPT DISABLED")
                    print("type \'echo script_enable\' in console to reenable!")
                    print("please wait until next server before reenabling.")
                    print("#############################")
                else:
                    console_log("Please wait until next server before reenabling.")
                    console_log("type \'echo script_enable\' in console to reenable!")
                    console_log("SCRIPT DISABLED")
            else:
                if debugmode == True:
                    print("Won conflict resolution, disabling other script.")
                else:
                    console_log("Won conflict resolution, disabling other script")

# detect whether server is valve or community thru status
hostname_pattern = "hostname:\\s*(.*)"
def hostname_handler(a, args):
    global allowchatprompt
    global community_compat
    global serverconmessage
    allowchatprompt = True
    if re.search("Valve Matchmaking Server", args.group(1)):
        community_compat = False
        if debugmode==True:
            print("### CONNECTED TO VALVE MATCHMAKING SERVER ###")
        serverconmessage = "Connected to valve server"
    else:
        community_compat = True
        if debugmode==True:
            print("### CONNECTED TO COMMUNITY SERVER ###")
        serverconmessage = "Connected to community server"

# detect cs2 server connection, works for official servers. dont know about community servers...
cs_connect_pattern = "ChangeGameUIState: CSGO_GAME_UI_STATE_LOADINGSCREEN -> CSGO_GAME_UI_STATE_INGAME"
def cs_connect_handler(a, args):
    global allowchatprompt
    global community_compat
    global serverconmessage
    allowchatprompt = True
    community_compat = False
    serverconmessage = "Connected to official CS2 server"
    lasttime = int(time.time()) - interval + 20

# disable messages, assume community server until proven otherwise
serverconnecting_pattern="Connecting to \\d*"
def serverconnect_handler(a, args):
    global serverconmessage
    global blockmessages
    blockmessages=True
    global community_compat
    community_compat = True 
    serverconmessage = "Connecting to server..."
# proven otherwise :D
serverconnecting_matchmaking_pattern="Connecting to matchmaking server \\d*"
def serverconnect_matchmaking_handler(a, args): 
    global serverconmessage
    serverconmessage = "Connecting to matchmaking server..."

# if server allows more than 32 players it's not official, use community compatibility fingerprint
playercount_pattern="Players:\\s*(\\d*)\\s*/\\s*(\\d*)"
def playercount_handler(a, args):
    global serverconmessage
    global allowchatprompt
    global maxplayers_over_32
    if int(args.group(2)) > 32:
        maxplayers_over_32 = True
        allowchatprompt = True
        if debugmode==True:
            print("ALLOWED PROMPT FOR OVER 32 MAXPLAYERS")
        #else:
            #print("\rMax players over 32, assuming community server              \r", end="")
        serverconmessage = "Max players over 32, assuming community server"
        community_compat = True
    else:
        maxplayers_over_32 = False

# yeah!!
pattern_commands = {
    steamid_pattern: status_output_process,
    fingerprint_pattern: conflict_handler,
    fingerprint_pattern_community: conflict_handler_community,
    hostname_pattern: hostname_handler,
    serverconnecting_pattern: serverconnect_handler,
    serverconnecting_matchmaking_pattern: serverconnect_matchmaking_handler,
    playercount_pattern: playercount_handler,
    cs_connect_pattern: cs_connect_handler,
    "#CS_CONNECT": cs_connect_handler
}
# yeah!!!!!
if debugmode == True:
    for index, command in commands.items():
        print("Registered command string: " + index)

# used for following console.log output
def follow(filename):
    with open(filename, 'r', errors="replace") as f:
        # Move to the end of the file if you only want new data
        f.seek(0, 2) 
        while True:
            try:
                line = f.readline()
                if not line:
                    time.sleep(0.1)  # Sleep briefly to avoid 100% CPU usage
                    continue
                yield line
            except UnicodeDecodeError: # this shouldnt happen with errors=replace but watever lool
                if debugmode == True:
                    print("Unicode decode error in console output: you can probably ignore this")

# doesnt do anything l9ol Owned
havewesentstatusyet = False

spinner_rotato = 0
spinners=["|","/","—","\\"]

# this ticks every time a line is printed to game console
for new_line in follow(path_use):
    if spinner_rotato==len(spinners)-1:
        spinner_rotato = -1
    spinner_rotato+=1
    ## send status once on script load to ensure community_compat is set if script is loaded while connected to a community server
    ## does not work unless command is sent after this loop is established
    if havewesentstatusyet == False and game_type=="tf":
        command_rcon("status")
        time.sleep(.1)
    curtime = int(time.time())
    if debugmode == True:
        print(new_line.replace("\x07", ""), end='')
    else:
        if serverconmessage != "":
            console_raw(serverconmessage,0)
        else:
            console_raw("IDLE",0)
        timeuntil = (lasttime+interval)-curtime
        if timeuntil<0 or re.search("Connecting to", serverconmessage):
            console_raw("Waiting for connection...", 1)
        else:
            perc = (interval-timeuntil)/interval
            percstring="\r["
            for i in range(1,22):
                if i==11:
                    percstring+=spinners[spinner_rotato]
                elif perc<(i/22):
                    percstring+=" "
                else:
                    percstring+="#"
            percstring+="] Next prompt in " + str(timeuntil) + " seconds"
            console_raw(percstring,1)
    for index, command in commands.items():
        if new_line.find(index) != -1:
            command(new_line)
    for index, command in pattern_commands.items():
        pattern_temp = re.search(index,new_line)
        if pattern_temp:
            command(new_line, pattern_temp)
    for index, array in file_commands.items():
        pattern_temp = re.search(commandstring + "!("+index+")",new_line)
        if pattern_temp:
            do_file_command(index, array)
    for index, array in file_pattern_commands.items():
        pattern_temp = re.search(index,new_line)
        if pattern_temp:
            do_file_command(index, array)
    for index, f in file_py_commands.items():
        pattern_temp = re.search(index,new_line)
        if pattern_temp:
            f(index)
    if (curtime>lasttime+interval) and doprompt==True and allowchatprompt==True:
        if silent == False:
            message="type !cat for a random cat fact!"
            cat_message(message)
        lasttime = curtime
        interval = random.randint(intervalmin,intervalmax)
    # this used to do something, now it doesn't
    # keeping it here because it may come in handy later
    if havewesentstatusyet == False and game_type=="tf":
        #command_rcon("echo CAT_CONFIRM_CONNECTION_PROCESS")
        havewesentstatusyet = True

    print_console_output()