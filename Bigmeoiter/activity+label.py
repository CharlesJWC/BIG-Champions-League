from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import timeit
import sys

start = timeit.default_timer()

sys.stdout.write('Loading csv file...')
activity_file_path = u'integrated_train_activity.csv'
label_file_path = u'C:/Jupyter_Root/BIG_Champions/final_data_rev/train/train_label.csv'
train_activity= pd.read_csv(activity_file_path, sep=',',low_memory=False,  encoding = "ISO-8859-1") # csv파일을 데이터프레임으로 불러옴.
train_label = pd.read_csv(label_file_path, sep=',',header=None, low_memory=False,  encoding = "ISO-8859-1") # csv파일을 데이터프레임으로 불러오기
sys.stdout.write('done!\n')

train_label.columns = train_label.iloc[0,:].tolist() # 데이터프레임에 필드명 추가
print(train_label.columns)
train_activity['label'] = None
idx_total_num = train_label.shape[0]
error_idx =[]
for i in range(1, idx_total_num):
    current_row = train_label.iloc[i:i+1]
    #print(current_row)
    current_id = current_row.loc[i,'acc_id']
    current_label = current_row.loc[i,'label']

    try:
        rlv_row_idx = train_activity.loc[current_id == train_activity.acc_id].index.tolist()
        for idx in rlv_row_idx:
            train_activity.loc[idx, 'label'] = current_label
    except Exception as ex:
        error_idx.append(i+1)
        continue

    #print('Process rate: {0:.2f} %\tcurrent index: {1}/{2} \t\r'.format(i/idx_total_num*100,i,idx_total_num))
    sys.stdout.write('Process rate: {0:.2f} %\tcurrent index: {1}/{2} \t\r'.format(i/idx_total_num*100,i,idx_total_num))
    #if i > 20:
    #    break



train_activity.to_csv('integrated_train_activity+label.csv', mode='w', header=True)

print('없는 데이터 개수 :',len(error_idx))
if len(error_idx) > 0 :
    f = open('error_index.txt', 'w',encoding='UTF-8')
    for en in range(len(error_idx)):
        f.write(str(error_idx[en]))
        f.write('\n')
    f.close()

end = timeit.default_timer()
print('\nElapsed time :', "{0:.3f}".format(end-start), 'seconds')
