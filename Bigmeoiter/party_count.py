file_path = u'C:/Jupyter_Root/BIG_Champions/final_data_rev/train/train_party.csv'

f = open(file_path, 'r')

cnt = 0
while True:
    if f.readline() != None:
        cnt += 1
    else:
        break
    print(cnt)
f.close()
print("레코드 개수: {0}".format(cnt-1))
