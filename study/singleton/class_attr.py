class TestClass:
    count = 0
    __slots__ = ('__name', 'age')  # 指定TestClass只能定义的属性

    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    def __new__(cls, *args, **kwargs):
        cls.count += 1
        return object.__new__(cls)

    def __call__(self):
        return self.name


if __name__ == '__main__':
    a = TestClass('Bob')
    b = TestClass('Tom')
    print(a.name)
    print(b.name)
    print('count = %d' % TestClass.count)

    c = TestClass('Jerry')
    print(c())
