# coding: utf-8

"""12306命令行火车票查询器

Usage:
    tickets [-gdtkz] <from> <to> <date>

Options:
    -h, --help    显示帮助菜单
    -g            高铁
    -d            动车
    -t            特快
    -k            快速
    -z            直达

Example:
    tickets 北京 上海 2018-01-03
    tickets -dg 成都 南京 2018-01-28
"""

from docopt import docopt
from stations import stations
import requests
import urllib3
from prettytable import PrettyTable
from colorama import init, Fore
import time
import configparser

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# colorama init
init()

# conf
conf = configparser.ConfigParser()
conf.read(r"E:\projects\12306-tools\conf.ini", encoding="utf-8-sig")
tryTime = conf.getint('Search_time', 'tryTime')
maxTryTime = conf.getint('Search_time', 'maxTryTime')
queryUrl = conf.get('Url', 'tickets_query_url')
from_station_glb = conf.get('Ticket_info', 'from_station')
to_station_glb = conf.get('Ticket_info', 'to_station')
date_glb = conf.get('Ticket_info', 'date')
option_glb = conf.get('Ticket_info', 'options')

class queryTrain(object):
    def __init__(self, req, headers):
        self.req = req
        self.headers = headers

    def query_trict(self, from_station, to_station, date):
        # 通过输入的地点，获取到地点-code
        global queryUrl
        url = queryUrl.format(
            date, from_station, to_station)
        # 请求url,并设置不验证O
        try:
            response = self.req.get(url, headers=self.headers, verify=False, timeout=6)
            response.encoding = 'utf-8'
            # 得到我们需要的数据
            availabel_trains = response.json()['data']['result']
            # 但是那个格式我们不能直接使用，那么就需要进行把数据格式化一下
            # availabel_trains = [i.split('|') for i in availabel_trains]
            return availabel_trains
        except Exception:
            print("查询车次异常，请稍后重试!")
            return None

class TrainsCollection:
    header = '车次 车站 时间 历时 商务座 一等 二等 高级软卧 软卧 动卧 硬卧 软座 硬座 无座'.split()
    code2stations = {v: k for k, v in stations.items()}

    def __init__(self, available_trains, options):
        """查询到的火车班次集合
        :param available_trains: 一个列表, 包含可获得的火车班次, 每个
                                 火车班次是一个字典
        :param options: 查询的选项, 如高铁, 动车, etc...
        """
        self.available_trains = available_trains
        self.options = options

    @property
    def trains(self):
        for raw_train in self.available_trains:
            train_datas =  raw_train.split('|')
            train_no = train_datas[3]
            initial = train_no[0].lower()
            if not self.options or initial in self.options:
                train = [
                    train_no,
                    '\n'.join([
                        Fore.GREEN + self.code2stations[train_datas[6]] + Fore.RESET,
                        Fore.RED + self.code2stations[train_datas[7]] + Fore.RESET]),
                    '\n'.join([
                        Fore.GREEN + train_datas[8] + Fore.RESET,
                        Fore.RED + train_datas[9] + Fore.RESET]),
                    train_datas[10],
                    # 商务座
                    train_datas[32] or '--',
                    # 一等座
                    train_datas[31] or '--',
                    # 二等座
                    train_datas[30] or '--',
                    # 高级软卧
                    train_datas[21] or '--',
                    # 软卧
                    train_datas[23] or '--',
                    # 动卧
                    train_datas[33] or '--',
                    # 硬卧
                    train_datas[28] or '--',
                    # 软座
                    train_datas[24] or '--',
                    # 硬座
                    train_datas[29] or '--',
                    # 无座
                    train_datas[26] or '--',
                ]
                yield train

    def pretty_print(self):
        pt = PrettyTable()
        pt._set_field_names(self.header)
        for train in self.trains:
            pt.add_row(train)
        print(pt)

def cli():
    """command-line interface"""
    try:
        arguments = docopt(__doc__)
        print("输入结果: ")
        print("出发地:{},目的地:{},出发日期:{}".format(arguments['<from>'], arguments['<to>'], arguments['<date>']))
        from_station = stations.get(arguments['<from>'])
        to_station = stations.get(arguments['<to>'])
        date = arguments['<date>']
        # 获取参数
        options = ''.join([
            key for key, value in arguments.items() if value is True
        ])
    except:
        global from_station_glb
        global to_station_glb
        global date_glb
        print("未输入参数，使用配置文件 conf.ini")
        print("出发地:{},目的地:{},出发日期:{}".format(from_station_glb, to_station_glb, date_glb))
        from_station = stations.get(from_station_glb)
        to_station = stations.get(to_station_glb)
        date = date_glb
        options = option_glb

    headers = {
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
    }
    query_ticket_data = queryTrain(requests.session(), headers).query_trict(from_station, to_station, date)
    if query_ticket_data == None:
        global tryTime
        global maxTryTime
        print('等待5s，第{}次重试......'.format(tryTime))
        time.sleep(5)
        tryTime = tryTime + 1
        if(tryTime == maxTryTime + 1):
            print('请检查网络是否正常\n检查参数是否正确，可能时间超出放票时间，结束查询')
            input("Press <enter>")
            return
        cli()
    else:
        print("输出车次数据: ")
        TrainsCollection(query_ticket_data, options).pretty_print()
        input("Press <enter>")

if __name__=='__main__':
    cli()