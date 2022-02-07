class Screen(object):

    def __init__(self):
        self.__width = None
        self.__height = None
        self.__resolution = 786432

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, w):
        self.__width = w

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, h):
        self.__height = h

    @property
    def resolution(self):
        return self.__resolution


if __name__ == '__main__':
    s = Screen()
    s.width = 1024
    s.height = 768
    print('resolution =', s.resolution)
    if s.resolution == 786432:
        print('测试通过!')
    else:
        print('测试失败!')
