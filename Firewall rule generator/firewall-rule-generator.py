print("---------------------------------------------------")
print("|                                                  |")
print("|                                                  |")
print("|           FIREWALL RULE GENERATOR                |")
print("|              LINUX / WINDOWS                     |")
print("|                                                  |")
print ("--------------------------------------------------")

#symbols
plus = "[+]"
minus = "[-]"
result ="[=]"

#Getting user inputs
def get_values():
    pro = input(f"{plus} Enter PROTOCOL (default tcp): ").lower()
    prt = input(f"{plus} Enter PORT: ").lower()
    src = input(f"{plus} Enter SOURCE: ").lower()
    act = input(f"{plus} Enter ACTION (ACCEPT,DROP): ").upper()
    mode = str(input(f"{plus} Enter MODE (Inbound,Outbound): ").lower())

    #Setting defualt values if values are not given
    if pro == "":
        pro = "tcp"
        
    if act not in ["ACCEPT","DROP"]:
        act = "DROP"

    if mode not in ["Inbound","Outbound"]:
        mode = "Inbound"

    arr = src.split(',')
    if len(arr) > 1:
        src = arr        

    return {"pro":pro,"prt":prt,"src":src,"act":act,"mode":mode}

#Windows values format
def get_windows_values():
    values = get_values()
    name = input(f"{plus} Enter RULE NAME: ").lower()

    values["name"] = name

    return values
    

#Firewall generator main class
class gen_firewall():
    def __init__ (self,src,pro,act,prt,mode):
        self.src = src
        self.pro = pro
        self.act = act
        self.prt = prt
        self.mode = mode

#Class for generation linux firewall rules
class gen_firewall_linux(gen_firewall):
    def __init__(self,src,pro,act,prt,mode):
        super().__init__(src,pro,act,prt,mode)
        self.template = f"sudo iptables -A {'INPUT' if self.mode == 'inbound' else 'OUTPUT'}"
        self.protocol = f"-p {self.pro}"
        self.port  = f"--dport {self.prt}" if self.prt != "" else ""
        self.action = f"-j {self.act}"
        self.source = f"-s {self.src}" if self.src != "" else ""

    def linux_firewall(self):
        if type(self.src) == list:
            for ip in range(0, len(self.src)):
                print(f"{self.template} {self.protocol} -s {self.src[ip]} {self.port} -j ACCEPT")
        else:                
            print(f"{self.template} {self.protocol} {self.source} {self.port} {self.action}")


#netsh advfirewall firewall add rule name="Block Outgoing to 203.0.113.5" dir=out protocol=TCP dir=in localport=22 remoteip=203.0.113.5 action=block
#Class for generating windows firewall rules
class gen_firewall_windows(gen_firewall):
    def __init__(self,src,pro,act,prt,mode,name):
        super().__init__(src,pro,act,prt,mode)
        self.name = name
        self.template = "netsh advfirewall firewall add rule"
        self.firewall_name = f"name=\"{self.name}\""
        self.dir = f"dir={'out' if self.mode == 'outbound' else 'in'}"
        self.remoteip = f"remoteip={self.src}"
        self.action = f"action={'accept' if self.act == 'ACCEPT' else 'block'}"
        self.protocol = f"protocol={self.pro}"
        self.localport = f"localport={self.prt}"

    def gen_win_firewall(self):
        print(f"{self.template} {self.firewall_name} {self.dir} {self.protocol} {self.localport if self.prt != "" else ""} {self.remoteip if self.src != "" else ""} {self.action}")


#Using loop to generate constant rules until the user stops the program
while True:
    platform = input("[+] Enter a platform (Linux, Windows) or quit: ").lower()

    print("")
    print(f"{plus} Required")
    print(f"{minus} Optional")
    print("")
    
    if platform == "linux":
        values = get_values()
        protocol, port, source, action, mode = values["pro"], values["prt"], values["src"], values["act"], values["mode"]
        print("\n")
        print("----------------------------------------------")
        print(f"{plus} Firewall Rule Generated for linux (iptables)")
        print("----------------------------------------------")
        rule = gen_firewall_linux(source,protocol,action,port,mode)
       
        rule.linux_firewall()
        print("\n")
        
    elif platform == "windows":
        values = get_windows_values()
        protocol, port, source, action, mode, name = values["pro"], values["prt"], values["src"], values["act"], values["mode"], values["name"]

        print("\n")
        print("----------------------------------------------")
        print(f"{result} Firewall Rule Generated for windows")
        print("---------------------------------------------- \n")
        windows_rule = gen_firewall_windows(source,protocol,action,port,mode,name)
        windows_rule.gen_win_firewall()
        print("\n")

    elif platform == "quit":
        quit()

    else:
        print('-------------------------------------------------------')
        print("Please Select a platform to continue")
        print('-------------------------------------------------------\n')


#This project was built by Boaz Amakye Adjei and not completed