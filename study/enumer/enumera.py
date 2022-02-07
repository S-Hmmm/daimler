from enum import Enum, unique


@unique
class TestEnum(Enum):
    Mon = 1
    Tue = 2
    Wen = 3
    Thu = 4
    Fri = 5
    Sat = 6
    Sun = 7


if __name__ == '__main__':
    print(TestEnum.Mon)
    print(TestEnum['Mon'])
    print(TestEnum.Mon.value)
    print(TestEnum(3))
