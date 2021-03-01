# Python-Microblocks

# Explanation
This package can use in order to connect and control remote machine
and make it to publish specific topics to the shared memory of the machine
or to get specific topics from the shared memory of the machine

#Usage
In the test_remote_shared_memory.py file yoou can found example of use of all the
functions within the client and server classes.
The main function are recieve and send in order to send to the server message
or recieve one from him. all the messages pass between the server and the client
are from Message class type.
The usage of the remote and the local shared memory ar the same, except that in the remote
you need to execute the functions send  and recieve on the client object instead of SharedMemoryWrapper object.
For example: `client.send(shared_memory_object)` - will publish the object on the remote server.
And the command `client.recieve(shared_memory_temp_object, 1, 30)` - will recieve the object with counter 1 from the remote server.
