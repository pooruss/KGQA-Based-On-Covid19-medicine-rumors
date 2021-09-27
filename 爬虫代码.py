import requests
import pandas as pd
import time #用于计时
import json


headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}


url = 'https://c.m.163.com/ug/api/wuhan/app/data/list-total'
r = requests.get(url, headers = headers)

data_json = json.loads(r.text)

data = data_json['data']

data_province = data['areaTree'][2]['children']

pd.DataFrame(data_province).head()

info = pd.DataFrame(data_province)[['id','lastUpdateTime','name']]

today_data = pd.DataFrame([province['today'] for province in data_province])
today_data.columns = ['today_'+i for i in today_data.columns]

total_data = pd.DataFrame([province['total'] for province in data_province])
total_data.columns = ['total_'+i for i in total_data.columns]

pd.concat([info,total_data,today_data],axis=1).head()


# 将提取数据的方法封装为函数
def get_data(data, info_list):
    info = pd.DataFrame(data)[info_list]  # 主要信息

    today_data = pd.DataFrame([i['today'] for i in data])  # 提取today数据
    today_data.columns = ['today_' + i for i in today_data.columns]  # 修改列名columns

    total_data = pd.DataFrame([i['total'] for i in data])
    total_data.columns = ['total_' + i for i in total_data.columns]

    return pd.concat([info, total_data, today_data], axis=1)



today_province = get_data(data_province,['id','lastUpdateTime','name'])



def save_data(data,name):
    file_name = name+'_'+time.strftime('%Y_%m_%d',time.localtime(time.time()))+'.csv'
    data.to_csv(file_name,index=None,encoding='utf_8_sig')
    print(file_name+' 保存成功！')




save_data(today_province, 'today_province')

areaTree = data['areaTree']#取出areaTree

today_world = get_data(areaTree,['id','lastUpdateTime','name'])


save_data(today_world,'today_world')

province_dict = {num: name for num, name in zip(today_province['id'], today_province['name'])}
start = time.time()
for province_id in province_dict:  # 遍历各省编号

    try:
        # 按照省编号访问每个省的数据地址，并获取json数据
        url = 'https://c.m.163.com/ug/api/wuhan/app/data/list-by-area-code?areaCode=' + province_id
        r = requests.get(url, headers=headers)
        data_json = json.loads(r.text)

        # 提取各省数据，然后写入各省名称
        province_data = get_data(data_json['data']['list'], ['date'])
        province_data['name'] = province_dict[province_id]

        # 合并数据
        if (province_id == '420000'):
            alltime_province = province_data
        else:
            alltime_province = pd.concat([alltime_province, province_data])

        print('-' * 20, province_dict[province_id], '成功',
              province_data.shape, alltime_province.shape,
              ',累计耗时：', round(time.time() - start), '-' * 20)
        # 设置延时等待
        time.sleep(5)

    except:
        print('-' * 20, province_dict[province_id], 'wrong', '-' * 20)



save_data(alltime_province,'alltime_province')



chinaDayList = data['chinaDayList']
alltime_China = get_data(chinaDayList,['date','lastUpdateTime'])
save_data(alltime_China, 'alltime_China')

country_dict = {key: value for key, value in zip(today_world['id'], today_world['name'])}

start = time.time()
for country_id in country_dict:  # 遍历各省编号

    try:
        # 按照省编号访问每个省的数据地址，并获取json数据
        url = 'https://c.m.163.com/ug/api/wuhan/app/data/list-by-area-code?areaCode=' + country_id
        r = requests.get(url, headers=headers)
        json_data = json.loads(r.text)

        # 提取各省数据，然后写入各省名称
        country_data = get_data(json_data['data']['list'], ['date'])
        country_data['name'] = country_dict[country_id]

        # 合并数据
        if (country_id == '9577772'):
            alltime_world = country_data
        else:
            alltime_world = pd.concat([alltime_world, country_data])

        print('-' * 20, country_dict[country_id], '成功',
              country_data.shape, alltime_world.shape,
              ',累计耗时：', round(time.time() - start), '-' * 20)
        # 设置延时等待
        time.sleep(3)

    except:
        print('-' * 20, country_dict[country_id], 'wrong', '-' * 20)




save_data(alltime_world,'alltime_world')