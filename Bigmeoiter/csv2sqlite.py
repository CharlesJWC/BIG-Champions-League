# ⓒ 2018 DSP lab.최중원. All Right Reserved.

import re
import sqlite3
import sys
import timeit


if len(sys.argv) > 3 :
    print('\n너무 많은 인자가 입력되었습니다.\nex) python step1_1_sqlite2csv.py input.csv output.sqlite')
elif len(sys.argv) < 3 :
    print('\n입력과 출력 파일명을 인자로 각각 입력해주세요.\nex) python step1_1_sqlite2csv.py input.csv output.sqlite')
else:

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    start = timeit.default_timer()


    con = sqlite3.connect(output_file)
    cur = con.cursor()
    cur.execute('SELECT * FROM table_adata')

    f = open(input_file, 'w',encoding='UTF-8')

    null_count = 0
    err_num = 0
    for row in cur.fetchall():

        mac = row[1]
        date = row[2].split(' ')
        year = date[3]
        mon = month_translate(date[1])
        day = date[2]
        hr, minute, sec = date[4].split(':')
        label = row[6]
        res = row[7]
        ft = [0,0,0,0]
        if (not(0<=int(hr)<24)) or (not(0<=int(minute)<60)) or (not(0<=int(sec)<60)):
            print('Data time Error : index =',row[0],'time =',hr,':',minute,':',sec)
            err_num = err_num + 1
            continue
        m = re.search('X([0-9a-zA-Z]*)R([0-9a-zA-Z]*)F([0-9a-zA-Z]*)H([0-9a-zA-Z]*)',res)

        for i in range(0,FEAT_NUM):
            ft[i] = replace_feature(m.group(i+1))

        # One-Hot 레이블링
        try :
    #         y_i = int(num_label(label)) - 1
    #         if y_i == 'NULL': null_count+=1
    #         y_oh = ['0', '0', '0', '0', '0', '0']
    #         y_oh[y_i] = '1'
    #         data = ",".join([mac]+['-'.join([year,mon, day, hr, minute, sec])]+ft+y_oh)

            # 숫자로 레이블링
            y_num = num_label(label)
            if y_num == 'NULL': null_count+=1
            data = ",".join([mac]+['-'.join([year,mon, day, hr, minute, sec])]+ft+[y_num])

            f.write(data)
            f.write('\n') # unrolling 할 때 지우기

        except ValueError as ex:
            print('Error : ', ex)  #에러가 발생 했을 경우 처리할 코드
            null_count+=1
    print('시간오류 데이터 개수 :',err_num)
    print('행동 NULL값 개수 : ', null_count)

    con.close()
    f.close()

    # 데이터 저장이 잘 되었는지 체크하기 위한 코드
    # print('회사 레이블링 SQL데이터를 가공한 csv데이터:\n')
    #
    # f_check = open("company_sqlite.csv", 'r', ,encoding='UTF-8')
    #
    # datas = f_check.readlines()
    # for i, data_row in enumerate(datas):
    #     print(data_row)
    #     if i >= 2: break
    #
    # f_check.close()

    end = timeit.default_timer()
    print('\nStep1-1 done!\t', 'Elapsed time :', "{0:.3f}".format(end-start), 'seconds')
