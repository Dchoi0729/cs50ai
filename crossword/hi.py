def add(value):
    return -1*value

a = [1,2,3,7,4,5,9,-12]

print(sorted(a, key=add))


# Sort a list of integers based on
# their remainder on dividing from 7
def func(x):
    return x % 7
  
L = [15, 3, 11, 7]
  
print("Normal sort :", sorted(L))
print("Sorted with key:", sorted(L, key=func))

c = ['aaa', 'bz', 'ccccc', 'd', 'zy', 'dd']

def z(value):
    if value[-1] == "z":
        return 10
    if value[-1] == "y":
        return 8
    else: 
        return 0

print(sorted(c, key=lambda x: (len(x), z(x))))