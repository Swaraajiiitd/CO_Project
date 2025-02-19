import math

def opcode(typ, fn):
    d = {
        'R': '0110011',
        'I': {'lw': '0000011', 'addi': '0010011', 'jalr': '1100111'},
        'S': '0100011',
        'B': '1100011',
        'J': '1101111'
    }
    for i in d:
        if i == typ:
            if i == 'I':
                for j in d[i]:
                    if j == fn:
                        op = d[i][j]
                        break
            else:
                op = d[i]
            break
    return op

def reg(r):
    d = {
        'zero': 0, 'ra': 1, 'sp': 2, 'gp': 3, 'tp': 4,
        't0': 5, 't1': 6, 't2': 7, 's0': 8, 'fp': 8, 's1': 9
    }
    for i in d:
        if i == r:
            dec = d[i]
            break
    else:
        if r[0] == 'a' and r[1].isdigit():
            dec = 10 + int(r[1])
        elif r[0] == 's' and r[1].isdigit():
            dec = 16 + int(r[1])
        elif r[0] == 't' and r[1].isdigit():
            dec = 25 + int(r[1])
    bin = dec2bin(dec)
    while len(bin) != 5:
        bin = '0' + bin
    return bin

def fn3(a):
    d = {
        '000': ['add', 'sub', 'addi', 'jalr', 'beq'],
        '010': ['slt', 'lw', 'sw'],
        '101': ['srl'],
        '110': ['or'],
        '111': ['and'],
        '001': ['bne']
    }
    for i in d:
        for j in d[i]:
            if j == a:
                return i
    print("Undefined Instruction")
    return

def fn7(a):
    if a == 'sub':
        return '0100000'
    else:
        return '0000000'

def dec2bin(dec):
    if dec == 0:
        return '0'
    bin_str = ''
    num = abs(dec)
    while num > 0:
        bin_str = str(num % 2) + bin_str
        num //= 2
    return bin_str

def labladdress(instrn): 
    temp = dict()
    pc = 0
    for i in instrn:
        i = i.replace(',', ' ')
        i = i.split()
        if i and i[0][-1] == ':':  
            temp[i[0][:-1]] = pc
        pc += 4
    return temp

def complement(imm):
    neg = ''
    for i in imm:
        neg += '1' if i == '0' else '0'
    return neg

