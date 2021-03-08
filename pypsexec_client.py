from pypsexec.client import Client
# creates an encrypted connection to the host with the username and password
c = Client("127.0.0.1", username="Administrator", password="1234")
c.connect()
try:
    c.create_service()

    # After creating the service, you can run multiple exe's without
    # reconnecting

    # run a simple cmd.exe program with arguments
    stdout, stderr, rc = c.run_executable("cmd.exe",
                                          arguments="/c echo Hello World")
    print(stdout, rc)

    # run whoami.exe as the SYSTEM account
    stdout, stderr, rc = c.run_executable("whoami.exe", use_system_account=True)
    print(stdout, rc)
finally:
    c.remove_service()
    c.disconnect()