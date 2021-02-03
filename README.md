# Botnet Tutorial

# FAQ
VM credentials: user: pi, password: password

You may run into an issue with reading shadow file, please run the script as sudo or chmod 666 the shadow file

## VM Setup:
There are two VM's required for this tutorial (you can technically do it in 1 VM, but you would need to install wireshark on your computer).
Rasperry Desktop:
    This VM should have access to the internet, it will attempt to reach out to external web resources, and if they are inaccessible then the tutorial cannot be effectively completed.
    My setup that I got to work is to have the VM on network in bridged mode, ensure the VM has a different IP then that of your host machine (physical computer). Once that is completed, you should be good to start the tutorial. 
Kali:
    This should be setup the same as above ideally, allow it to connect to the outside network. The VMs should be able to talk to one another, and host should be able to talk to the VMs and vice versa.

VM can be found here: 
scp UTORID@dh2020pcXX.utm.utoronto.ca:/virtual/csc427/botnettutorial-vm.zip .


If you are not in vmware 16, please open **workstation pro** of whatever version you have, right click, manage, hardware compatibility, accept defaults, alter, then start

There is a reported issue with the VM if you are not using the latest version of vmware, i.e. vmware version 16. Please update to this version

## Task 1

There seem to be a bot running in your computer. And looks like it is trying to ping the server constantly. Can you find and block it with techniques introduced during the lecture?

Describe how you found how to block the botnet and what steps needed to be taken to do so in `botnet.txt`.

## Task 2

After blocking the annoying hidden botnet, now you are implementing your own one with the scripts from a site that you really shouldn't download anything from.

If you take a look at the server and bot scripts, you would realized that this botnet has a very simple centralized structure as all bots connect to the server directly.

Ideally, you would have a server runs on your local machine and have several VMs as bots. It's okay do this tutorial with just one VM and running both server and bots on it.

Functions for communication between the server and bots are implemented for you. However, there are some commands the server would like to execute are missing. Check both `server.py` and `bot.py` for implementation details.

### server.py

**If server and client are running on different machines, in server.py please change 127.0.0.1 to the IP of the machine**

If you have the bot and server running on the same machine, then you can use `127.0.0.1` to connect the bot to the server, however it is suggested that you run the server and bot client separately if you can. As well, at some point you may want to run a bot separate from the VM, but some steps may require you to run a bot on a linux machine, this can be done on a kali VM or the provided VM image, some configuration may be required, specifically running `sudo ufw allow 1338` to allow traffic through the firewall for the bot to communicate with the server.

The server has some built-in functions `send_cmd` and `receive_message` that could talk to its bots. It also has some ready-to-go commands:
- "update": updates new joined or dead bots from last time the server checks. You should constantly check if there is any new joined bots with the command.
- "ping": ping all your bots.
- "list": lists all active bots
- "stop": all bots stop DDoS attacking if they were doing so.
- "help": lists available commands. Well actually it doesn't work as the follow commands need to be implemented:

**TODO**

1. - "ddos" + `http://IP:PORT`: Why would 127.0.0.1:80 get you to download these two scripts?! It's so annoying, let's ddos it. (Don't forget to include the protocol http) (No implementation needed)

Before launching the attack, open wireshark and start the capture, then launch the attack, now take a look at the traffic. Describe what's happening in terms of anything that would be alerting to a network admin? Write down your observation in `botnet.txt`. *In this step the bot should not be attacking 127.0.0.1 ideally so that you can see traffic on the adapter*

2. - "shadow": of course, we are always interested in the shadow file. (Implementation needs to be done in `bot.py`, `server.py`) Figure out what the passwords on the system are.

Break as many passwords as you can, and include them in `botnet.txt`. 

3. - "screenshot": getting a screenshot of all bots' screen. (Implementation needs to be done in `bot.py`)

Take a screenshot of the bot machine showing that the `bot.py` script is the one that executed the screenshot.

4. - "ssh" + `SSH_KEY`: except for talking to bots through sockets. Let's leave a backdoor as part of botnet maintenance. (Server side: needs to generate a key and send it to bots)

### bot.py

The script takes two inputs, the IP address of the server and the port its on. This bot is connecting to the server on `127.0.0.1` if localhost, or the IP of the machine running server.py otherwise, on port on 1338. Start it with `python3 bot.py {SERVER IP} 1338`. 

In `bot.py`, a function for transferring files and replying to the server `replyToServer` is ready for use. Your task is to implement the following actions:

**TODO**

1. - "ddos": receiving the IP and port of the target from the server, the bot would then spam requests to the target till it receives "stop" command (which is implemented for you already). Describe what's happening in terms of anything that would be alerting to a network admin in `botnet.txt`.

2. - "shadow": find the shadow file and send it back to the server.

3. - "screenshot": take a screenshot, and send it over. Notice that in order to reduce traces, this needs to be done without saving data as a file.
### Ideally this is done in memory, which is possible, however if you are having issues you can save the file and figure out a way to hide your traces a different way

4. - "ssh": append the key sent from the server to its ssh file.


## Submission

You should submit `botnet.txt` for short answers and both `server.py` and `bot.py` scripts to show that the work was done!
