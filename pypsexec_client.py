from pypsexec.client import Client
# creates an encrypted connection to the host with the username and password
# 127.0.0.1
c = Client("192.168.2.16", username="RFManager", password="1234")
c.connect()
try:

    c.create_service()

    # After creating the service, you can run multiple exe's without
    # reconnecting

    stdout, stderr, rc = c.run_executable("cmd.exe", arguments="/c echo hello world")
    #stdout, stderr, rc = c.run_executable("cmd.exe", arguments="/c cd.. & cd.. & cd test_remote & py start_server.py")
    print(stdout, stderr)

finally:
    c.remove_service()
    c.disconnect()