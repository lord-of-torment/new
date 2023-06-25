import  requests
from lxml import  etree
str1='2023-06-20'
list2=int(str1.replace('-',''))
date_str = input('输入日期范围形如20230101-20230301:')
date_list1 = date_str.split('-')
date_list1 = [int(i) for i in date_list1]
date_list = date_list1
print(date_list)

if list2 in range(date_list[0],date_list[1]):
    print('1')