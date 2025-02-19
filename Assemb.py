import math
def opcode(typ,fn):
    d={'R':'0110011','I':{'lw':'0000011','addi':'0010011','jalr':'1100111'},'S':'0100011','B':'1100011','J':'1101111'}
    for i in d:
        if i==typ:
            if i=='I':
                for j in d[i]:
                    if j==fn:
                        op=d[i][j]
                        break
            else:
             op=d[i]
            break
    return op
def reg(r):
    d={'zero':0,'ra':1,'sp':2,'gp':3,'tp':4,'t0':5,'t1':6,'t2':7,'s0':8,'fp':8,'s1':9}
    for i in d:
        if i==r:
            dec=d[i]
            break
    else:
        if r[0]=='a' & r[1]>'1':
            dec=10+int(r[1])
        elif r[0]=='s' & r[1]>'1':
            dec=16+int(r[1])
        elif r[0]=='t' & r[1]>'2':
            dec=25+int(r[1])
    bin=dec2bin(dec)
    while(len(bin)!=5):
        bin='0'+bin
    return bin
def fn3(a):
    d={'000':['add','sub','addi','jalr','beq'],'010':['slt','lw','sw'],'101':['srl'],'110':['or'],'111':['and'],'001':['bne']}
    for i in d:
        for j in d[i]:
            if j==a:
                return i
    print("Undefined Instruction")
    return
def fn7(a):
    if a=='sub':
        return '0100000'
    else:
        return '0000000'
def dec2bin(dec):
    bin=0
    if dec==0:
        return str(bin)
    num=dec
    for i in range((int(math.log(num,2)))+1):
        d=dec%2
        bin+=d*10**i
        dec=dec//2
    bin=str(bin)
    return bin
def labladdress(instrn):
    temp=dict()
    pc=0
    for i in instrn:
     i=i.replace(',',' ')
     i=i.split()
     if i[0][-1]==':':
        temp[i[0][:-1]]=pc
     pc+=4
    return temp
def complement(imm):
    imm=1
    neg=''
    for i in imm:
        neg+='1' if i=='0' else '0'
    return neg

    


f=open(r"C:\Users\Sameeksha Jain\Downloads\Ex_test_1.txt",'r')
fh=open('Output.txt','w')
instrn=f.read()
instrn=instrn.split('\n')
instrn=instrn[:-1]
print(instrn)
binry=typ=''
temp=labladdress(instrn)
print(temp)
pc=0
d={'R':['add','sub','slt','srl','or','and'],'I':['lw','addi','jalr'],'S':['sw'],'B':['beq','bne'],'J':['jal']}
for i in instrn:
    i=i.replace(',',' ')
    i=i.split()
    if i[0][-1]==':':
        i=i[1:]
    for j in d:
        for k in d[j]:
            if k==i[0]:
                typ=j
                break
        else:
            continue
        break
    if typ=='R':
        binry=fn7(i[0])+' '+reg(i[3])+' '+reg(i[2])+' '+fn3(i[0])+' '+reg(i[1])+' '+opcode(typ,i[0])
    elif typ=='I':
        if len(i)==3:
            j=0
            i.append('')
            while(i[2][j].isdigit()):
                i[3]+=i[2][j]
                j+=1
            i[2]=i[2][j+1:-1]
        if int(i[3])<0:
            imm=dec2bin(abs(int(i[3]))-1)
            imm=complement(imm)
        else:
            imm=dec2bin(int(i[3]))
        while(len(imm)<12):
            imm=imm[0]+imm
        binry=imm+' '+reg(i[2])+' '+fn3(i[0])+' '+reg(i[1])+' '+opcode(typ,i[0])
    elif typ=='S':
        j=0
        i[3]=''
        while(i[2][j].isdigit()):
                i[3]+=i[2][j]
                j+=1
        i[2]=i[2][j:]
        if int(i[3])<0:
            imm=dec2bin(abs(int(i[3]))-1)
            imm=complement(imm)
        else:
            imm=dec2bin(int(i[3]))
        while(len(imm)<12):
            imm=imm[0]+imm
        binry=imm[11:4:-1]+' '+reg(i[2])+' '+reg(i[1])+' '+fn3(i[0])+' '+imm[4::-1]+' '+opcode(typ,i[0])
    elif typ=='B':
        if i[3].isdigit():
            imm=int(i[3])
        else: 
         for labl in temp:
            if i[3]==labl:
                imm=pc-temp[labl]
                break
        if imm<0:
            imm=dec2bin(abs((imm))-1)
            imm=complement(imm)
        else:
            imm=dec2bin(imm)
        while(len(imm)<12):
            imm=imm[0]+imm
        bin=imm[11]+imm[9:3:-1]+' '+reg(i[2])+' '+reg(i[1])+' '+fn3(i[0])+imm[3::-1]+imm[10]+opcode(typ,i[0])
    elif typ=='J':
        for labl in temp:
            if i[2]==labl:
                imm=pc-temp[labl]
                break
        if int(i[3])<0:
            imm=dec2bin(abs((imm))-1)
            imm=complement(imm)
        else:
            imm=dec2bin(imm)
        while(len(imm)<20):
            imm=imm[0]+imm
        bin=imm[19]+imm[9::-1]+imm[10]+imm[18:10:-1]+' '+reg(i[1])+' '+opcode(typ,i[0])
    print(binry)
    fh.write(binry+'\n')
    pc+=4
fh.close()




        
        

