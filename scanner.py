import json, math, os
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import pandas as pd
import yfinance as yf

with open("universe.json", encoding="utf-8") as f: universe=json.load(f)

def rsi(s, n=14):
    d=s.diff(); up=d.clip(lower=0).rolling(n).mean(); down=-d.clip(upper=0).rolling(n).mean()
    return 100-(100/(1+up/down.replace(0, float("nan"))))

def scan(tickers, key):
    out=[]
    for ticker in tickers:
        try:
            h=yf.download(ticker, period="1y", interval="1d", auto_adjust=True, progress=False, threads=False)
            if h.empty or len(h)<65: continue
            close=h["Close"].squeeze().dropna()
            vol=h["Volume"].squeeze().dropna()
            last=float(close.iloc[-1]); r=float(rsi(close).iloc[-1])
            ret1=(last/float(close.iloc[-22])-1)*100 if len(close)>22 else 0
            ret6=(last/float(close.iloc[-126])-1)*100 if len(close)>126 else ret1
            ma50=float(close.rolling(50).mean().iloc[-1]); ma200=float(close.rolling(200).mean().iloc[-1]) if len(close)>=200 else ma50
            avgvol=float(vol.tail(20).mean()) if len(vol)>=20 else 0
            volratio=float(vol.iloc[-1]/avgvol) if avgvol else 0
            # Scores are transparent heuristic ranks, not a predictive AI model.
            if key=="bharat_bargains":
                score=max(0,min(100,50+ret6*0.7+(last/ma50-1)*100*0.5-(r-55)*0.35))
                reason="Value watchlist + positive trend (valuation not verified)"
            elif key=="infra_titans":
                score=max(0,min(100,45+ret1*1.2+(last/ma50-1)*100*0.8+(volratio-1)*5))
                reason="Infrastructure watchlist + momentum"
            else:
                score=max(0,min(100,45+ret1*1.1+ret6*0.25+(last/ma50-1)*100*0.7+(volratio-1)*4))
                reason="Momentum + moving-average + volume rules"
            if last>ma50 and r>=48 and r<=78 and ret1>0:
                out.append({"symbol":ticker.replace(".NS",""),"company":ticker.replace(".NS",""),"close":round(last,2),"rsi":round(r,2),"return_1m":round(ret1,2),"score":round(score,1),"reason":reason,"as_of":str(close.index[-1].date())})
        except Exception as e:
            print("skip",ticker,repr(e))
    return sorted(out,key=lambda x:x["score"],reverse=True)[:10]

result={"generated_at":datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%d %b %Y, %I:%M %p IST"),"data_note":"Yahoo Finance daily adjusted prices; verify quotes independently","strategies":{}}
for k, symbols in universe.items(): result["strategies"][k]=scan(symbols,k)
result["total_picks"]=sum(map(len,result["strategies"].values()))
os.makedirs("data",exist_ok=True)
with open("data/picks.json","w",encoding="utf-8") as f: json.dump(result,f,ensure_ascii=False,indent=2)
print("Generated",result["total_picks"],"picks")
