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
            dec = 16 + int(r[1:])
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
    else:
      raise Exception("Undefined Instruction")
      

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

def labladdress(instrn): #creating a dictionary of labels and its addresses as key-value pairs present in the given input file
    temp = dict()
    pc = 0
    for i in instrn:
        i = i.replace(',', ' ')
        i = i.split()
        if i and i[0].count(':')>0: 
            n=i[0].find(':')
            if i[0][:n] not in temp:
              temp[i[0][:n]] = pc
            else:
                raise Exception('Multiple labels with same name')
        pc += 4
    return temp

def complement(imm): #getting 2's complement
    neg = ''
    for i in imm:
        neg += '1' if i == '0' else '0'
    return neg


try:
        with open("assembler.txt", 'r') as f:
            instrn = f.read().splitlines()
            instrn = [x for x in instrn if x.strip()]  # Remove empty lines
            for i in instrn:
                i=i.replace(' ','')
                if i=='beqzero,zero,0':
                    break
            else:
                raise Exception("Virtual Halt missing")

        with open('Output.txt', 'w') as fh:            
            binry = typ = ''
            temp = labladdress(instrn) #getting a dictionary of labels and corresponding addresses
            pc = 0
            d = {
                'R': ['add', 'sub', 'slt', 'srl', 'or', 'and'],
                'I': ['lw', 'addi', 'jalr'],
                'S': ['sw'],
                'B': ['beq', 'bne'],
                'J': ['jal']
            }
            #Traversing through each instruction line and converting it to binary
            for i in instrn:
                for j in i:       #Adding a space between label and instruction if not present
                    n=i.find(':')
                    if j==':' and i[n+1]!=' ':
                        i=list(i)
                        i.insert(n+1,' ')
                        i=''.join(i)
                i = i.replace(',', ' ') #splitting an instruction into a list of instruction name,immediates,registers, label, etc. 
                i = i.split()
                if not i:  # Skip empty lines
                    continue
                    
                if i[0][-1] == ':':   #removing label from instruction list
                    i = i[1:]
                    if not i:  # Skip label-only lines
                        continue

                # Find instruction type
                typ = ''
                for j in d:
                    for k in d[j]:
                        if k == i[0]:
                            typ = j
                            break
                    if typ:
                        break
                else:
                    raise Exception("Undefined Instruction")
                

                #converting assembly instruction to binary according to its type
                try:           
                    if typ == 'R':
                        binry = fn7(i[0]) + reg(i[3]) + reg(i[2]) + fn3(i[0])+ reg(i[1])+ opcode(typ, i[0])
                    
                    elif typ == 'I':
                        if len(i) == 3:  # Memory-type instruction- lw
                            j = 0
                            imm_str = ''
                            temp_str = i[2]  # Store the operand like "4(t0)"
                            
                            # Extract immediate value
                            while j < len(temp_str) and (temp_str[j].isdigit() or temp_str[j] == '-'):
                                imm_str += temp_str[j]
                                j += 1
                            
                            if not imm_str:  # If no immediate value found
                                imm_str = '0'
                            
                            # Get the register name from between parentheses
                            reg_str = temp_str[j:].strip('()')
                            
                            # Update instruction parts
                            i.append(imm_str)  # Add immediate as i[3]
                            i[2] = reg_str    # Update register
                        
                        # Convert immediate value to binary
                        imm_val = int(i[3])
                        if abs(imm_val)> 2**11-1:
                            raise Exception("Immediate Overflow")
                        if imm_val < 0:
                            imm = dec2bin(abs(imm_val)-1)  #-1 to compensate for non-addition of +1 in 1's complement 
                            while len(imm) < 12:
                                imm = '0' + imm
                            imm = complement(imm)
                        else:
                            imm = dec2bin(imm_val)
                            while len(imm) < 12:
                                imm = '0' + imm
                       
                        binry = imm + reg(i[2]) + fn3(i[0]) + reg(i[1]) + opcode(typ, i[0])
                    
                    elif typ == 'S':
                        j = 0
                        imm_str = ''
                        while j < len(i[2]) and (i[2][j].isdigit() or i[2][j] == '-'):
                            imm_str += i[2][j]
                            j += 1
                        
                        if not imm_str:
                            imm_str = '0'
                            
                        i.append(imm_str)  # Add as i[3]
                        i[2] = i[2][j:].strip('()')  # Update register
                        imm_val = int(i[3])
                        if abs(imm_val)> 2**11-1:
                            raise Exception("Immediate Overflow")
                        if imm_val < 0:
                            imm = dec2bin(abs(imm_val)-1)
                            while len(imm) < 12:
                                imm = '0' + imm
                            imm = complement(imm)
                        else:
                            imm = dec2bin(imm_val)
                            while len(imm) < 12:
                                imm = '0' + imm
                                
                        binry = imm[0:7] + reg(i[1])+ reg(i[2]) + fn3(i[0])+ imm[7:]+ opcode(typ, i[0])
                    
                    elif typ == 'B':
                        if i[3].isdigit() or i[3].startswith('-'):
                            imm = int(i[3])
                        else:
                            for labl in temp:
                                if i[3] == labl:
                                    imm = temp[labl] - pc
                                    break
                            else:
                                raise ValueError(f"Undefined label: {i[3]}")
                        if abs(imm)> 2**12-1:
                            raise Exception("Immediate Overflow")
                        
                        if imm < 0:
                            imm_bin = dec2bin(abs(imm)-1)
                            while len(imm_bin) < 13:
                                imm_bin = '0' + imm_bin
                            imm_bin = complement(imm_bin)
                        else:
                            imm_bin = dec2bin(imm)
                            while len(imm_bin) < 13:
                                imm_bin = '0' + imm_bin
                        
                        binry = (imm_bin[0] + imm_bin[2:8] + reg(i[2]) +  reg(i[1]) +
                                fn3(i[0]) + imm_bin[8:12] + imm_bin[1] + opcode(typ, i[0]))
                    
                    elif typ == 'J':
                        for labl in temp:
                            if i[2] == labl:
                                imm = temp[labl] - pc
                                break
                        else:
                            if i[2].isdigit:
                                imm=int(i[2])
                            else:
                                raise ValueError(f"Undefined label: {i[2]}")
                        if abs(imm_val)> 2**20-1:
                            raise Exception("Immediate Overflow")
                        if imm < 0:
                            imm_bin = dec2bin(abs(imm)-1)
                            while len(imm_bin) < 21:
                                imm_bin = '0' + imm_bin
                            imm_bin = complement(imm_bin)
                        else:
                            imm_bin = dec2bin(imm)
                            while len(imm_bin) < 21:
                                imm_bin = '0' + imm_bin
                                
                        binry = imm_bin[0] + imm_bin[10:20] + imm_bin[9] + imm_bin[1:9] + reg(i[1]) +  opcode(typ, i[0])
                    
                    fh.write(binry + '\n')
                    pc += 4

                except Exception as e:
                    print(f"Error processing instruction: {i}")
                    print(f"Error details: {str(e)}")
                    break

except Exception as e:
        print(f"Error processing file: {str(e)}")
