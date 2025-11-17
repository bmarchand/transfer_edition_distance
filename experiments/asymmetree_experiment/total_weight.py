import sys

network1 = sys.argv[-2]
network2 = sys.argv[-1]

weight = 0

for line in open(network1).readlines():
    if line.find("transfer") >= 0:
        weight += 1 

for line in open(network2).readlines():
    if line.find("transfer") >= 0:
        weight += 1 

print("total weight",weight)
