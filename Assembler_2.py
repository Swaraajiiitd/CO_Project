try:
        with open("Ex_test_5.txt", 'r') as f:
            instrn = f.read().splitlines()
            instrn = [x for x in instrn if x.strip()]  

        with open('Output.txt', 'w') as fh:
            binry = typ = ''
            temp = labladdress(instrn)
            pc = 0
            d = {
                'R': ['add', 'sub', 'slt', 'srl', 'or', 'and'],
                'I': ['lw', 'addi', 'jalr'],
                'S': ['sw'],
                'B': ['beq', 'bne'],
                'J': ['jal']
            }

            for i in instrn:
                i = i.replace(',', ' ')
                i = i.split()
                if not i: 
                    continue
                    
                if i[0][-1] == ':':
                    i = i[1:]
                    if not i: 
                        continue

             
                typ = ''
                for j in d:
                    for k in d[j]:
                        if k == i[0]:
                            typ = j
                            break
                    if typ:
                        break

                try:
                    if typ == 'R':
                        binry = fn7(i[0]) + ' ' + reg(i[3]) + ' ' + reg(i[2]) + ' ' + fn3(i[0]) + ' ' + reg(i[1]) + ' ' + opcode(typ, i[0])
                    
                    elif typ == 'I':
                        if len(i) == 3:  
                            j = 0
                            imm_str = ''
                            temp_str = i[2]  
                            
                           
                            while j < len(temp_str) and (temp_str[j].isdigit() or temp_str[j] == '-'):
                                imm_str += temp_str[j]
                                j += 1
                            
                            if not imm_str: 
                                imm_str = '0'
                            
                           
                            reg_str = temp_str[j:].strip('()')
                            
                           
                            i.append(imm_str)  
                            i[2] = reg_str   
                        
                       
                        imm_val = int(i[3])
                        if imm_val < 0:
                            imm = dec2bin(abs(imm_val))
                            while len(imm) < 12:
                                imm = '0' + imm
                            imm = complement(imm)
                        else:
                            imm = dec2bin(imm_val)
                            while len(imm) < 12:
                                imm = '0' + imm
                        
                        binry = imm + ' ' + reg(i[2]) + ' ' + fn3(i[0]) + ' ' + reg(i[1]) + ' ' + opcode(typ, i[0])
                    
                    elif typ == 'S':
                        j = 0
                        imm_str = ''
                        while j < len(i[2]) and (i[2][j].isdigit() or i[2][j] == '-'):
                            imm_str += i[2][j]
                            j += 1
                        
                        if not imm_str:
                            imm_str = '0'
                            
                        i.append(imm_str) 
                        i[2] = i[2][j:].strip('()')  # Update register
                        
                        imm_val = int(i[3])
                        if imm_val < 0:
                            imm = dec2bin(abs(imm_val))
                            while len(imm) < 12:
                                imm = '0' + imm
                            imm = complement(imm)
                        else:
                            imm = dec2bin(imm_val)
                            while len(imm) < 12:
                                imm = '0' + imm
                                
                        binry = imm[0:7] + ' ' + reg(i[2]) + ' ' + reg(i[1]) + ' ' + fn3(i[0]) + ' ' + imm[7:] + ' ' + opcode(typ, i[0])
                    
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
                        
                        if imm < 0:
                            imm_bin = dec2bin(abs(imm))
                            while len(imm_bin) < 12:
                                imm_bin = '0' + imm_bin
                            imm_bin = complement(imm_bin)
                        else:
                            imm_bin = dec2bin(imm)
                            while len(imm_bin) < 12:
                                imm_bin = '0' + imm_bin
                                
                        binry = (imm_bin[0] + ' ' + imm_bin[2:8] + ' ' + reg(i[2]) + ' ' + reg(i[1]) + ' ' + 
                                fn3(i[0]) + ' ' + imm_bin[8:12] + ' ' + imm_bin[1] + ' ' + opcode(typ, i[0]))
                    
                    elif typ == 'J':
                        for labl in temp:
                            if i[2] == labl:
                                imm = temp[labl] - pc
                                break
                        else:
                            if i[2].isdigit():
                                imm=int(i[2])
                            else:
                            raise ValueError(f"Undefined label: {i[2]}")
                        
                        if imm < 0:
                            imm_bin = dec2bin(abs(imm))
                            while len(imm_bin) < 20:
                                imm_bin = '0' + imm_bin
                            imm_bin = complement(imm_bin)
                        else:
                            imm_bin = dec2bin(imm)
                            while len(imm_bin) < 20:
                                imm_bin = '0' + imm_bin
                                
                        binry = imm_bin[0] + ' ' + imm_bin[10:] + ' ' + imm_bin[9] + ' ' + imm_bin[1:9] + ' ' + reg(i[1]) + ' ' + opcode(typ, i[0])
                    
                    print(binry)
                    fh.write(binry + '\n')
                    pc += 4

                except Exception as e:
                    print(f"Error processing instruction: {i}")
                    print(f"Error details: {str(e)}")
                    continue

except Exception as e:
        print(f"Error processing file: {str(e)}")
