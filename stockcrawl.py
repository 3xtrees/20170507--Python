'''
Created on 2017/5/7
@author: 3xtrees
'''  
# -*- coding: gbk -*- 
import requests
import json
import timeit
import io
import os

def load_all_quote_symbol():
        print("load_all_quote_symbol start..." + "\n")
        start = timeit.default_timer()
        all_quotes = []
        all_quotes_url = 'http://money.finance.sina.com.cn/d/api/openapi_proxy.php'
        try:
            count = 1
            while (count < 100):
                para_val = '[["hq","hs_a","",0,' + str(count) + ',500]]'
                r_params = {'__s': para_val}
                r = requests.get(all_quotes_url, params=r_params)
                if(len(r.json()[0]['items']) == 0):
                    break
                for item in r.json()[0]['items']:
                    quote = {}
                    code = item[0]
                    name = item[2]
                    ## convert quote code
                    if(code.find('sh') > -1):
                        code = code[2:] + '.SS'
                    elif(code.find('sz') > -1):
                        code = code[2:] + '.SZ'
                    ## convert quote code end
                    quote['Symbol'] = code
                    quote['Name'] = name
                    all_quotes.append(quote)
                count += 1
        except Exception as e:
            print("Error: Failed to load all stock symbol..." + "\n")
            print(e)
        print("load_all_quote_symbol end... time cost: " + str(round(timeit.default_timer() - start)) + "s" + "\n")
        print("total " + str(len(all_quotes)) + " quotes are loaded..." + "\n")
        return all_quotes
    
def data_export(export_path, all_quotes, file_name):
        start = timeit.default_timer()
        if not os.path.exists(export_path):
            os.makedirs(export_path)
        if(all_quotes is None or len(all_quotes) == 0):
            print("no data to export...\n")
        print("start export to JSON file...\n")
        f = io.open(export_path + '/' + file_name + '.json', 'w', encoding='utf-8')
        json.dump(all_quotes, f, ensure_ascii=False)
        print("export is complete... time cost: " + str(round(timeit.default_timer() - start)) + "s" + "\n")

if __name__ == '__main__':
    all_quotes = load_all_quote_symbol()
    export_path = os.path.expanduser('.')+'\\tmp\\stock_export'
    data_export(export_path, all_quotes, file_name = 'result')