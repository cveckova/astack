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

IP=""
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
            aux=f.readline().strip()
            if not aux:
                #f.write("Client disconnected")
                break
            
            if aux=="PUSH":
                num=[]
                while True:
                    line=f.readline().strip()
                    pomocna=len(num)
                    m=re.match(r"[0-9]+",line)
                    if(line==''):
                        if pomocna==0:
                            f.write("201 Request content empty\n")
                            f.flush()
                            break
                        else:
                            if not (m.group(1).isdigit()):
                                f.write("202 Not a number\n")
                                f.flush()
                                break
                            else:
                                stack1.push(num)
                                f.write("100 OK")
                                break
                    
            elif aux=="MULTIPLY":
                num=[]
                line=f.readline().strip()
                if(line==''):
                    pom=stack1.multiply()
                    if pom==False:
                        f.write("203 Stack too short\n")
                        break
                    else:
                        f.write("100 OK\n")
                        f.flush()
                        break
                else:
                    f.write("204 Request content nonempty\n")
                    f.flush()
                    break
            
            elif aux=="ADD":
                num=[]
                line=f.readline().strip()
                if(line==''):
                    pom=stack1.add()
                    if pom==False:
                        f.write("203 Stack too short\n")
                        break
                    else:
                        f.write("100 OK\n")
                        f.flush()
                        break
                else:
                    f.write("204 Request content nonempty\n")
                    f.flush()
                    break
            
            elif aux=="PEEK":
                num=[]
                line=f.readline().strip()
                if(line==''):
                    ans=stack1.peek()
                    if ans == False:
                        f.write("203 Stack too short\n")
                        break
                    else:
                        f.write("100 OK\n")
                        f.write(ans)
                        f.flush()
                        break
                else:
                    f.write("204 Request content nonempty\n")
                    f.flush()
                    break
                        
            elif aux=="ZAP":
                num=[]
                line=f.readline().strip()
                if(line==''):
                    stack1.zap()
                    f.write("100 OK\n")
                    f.flush()
                    break
                else:
                    f.write("204 Request content nonempty\n")
                    f.flush()
                    break
            else:
                f.write("301 Bad request\n")
                f.flush()
                break
                
        conn_s.close()
        sys.exit(0)

    else:
        conn_s.close()
