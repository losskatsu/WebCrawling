#!/usr/bin/env python
# coding: utf-8

# In[1]:


from urllib.request import urlopen
from bs4 import BeautifulSoup
import pymysql
import time
import requests

def stock_crawling(item):
    url = "http://comp.fnguide.com/SVO2/ASP/SVD_main.asp?pGB=1&gicode=A"+item+"&cID=&MenuYn=Y&ReportGB=&NewMenuID=11&stkGb=&strResearchYN="
    html = urlopen(url)
    bs_obj = BeautifulSoup(html, "html.parser")
    
    # 날짜
    date1 = bs_obj.find("span", {"class":"date"})
    date2 = date1.text
    date = date2.replace('[','').replace(']','').replace('/','-')
    
    # 기업 정보
    corp_name1 = bs_obj.find_all("h1", {"id":"giName"})
    corp_name = corp_name1[0].text

    # 종목 코드
    code1 = bs_obj.find_all("div", {"class":"corp_group1"})
    code2 = code1[0].find("h2")
    code = code2.text
    
    # 주가
    stock_price1 = bs_obj.find("span", {"id":"svdMainChartTxt11"})
    stock_price2 = stock_price1.text
    stock_price = int(stock_price2.replace(',', '').strip())
    
    # 외국인 보유 비중
    fgn_own_ratio1 = bs_obj.find("span", {"id":"svdMainChartTxt12"})
    fgn_own_ratio = float(fgn_own_ratio1.text)

    # 상대수익률
    rel_return1 = bs_obj.find("span", {"id":"svdMainChartTxt13"})
    rel_return = float(rel_return1.text)

    # 상단 리스트
    up_list = bs_obj.find("div", {"class":"corp_group2"})
    dd = up_list.find_all("dd")

    # PER
    per = float(dd[1].text)

    # 12M PER
    per_12m = float(dd[3].text)

    # 업종 PER
    per_ind = float(dd[5].text)
    
    # PBR
    pbr = float(dd[7].text)
    
    # 배당 수익률
    div_yid1 = dd[9].text
    div_yid2 = div_yid1.replace('%','')
    div_yid = float(div_yid2)

    # 시세 현황 테이블
    table1 = bs_obj.find("div", {"id":"div1"})
    table2 = table1.find_all("td")
    
    # 거래량
    volume1 = table2[1].text
    volume = int(volume1.replace(',', '').strip())
    
    # 거래 대금
    trans_price1 = table2[3].text
    trans_price = int(trans_price1.replace(',', '').strip())
    
    # 시가 총액(우선주 포함)
    mk_cpt_pfr1 = table2[6].text
    mk_cpt_pfr = int(mk_cpt_pfr1.replace(',', '').strip())
    
    # 시가총액(보통주)
    mk_cpt_cm1 = table2[8].text
    mk_cpt_cm = int(mk_cpt_cm1.replace(',', '').strip())
    
    # 결과모음 리스트
    # [날짜, 기업정보, 종목코드, 주가, 외국인 보유비중, 상대수익률,
    #  per, 12m per, 업종per, pbr, 배당수익률
    #  테이블, 거래량, 거래 대금, 시가총액(우선주포함), 시가총액(보통주)] 
    res = [date, corp_name, code, stock_price, fgn_own_ratio, rel_return,per, per_12m, per_ind, pbr, div_yid, volume, trans_price, mk_cpt_pfr, mk_cpt_cm]
    
    return res

def db_insert(res):
    try:
        conn = pymysql.connect(host='localhost', user='root', 
                               password='1234', db='stock', charset='utf8')
        sql_state = """INSERT INTO stock.daily_market(dt, item_name, item_code, price, foreign_ownership_ratio, rel_return, per, per_12m, per_ind, pbr, dividend_yield, volume, trans_price, market_capital_prefer, market_capital_common) VALUES ('%s', '%s', '%s', %d, %f, %f, %f, %f, %f, %f, %f, %d, %d, %d, %d)"""%(tuple(res))
        db =  conn.cursor()
        db.execute(sql_state)
        conn.commit()
    except: 
        token = "xoxb-1884011609779-1883945975650-babfTvQLWSlRWP2aHhiKzOEG"
        channel = "#stock_alarm01"
        text = "Check your stock crawler."

        requests.post("https://slack.com/api/chat.postMessage",
            headers={"Authorization": "Bearer "+token},
            data={"channel": channel,"text": text})        
    finally:
        conn.close()
        
if __name__ == '__main__':
        
    item_list = ['005930', '066570']
    
    for item in item_list:
        res = stock_crawling(item)
        db_insert(res)
        time.sleep(3)


# In[ ]:




