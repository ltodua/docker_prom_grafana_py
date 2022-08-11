import time
import json, requests
from prometheus_client.core import GaugeMetricFamily, REGISTRY
from prometheus_client import start_http_server

class CustomCollector(object):
    def __init__(self):
        pass
    def collect(self):
        gauge = GaugeMetricFamily("gauge_eur_today", "eur currency to gel today. RN", labels=["value"])
        gauge2 = GaugeMetricFamily("gauge_eur_year", "eur currency to gel in past several months", labels=['day', 'month', 'year']) #, timestamp=["time"])

        gauge_command = requests.get('https://api.businessonline.ge/api/rates/nbg/eur')
        gauge_output = gauge_command.text

        gauge.add_metric(["EUR_to_GEL_today"], gauge_output)

        gauge2_command = requests.get('https://api.businessonline.ge/api/rates/nbg/eur/2021-01-01/2023-08-01')
        with open("currency.json", "w") as file:
            json.dump(gauge2_command.json(), file, ensure_ascii=False, indent=4)
            
        file = open("currency.json")
        items = json.load(file)

        for item in items:
            try:
                
                day = item["Date"][:10][-2:]
                month = item["Date"][:10][5:7]
                year= item["Date"][:10][:4]
                #print(month)
                gauge2.add_metric([day, month, year], item["Rate"] )
                #gauge2.set()
                #gauge2.add_metric( labels=["EUR_to_GEL"], item["Rate"] )
                #gauge.inc(item["Rate"])
                # print("at date: ", item["Date"][:10], "was -> this:", item["Rate"])

            except Exception as e:
                pass #print(e)



        yield gauge
        yield gauge2

if __name__ == "__main__":
    port = 9200
    frequency = 1
    start_http_server(port)
    REGISTRY.register(CustomCollector())
    while True:
        # period between collection
        time.sleep(frequency)