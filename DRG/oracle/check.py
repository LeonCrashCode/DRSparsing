import sys

cnt = 0
total = 0
lcnt = 1
for line in open(sys.argv[1]):
        line = line.strip()
        if line[0] == "#":
                continue
        tuples = line.split("|||")
        tuples = [tup.strip() for tup in tuples]
        for i in range(len(tuples)):
                j = 0
                while j < i:
                        if tuples[i] == tuples[j]:
                                print lcnt, tuples[i]
                                cnt += 1
                        j += 1
        lcnt += 1
        total += len(tuples)

print cnt,total

