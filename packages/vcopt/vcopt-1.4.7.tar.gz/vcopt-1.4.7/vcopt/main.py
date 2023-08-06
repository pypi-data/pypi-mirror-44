# -*- coding: utf-8 -*-
import numpy as np
import numpy.random as nr
import math, time
from copy import deepcopy
import matplotlib.pyplot as plt
np.set_printoptions(threshold=np.inf, precision=8, suppress=True, floatmode='maxprec')



class vcopt:
    def __init__(self):
        pass
    def __del__(self):
        pass
    
    #setting
    def setting(self, para_range, score_func, aim, show_pool_func, show_para_func, seed, verbose, **kwargs):
        self.para_range = np.array(para_range)
        self.para_num = len(para_range)
        self.score_func = score_func
        self.aim = aim
        self.show_para_func = show_para_func
        self.show_pool_func = show_pool_func
        self.seed = seed
        nr.seed(self.seed)
        self.verbose = verbose
        self.kwargs = kwargs
        self.start = time.time()
    
    #set hyper para
    def set_hyper(self, pool_num, parent_num, child_num):
        self.pool_num = pool_num
        self.parent_num = parent_num
        self.child_num = child_num
        #self.rate = rate
    
    #set pool
    def set_pool(self, dtype):
        self.pool, self.pool_score = np.zeros((self.pool_num, self.para_num), dtype=dtype), np.zeros(self.pool_num)
        self.parent, self.parent_score = np.zeros((self.parent_num, self.para_num), dtype=dtype), np.zeros(self.parent_num)
        self.child, self.child_score = np.zeros((self.child_num, self.para_num), dtype=dtype), np.zeros(self.child_num)

    #score pool
    def score_pool(self):        
        for i in range(self.pool_num):
            self.pool_score[i] = self.score_func(self.pool[i], **self.kwargs)
    
    #score child
    def score_child(self):        
        for i in range(self.child_num):
            self.child_score[i] = self.score_func(self.child[i], **self.kwargs)
    
    #save best
    def save_best(self):
        self.best_index = np.argmin(np.abs(self.aim - self.pool_score))
        #pool_score_best is the score
        self.pool_best = deepcopy(self.pool[self.best_index])
        self.pool_score_best = deepcopy(self.pool_score[self.best_index])

    #save mean
    def save_mean(self):
        #pool_score_mean is a pseudo score
        self.mean_abs_gap = np.mean(np.abs(self.aim - self.pool_score))
        if self.aim < self.pool_score_best:
            self.pool_score_mean = self.aim + self.mean_abs_gap
        else:
            self.pool_score_mean = self.aim - self.mean_abs_gap
        self.mean_abs_gap_save = deepcopy(self.mean_abs_gap)

    #make parent
    def make_parent(self, it):
        #self.pool_select = nr.choice(range(self.pool_num), self.parent_num, replace = False)
        self.pool_select = it
        self.parent = self.pool[self.pool_select]
        self.parent_score = self.pool_score[self.pool_select]

    #make family
    def make_family(self):
        self.family = np.vstack((self.child, self.parent))
        self.family_score = np.hstack((self.child_score, self.parent_score))
    
    #JGG
    def JGG(self):
        #np.argpartition(-array, K)[:K] returns max K index
        #np.argpartition(array, K)[:K] returns min K index
        self.family_select = np.argpartition(np.abs(self.aim - self.family_score), self.parent_num)[:self.parent_num]
        #return to pool
        self.pool[self.pool_select] = self.family[self.family_select]
        self.pool_score[self.pool_select] = self.family_score[self.family_select]

    #end check
    def end_check(self):
        self.mean_abs_gap = np.mean(np.abs(self.aim - self.pool_score))
        if self.mean_abs_gap < self.mean_abs_gap_save:
            return True
        else:
            return False
        
    def show_pool(self, n):
        self.kwargs.update({'gen_num':n, 'best_index':self.best_index,\
                            'best_score':round(self.pool_score_best, 4),\
                            'mean_score':round(self.pool_score_mean, 4),\
                            'time':round(time.time() - self.start, 2)})
        self.show_pool_func(self.pool, **self.kwargs)
    
    '''
    #print bar
    def print_bar(self, n):
        n0 = int(20*n/(self.maxgen+1)) + 1
        n1 = 20 - n0
        t = time.time() - self.start
        bar = '\r{}% [{}{}] time:{}s gen:{}  φ(□　□;)'.format(str((n*100//self.maxgen)).rjust(3), '#'*n0, ' '*n1, np.round(t, 1), n)
        print(bar, end='')
        #print(bar)
        

    
    #print bar final
    def print_bar_final(self, n):
        n0 = int(20*n/(self.maxgen+1)) + 1
        n1 = 20 - n0
        t = time.time() - self.start
        bar = '\r{}% [{}{}] time:{}s gen:{}  φ(□　□*)!!'.format(str((n*100//self.maxgen)).rjust(3), '#'*n0, ' '*n1, np.round(t, 1), n)
        #print(bar, end='')
        print(bar)
    '''
    
    #2-opt
    def opt2(self, para, score_func, aim, show_para_func=None, seed=None, step_max=float('inf'), **kwargs):
        #
        para, score = np.array(para), score_func(para, **kwargs)
        if seed != 'pass': nr.seed(seed)
        step = 0
        #
        if show_para_func != None:
            kwargs.update({'step_num':step, 'score':round(score, 3)})
            show_para_func(para, **kwargs)
        #opt
        while 1:
            update = False
            if step >= step_max:
                #print('stop')
                break
            
            i_set = np.arange(0, len(para)-1)
            nr.shuffle(i_set)
            for i in i_set:
                #continue check
                if update == True: break
                
                j_set = np.arange(i + 1, len(para))
                nr.shuffle(j_set)
                for j in j_set:
                    #continue check
                    if update == True: break
                    
                    #try
                    para_tmp = np.hstack((para[:i], para[i:j+1][::-1], para[j+1:]))
                    score_tmp = score_func(para_tmp, **kwargs)
                    
                    #check and update
                    if np.abs(aim - score_tmp) < np.abs(aim - score):
                        para, score = para_tmp, score_tmp
                        step += 1
                        if show_para_func != None:
                            kwargs.update({'step_num':step, 'score':round(score, 3)})
                            show_para_func(para, **kwargs)
                        update = True
            if update == False:
                #print('end')
                break
        return para, score





    #######################################################################################################################
    #######################################################################################################################
    def tspGA(self, para_range, score_func, aim, show_pool_func=None, show_para_func=None, seed=None, verbose=0, pool_num=None, **kwargs):
        #
        self.setting(para_range, score_func, aim, show_pool_func, show_para_func, seed, verbose, **kwargs)
        #self.set_hyper(self.para_num*10, self.para_num*1, self.para_num*1)
        self.set_hyper(self.para_num*10, 2, 2)
        if pool_num != None: self.set_hyper(pool_num, 2, 2)
        
        self.set_pool(int)
        
        self.opt2_num = 1
        
        #gen 1 pool
        for i in range(self.pool_num):
            self.pool[i] = deepcopy(self.para_range)
            nr.shuffle(self.pool[i])
            #mini 2-opt
            self.pool[i], self.pool_score[i] = self.opt2(self.pool[i], self.score_func, self.aim,\
                                                         seed='pass', step_max=self.opt2_num, **self.kwargs)
        
        #
        #self.score_pool()
        self.save_best()
        self.save_mean()
        
        #show
        if self.show_pool_func != None:
            self.show_pool(0)
        
        #gen 2-
        #count = 0
        for n in range(1, 1000000 + 1):
            #
            #self.make_parent()
            
            self.opt2_num = n // 10
            #print(self.opt2_num)
            
            #iteration
            iteration = np.arange(self.pool_num)
            nr.shuffle(iteration)
            iteration = iteration.reshape((self.pool_num//self.parent_num), self.parent_num)
            for it in iteration:
                #
                self.make_parent(it)            
            
                #辺に着目したヒュリスティック操作
                #==============================================================
                #ex_parent
                #self.ex_parent = np.hstack((self.parent[:, -1].reshape(self.parent_num, 1), self.parent, self.parent[:, 0].reshape(self.parent_num, 1)))
                self.ex_parent = np.hstack((self.parent[:, -3:].reshape(self.parent_num, 3), self.parent, self.parent[:, :3].reshape(self.parent_num, 3)))
                #print(self.parent)
                #print(self.ex_parent)
                #child
                for i in range(self.child_num):
                    #first para
                    s = self.parent[nr.randint(self.parent_num), 0]
                    if nr.rand() < (1.0 / self.para_num):
                        s = self.para_range[nr.randint(self.para_num)]
                    #s = self.para_range[nr.randint(self.para_num)]
                    self.child[i, 0] = s
                    #following para
                    for j in range(1, self.para_num):
                        
                        #left right mask of ex_parent
                        #mask = np.zeros((self.parent_num, self.para_num + 2), dtype=bool)
                        #true left
                        #mask[:, :-2] += (self.parent == s)
                        #true right
                        #mask[:, 2:] += (self.parent == s)
                        #print(self.child)
                        
                        mask_3 = np.zeros((self.parent_num, self.para_num + 6), dtype=bool)
                        mask_2 = np.zeros((self.parent_num, self.para_num + 6), dtype=bool)
                        #mask_1 = np.zeros((self.parent_num, self.para_num + 6), dtype=bool)
                        mask_3[:, 4:-2] += (self.parent == s)
                        mask_3[:, 2:-4] += (self.parent == s)
                        mask_2[:, 5:-1] += (self.parent == s)
                        mask_2[:, 1:-5] += (self.parent == s)
                        #mask_1[:, 6:] += (self.parent == s)
                        #mask_1[:, :-6] += (self.parent == s)
                        #print(mask_1)
                        
                        #p (index in para_range)
                        p = np.ones(self.para_num) * (1.0 / self.para_num)
                        for k in self.ex_parent[mask_3]:
                            p[np.where(self.para_range==k)[0]] += 1.0 / self.parent_num
                        for k in self.ex_parent[mask_2]:
                            p[np.where(self.para_range==k)[0]] += 0.1 / self.parent_num
                        #for k in self.ex_parent[mask_1]:
                        #    p[np.where(self.para_range==k)[0]] += 0.1
                        
                        #print(p)
                        #mask passed para
                        for k in self.child[i, 0:j]:
                            p[np.where(self.para_range==k)[0]] = 0.0
                        
                        #choice
                        p *= 1.0 / np.sum(p)
                        s = nr.choice(self.para_range, p=p)
                        #child
                        self.child[i, j] = s
                #==============================================================
                #
                #self.score_child()
                self.make_family()
                #mini 2-opt
                for i in range(self.parent_num + self.child_num):
                    self.family[i], self.family_score[i] = self.opt2(self.family[i], self.score_func, self.aim,\
                                                                     seed='pass', step_max=self.opt2_num, **self.kwargs)
                self.JGG()
            
            self.save_best()

            #end check
            if self.end_check():
                pass
            else:
                break
            
            self.save_mean()
            
            #show
            if self.show_pool_func != None:
                self.show_pool(n * self.pool_num)
        
        #show
        #if self.show_pool_func != None:
        #    self.show_pool(n * self.pool_num)
        #2-opt
        #self.pool_best, self.pool_score_best = self.opt2(self.pool_best, self.score_func, self.aim,\
        #                                                 seed='pass', show_para_func=self.show_para_func, **self.kwargs)
        return self.pool_best, self.pool_score_best
    
    
    
    
    #==============================================================#==============================================================
    #==============================================================#==============================================================
    def dcGA(self, para_range, score_func, aim, show_pool_func=None, show_para_func=None, seed=None, verbose=0, pool_num=None, **kwargs):
        #
        self.setting(para_range, score_func, aim, show_pool_func, show_para_func, seed, verbose, **kwargs)
        self.set_hyper(self.para_num*10, 2, 6)
        if pool_num != None: self.set_hyper(pool_num, 2, 6)
        
        self.set_pool(int)
        
        #3 choices
        self.choice = np.array([[0,0,1],[0,1,0],[0,1,1],[1,0,0],[1,0,1],[1,1,0]], dtype=int)
        
        #gen 1 pool
        for i in range(self.pool_num):
            for j in range(self.para_num):
                self.pool[i, j] = nr.choice(self.para_range[j])
        
        #
        self.score_pool()
        self.save_best()
        self.save_mean()
        
        #show
        if self.show_pool_func != None:
            self.show_pool(0)
        
        #gen 2-
        #count = 0
        for n in range(1, 1000000 + 1):
            #
            #self.make_parent()
            #iteration
            iteration = np.arange(self.pool_num)
            nr.shuffle(iteration)
            iteration = iteration.reshape((self.pool_num//self.parent_num), self.parent_num)
            for it in iteration:
                #
                self.make_parent(it)            
            
                #2-point cross
                #==============================================================
                #cross point
                cross_point = nr.choice(range(1, self.para_num), 2, replace = False)
                if cross_point[0] > cross_point[1]:
                    cross_point[0], cross_point[1] = cross_point[1], cross_point[0]
                #child
                for i in range(len(self.choice)):
                    self.child[i] = np.hstack((self.parent[self.choice[i, 0], :cross_point[0]],
                                               self.parent[self.choice[i, 1], cross_point[0]:cross_point[1]],
                                               self.parent[self.choice[i, 2], cross_point[1]:]))
                #==============================================================
                #mutation
                #==============================================================
                for ch in self.child:
                    for j in range(self.para_num):
                        if nr.rand() < (1.0 / self.para_num):
                            ch[j] = nr.choice(self.para_range[j])
                #==============================================================
                #
                self.score_child()
                self.make_family()
                self.JGG()
            
            self.save_best()

            #end check
            if self.end_check():
                pass
            else:
                break
            
            self.save_mean()
            
            #show
            if self.show_pool_func != None:
                self.show_pool(n * self.pool_num)

        return self.pool_best, self.pool_score_best
        
        
        
        
    #==============================================================#==============================================================
    #==============================================================#==============================================================
    def rcGA(self, para_range, score_func, aim, show_pool_func=None, show_para_func=None, seed=None, verbose=0, **kwargs):
        #
        self.setting(para_range, score_func, aim, show_pool_func, show_para_func, seed, verbose, **kwargs)
        self.set_hyper(self.para_num*10, self.para_num*1, self.para_num*10)
        if self.para_num >= 10: self.set_hyper(self.para_num*12, self.para_num*1, self.para_num*12)
        if self.para_num >= 20: self.set_hyper(self.para_num*15, self.para_num*1, self.para_num*15)
        if self.para_num >= 50: self.set_hyper(self.para_num*20, self.para_num*1, self.para_num*20)
        
        self.set_pool(float)
        
        #
        self.sd = 1.0*0.9 / math.sqrt(self.parent_num)
        
        #gen 1 pool
        for j in range(self.para_num):
            self.pool[:, j] = nr.rand(self.pool_num) * (self.para_range[j, 1] - self.para_range[j, 0]) + self.para_range[j, 0]
        
        #
        self.score_pool()
        self.save_best()
        self.save_mean()
        
        #show
        if self.show_pool_func != None:
            self.show_pool(0)
        
        #gen 2-
        #count = 0
        for n in range(1, 1000000 + 1):
            #
            #self.make_parent()
            #iteration
            iteration = np.arange(self.pool_num)
            nr.shuffle(iteration)
            iteration = iteration.reshape((self.pool_num//self.parent_num), self.parent_num)
            for it in iteration:
                #
                self.make_parent(it)            

                #REX
                #==============================================================
                #parant average
                ave = np.mean(self.parent, axis=0)
                #child
                self.child[:, :] = float('inf')
                for i in range(self.child_num):
                    for j in range(self.para_num):
                        while self.child[i, j] < self.para_range[j, 0] or self.para_range[j, 1] < self.child[i, j]:
                            #average
                            self.child[i, j] = ave[j]
                            #perturbation
                            for k in range(self.parent_num):
                                self.child[i, j] += nr.normal(0, self.sd) * (self.parent[k][j] - ave[j])
                #==============================================================
                #
                self.score_child()
                self.make_family()
                self.JGG()

            self.save_best()

            #end check
            if self.end_check() and np.max(np.std(self.pool, axis=0) / [self.para_range[:, 1] - self.para_range[:, 0]]) > 0.0001:
                pass
            else:
                break
            
            self.save_mean()
            
            #show
            if self.show_pool_func != None:
                self.show_pool(n * self.pool_num)

        return self.pool_best, self.pool_score_best
    
    
    
    
    


    
























if __name__ == '__main__':

    
    #Rastrigin関数（評価関数）
    def rastrigin_score(para, **kwargs):
        k = 0
        for x in para:
            k += 10 + (x*x - 10 * math.cos(2*math.pi*x))
        return k
                
        
    
                
    #poolの可視化
    def rastrigin_show_pool(pool, **kwargs):
        
        #任意で次の変数が使用できます
        gen_num = kwargs['gen_num']
        best_index = kwargs['best_index']
        best_score = kwargs['best_score']
        mean_score = kwargs['mean_score']
        time = kwargs['time']
    
        score = np.ones(len(pool)) * 99999
        
        for i in range(len(pool)):
            score[i] = rastrigin_score(pool[i])
        
        print('---------------')
        print(np.argmin(score), score[np.argmin(score)])
        print(kwargs['best_index'], score[kwargs['best_index']])
        print(kwargs['best_score'])
    
        #プロット
        plt.figure(figsize=(6, 6))
        #次元の数だけ横線を引く
        for dim in range(len(pool[0])):
            plt.plot([-5, 5], [dim, dim], 'k-')
        #poolを次元ごとに100個まで薄い黒でプロット
        for dim in range(len(pool[0])):
            plt.plot(pool[:100, dim], [dim]*len(pool[:100]), 'ok', markersize=8, alpha=(2.0/len(pool[:100])))
        #エリートは赤でプロット
        plt.plot(pool[best_index, :], range(len(pool[0])), 'or', markersize=8)
        #タイトルをつけて表示
        plt.xlabel('para'); plt.ylabel('dim')
        plt.title('gen={}, best={} mean={} time={}'.format(gen_num, best_score, mean_score, time))
        #plt.savefig('save/{}.png'.format(gen_num))
        plt.show()
        print()
            
            
            
    #パラメータ範囲
    para_range = np.ones((5, 2)) * 5.12
    para_range[:, 0] *= -1
    print(para_range)
    
    #GAで最適化
    para, score = vcopt().rcGA(para_range,                           #para_range
                                rastrigin_score,                     #score_func
                                0.0,                                 #aim
                                show_pool_func=rastrigin_show_pool,  #show_para_func=None
                                seed=None)                           #seed=None
                                                                     #other your variables
    
    #結果の表示
    print(para)
    print(score)