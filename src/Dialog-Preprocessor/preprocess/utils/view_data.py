import sys

for idx, line in enumerate(sys.stdin):
    line = line.strip().split('\t')
    print("Line %d: %s" % (idx, line[0]))
    for c in line[1:]:
        print("\t%s" % c)
    print('\n\n')