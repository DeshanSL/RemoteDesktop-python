def ReadConf():
    config = open("config.txt", "r")
    IP = str(config.readline().strip())
    Port = int(config.readline().strip())
    return IP, Port