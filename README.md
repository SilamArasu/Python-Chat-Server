# Python-Chat-Server
A Python chat server(LAN), with multiple chat rooms.
Based on pychat(https://github.com/xysun/pychat) with new added features.


## Instruction
### Server-side
```python
  python3 server.py 
```
### Client-side
```python
  python3 client.py [server-ip](Optional)
```
  * Register if you are new or login if you are not
  * Enter <manual> to get command list. 

### Features
Apart from features of pychat in above link, I have added features such as:
* AES Encryption of socket-socket connection
* Personal Chat 
* Block/Unblock to stop seeing message from particular user
* Store Personal and Group chat messages in a database and retrieve it
