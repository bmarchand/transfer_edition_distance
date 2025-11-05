import sys

network1 = sys.argv[-2]
network2 = sys.argv[-1]

weight = 0

for line in open(network1).readlines():
    if line.find("transfer") >= 0:
        weight += float(line.split(" ")[-1].rstrip("\n"))

for line in open(network2).readlines():
    if line.find("transfer") >= 0:
        weight += float(line.split(" ")[-1].rstrip("\n"))

print("total weight",weight)
