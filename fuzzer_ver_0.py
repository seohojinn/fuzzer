import sys

program = sys.argv[1]

f = open(program,'r')

vuln_funcs = ['strcpy','scanf','gets','cin','strcat','sprintf']
value = []

i = 0

lines = f.readlines()

for line in lines:

    i += 1
    for vuln_func in vuln_funcs:
        if vuln_func in line:
            value.append(str(i) + "번째 line " + vuln_func + " 함수 탐지 ##")

for data in value:
    print(data)

if len(value) == 0:
    print("== 탐지된 함수 없음 == ")

f.close()
