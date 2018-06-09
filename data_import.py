#coding:utf-8
#!/usr/bin/env python

import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OnlineSystem.settings")
django.setup()


from EntryNOC.models import UserFullName,EntryNOC
import xlrd,datetime
# from xlrd import xldate_as_tuple

data= xlrd.open_workbook('NOC_Quality_Finding_Track_2018.xlsx') #打开文件
table = data.sheet_by_index(0) #获取工作表
# nrows = table.nrows #行数
# ncols = table.ncols #列数

# colnames =  table.row_values(0)
WorkList = []
dict_choice = {
    '--------': '--',
    'NOC Daily QC ':'QC',
    'WAN PMA report':'PM',
    'NOC QM':'QM',
    'Dept. QM':'DM',
    'CI/OSN2 ':'N2',
    'CI/OSN3':'N3',
    'CI/OSN 6/7/9':'N6',
    'CI/OSN 6/7/8':'N7',
    'CI/OSN5/6/8':'N8',
    'CI/OSR5-SG':'R5',
    'OSR1-LA':'AM',
    'OSR1-NA':'AM',
    'CI/OSR1-AM':'AM',
    'Resolved':'R',
    'Cancelled':'C',
    'Open':'A',
    'Minor':'Mi',
    'Major':'Ma',
    'Critical':'Cr',
    'Partial accpet ':'P',
    'Fully accept':'A',
    'Not accept':'R',
    'User Feedback':'UF',
}
for i in range(49,90):
    row = table.row_values(i) #获取每行值
    # print(row)
    # date = row[0]
    # date_year = date.split('/')[0]
    # date_month = date.split('/')[0]
    # date_day = date.split('/')[0]
    # xlrd.xldate.xldate_as_datetime(row[0],0)
    user = row[5]
    user_firstname = user.split(' ')[0]
    user_lastname = user.split(' ')[1]
    # print(i)
    WorkList.append(EntryNOC(rep_date=xlrd.xldate.xldate_as_datetime(row[0],0),
                             last_modify_date=xlrd.xldate.xldate_as_datetime(row[0],0),
                             finding_source=dict_choice[row[1]],
                             ticket_num=row[2],
                             finding_description=row[3],
                             finding_level=dict_choice[row[4]],
                             finding_responsible=UserFullName.objects.get(first_name=user_firstname,last_name=user_lastname),
                             quality_track_measurement=row[7],
                             acknowledge_status=dict_choice[row[8]],
                             quality_track_comments=row[9],
                             finding_final_status=dict_choice[row[10]]))

print('list is done!')
EntryNOC.objects.bulk_create(WorkList)
print ('数据导入成功!')

