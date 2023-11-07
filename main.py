"""
This file runs Ising simulation
Created: Mar. 30, 2019
Last Edited: Apr. 6, 2019
By Bill
修改  by 卜佳锐 2023-10-28
"""

import IsingGrid
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from copy import deepcopy


#---------------Simulation---------------------

def MCrun(eq_steps, sample_steps, interval, temperature):
    '''进行Monte Carlo模拟, 弛豫并采样, 输出 [m, 磁化率Xa]. '''
    
    
    m2list=[]       # m^2
    mlist=[]
    Xlist=[]

    g.orderize_upordown(g.size)

    for step in range(eq_steps):        #弛豫

        g.singleFlip(temperature)
        # clusterSize = g.clusterFlip(temperature)      #疑似会导致死循环<<<<<

    for step in range(sample_steps):

        g.singleFlip(temperature)
        if (step + 1) % interval == 0:      #采样
            
            m2list.append(g.avrM2()  )            #注意调用方法时, 后面要加括号!!
            mlist.append(  g.avrM() )               #有正有负才对!!!!
            
            Xlist.append( ( g.avrM2() - g.avrM()**2 )/temperature )     #暂时不乘离子数N. <<<<<<<<<

    m=np.mean(mlist)
    
    Xa=np.mean(Xlist)

    # Xa=size**2/temperature *(np.mean(m2list)-m**2)      #平均磁化率 per spin    #好像定义不太对. 如何定义"平均"

    return [m, Xa]
    
    # if (step + 1) % (10 * interval) == 0:
    #     print("Step ", step + 1, "/", eq_steps, ", Cluster size ", clusterSize, "/", size * size)



#---------------Fundamental parameters------------------

size = 40
# temperature = 10
eq_steps = 7500         #弛豫步数
pre_eq_steps=30000

interval = 5      #采样间隔
sample_steps=2000*interval    #采样步数

Jfactor = 97
H=0

# Generate grid

g = IsingGrid.Grid(size, Jfactor,H)



#--------------------第1问  m~T关系------------------------------------

Tarray=np.arange(100, 300, 10)
mdata=[]

for T in Tarray:
    
    m1=MCrun(eq_steps, sample_steps, interval, T)[0]
    mdata.append( abs(m1))

#--------------------plot----------------------
plt.rcParams['font.sans-serif']=['STSong']     # 中文宋体

fig1=plt.figure(num=1)
ax1 = fig1.add_subplot(1,1,1)
ax1.scatter(Tarray, mdata)
ax1.set_xlabel('T')
ax1.set_ylabel('平均磁矩m')
ax1.set_title('Size=%d,  J=%.1f,  H=%.1f' %(size, Jfactor, H) )
plt.show()


#---------------------第2问  不同size, m,X随T变化关系-----------------------------------
# Sizelist=[10, 50, 100, 200]
# Tarray=np.arange(120, 300, 5)
# mdata=np.zeros((len(Sizelist), len(Tarray) ))
# Xdata=np.zeros((len(Sizelist), len(Tarray) ))

# for i in range(len(Sizelist) ):         #手动调试<<<<<<
#     size=Sizelist[i]
#     eq_steps= size**2 
#     pre_eq_steps=4* size**2
#     interval=1
#     sample_steps=size**2 *interval +400

#     mrow=[]
#     Xrow=[]

#     # g.orderize(size)        #有序初始化
#     # g.randomize()


#     # for step in range(pre_eq_steps):        #预先弛豫

#     #     g.singleFlip(Tarray[0])

#     for T in Tarray:
        
#         tempm, tempX=MCrun(eq_steps, sample_steps, interval, T)
#         mrow.append(tempm )
#         Xrow.append(tempX )
        

#     mdata[i]=mrow
#     Xdata[i]=Xrow

# #---------plot----------
# plt.rcParams['font.sans-serif']=['STSong']     # 中文宋体

# fig2=plt.figure(num=2)
# ax1 = fig2.add_subplot(2,4,1)
# ax1.scatter(Tarray, mdata[0])
# ax1.set_xlabel('T')
# ax1.set_ylabel('平均磁矩m')
# ax1.set_title('Size=%d' %(10,) )

# ax2 = fig2.add_subplot(2,4,2)
# ax2.scatter(Tarray, mdata[1])
# ax2.set_xlabel('T')
# ax2.set_ylabel('平均磁矩m')
# ax2.set_title('Size=%d' %(50, ) )

# ax3 = fig2.add_subplot(2,4,3)
# ax3.scatter(Tarray, mdata[2])
# ax3.set_xlabel('T')
# ax3.set_ylabel('平均磁矩m')
# ax3.set_title('Size=%d' %(100,) )

# ax4 = fig2.add_subplot(2,4,4)
# ax4.scatter(Tarray, mdata[3])
# ax4.set_xlabel('T')
# ax4.set_ylabel('平均磁矩m')
# ax4.set_title('Size=%d' %(200, ) )

# ax5 = fig2.add_subplot(2,4,5)
# ax5.scatter(Tarray, Xdata[0])
# ax5.set_xlabel('T')
# ax5.set_ylabel('平均磁化率X')
# ax5.set_title('Size=%d' %(10, ) )

# ax6 = fig2.add_subplot(2,4,6)
# ax6.scatter(Tarray, Xdata[1])
# ax6.set_xlabel('T')
# ax6.set_ylabel('平均磁化率X')
# ax6.set_title('Size=%d' %(50, ) )

# ax7 = fig2.add_subplot(2,4,7)
# ax7.scatter(Tarray, Xdata[2])
# ax7.set_xlabel('T')
# ax7.set_ylabel('平均磁化率X')
# ax7.set_title('Size=%d' %(100,) )

# ax8 = fig2.add_subplot(2,4,8)
# ax8.scatter(Tarray, Xdata[3])
# ax8.set_xlabel('T')
# ax8.set_ylabel('平均磁化率X')
# ax8.set_title('Size=%d  ' %(200,) )


# plt.tight_layout()
# plt.show()


#---------------------第3问  不同H, m,X随T变化关系---------------应该把m正负分开画更好!!--------------------
# Hlist=[Jfactor/10, Jfactor/5, Jfactor/3, Jfactor/2, Jfactor]
# size=20
# eq_steps = 3000        #弛豫步数
# pre_eq_steps=900

# interval = 2      #采样间隔
# sample_steps=1500*interval    #采样步数

# Tarray=np.arange(120, 600, 10)
# mdata=np.zeros((len(Hlist), len(Tarray) ))
# Xdata=np.zeros((len(Hlist), len(Tarray) ))

# for i in range(len(Hlist)):
#     H=Hlist[i]
#     mrow=[]
#     Xrow=[]

#     # g.orderize_upordown(size)        #有序初始化
#     # g.randomize()

#     # for step in range(pre_eq_steps):        #预先弛豫  #MC自带初始化了, 不需要预弛豫了. 

#     #     g.singleFlip(Tarray[0])

#     for T in Tarray:
    
#         tempm, tempX=MCrun(eq_steps, sample_steps, interval, T)
#         mrow.append(tempm )
#         Xrow.append(tempX )
        

#     mdata[i]=mrow
#     Xdata[i]=Xrow             

# plt.rcParams['font.sans-serif']=['STSong']     # 中文宋体
# fig3=plt.figure(num=3)

# ax1 = fig3.add_subplot(2,5,1)
# ax1.scatter(Tarray, mdata[0])
# ax1.set_xlabel('T')
# ax1.set_ylabel('平均磁矩m')
# ax1.set_title('H=%.1f' %(9.7,) )

# ax2 = fig3.add_subplot(2,5,2)
# ax2.scatter(Tarray, mdata[1])
# ax2.set_xlabel('T')
# ax2.set_ylabel('平均磁矩m')
# ax2.set_title('H=%.1f' %(19.4, ) )

# ax3 = fig3.add_subplot(2,5,3)
# ax3.scatter(Tarray, mdata[2])
# ax3.set_xlabel('T')
# ax3.set_ylabel('平均磁矩m')
# ax3.set_title('H=%.1f' %(32.3, ) )

# ax4 = fig3.add_subplot(2,5,4)
# ax4.scatter(Tarray, mdata[3])
# ax4.set_xlabel('T')
# ax4.set_ylabel('平均磁矩m')
# ax4.set_title('H=%.1f' %(48.5, ) )

# ax5 = fig3.add_subplot(2,5,5)
# ax5.scatter(Tarray, mdata[4])
# ax5.set_xlabel('T')
# ax5.set_ylabel('平均磁矩m')
# ax5.set_title('H=%.1f' %(97, ) )

# ax6 = fig3.add_subplot(2,5,6)
# ax6.scatter(Tarray, Xdata[0])
# ax6.set_xlabel('T')
# ax6.set_ylabel('平均磁化率X')
# ax6.set_title('H=%.1f' %(9.7,) )

# ax7 = fig3.add_subplot(2,5,7)
# ax7.scatter(Tarray, Xdata[1])
# ax7.set_xlabel('T')
# ax7.set_ylabel('平均磁化率X')
# ax7.set_title('H=%.1f' %(19.4, ) )

# ax8 = fig3.add_subplot(2,5,8)
# ax8.scatter(Tarray, Xdata[2])
# ax8.set_xlabel('T')
# ax8.set_ylabel('平均磁化率X')
# ax8.set_title('H=%.1f' %(32.3, ) )

# ax9 = fig3.add_subplot(2,5,9)
# ax9.scatter(Tarray, Xdata[3])
# ax9.set_xlabel('T')
# ax9.set_ylabel('平均磁化率X')
# ax9.set_title('H=%.1f' %(48.5, ) )

# ax10 = fig3.add_subplot(2,5,10)
# ax10.scatter(Tarray, Xdata[4])
# ax10.set_xlabel('T')
# ax10.set_ylabel('平均磁化率X')
# ax10.set_title('H=%.1f' %(97, ) )

# plt.tight_layout()
# plt.show()






# #--------Animation-----------------

# print("Animation begins.")

# for frame in range(0, len(data)):
#     ax.cla()
#     ax.imshow(data[frame], cmap=mpl.cm.winter)
#     ax.set_title("Step {}".format(frame * interval))
#     plt.pause(0.1)

# print("Animation completes.")