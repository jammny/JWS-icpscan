'''
    JWS-icpscan是JWS系统的备案信息收集模块。
                                        ——by-jammny
'''
from pandas import DataFrame
from bs4 import BeautifulSoup
from prettytable import from_csv
from colorama import init, Fore
import requests, sys
# 加上这行代码即可，关闭安全请求警告
requests.packages.urllib3.disable_warnings()

class ICPScan:
    def __init__(self, target):
        self.target = target
        self.r_dict = {}
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
            'Connection': 'close'
        }

    # 天眼备案信息获取：
    def tianyan(self):
        try:
            url = "https://beian.tianyancha.com/search/{}".format(self.target)
            req = requests.get(url=url, headers=self.headers, timeout=3, verify=False)
            bf = BeautifulSoup(req.text, 'lxml')  # 获取HTML内容
            res = bf.find_all('tbody')  # 筛选内容
            res = res[0].find_all('tr')
            for i in range(0, len(res)):
                # 网站备案/许可证号
                a = res[i].find_all('a')
                a = a[0].string
                # 网站名称
                c = res[i].find_all('span')
                c = c[1].string
                # 主办单位名称
                b = res[i].find_all('em')
                b = b[0].string
                # 网站域名
                d = res[i].find_all('span')
                d = d[2].string
                # 审核时间
                e = res[i].find_all('td')
                e = e[5].string
                self.r_dict[str(i + 1)] = ([a, b, c, d, e])
        except:
            print(Fore.RED + ">>>>查询失败！建议检测网络，或者更换本地IP。")

    # 结果展示
    def show_result(self):
        tables_list = []
        for i in self.r_dict:
            table_list = []
            r_list = self.r_dict[i]
            for n in range(0,len(r_list)):
                table_list.append(r_list[n])
            tables_list.append(table_list)
        self.write_csv(tables_list)
        # 命令行结果展示
        with open("result/{}.csv".format(self.target), "r", encoding="utf-8") as f:
            table = from_csv(f)
        print(table)

    # 数据写入csv
    def write_csv(self, tables_list):
        name = ['网站备案/许可证号', '主办单位名称', '网站名称', '网站域名', '审核时间']
        c = DataFrame(columns=name, data=tables_list)
        c.to_csv('result/{}.csv'.format(self.target))

    # 程序入口
    def run(self):
        self.tianyan()
        self.show_result()

if __name__ == "__main__":
    init(autoreset=True)
    print(Fore.BLUE + r'''
       ___          _______       _                                
      | \ \        / / ____|     (_)                               
      | |\ \  /\  / / (___ ______ _  ___ _ __  ___  ___ __ _ _ __  
  _   | | \ \/  \/ / \___ \______| |/ __| '_ \/ __|/ __/ _` | '_ \ 
 | |__| |  \  /\  /  ____) |     | | (__| |_) \__ \ (_| (_| | | | |
  \____/    \/  \/  |_____/      |_|\___| .__/|___/\___\__,_|_| |_|
                                        | |                        
                                        |_|                        ——by jammny.2021.5.15
    ''')
    target = input(Fore.GREEN + ">>>>输入企业/公司名称：")
    # target = sys.argv[1]
    icp = ICPScan(target)
    icp.run()
