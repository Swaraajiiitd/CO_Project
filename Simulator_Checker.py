def compare(a1,a2,n):
    a1=a1.split()
    a2=a2.split()
    for i in range(len(a1)):
        if a1[i]!=a2[i]:
            print('ERROR in Register:',i+1)

f=open(r'C:\Users\Swaraaj Krishna\OneDrive\Desktop\Co_project\output1.txt','r')
g=open(r'C:\Users\Swaraaj Krishna\OneDrive\Desktop\Co_project\simple_10_r.txt','r')


r1=f.read()
r2=g.read()
r1=r1.split('\n')
r2=r2.split('\n')
print(r1,'\n',r2,'\n',len(r1),len(r2))
for i in range(len(r1)):
    if r1[i].startswith('0x00010000:'):
     print('Data Memory')
    compare(r1[i],r2[i],i+1)
    print('Inst. No.: ',i)
