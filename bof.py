# python3
# used to exploit buffeOverflow vulnerabilities 
# BOF script
import sys,os
import codecs
import math
import re






if(float(sys.version[:3])<=3.6):
 print("python Version 3 is required ")
 exit()

banner = """ 
\033[1;31;49m
    ____   ____  ______ 
   |  _ \\ / __ \\|  ____|
   | |_) | |  | | |__   \033[0m
   \033[96m|  _ <| |  | |  __|  \033[0m
   \033[93m| |_) | |__| | |     
   |____/ \\____/|_|     \033[0m
                     


                            email:rayane101213@gmail.com
\nUsage : python3 bof.py [options...] [input]                                                        
Tool to help exploiting Buffer_Overflow Vulnerabilities  
type --help for more options

"""
print(banner)

#colors 
blue = "\033[34m"
red = "\033[1;31;49m"
bold = "\033[01m"
end = "\033[0m"
yellow='\033[93m'

#badchars 
def badchars(value): 

 c = 256
 
 string = ""
 for i in range(c):
  data = str(hex(i))
  if(i<16):
    data = data.replace("0x","\\x0")
  else:
    data = data.replace("0x","\\x")
  string += data

 n = value*4
 chunks = [string[i:i+n] for i in range(0, len(string), n)]
 
 return chunks




#offset generator

A  = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" # 41-5A hex 
B = "abcdefghijklmnopqrst"       # 61-7A hex
C   = "0123456789"                 # 30-39 hex


def Generate_string(wanted_length):
 
  string = ""
  string_length=int(wanted_length)
  string2 = ""
  if(len(string)<int(wanted_length)):
   for a in A:
    for b in B:
     for c in C:
      string += a+b+c
  
  for counter in string:
   if(len(string2)<string_length):
    string2 += counter

  return string2 


def splits(data,data_len):  #split the hex number into array of 2 numbers
#example 0xff0a ==> [ff,0a]
 arr = []
 arr2= []

 for i in range(data_len):
  ii = i % 2
  if(ii == 0 ):
   arr.append(str(i))

 end = str(int(arr[-1])+2)
 arr.append(end)

 for i in arr:
   i = int(i)
   data_hex = str(data[i:i+2])
   arr2.append(data_hex)	
 arr2.pop()
 return arr2
   
def sort_arry(arry,sort): # hex sort // ff0a sorted in [\xff\x0a] or [ff 0a] 
 strin = ""
 for i in arry:
  strin += i+sort
 return strin

def reverse_array(arr3,sort): #hex reverse ff0a to 0aff or [\x0a\xff] 
 arr3.reverse() 
 my_hex_reversed =""
 for i in arr3:
  my_hex_reversed += "{}{}".format(sort,i)
 return my_hex_reversed


def ASCII_to_Hex_reversed_pattern(asciis): #FF0A => \x0A\xFF
   
  if(re.search("0x",asciis)):
   asciis = asciis.replace("0x","")

  data = asciis
  data_len = len(data)
  
  myData = splits(data,data_len)
  #reverse hex
  hexadecimal = reverse_array(myData,"\\x")
  return hexadecimal

#print("\033[1;31;49m[*] \033[0mreversed Hexa  : {}".format(ASCII_to_Hex_reversed_pattern()))
  

def string_to_hex(value):
 byte = bytes(value,"ascii")
 somethinghex = codecs.encode(byte,"hex").decode('ascii')
 return somethinghex

def string_to_reversed_hex(value):
 hel = string_to_hex(value)
 data = ASCII_to_Hex_reversed_pattern(hel)
 return data

def hex_to_string(value):
 byte = bytes(value,"ascii")
 somethinghex = codecs.encode(byte,"ascii")
 return something


def byte_to_string(value):
 bytes_object = bytes.fromhex(value[0:])
 ascii_string = bytes_object.decode("ASCII")
 return str(ascii_string)


def find_the_offset(something,length): # and givin the info #gihub
 data = Generate_string(length)
 string = ""
 
 somethinghex = something
 datahex = string_to_hex(data)
  
 somethinghex_splited = splits(somethinghex,len(somethinghex))
 somethinghex_splited_hexa = reverse_array(somethinghex_splited,"")
 
 datahex_splited = splits(datahex,len(datahex))
 datahex_splited_hexa = reverse_array(datahex_splited,"")
 
 
 
 try:
  re.search(something,datahex_splited_hexa) 
  bytes_object = bytes.fromhex(somethinghex_splited_hexa[0:])
  ascii_string = bytes_object.decode("ASCII")
  print(bold+blue+"[*]"+end+" Offset :   {}".format(ascii_string))
  print(bold+blue+"[*]"+end+" Offset hex : 0x{}".format(somethinghex_splited_hexa))
  

  data = data.split(ascii_string)
  print(bold+blue+"[*]"+end+" python [ paylod = A*{} ]".format(len(data[0])))
 except:
  print(bold+red+"[-]"+end+" Failed to find the offset")


#Ab1Ab 4162314162
#6241316241

os.system("clear")
print(banner)
d=0
for i in sys.argv:
 i = str(i)
 if(i=="--help" or i=='-h'):
  print("""
    --badchars   / -bc   -generate bad characterslist option[-bc length]
    --pattern    / -p    -generate pattern by specifyin the length [-p 500]
    --hexrev     / -hex  -reverse a hexa string [FF5a = \\x5a\\FF]
    --offsetptrn / -ofp  -search in pattern by specific length [-ofp 5aFF 100] 
  	""")
 else:
  
  if(i=='--badchars' or i=="-bc"):
   d+=1
  
   try:
    datfa = sys.argv[d+1]
    print(bold+blue+"[*]"+end+" badchars generate succefully \n")
    for ff in badchars(int(datfa)):
     print("buffer += {}".format(ff))
    d+=1
   except:
    print(bold+red+"[-]"+end+" faild to generate badchars \n")


  if(i=='--pattern' or i=="-p"):

   d+=1
   try:
    length=str(sys.argv[d+1])
    print(bold+blue+"\n[*]"+end+" patter generated succefully\n\n{}\n".format(Generate_string(length)))
    d+=1
   except:
   	print("\n{}{}[-]\033[0m failed to generate the pattern \n".format(bold,red))
  
  if(i=="--hexrev"  or i=="-hex" ):
   d+=1
   
   try:
    ptrn=str(sys.argv[d+1])
    d+=1
    print(bold+blue+"\n[*]"+end+" hexa reversed succefully")
    print("\033[01m\033[34m[*]\033[0m reversed Hex ["+ptrn+"] "+red+"==>"+end+" {}\n\n".format(ASCII_to_Hex_reversed_pattern(ptrn)))
   except:
   	print(bold+red+"[-]"+end+" failed to reverse hexa "+"\n\n")

  if(i=="--offsetptrn"  or i=="-ofp"):
   d+=1
   off =str(sys.argv[d+1])
   d+=1
   length = len(sys.argv[d+1])
   d+=1
   try:
    if(int(length)<=1):
     print(bold+red+"[-]"+end+"please Enter The patter length ")
    else:
     find_the_offset(off,length)
     print()

   except:
   	print()
   else:
    print("Command not found , type -h or --help ") 
	








