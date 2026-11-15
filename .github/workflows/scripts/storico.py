import yfinance as yf, pandas as pd, time, os

T = "VFINX VGTSX VEIEX FSELX NAESX VINEX VEXMX VGHCX FDFAX FSDPX FSENX VUSTX VFITX VBMFX ^SPGSCI ^IRX ^GSPC DFSVX DFISX FSAGX"
T = T.split()
os.makedirs("data", exist_ok=True)

out = {}
log = []
for t in T:
    s = None
    for k in range(3):
        try:
            d = yf.download(t, start="1990-01-01", interval="1mo", auto_adjust=True, progress=False)
            if len(d):
                c = d["Close"]
                s = c.iloc[:, 0] if hasattr(c, "columns") else c
                break
        except Exception as e:
            print(t, e)
        time.sleep(3)
    if s is not None:
        out[t] = s
    inizio = str(s.index[0].date()) if s is not None else "-"
    log.append(t + "," + str(0 if s is None else len(s)) + "," + inizio)
    print(log[-1])
    time.sleep(1)

df = pd.DataFrame(out)

for sid in ["DEXUSEU", "DEXGEUS"]:
    try:
        f = pd.read_csv("https://fred.stlouisfed.org/graph/fredgraph.csv?id=" + sid, index_col=0, parse_dates=True)
        f = pd.to_numeric(f.iloc[:, 0], errors="coerce")
        f = f.resample("MS").last()
        df[sid] = f
        log.append(sid + "," + str(f.notna().sum()) + "," + str(f.dropna().index[0].date()))
    except Exception as e:
        log.append(sid + ",0,-")
        print(sid, e)

df.to_csv("data/storico_mensili.csv")
with open("data/storico_log.csv", "w") as f:
    f.write("ticker,righe,inizio\n" + "\n".join(log) + "\n")
