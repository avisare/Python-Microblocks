# Python-Microblocks
This python scripts created in order to enable
connection to remote machine, or any other local usage 
with shared memory.

# Usage
In order to create the server to listen on the remote machine,
execute the script *`remote_agent.py`, with the remote **configuration files as
an argument. 

After you started the remote machine to listen on the specific port,
you should start the client aka - your test, with a suitable configuration file.
Just execute the script `shared_memory_client.py` with configuration files as an argument.
The first three lines in the main function will always be the same, after that, you should write your test.
For example if you would like to publish a topic on the ***remote machine, just write object.SMT_Publish() with suitable
parameters. Also, you don't have to use the shared memory client and server.
You can use the transportation protocols module for your needs. You can create tcp client,
tcp server, udp responder, udp initiator, udp strict, with the `connection_factory.py` file,
with the ConnectionFactory class.
###*Pay Attention!
Before executing the `remote_agent.py` script, move the installer in the current directory named 
shared_memory_installer.exe to folder named servers in the remote machine.

###**Pay Attention!
The configuration files you passed as arguments, should exist
in the remote machine.

###***Pay Attention!
The syntax in order to publish topic or get object on the local machine
or on the remote machine is exactly the same. 