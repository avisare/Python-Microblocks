# Python-Microblocks
This python scripts created in order to enable
connection to remote machine, or any other local usage 
with shared memory.

# Usage
In order to create the server to listen on the remote machine,
execute the script *`start_client.py`, with the remote **configuration files as
an argument. you can also set the configuration without configuration files.
You should first run `start_client.py` with the run_test.py script without any
cmd arguments, in order to check that everything is good.

After you started the remote machine to listen on the specific port,
you should start the client aka - your test, with a suitable configuration file.
Just execute the script `start_client.py` with configuration files as an argument.
The first three lines in the main function will always be the same, after that, you should write your test.
For example if you would like to publish a topic on the ***remote machine, just write object.SMT_Publish() with suitable
parameters. Also, you don't have to use the shared memory client and server.
You can use the transportation protocols module for your needs. You can create tcp client,
tcp server, udp responder, udp initiator, udp strict, with the `connection_factory.py` file,
with the ConnectionFactory class.
# Configuration File
The configuration file should contain list of the topic names
you want to create at the start of the program, and also for each topic,
its info (max data size, history depth and cells count ) - probably it will be changed,
and the parser will do it automatically in the future.
After that you should write the control method: remote or local.
In case you want remote, you need to write the transportation protocol (TCP/UDP)
and the connection mode. connection mode can be client or server if you chose TCP,
and can be responder, initiator and strict if you chose UDP.
Each method required  different fields in the config file:

TCP+server: responder_port

TCP+client: responder_port, responder_ip

UDP+responder: responder_port

UDP+client: responder_port, responder_ip

UDP+strict: local_port, responder_port, responder_ip

The configuration file can contain also `timeout_remote_seconds` in seconds, until
the connection to the remote machine will be close, and `timeout_seconds` in secondss,
until the connection will stop waiting to message in recv function.
There is example config file in the installation directory named `config.json`.

### *Pay Attention!
Before executing the `start_client.py` script, move the installer in the current directory named 
shared_memory_installer.exe to folder named servers in the remote machine.

### **Pay Attention!
The configuration files you passed as arguments, should exist
in the remote machine.

### ***Pay Attention!
The syntax in order to publish topic or get object on the local machine
or on the remote machine is exactly the same. 

# Be Aware
The server can maybe take few seconds to load and bind the socket,
so if when you try to connect and run the `start_client.py` script,
you receive a ConnectionResetError, just try to run the `start_client.py`
script again after couple of seconds.