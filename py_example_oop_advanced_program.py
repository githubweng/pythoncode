# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


'''


'''



class Student(object):
    #为了达到限制的目的，Python允许在定义class的时候，定义一个特殊的__slots__变量，来限制该class实例能添加的属性
    __slots__ = ('name','age')



class GraduateStudent(Student):
    #子类实例允许定义的属性就是自身的__slots__加上父类的__slots__
    __slots__ = ('score')


#Python内置的@property装饰器就是负责把一个方法变成属性调用
#@property把一个getter方法变成属性，只需要加上@property就可以了
#此时，@property本身又创建了另一个装饰器@score.setter，负责把一个setter方法变成属性赋值，于是，我们就拥有一个可控的属性操作

#还可以定义只读属性，只定义getter方法，不定义setter方法就是一个只读属性
#上面的birth是可读写属性，而age就是一个只读属性，因为age可以根据birth和当前时间计算出来。

    @property
    def birth(self):
        return self._birth

    @birth.setter
    def birth(self, value):
        self._birth = value

    @property
    def age(self):
        return 2015 - self._birth


class Teacher(object):
    pass

#通过多重继承，一个子类就可以同时获得多个父类的所有功能
#在设计类的继承关系时，通常，主线都是单一继承下来的，但是，如果需要“混入”额外的功能，通过多重继承就可以实现，这种设计通常称之为MixIn
#MixIn的目的就是给一个类增加多个功能，这样，在设计类的时候，我们优先考虑通过多重继承来组合多个MixIn的功能，而不是设计多层次的复杂的继承关系。

class PhD(Teacher,Student):
    pass


'''
__str__
__repr__

__iter__ ：如果一个类想被用于for ... in循环，类似list或tuple那样，就必须实现一个__iter__()方法
该方法返回一个迭代对象，然后，Python的for循环就会不断调用该迭代对象的__next__()方法拿到循环的下一个值
直到遇到StopIteration错误时退出循环。

__getitem__：让实例表现得像list那样按照下标取出元素

__getattr__：动态返回一个属性,当调用不存在的属性时，python解释器会试图调用__getattr__()来尝试获得
这实际上可以把一个类的所有属性和方法调用全部动态化处理了，不需要任何特殊手段。
这种完全动态调用的特性有什么实际作用呢？作用就是，可以针对完全动态的情况作调用。

__call__：一个对象实例可以有自己的属性和方法，当我们调用实例方法时，我们用instance.method()来调用。在Python中，还可以直接在实例本身上调用

'''
class LanguageTeacher(Teacher):
    def __init__(self, name):
        self.name = name
    #__str__()打印一个实例时，直接返回实例所带参数
    #__str__()返回用户看到的字符串
    def __str__(self):
        return 'LanguageTeacher object (name=%s)' % self.name
    #__repr__()调用一个实例时，直接返回实例所带参数
    #__repr__()为调试服务，返回程序开发者看到的字符串
    __repr__ = __str__
    
    def __getattr__(self,attr):
        if attr == 'language':
            return 'English'
        if attr == 'hometown': 
            #可以返回一个函数，但是调用方法要变成 实例.属性()
            return lambda:'BeiJing'
        #__getattr__默认返回None，调用以上之外类内不存在的任意属性，均会返回None
        #要让class只响应特定的几个属性，我们就要按照约定，抛出AttributeError的错误
        raise AttributeError('\'LanguageTeacher\' object has no attribute \'%s\'' % attr)


class Fib(object):
    def __init__(self):
        self.a, self.b = 0, 1 #初始化两个计数器a，b
    def __iter__(self):
        return self #实例本身就是迭代对象，故返回自己
    def __next__(self):
        self.a, self.b = self.b, self.a + self.b #计算下一个值
        if self.a > 100000: #退出循环的条件
            raise StopIteration()
        return self.a #返回下一个值

class FibList(object):
    def __getitem__(self, n):
        if isinstance(n, int): #n是索引
            a, b = 1, 1
            for x in range(n):
                a, b = b, a + b
            return a
        if isinstance(n, slice): #n是切片
            start = n.start
            stop = n.stop
            if start is None:
                start = 0
            a, b = 1, 1
            L = []
            for x in range(stop):
                if x >= start:
                    L.append(a)
                a, b = b, a + b
            return L

#FibList没有对step参数做处理
#也没有对负数作处理，所以，要正确实现一个__getitem__()还是有很多工作要做的。
#此外，如果把对象看成dict，__getitem__()的参数也可能是一个可以作key的object，例如str。
#与之对应的是__setitem__()方法，把对象视作list或dict来对集合赋值。最后，还有一个__delitem__()方法，用于删除某个元素。
#总之，通过上面的方法，我们自己定义的类表现得和Python自带的list、tuple、dict没什么区别，这完全归功于动态语言的“鸭子类型”，不需要强制继承某个接口。


#利用完全动态的__getattr__，我们可以写出一个链式调用
class Chain(object):
    def __init__(self, path=''):
        self._path = path
    def __getattr__(self, path):
        return Chain('%s/%s' % (self._path, path))
    def __str__(self):
        return self._path
    __repr__ = __str__
