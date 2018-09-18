from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import timeit
import sys

start = timeit.default_timer()

sys.stdout.write('Loading csv file...')
file_path = u'C:/Jupyter_Root/BIG_Champions/final_data_rev/train/train_activity.csv'
train_activity = pd.read_csv(file_path, sep=',',header=None, low_memory=False,  encoding = "ISO-8859-1") # csv파일을 데이터프레임으로 불러오기
sys.stdout.write('done!\n')

train_activity.columns = train_activity.iloc[0,:].tolist() # 데이터프레임에 필드명 추가

df_columns = ['acc_id']
fields =     ['cnt_dt',
              'play_time',
              'npc_exp',
              'npc_hongmun',
              'quest_exp',
              'quest_hongmun',
              'item_hongmun',
              'game_combat_time',
              'get_money',
              'duel_cnt',
              'duel_win',
              'partybattle_cnt',
              'partybattle_win',
              'cnt_enter_inzone_solo',
              'cnt_enter_inzone_light',
              'cnt_enter_inzone_skilled',
              'cnt_enter_inzone_normal',
              'cnt_enter_raid',
              'cnt_enter_raid_light',
              'cnt_enter_bam',
              'cnt_clear_inzone_solo',
              'cnt_clear_inzone_light',
              'cnt_clear_inzone_skilled',
              'cnt_clear_inzone_normal',
              'cnt_clear_raid',
              'cnt_clear_raid_light',
              'cnt_clear_bam',
              'normal_chat',
              'whisper_chat',
              'district_chat',
              'party_chat',
              'guild_chat',
              'faction_chat',
              'cnt_use_buffitem',
              'gathering_cnt',
              'making_cnt']


for field in fields:
    df_columns += ['avr_'+field]

for k in range(1,8):
    df_columns += ['diff_playtime_'+str(k)+'to'+str(k+1)+'wk']

for k in range(1,9):
    for field in fields:
        df_columns += [str(k)+'wk_'+field]

whole_train_activity = DataFrame(None, columns = df_columns)
numeric_columns = whole_train_activity.columns.tolist()[1:332] # 1+36+7+36*8
whole_train_activity[numeric_columns] = whole_train_activity[numeric_columns].astype(float)

row_id = None
idx = -1
wk_cnt = 0
idx_total_num = train_activity.shape[0]

for i in range(1, idx_total_num):
    current_row = train_activity.iloc[i:i+1]
    #display(current_row)
    current_id = current_row.loc[i,'acc_id']
    if current_id != row_id:
        if row_id is not None: # evaluate average columns
            for field in fields:
                whole_train_activity.loc[idx, 'avr_'+field] = whole_train_activity.loc[idx, 'avr_'+field] / wk_cnt
            wk_cnt = 0

        row_id = current_id
        idx += 1
        wk_cnt += 1
        whole_train_activity.loc[idx, 'acc_id'] = row_id
        current_wk = int(current_row.loc[i,'wk'])
        for field in fields:
            current_field = str(current_wk)+'wk_'+field
            whole_train_activity.loc[idx, current_field] = np.float64(current_row.loc[i, field])
            whole_train_activity.loc[idx, 'avr_'+field] = 0
            whole_train_activity.loc[idx, 'avr_'+field] += np.float64(current_row.loc[i, field])

    else:
        wk_cnt += 1
        current_wk = int(current_row.loc[i,'wk'])
        for field in fields:
            current_field = str(current_wk)+'wk_'+field
            whole_train_activity.loc[idx, current_field] = np.float64(current_row.loc[i, field])
            whole_train_activity.loc[idx, 'avr_'+field] += np.float64(current_row.loc[i, field])
        if ~np.isnan(whole_train_activity.loc[idx, str(current_wk-1)+'wk_play_time']):
            whole_train_activity.loc[idx, 'diff_playtime_'+str(current_wk-1)+'to'+str(current_wk)+'wk'] = \
                whole_train_activity.loc[idx, str(current_wk)+'wk_play_time'] - whole_train_activity.loc[idx, str(current_wk-1)+'wk_play_time']

    if i % 10000 == 0:
        whole_train_activity.to_csv('integrated_train_activity.csv', mode='w', header=True)

    sys.stdout.write('Process rate: {0:.2f} %\tcurrent index: {1}/{2} \t\r'.format(i/idx_total_num*100,i,idx_total_num))
    #if i > 20:
    #    break


whole_train_activity.to_csv('integrated_train_activity.csv', mode='w', header=True)
whole_train_activity.describe().to_csv('result_analyser.csv', mode='w', header=True)

end = timeit.default_timer()
print('\nElapsed time :', "{0:.3f}".format(end-start), 'seconds')
