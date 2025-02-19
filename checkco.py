def compare(a1,a2,n):
    for i in range(len(a1)):
        if a1[i]!=a2[i]:
            print(i+1,' ')
    print('Inst. No.',n)
f=open(r'C:\Users\Sameeksha Jain\Documents\IP\c programs\generated.txt','r')
g=open(r'C:\Users\Sameeksha Jain\Documents\IP\c programs\given.txt','r')
r1=f.read()
r2=g.read()
r1=r1.split('\n')
r2=r2.split('\n')
print(r1,'\n',r2,'\n',len(r1),len(r2))
for i in range(len(r1)):
    if r1[i]!='':
     compare(r1[i],r2[i],i+1)
     print('Hi')
