#!/usr/bin/python3

from datetime import date
import time
import matplotlib.pyplot as plt
import serial
import RPi.GPIO as GPIO
import os
import sys

from read_m5_class import m5logger
from readser_class import readser

today = date.today()
t=time.localtime()
current_time=time.strftime("_H%H_M%M_S%S",t)
fn="ACS_LOG_"+str(today)+current_time+".csv"
f=open(fn,'w',encoding="utf-8")
start = time.time()

ldata0=[0]*10
ldata=[ldata0]*10
ser1 = serial.Serial("/dev/ttyACM0",9600)
ser2 = serial.Serial("/dev/ttyACM1",9600)
ser3 = serial.Serial("/dev/ttyUSB0",115200)
read_ser1=readser()
read_ser2=readser()
sport=m5logger()

data=[0]*10
data02=[0]*3
data2=[data02]*10
data03=[0]*10
data3=[data03]*10

fig, ax = plt.subplots(2, 2)
while True:
 try:
  ttime=time.time()-start
  if ttime<0.001:
    ttime=0.0
  st=time.strftime("%Y %b %d %H:%M:%S", time.localtime())
  ss=str(time.time()-int(time.time()))
  rttime=round(ttime,2)
  curr1=read_ser1.read(ser1)
  curr2=read_ser1.read(ser2)
  if curr1[0]=="CUR":
    cur=float(curr1[1])
  else:
    dcu=[float(curr1[1]),float(curr1[2]),float(curr1[3])]
  if curr2[0]=="DCU":
    dcu=[float(curr2[1]),float(curr2[2]),float(curr2[3])]
  else:
    cur=float(curr2[1])
  array2=sport.read_logger(ser3)
  ss=st+ss[1:5]+","+str(rttime)+","
  ss12=ss
  ss=ss+str(cur)+","
  for i in range(0,len(array2)-1):
    ss=ss+str(array2[i])+","
  ss=ss+str(array2[len(array2)-1])
  f.write(ss+"\n")
  print("dcu=",dcu)
  data.pop(-1)
  data2.pop(-1)
  data3.pop(-1)
  data.insert(0,cur)
  data2.insert(0,dcu)
  data3.insert(0,array2)
  rez2 = [[data2[j][i] for j in range(len(data2))] for i in range(len(data2[0]))] # transposing a matrix
  rez3 = [[data3[j][i] for j in range(len(data3))] for i in range(len(data3[0]))] # transposing a matrix
#
#
  x=range(0, 10, 1)
#  plt.figure(100)
#  plt.clf()
#  ax[0,0].ylim(-25,30)
  tl=[0]*10
  h3=[]
  for i in range(0,10):
   tl[i],=ax[0,0].plot(x,rez3[i],label="T"+str(i))
  for i in range(0,10):
    h3.append(tl[i])
  ax[0,0].legend(handles=h3)
#  plt.pause(0.1)
#
#  plt.figure(200)
#  plt.clf()
#  ax[0,1].ylim(0,400000)
  ax[0,1].plot(x,data)
#  plt.pause(0.1)
#
#  plt.figure(300)
#  plt.clf()
#  ax[1,0].ylim(0,150)
  tl=[0]*3
  h2=[]
  for i in range(0,len(rez2)):
   tl[i],=ax[1,0].plot(x,rez2[i],label="C"+str(i))
  for i in range(0,len(rez2)):
    h2.append(tl[i])
  ax[1,0].legend(handles=h2)
#
  fig.tight_layout()
  plt.show()
  plt.pause(0.1)
  plt.clf()
 except KeyboardInterrupt:
  f.close()
  ser1.close()
  ser2.close()
  ser3.close()
  exit()
