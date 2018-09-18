import sys

args = sys.argv[1:]
output_path = args[0]
filename = args[1]
min = int(args[2])
max = int(args[3])

file_path = u'C:/Jupyter_Root/BIG_Champions/final_data_rev/train/train_'+filename+u'.csv'

f = open(file_path, 'r')
f2 = open(output_path, 'w')

for i in range(1, max+1):
    if i == 1:
        line = f.readline()
        f2.write(line)

    if i >= min:
        line = f.readline()
        f2.write(line)
    else:
        f.readline()

f.close()
f2.close()
