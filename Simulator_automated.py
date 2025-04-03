import sys
try:
    def dec2hex(s):
        d={10:'A',11:'B',12:'C',13:'D',14:'E',15:'F'}
        r=''
        a=0
        while(s):
            if s%16>9:
                r+=d[s%16]
            else:
                r+=str((s%16))
            s//=16
            a+=1
        return r[::-1]
    def bin2dec(s):
        new=''
        if s[0]=='1' and len(s)!=5:
            for i in s:
                new+='0' if i=='1' else '1'
            s=new
        s=str(int(s))
        dec=a=0
        for i in s[::-1]:
            dec+=int(i)*2**a
            a+=1
        if new!='':
            return -1*(dec+1)
        else:
            return dec
    def dec2bin(s):
        r=a=0
        old=s
        if s<0:
            s=-1*(s+1)
        while(s):
            r+=(s%2)*10**a
            s//=2
            a+=1
        r=str(r)
        new=''
        while(len(r)!=32):
            r='0'+r
        if old<0:
            for i in r:
                new+='0' if i=='1' else '1'
            return new
        return r
        
    def type(s):
      d={'R':['0110011'],'I':['0000011','0010011','1100111'],'S':['0100011'],'B':['1100011'],'J':['1101111'],'rst':['0000000'],'halt':['1111111'],'rvrs':['0001000']}
      for i in d:
        for j in d[i]:
            if j==s:
                return i
      else:
        raise Exception("Invalid Opcode")
    def checkrgstr(s):
        for i in s:
            if i not in rgstr:
                raise Exception("Invalid Register")
    def Rtype(s):
        d={'000':'add','010':'slt','101':'srl','110':'or','111':'and','011':'mul'}
        rs2='x'+str(bin2dec(s[7:12:]))
        rs1='x'+str(bin2dec(s[12:17:]))
        rd='x'+str(bin2dec(s[20:25:]))
        checkrgstr([rs1,rs2,rd])
        rs1=rgstr[rs1]
        rs2=rgstr[rs2]
        f7=s[:7:]
        f3=s[17:20:]
        if f7=='0100000':
                rgstr[rd]=rs1-rs2
        elif f7=='0000000':
            oprtn=d[f3]
            if oprtn=='add':
                rgstr[rd]=rs1+rs2
            elif oprtn=='mul':   #f3 for mul:001 and f7 : 0000000
                rgstr[rd]=rs1*rs2
            elif oprtn=='slt':
                rgstr[rd]=1 if rs1<rs2 else 0 
            elif oprtn=='srl':
                rgstr[rd]=rs1//2**rs2
            elif oprtn=='or':
                '''r=a=0
                while(rs1 or rs2):
                    if rs1%2==1 or rs2%2==1:
                        r+=2**a
                        a+=1
                        rs1//=2
                        rs2//=2'''
                rgstr[rd]=rs1|rs2
            elif oprtn=='and':
                '''r=a=0
                while(rs1 or rs2):
                    if rs1%2==1 and rs2%2==1:
                        r+=2**a
                        a+=1
                        rs1//=2
                        rs2//=2'''
                rgstr[rd]=rs1&rs2
            else:
                raise Exception("Invalid RType Instruction")
        else:
            raise Exception("Invalid RType Instruction")
        rgstr['PC']+=4
        rgstr['x0']=0
    def IType(s):
        d={'0000011':'lw','0010011':'addi','1100111':'jalr'}
        oprtn=d[s[-7::]]
        imm=bin2dec(s[:12:])
        rs1='x'+str(bin2dec(s[12:17:]))
        rd='x'+str(bin2dec(s[20:25:]))
        checkrgstr([rs1,rd])
        rs1=rgstr[rs1]
        f3=s[17:20:]
        if f3 not in ['000','010']:
            raise Exception("Invalid IType Instruction")
        if oprtn=='lw':
            if ('000'+str(dec2hex(imm+rs1))) in dm:
             memadr=str(dec2hex(imm+rs1))
             rgstr[rd]=dm['000'+memadr]
            else:
                rgstr[rd]=sm[imm+rgstr['x2']]
            rgstr['PC']+=4
        elif oprtn=='addi':
            rgstr[rd]=rs1+imm
            rgstr['PC']+=4
        else:
            rgstr[rd]=rgstr['PC']+4
            rgstr['PC']=imm+rs1
        rgstr['x0']=0
    def SType(s):
        imm=bin2dec(s[:7:]+s[20:25:])
        if s[17:20:]!='010':
            raise Exception("Invalid SType Instruction")
        rs2='x'+str(bin2dec(s[7:12:]))
        rs1='x'+str(bin2dec(s[12:17:]))
        checkrgstr([rs1,rs2])
        if ('000'+str(dec2hex(imm+rgstr[rs1]))) in dm: 
          memadr=str(dec2hex(imm+rgstr[rs1]))
          dm['000'+memadr]=rgstr[rs2]
        else:
            sm[imm+rgstr['x2']]=rgstr[rs2]
        rgstr['PC']+=4
        rgstr['x0']=0
    def BType(s):
        imm=bin2dec(s[0]+s[24]+s[1:7:1]+s[20:24:1]+'0')
        rs1='x'+str(bin2dec(s[7:12:]))
        rs2='x'+str(bin2dec(s[12:17:]))
        checkrgstr([rs1,rs2])
        rs1=rgstr[rs1]
        rs2=rgstr[rs2]
        f3=s[17:20:]
        if f3=='000':
            if rs1==rs2:
                rgstr['PC']+=imm
            else:
                rgstr['PC']+=4
        elif f3=='001':
            if rs1!=rs2:
                rgstr['PC']+=imm
            else:
                rgstr['PC']+=4
        else:
            raise Exception("Invalid BType Instruction")
        rgstr['x0']=0
    def JType(s):
        imm=bin2dec(s[0]+s[12:20:1]+s[11]+s[1:11:]+'0')
        rd='x'+str(bin2dec(s[20:25:]))
        checkrgstr([rd])
        rgstr[rd]=rgstr['PC']+4
        rgstr['PC']+=imm
        rgstr['x0']=0
    input_file=sys.argv[1]
    output_file_bin=sys.argv[2]
    output_file_read=sys.argv[3]
    sm=dict()
    rgstr={'PC':0,'x0':0,'x1':0,'x2':380,'x3':0,'x4':0,'x5':0,'x6':0,'x7':0,'x8':0,'x9':0,'x10':0,'x11':0,'x12':0,'x13':0,'x14':0,'x15':0,'x16':0,'x17':0,'x18':0,'x19':0,'x20':0,'x21':0,'x22':0,'x23':0,'x24':0,'x25':0,'x26':0,'x27':0,'x28':0,'x29':0,'x30':0,'x31':0}
    dm={'00010000':0,'00010004':0,'00010008':0,'0001000C':0,'00010010':0,'00010014':0,'00010018':0,'0001001C':0,'00010020':0,'00010024':0,'00010028':0,'0001002C':0,'00010030':0,'00010034':0,'00010038':0,'0001003C':0,'00010040':0,'00010044':0,'00010048':0,'0001004C':0,'00010050':0,'00010054':0,'00010058':0,'0001005C':0,'00010060':0,'00010064':0,'00010068':0,'0001006C':0,'00010070':0,'00010074':0,'00010078':0,'0001007C':0,}
    with open(input_file,'r') as f:
        r=f.read().split('\n')
        c=0
        n=1
        ins_dic=dict()
        in_me_0=in_me_1=''
        for i in r:
            ins_dic[c]=i
            c+=4
        while True:
            i=ins_dic[rgstr['PC']]
            op=type(i[-7::])
            if op=='R':
                Rtype(i)
            elif op=='I':
                IType(i)
            elif op=='S':
                SType(i)
            elif op=='B':
                BType(i)
            elif op=='J':
                JType(i)
            elif op=='rst': #opcode for rst:0000000
                for j in rgstr:
                    if j!='PC':
                        rgstr[j]=0
                rgstr['PC']+=4
            elif op=='halt':  #opcode for halt:1111111
                break
            elif op=='rvrs':  #opcode for rvrs:0001000
                rs1='x'+str(bin2dec(i[12:17:]))
                rs1=dec2bin(rgstr[rs1])
                rd='x'+str(bin2dec(i[20:25:]))
                d=rs1[::-1]
                rgstr[rd]=bin2dec(d)
                rgstr['PC']+=4
            else:
                raise Exception("Invalid Opcode")
            for j in rgstr:
                  in_me_1+=str(rgstr[j])+' '
                  in_me_0+='0b'+dec2bin(rgstr[j])+' '
            in_me_1+='\n'
            in_me_0+='\n'
            #print('Instruction:',rgstr['PC'])
            n+=1
            if i=='00000000000000000000000001100011':
                break 
        with open(output_file_bin,'w') as g:
             da_me_0=da_me_1=''
             for i in dm:
                da_me_1+='0x'+i+':'+str(dm[i])+'\n'
                da_me_0+='0x'+i+':'+'0b'+dec2bin(dm[i])+'\n'
             g.write(in_me_0+da_me_0)
        with open(output_file_read,'w') as h:
                h.write(in_me_1+da_me_1)

except Exception as e:
        print(f"Error processing file: {str(e)}")