import random

hi = {"a" : 0.1, "b": 0.2, "c" : 0.7}

print(random.choice(list(hi.keys())))

b = dict()
print(b)
for key in hi.keys():
    print(key)

print(hi.values())
print(hi.keys())


counter = {"a" : 0, "b": 0, "c" : 0}
for i in range(1000):
    g = random.choices(list(hi.keys()),hi.values())[0]
    counter[g] += 1

print(counter)

for i in hi:
    print(i)
#print(random.choices(list(hi.keys()),list(hi.values())))