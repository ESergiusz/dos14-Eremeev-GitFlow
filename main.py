import os

if os.environ["SHELL"] == "/bin/bash":
    print("Greetings bash")
else:
    print("Hello", os.environ["SHELL"])