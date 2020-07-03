#!/usr/bin/env python3
import socket
import re
import os
import sys

class Stack:

    def __init__(self):
        self.stack = []

    def push(self, num):
        for n in num:
            self.stack.append(n)
    
    def multiply(self):
        if(len(self.stack)<2):
            return False
        a=self.stack.pop()
        b=self.stack.pop()
        self.stack.append(a*b)
        return True
    
    def add(self):
        if(len(self.stack)<2):
            return False
        a=self.stack.pop()
        b=self.stack.pop()
        self.stack.append(a+b)
        return True
    
    def peek(self):
        if(len(self.stack)<1):
            return False
        return self.stack[-1]
    
    def zap(self):
        self.stack.clear()

IP="127.0.0.1"
PORT=9999
bind_address=(IP,PORT)

socket1=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket1.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

socket1.bind(bind_address)
clients={}
socket1.listen(10) 

while True:
    conn_s,addr=socket1.accept()
    if not os.fork():
        socket1.close()
        f=conn_s.makefile(mode="rw",encoding="utf-8")
        stack1= Stack()
        while True:
            aux=f.readline()
            if not aux:
                break
            aux = aux.strip() 
            if aux=="PUSH":
                num=[]
                while True:
                    line=f.readline().strip()
                    pomocna=len(num)
                    m=re.match(r"[0-9]+",line)
                    if(line==''):
                        if pomocna==0:
                            f.write("201 Request content empty\n\n")
                            f.flush()
                        else:
                            stack1.push(num)
                            f.write("100 OK\n\n")
                            f.flush()
                    else:
                        if not (m.group(0).isdigit()):
                            f.write("202 Not a number\n\n")
                            f.flush()
                        else:
                            num.append(int(m.group(0)))

            elif aux=="MULTIPLY":
                line=f.readline().strip()
                if(line==''):
                    pom=stack1.multiply()
                    if not pom:
                        f.write("203 Stack too short\n\n")
                        f.flush()
                    else:
                        f.write("100 OK\n\n")
                        f.flush()
                else:
                    f.write("204 Request content nonempty\n\n")
                    f.flush()
            
            elif aux=="ADD":
                line=f.readline().strip()
                if(line==''):
                    pom=stack1.add()
                    if not pom:
                        f.write("203 Stack too short\n\n")
                        f.flush()
                    else:
                        f.write("100 OK\n\n")
                        f.flush()
                else:
                    f.write("204 Request content nonempty\n\n")
                    f.flush()
            
            elif aux=="PEEK":
                line=f.readline().strip()
                if(line==''):
                    ans=stack1.peek()
                    if ans == False:
                        f.write("203 Stack too short\n\n")
                        f.flush()
                    else:
                        f.write("100 OK\n")
                        f.write(str(ans))
                        f.write("\n\n")
                        f.flush()
                else:
                    f.write("204 Request content nonempty\n\n")
                    f.flush()
                        
            elif aux=="ZAP":
                line=f.readline().strip()
                if(line==''):
                    stack1.zap()
                    f.write("100 OK\n\n")
                    f.flush()
                else:
                    f.write("204 Request content nonempty\n\n")
                    f.flush()
            else:
                f.write("301 Bad request\n\n")
                f.flush()
                break
                
        conn_s.close()
        sys.exit(0)

    else:
        conn_s.close()
