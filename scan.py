from os import _exit
from random import randint
import socket, threading, sys, time
from scapy.all import *

localHostIP = socket.gethostbyname(socket.gethostname())
localHostPort = randint(1024, 65535)
BDSIP = str(sys.argv[1])
motdData = b'\x01\x00\x00\x00\x00$\r\x12\xd3\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x124Vx\n'
serverCount = 0

def sendPacket(startNum, count):
    port = startNum
    while True:
        Time = time.strftime('%H:%M:%S')
        if port % 1000 == 0:
            print(f"[{Time} I] Scaning port: {str(port)} ~ {str(port + 1000)}")
        send(IP(src=localHostIP, dst=BDSIP) / UDP(sport=localHostPort, dport=port) /
             motdData,
             verbose=False)
        if port == 65535:
            print(f"[{Time} I] Port {startNum} ~ 65535 Done")
            while True:
                time.sleep(1)
        elif port == startNum + count - 1:
            print(f"[{Time} I] Port {startNum} ~ {startNum + count} Done")
            time.sleep(10)
            print("BE Server Count: " + str(serverCount))
            print("BDS Count: " + str(bdsCount))
            print("NK Count: " + str(nkCount))
            print("Geyser Count: " + str(geyserCount))
            print("Skipped Count: " + str(skipped))
            print("Error Count: " + str(error))
            _exit(0)
        port += 1


t1 = threading.Thread(target=sendPacket, args=(0, 10000))
t2 = threading.Thread(target=sendPacket, args=(10000, 10000))
t3 = threading.Thread(target=sendPacket, args=(20000, 10000))
t4 = threading.Thread(target=sendPacket, args=(30000, 10000))
t5 = threading.Thread(target=sendPacket, args=(40000, 10000))
t6 = threading.Thread(target=sendPacket, args=(50000, 10000))
t7 = threading.Thread(target=sendPacket, args=(60000, 5535))
t1.setDaemon(True)
t2.setDaemon(True)
t3.setDaemon(True)
t4.setDaemon(True)
t5.setDaemon(True)
t6.setDaemon(True)
t7.setDaemon(True)
t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
t6.start()
t7.start()

bdsCount = 0
nkCount = 0
geyserCount = 0
skipped = 0
error = 0
payloads = []

while True:
    sk_rec = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sk_rec.bind((localHostIP, localHostPort))
    try:
        data, addr = sk_rec.recvfrom(10240)
        date = time.strftime('%H:%M:%S')
        if addr[1] not in payloads:
            payloads.append(addr[1])
        else:
            skipped += 1
            print(f"[{date} R] Duplicate server found, skipped. Source: {addr[0]}:{addr[1]}")
            continue
        infos = []
        data1 = data.split(b"MCPE")
        infos_byte = data1[1].split(b";")
        for info in infos_byte:
            try:
                context = info.decode()
            except:
                context = str(info)[2:-1]
            infos.append(context)
        print("")
        print(f"[{date} R] Motd: {infos[1]}")
        print(f"[{date} R] Versin: {infos[3]}/{infos[2]}")
        print(f"[{date} R] Online: {infos[4]}/{infos[5]}")
        print(f"[{date} R] Map: {infos[7]}/{infos[8]}")
        print(f"[{date} R] Port(v4/v6): {infos[10]}/{infos[11]}")
        print(f"[{date} R] Source: {addr[0]}:{addr[1]}")
        serverCount += 1
        print(f"[{date} C] {str(serverCount)}")
        if re.search(b"edicated", data):
            bdsCount += 1
        if re.search(b"nukkit", data):
            nkCount += 1
        if re.search(b"eyser", data):
            geyserCount += 1
        sk_rec.close()
    except:
        print(f"[{time.strftime('%H:%M:%S')} R] An error occurred, skipped.")
        error += 1
        pass

