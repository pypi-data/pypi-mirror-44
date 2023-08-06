class A:
    def __init__(self):
        self.b = 0

    def __str__(self):
        return str({'a': 9})

    def __repr__(self):
        return str({'a': 7})

    def __setattr__(self, key, value):
        print(key, value)

# a = A()
# a.b = 6
# A.c = 9
a = [1, 2, 3, 4, 5]
print(a[:3], a[3:])