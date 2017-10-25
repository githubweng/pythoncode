# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 16:42:39 2017

@author: nocman
"""

'''
把函数作为参数传入，这样的函数称为高阶函数，函数式编程就是指这种高度抽象的编程范式。

偏函数

#函数式编程

#从一组字符串中筛选出小数是整数倒序的浮点数字符串，并使用map/reduce函数将其中最长的一个转换为浮点数
#这组原始序列是依据题目创建的，所以会有很多情况没有考虑到，如果应用正则表达式做if的筛选，可以做的更为周全
'''


list0 = ['python','123.321','789.789','6789.9876','123456.654321']

'''
lambda:当我们在传入函数时，有些时候，不需要显式地定义函数，直接传入匿名函数更方便。在Python中，对匿名函数提供了有限支持。
匿名函数有个限制，就是只能有一个表达式，不用写return，返回值就是该表达式的结果。
list(map(lambda x: x * x, [1, 2, 3, 4, 5, 6, 7, 8, 9]))

filter()函数用于过滤序列，接受一个函数（“筛选”函数）和一个序列，把传入函数依次作用域每个元素，根据返回值是True还是False来决定是否丢弃该元素
filter()返回的是一个Iterator，要强迫filter()完成全部计算结果，需要list()函数获得所以结果并返回list

sorted()函数，接收一个key函数来实现自定义的排序，反向排序可以存入第三个参数reverse=True

偏函数
functools.partial的作用就是，把一个函数的某些参数给固定住（也就是设置默认值），返回一个新的函数，调用这个新函数会更简单。
创建偏函数时，实际上可以接收函数对象、*args和**kw这3个参数
例如max2=functools.partial(max,10)，实际为将10带入max()中做比较，max2(2,3,4)相当于*arg=(10,2,3,4),max2(*arg)
'''

from functools import reduce #调用reduce

#定义一个fa函数，用于filter()筛选，返回正反写都一样的字符串
def fa(x):
    return x==x[::-1]

#依据筛选函数，对list0做筛选，因为filter()返回iterator，通过list()返回list
list1=list(filter(fa,list0))

#构造一个偏函数，传入函数参数reverse=True，即sorted2默认为倒序排列，相当于传入了**kw，'reverse':True
import functools
sorted2 = functools.partial(sorted,reverse=True)
#通过sorted2()，以len()为key，对list1进行排序
list2=sorted2(list1,key=len)

#以上几句可以利用匿名函数缩略为：sorted(list(filter(lambda x:x==x[::-1],list0)),key=len)
#lambda x:x==x[::-1]，参照函数fa()，可见冒号前的x为函数参数，冒号后为表达式，返回既是表达式结果

#用map/reduce做一个str2float函数
def fb(x,y):    #定义str2float的调用函数1
    return x*10 + y

def char2num(n):    #定义str2float的调用函数2
    return {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9}[n]

def str2float(s):
    if '.' in s:    #如果是浮点数的字符串，以“.”分割字符串，将浮点数的字符串通过.拆分为两个整型字符串后更好处理
        s1=s.split('.')[0]
        s2=s.split('.')[1]
        '''
        map/reduce两个高阶函数，经常作为一个组合来使用
        map映射：通过函数处理一组数据，产生一组中间键，归类，通过map产生的是一个Iterator，要通过list()函数来转换为list
        reduce归约：合并集合的数值，产生较小集合的数值
        即将一组数据，先通过map进行统一的一个步骤处理，再通过reduce进行一个总结
        举个例子：售卖春卷的店，需要将萝卜、黄瓜、土豆、肉等通过切丝这个map做一个统一的处理，再将这些处理过的材料，用春卷皮包裹这个reduce来最终制作出一个春卷
        '''
        #在map中，我们先用char2num这个函数，对s1的每个字符进行一个转换为整型的操作，例如'123'就被转换为了1，2，3
        #再在reduce中，我们用fn这个函数，将map产生的1，2，3，组合为123，这样通过map/redcue后，字符串'123'就转换为了整型123
        x1=reduce(fb,map(char2num,s1))
        #利用lambda函数的简化：x1=reduce(lambda x,y:x*10+7,map(char2num,s1))
        x2=reduce(fb,map(char2num,s2))/(10**len(s2)) #连续两个*表示次方
        return x1+x2
    else:
        x3=reduce(fb,map(char2num,s)) #如果本身是整型字符串，直接转换即可
        return x3

'''
返回函数存在一些难点：

返回函数：在函数（外部函数）内部再定义一个内部函数，内部函数引用外部函数的参数和局部变量
当外部函数返回内部函数时，相关参数和变量都保存再返回函数中，这种程序结构称为“闭包”

注意点：每次调用外部函数时都会返回一个新的函数，即使时传入相同参数

返回闭包时牢记一点：返回函数不要引用任何循环变量，或者后续会发生变化的变量
因为返回函数引用变量，但不会立即执行，等到循环结束函数都返回时，引用的变量已经变成循环最后的结果
如果一定要引用循环变量，只能再创建一个函数，用该函数的参数绑定变量当前的值，无论循环变量后续如何更改，已绑定到函数的参数的值不变
'''

#定义装饰器，同时也是一种返回函数
def log(text):
    def decorator(func): #接收一个函数func()作为参数，返回一个函数wrapper()
        def wrapper(*args, **kw): #接收任意参数，返回的是将接收的任意参数带入decorator()接收的函数func()
            #函数对象的__name__属性，可以获取函数名称
            #打印text，func():
            print('%s %s():' % (text, func.__name__)) 
            return func(*args, **kw)
        return wrapper
    return decorator

#excute = log('the top one is got by function')(excute)
@log('the top one is got by function') #增强下方函数excute的功能，传入执行参数“excute”
def excute(x):
    list3=[]
    for n in x:
        list3.append(str2float(n))
    return list3[0]





