from abc import ABCMeta, abstractmethod


class PrintClassA(object):

    def printing(self):
        return 'ClassA'


class PrintClassB(object):

    def printing(self):
        return 'ClassB'


class ReadA(object):

    def read(self):
        return 'ReadA'


class ReadB(object):

    def read(self):
        return 'ReadB'


class AbstractFactory(metaclass=ABCMeta):

    @abstractmethod
    def print_name(self):
        pass

    @abstractmethod
    def read_class(self):
        pass


class FactoryA(AbstractFactory):

    def print_name(self):
        return PrintClassA()

    def read_class(self):
        return ReadA()


class FactoryB(AbstractFactory):

    def print_name(self):
        return PrintClassB()

    def read_class(self):
        return ReadB()


if __name__ == '__main__':
    a = FactoryA()
    b = FactoryB()
    pa = a.print_name()
    pb = b.print_name()
    ra = a.read_class()
    rb = b.read_class()
    print(pa, pb, ra, rb)



