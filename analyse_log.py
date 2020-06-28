import apache_log_parser
import datetime
import psutil
import csv
import re
import os

def get_area():
    area = {"memory_flag":"","line_num":0,"end_flag":""}
    print("メモリ使用率を設定")
    area["memory_usage"] = float(input())
    print("期間を指定しますか？　 y or n ")
    if(input() == "n"):
        area["flag"] = "n"
        return area
    print("from")
    from_date = list(map(int , input().split()))
    from_d = datetime.datetime(from_date[0],from_date[1],from_date[2]
                    ,0,0,tzinfo=datetime.timezone(datetime.timedelta(hours=9)))
    print("to") 
    to_date = list(map(int, input().split()))
    to_d = datetime.datetime(to_date[0],to_date[1],to_date[2]
                    ,0,0,tzinfo=datetime.timezone(datetime.timedelta(hours=9)))
    area["flag"], area["from"], area["to"] = "y", from_d , to_d
    
    return area

def multiple_read_apache_log(D,area):
    P = []      ##ログデータ格納
    for i in range(area["file_num"],len(D)):
        if(re.compile("access_log.*").search(D[i])):
            area["file_num"] = i
            read_apache_log(D[i],P,area)
            if(area["memory_flag"] == "on"):
                break
            else:
                area["line_num"] = 0
    else:
        area["end_flag"] = "on" 
    return P

def read_apache_log(fn,P,area,logformat='%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"'):
    parser = apache_log_parser.make_parser(logformat)
    cou = area["line_num"]
    count = 0
    with open(fn) as f:
        for line in f:
            if(cou > 0):
                cou -=1
                continue
            count += 1
            try:
                parsed_line = parser(line)
                host, time = parsed_line["remote_host"], parsed_line["time_received_tz_datetimeobj"]
                if(area["flag"] == "n"):
                    P.append([host,time])
                elif(area["from"] <= time <= area["to"]):
                    P.append([host,time])
            except ValueError:
                pass
            mem = psutil.virtual_memory() 
            if(mem.percent >= area["memory_usage"]):
                area["line_num"] += count            
                area["memory_flag"] = "on"
                break
        else:
            area["memory_flag"] = "ok"


def count_access(HT):
    host_access = {}
    time_access = {str(k) : 0 for k in range(24)}
    for i in range(len(HT)):
        host = HT[i][0]
        time = str(HT[i][1].hour)
        if(host_access.get(host,"None") == "None"):
            host_access[host] = 1
        else:
            host_access[host] += 1

        if(time_access.get(time)!="None"):
            time_access[time] += 1

    host_access = dict(sorted(host_access.items(), key = lambda x:x[1],reverse=True))
    return host_access,time_access

def make_csv_file(access,fn):
    l = {}
    try:
        with open(fn,'r') as f:
            reader = csv.DictReader(f)
            l = [row for row in reader][0]
            for i in range(len(access.keys())):
                key = list(access.keys())[i]
                try:
                    l[key] = str(int(l[key]) + access[key])
                except:
                    l[key] = access[key]
            
            with open(fn,'w') as f:
                writer = csv.DictWriter(f, l.keys())
                writer.writeheader()
                writer.writerow(l)

    except FileNotFoundError:
        with open(fn,'w') as f:
            writer = csv.DictWriter(f, access.keys())
            writer.writeheader()
            writer.writerow(access)

def make_file_name(area):
    fn_host = "host.csv"
    fn_time = "time.csv"
    if(area["flag"] == "y"):
        f_d = area["from"].strftime('%Y%m%d')
        t_d = area["to"].strftime('%Y%m%d')
        fn_host = "host_"+f_d+"_"+t_d+".csv"
        fn_time = "time_"+f_d+"_"+t_d+".csv"
    return fn_host, fn_time


def main():
    D = os.listdir()    ##カレントディレクトリのファイル名参照
    area = get_area()
    area["file_num"] = 0
    while area["end_flag"] == "":
        host_time = multiple_read_apache_log(D,area)
        ##期間指定に該当するデータのみcount_accessにぶち込む
        host_access, time_access = count_access(host_time)
        fn_host, fn_time = make_file_name(area)
        make_csv_file(host_access,fn_host)
        make_csv_file(time_access,fn_time)
        area["memory_flag"] = ""
        host_time, host_access, time_access = [],[],[]

    print("解析終了")



if __name__ == '__main__':
    main()
	
