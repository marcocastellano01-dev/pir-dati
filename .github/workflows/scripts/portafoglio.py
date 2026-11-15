import yfinance as yf, pandas as pd, time, os

CORE = "SXR8.DE IS3Q.DE XDWX.DE XDWD.DE PRAM.DE PRAN.MI SGLD.MI VVSM.DE AVWS.DE ZPRS.DE COPG.L JPGL.DE XDEW.DE XDWS.DE WHCA.DE IB1T.DE EQQQ.MI SXRV.DE XEON.DE CSPX.L EIMI.L EXSA.DE ZPRV.DE SXLE.MI"
PROXY = "SPY RSP QQQ URTH ACWI VT EEM VWO GLD SMH SOXX COPX DBMF KMLM CTA XLP XLV XLE QUAL MTUM VLUE AVUV AVDV DLS VSS IJR VB EFA"
IDEE = "VALL.MI VGLA.DE VWCE.DE EMXC EEMS DGS FRDM XCS6.DE EMIM.L SPYY.DE IUSN.DE WSML.L XDEM.DE"
ALTRO = "BTC-USD ETH-USD BTC-EUR ETH-EUR NVDA PYPL STMMI.MI EURUSD=X ^VIX ^IRX ^TNX ^GSPC ^NDX"

T = (CORE + " " + PROXY + " " + IDEE + " " + ALTRO).split()
os.makedirs("data", exist_ok=True)

def scarica(t, interval):
    for k in range(3):
        try:
            d = yf.download(t, start="2000-01-01", interval=interval, auto_adjust=True, progress=False)
            if len(d):
                s = d["Close"]
                return s.iloc[:, 0] if hasattr(s, "columns") else s
        except Exception as e:
            print(t, e)
        time.sleep(3)
    return None

mens, giorn, log = {}, {}, []
for t in T:
    m = scarica(t, "1mo")
    time.sleep(1)
    g = scarica(t, "1d")
    time.sleep(1)
    if m is not None:
        mens[t] = m
    if g is not None:
        giorn[t] = g
    inizio = str(g.index[0].date()) if g is not None else "-"
    log.append(t + "," + str(0 if g is None else len(g)) + "," + inizio)
    print(log[-1])

pd.DataFrame(mens).to_csv("data/portafoglio_mensili.csv")
pd.DataFrame(giorn).to_csv("data/portafoglio_giornalieri.csv.gz", compression="gzip")
with open("data/portafoglio_log.csv", "w") as f:
    f.write("ticker,righe_giornaliere,inizio\n" + "\n".join(log) + "\n")
