"""
This file defines Ising Grid class
Created: Mar. 30, 2019
Last Edited: Apr. 3, 2019
By Bill
"""
#网址: https://github.com/DogofPavlov996/2D-Ising-Model-Python/tree/master


import numpy as np


class Grid(object):
    """Grid is a 2-D, periodic-boundaried and square canvas consisting of spins"""
    """Initial Grid only consists of positive spins"""

    def __init__(self, size, Jfactor, H):
        self.size = size
        self.Jfactor = Jfactor
        self.H=H
        self.canvas = np.ones([size, size], int)

    def randomize(self):
        self.canvas = np.random.randint(0, 2, [self.size, self.size]) * 2 - 1

    #我自定义的有序初始化, 避免临界慢化
    def orderize(self, num):
        self.canvas= np.ones([self.size, self.size], int)
        for i in range(num):
            x = np.random.randint(0, self.size)
            y = np.random.randint(0, self.size)
            self.canvas[x, y] = -self.canvas[x, y]

    def orderize_upordown(self, num):
        self.canvas= np.ones([self.size, self.size], int)
        
        if np.random.random() > 0.5:
            self.canvas=-1* self.canvas

        for i in range(num):
            x = np.random.randint(0, self.size)
            y = np.random.randint(0, self.size)
            self.canvas[x, y] = -self.canvas[x, y]


    def set_positive(self):
        self.canvas = np.ones([self.size, self.size], int)

    def set_negative(self):
        self.canvas = -np.ones([self.size, self.size], int)

    def left(self, x, y):
        if x < 0.5:
            return [self.size - 1, y]
        else:
            return [x - 1, y]

    def right(self, x, y):
        if x > self.size - 1.5:
            return [0, y]
        else:
            return [x + 1, y]

    def up(self, x, y):                 #哦!对的!   python中矩阵的起始位置在左上方!
        if y < 0.5:
            return [x, self.size - 1]
        else:
            return [x, y - 1]

    def down(self, x, y):
        if y > self.size - 1.5:
            return [x, 0]
        else:
            return [x, y + 1]

    #--------------Calculate energies and magnetizations--------------------

    def unitE(self, x, y):                  #(x,y)点的能量. (我加上了外磁场!!!)
        [leftx, lefty] = self.left(x, y)
        [rightx, righty] = self.right(x, y)
        [upx, upy] = self.up(x, y)
        [downx, downy] = self.down(x, y)
        return -self.Jfactor * self.canvas[x, y] * \
            (self.canvas[leftx, lefty] + self.canvas[rightx, righty] +
             self.canvas[upx, upy] + self.canvas[downx, downy]) - self.H* self.canvas[x, y]

    def deltaE(self, x, y):
        return -2 * self.unitE(x, y)        #??????我把-4改成了-2. 哦对的.

    def totalE(self):
        totalEnergy = 0
        for x in range(0, self.size):
            for y in range(0, self.size):
                mag_E=-self.H* self.canvas[x,y]
                totalEnergy = totalEnergy + (self.unitE(x, y) -mag_E)/2  +mag_E        #《潜在问题: 互能重复计算了, 共计算了2次》, 已解决
        return totalEnergy

    def totalM(self):
        return np.sum(self.canvas)

    def avrE(self):
        return self.totalE() / (self.size **2)

    def avrM(self):
        return self.totalM() / (self.size **2)

    def avrM2(self):
        return 1                        # sum s_{x,y}^2 / N  恒等于1




    # Single flip (Metropolis method)

    def singleFlip(self, temperature):
        """Single flip (Metropolis method)"""

        # Randomly pick a spin to flip

        x = np.random.randint(0, self.size)
        y = np.random.randint(0, self.size)

        # Metropolis acceptance rate

        dE = self.deltaE(x, y)

        if dE < 0:
            self.canvas[x, y] = -self.canvas[x, y]
        else:
            if np.random.rand() < np.exp(-dE / temperature):        #   √√√ k=1
                self.canvas[x, y] = -self.canvas[x, y]

        # Return cluster size

        return 1        #????????????哦对的. 

    # Cluster flip (Wolff method)

    def clusterFlip(self, temperature):
        """Cluster flip (Wolff method)"""

        # Randomly pick a seed spin

        x = np.random.randint(0, self.size)
        y = np.random.randint(0, self.size)

        sign = self.canvas[x, y]
        P_add = 1 - np.exp(-2 * self.Jfactor / temperature)
        stack = [[x, y]]
        lable = np.ones([self.size, self.size], int)
        lable[x, y] = 0

        while len(stack) > 0.5:                 #   <<<<<<<<疑似导致死循环

            # While stack is not empty, pop and flip a spin

            [currentx, currenty] = stack.pop()
            self.canvas[currentx, currenty] = -sign

            # Append neighbor spins

            # Left neighbor

            [leftx, lefty] = self.left(currentx, currenty)

            if self.canvas[leftx, lefty] * sign > 0.5 and \
                    lable[leftx, lefty] and np.random.rand() < P_add:
                stack.append([leftx, lefty])
                lable[leftx, lefty] = 0

            # Right neighbor

            [rightx, righty] = self.right(currentx, currenty)

            if self.canvas[rightx, righty] * sign > 0.5 and \
                    lable[rightx, righty] and np.random.rand() < P_add:
                stack.append([rightx, righty])
                lable[rightx, righty] = 0

            # Up neighbor

            [upx, upy] = self.up(currentx, currenty)

            if self.canvas[upx, upy] * sign > 0.5 and \
                    lable[upx, upy] and np.random.rand() < P_add:
                stack.append([upx, upy])
                lable[upx, upy] = 0

            # Down neighbor

            [downx, downy] = self.down(currentx, currenty)

            if self.canvas[downx, downy] * sign > 0.5 and \
                    lable[downx, downy] and np.random.rand() < P_add:
                stack.append([downx, downy])
                lable[downx, downy] = 0

        # Return cluster size

        return self.size * self.size - sum(sum(lable))








