# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 16:21:38 2017

@author: nocman
"""
#当我们定义一个class的时候，我们实际上就定义了一种数据类型。我们定义的数据类型和Python自带的数据类型
#判断一个变量的类型可以使用isinstance
class Student(object):
#Student，类名，通常大写开头的单词。object，表示该类是从哪个类继承下来的，通常没有合适的类就使用object类
#创建好Student类，就可以根据Student类创建出Student的实例，如：a=Student()
#可以自由地给实例变量绑定属性，如a.name=‘tom’
    
    def __init__(self,name,score,hometown):
    #类可以起到模板的作用，因此，可以在创建实例的时候，把我们认为必须绑定的属性强制填写进去，通过定义一个特殊的__init__方法
        self.name = name
        self.score = score
        self.__hometown = hometown
        #访问限制，私有变量，无法直接从外部访问实例变量.__hometown
        #不能直接访问__hometown是因为python解释器把__hometown改成了_Student__hometown

    #类属性
    manager = 'Zephyr'
    
    #数据封装：面向对象编程的一个重要特点，在Student类的内部定义访问数据的函数
    #这样就把数据封装起来，这些封装的函数和Student类本身是关联的，称之为类的方法
    #方法可以直接在实例变量上调用，不需要知道内部细节    
    def print_score(self):
        print('%s: %s' % (self.name,self.score))
    def get_grade(self):
        if self.score >= 90:
            return self.name + ' is A'
        elif self.score >= 60:
            return self.name + ' is B'
        else:
            return self.name + ' is C'

    '''
    非数据封装的格式，在class外置顶
    def print_score(std):
        print('%s: %s' % (std.name, std.score))
    def get_grade(std):
        if std.score >= 90:
            return std.name + ' is A'
        elif std.score >= 60:
            return std.name + ' is B'
        else:
            return std.name + ' is C'
    '''


    def get_hometown(self):
        return self.__hometown #访问限制，私有变量的获取
    def set_hometown(self,hometown): 
    #若要允许外部代码修改hometown，可以定义函数，这样做的好处是对参数进行检查，避免传入无效参数
        if type(hometown) == str:
            self.__hometown = hometown
        else:
            raise ValueError('bad input')

    #继承和多态的示例中需要用到的函数
    def learn(self):
        print('students are learning...')
    def discuss(self):
        print('stuednts are discussing...')
    def sing(self):
        print('students are singsing...')


#以Student为父类创建的子类Pupil、Junior、Highschool、Undergraduate、Postgraduate、
#子类获得父类的全部功能，自动拥有类父类的全部方法
#子类的实例既是父类型也是子类型

class Pupil(Student):
    def discuss(self):
    #定义与父类一样的方法discuss，子类实例调用discuss方法是会直接调用子类的discuss而不是父类的
    #子类的discuss覆盖了父类的discuss方法，即为多态
        print('pupils are discussing...')

    def sing(self):
        print('pupils are singing')


class Junior(Student):
    pass

class Highschool(Student):
    pass

class Undergraduate(Student):
    pass

class grade7(Junior):
    pass

#从java的角度分析以下函数，必须传入与x相同类型的数据
#而对于鸭子类型语言的python，只要传入的x具备discuss这个方法，就可以执行该函数
def discuss_twice(x):
    x.discuss()
    x.discuss()

#新增一个Student的子类，无需对函数sing_discuss()做任何修改
#实际上，任何依赖Student作为参数的函数或方法都可以不加修改地正常运行，原因就在于多态

class Postgraduate(Student):
    def discuss(self):        
        print('Postgraduate are discussing...')

#对于一个变量，我们只需要知道它是Student类型，无需确切地知道它的子类型，就可以放心地调用discuss()方法
#而具体调用的discuss()方法是作用在Student、Pupil还是Postgraduate对象上，由运行时该对象的确切类型决定，这就是多态真正的威力：
#调用方只管调用，不管细节，而当我们新增一种Student的子类时，只要确保discuss()方法编写正确，不用管原来的代码是如何调用的。这就是著名的“开闭”原则：


#静态语言和动态语言
class Teacher(object):
    def discuss(self):
        print('teachers are discussing...')



'''
bart = Student()
bart.name = 'Bart Simpson'
'''




