"""
=============================================================
 Dashboard de Inversión Publicitaria en Colombia 1995–2031
 Streamlit App — datos embebidos, sin dependencia de archivo
=============================================================
Requisitos:
  pip install streamlit plotly pandas numpy scipy

Ejecutar local:
  streamlit run app.py

Desplegar en Streamlit Cloud:
  1. Sube este archivo a GitHub (repo público o privado)
  2. Ve a https://share.streamlit.io
  3. Conecta tu repo → Branch: main → File: app.py
  4. Deploy → obtienes link público
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from scipy import stats
import json

st.set_page_config(
    page_title="Inversión Publicitaria Colombia",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── CSS PERSONALIZADO ──────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.main { background: #07101f; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1400px; }
h1 { font-family: 'Syne', sans-serif !important; font-weight: 800 !important; }
h2, h3 { font-family: 'Syne', sans-serif !important; font-weight: 700 !important; }
.metric-card {
    background: #101d30; border: 1px solid #152035; border-radius: 12px;
    padding: 14px 18px; margin: 4px 0; position: relative; overflow: hidden;
}
.metric-card::after {
    content: ''; position: absolute; bottom: 0; left: 0; right: 0;
    height: 2px; background: currentColor; opacity: 0.25;
}
.stTabs [data-baseweb="tab-list"] { background: #0b1627; border-radius: 8px; padding: 4px; }
.stTabs [data-baseweb="tab"] {
    color: #4e6480; font-family: 'DM Sans', sans-serif;
    font-size: 0.82rem; font-weight: 500;
}
.stTabs [aria-selected="true"] { color: #f97316 !important; background: rgba(249,115,22,0.1) !important; }
</style>
""", unsafe_allow_html=True)

# ─── DATOS EMBEBIDOS ────────────────────────────────────────────
@st.cache_data
def load_data():
    raw = '''{"hist":{"years":[1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025],"tv":[221931.99,251590.28,308436.80000000005,332051.07999999996,346974.719988,399130.762695,452927.813906,483256.045584,550581.0,618950.0,710152.0,810636.0,923191.0,916858.0,882405.0,984641.0,1082169.0,1106903.0,1165535.0,1226670.0,1174157.0,1046498.0,969393.0,942134.0,949774.0,819524.0,1107062.0,1114837.0,1034108.0,1007426.60181,969771.837448],"tv_nac":[198962.38,229243.05,286168.84,304204.85,327958.083988,374799.945218,430507.51055,452990.730262,518029.0,584915.0,673410.0,763408.0,863885.0,858225.0,823611.0,919366.0,1020467.0,1043509.0,1098966.0,1155026.0,1102929.0,990127.0,917494.0,889760.0,889057.0,763423.0,1037067.0,1043937.0,975070.0,955310.260459,908656.993012],"tv_local":[22969.61,22347.23,22267.96,27846.23,19016.636,24330.817477,22420.303356,30265.315322,32552.0,34035.0,36742.0,47228.0,59306.0,58633.0,58794.0,65275.0,61702.0,63394.0,66569.0,71644.0,71228.0,56371.0,51899.0,52374.0,60717.0,56101.0,69995.0,70900.0,59038.0,52116.341351,61114.844436],"prensa":[307647.0,307647.0,307647.0,307647.0,307647.0,307647.0,307647.0,307647.0,307647.0,320890.0,353131.0,414077.0,526803.0,496891.0,478655.0,536026.0,599099.0,607059.0,637900.0,636192.0,574232.0,503065.0,465685.0,418083.0,376697.0,225403.0,253875.0,269501.0,246444.0,215570.0,206962.0],"radio":[224890.905032,224890.905032,224890.905032,224890.905032,172073.164257,188868.198375,175153.156378,192641.842395,209554.0,222096.0,257508.0,294505.0,345592.0,352518.0,365762.0,419008.0,443469.0,466508.0,521607.0,550216.0,561034.0,517723.0,528459.0,549185.0,541920.0,373737.0,499184.0,578788.0,578117.0,558882.425531,560706.329588],"digital":[0,0,0,0,0,0,0,0,0,0,0,0,0,40601.0,50016.0,94682.0,126366.0,162205.0,215507.0,255389.0,376110.0,409739.0,600476.0,848594.0,1080535.0,1251333.0,2040158.0,2354697.850382,2663179.0,2825565.16864,3066685.2979064],"revistas":[32751.156,35404.709,40055.50916,47905.297016,46349.039184,53527.665106,50546.114343,53647.97818,61775.0,70553.0,83440.0,105912.0,118890.0,108196.0,93488.0,99876.0,109519.0,110206.0,108706.0,103048.0,95061.0,77516.0,71067.0,59988.0,48036.0,19606.0,14732.0,11470.0,10513.0,8622.211773,6839.0],"exterior":[145738.0,145738.0,145738.0,145738.0,145738.0,145738.0,145738.0,145738.0,145738.0,145738.0,145738.0,145738.0,145738.0,145738.0,145738.0,145738.0,145738.0,145738.0,145738.0,145738.0,145885.0,130590.0,181973.0,184168.0,209888.0,82238.0,166607.0,274741.0,279346.0,292695.969141,328924.632627],"total":[254683.146,286994.98899999994,348492.30916000006,604847.282048,565396.923429,641526.626176,678627.084627,729545.866159,1129557.0,1232489.0,1404231.0,1625130.0,1914476.0,1915064.0,1870326.0,2134233.0,2360622.0,2452881.0,2649255.0,2917253.0,2926479.0,2685131.0,2817053.0,3002152.0,3206850.0,2771841.0,4081618.0,4604034.850382,4811707.0,4908762.376894999,5139889.0975694],"ipc":[0.1946,0.2163,0.17679999999999998,0.16699999999999998,0.09230000000000001,0.0875,0.0765,0.0699,0.0649,0.055,0.048499999999999995,0.044800000000000006,0.056900000000000006,0.0767,0.02,0.0317,0.0373,0.024399999999999998,0.0194,0.0366,0.0677,0.0575,0.0409,0.0318,0.038,0.0161,0.0562,0.1312,0.0928,0.052,0.052],"trm":[912.9,1002.94,1115.69,1402.92,1776.0,2087.73,2299.24,2361.07,2877.19,2607.87,2320.08,2358.38,2000.06,1969.95,2147.81,1897.74,1848.06,1768.23,1868.9,2000.36,2747.73,2977.77,2951.0,2956.0,3281.0,3693.0,3743.0,4255.44,4325.05,4072.59,4072.59],"internet":[0.001,0.003,0.005,0.012,0.018000000000000002,0.03,0.045,0.057999999999999996,0.07200000000000001,0.09300000000000001,0.121,0.15,0.184,0.226,0.27,0.325,0.379,0.42,0.47100000000000003,0.516,0.5720000000000001,0.63,0.665,0.684,0.7090000000000001,0.72,0.752,0.768,0.773,0.757,0.757]},"cagr":{"TV Nacional":5.19,"TV Local":3.32,"Prensa":-1.79,"Radio":3.44,"Digital":28.97,"Revistas":-5.09,"Exterior":7.68,"TOTAL":10.53},"forecast":{"TV Nacional":{"hist_x":[1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025],"hist_y":[198962.38,229243.05,286168.84,304204.85,327958.083988,374799.945218,430507.51055,452990.730262,518029.0,584915.0,673410.0,763408.0,863885.0,858225.0,823611.0,919366.0,1020467.0,1043509.0,1098966.0,1155026.0,1102929.0,990127.0,917494.0,889760.0,889057.0,763423.0,1037067.0,1043937.0,975070.0,955310.260459,908656.993012],"fc":[1452779.8127000597,1523460.373372929,1597579.6806565088,1675305.036254975,1756811.8814254827,1842284.1929832343],"lo":[854301.0815793728,719000.6733856668,636899.5488551487,579316.9207634248,535936.0096363312,501801.12067593896],"hi":[2470521.4937653434,3227996.29422969,4007320.8414644646,4844752.265828312,5758874.065603592,6763657.767730903],"fc_yrs":[2026,2027,2028,2029,2030,2031]},"TV Local":{"hist_x":[1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025],"hist_y":[22969.61,22347.23,22267.96,27846.23,19016.636,24330.817477,22420.303356,30265.315322,32552.0,34035.0,36742.0,47228.0,59306.0,58633.0,58794.0,65275.0,61702.0,63394.0,66569.0,71644.0,71228.0,56371.0,51899.0,52374.0,60717.0,56101.0,69995.0,70900.0,59038.0,52116.341351,61114.844436],"fc":[84653.16200422418,88075.46139747738,91636.11513993215,95340.71652538094,99195.08496941773,103205.27515094454],"lo":[53221.524822994725,45689.023893416226,41016.78904775041,37684.83936253226,35139.65745824469,33112.567454734344],"hi":[134647.73625232995,169784.47424210238,204725.37692219598,241207.13744133757,280015.9589996618,321670.27922382596],"fc_yrs":[2026,2027,2028,2029,2030,2031]},"Prensa":{"hist_x":[2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025],"hist_y":[307647.0,320890.0,353131.0,414077.0,526803.0,496891.0,478655.0,536026.0,599099.0,607059.0,637900.0,636192.0,574232.0,503065.0,465685.0,418083.0,376697.0,225403.0,253875.0,269501.0,246444.0,215570.0,206962.0],"fc":[308132.51778656244,298774.40513833985,289416.29249011725,280058.1798418984,270700.0671936758,261341.9545454532],"lo":[58230.83513380916,0.0,0.0,0.0,0.0,0.0],"hi":[558034.2004393158,652188.7540057208,722258.7037416399,779861.545147405,829497.2172968121,873473.5629076292],"fc_yrs":[2026,2027,2028,2029,2030,2031]},"Radio":{"hist_x":[1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025],"hist_y":[224890.905032,172073.164257,188868.198375,175153.156378,192641.842395,209554.0,222096.0,257508.0,294505.0,345592.0,352518.0,365762.0,419008.0,443469.0,466508.0,521607.0,550216.0,561034.0,517723.0,528459.0,549185.0,541920.0,373737.0,499184.0,578788.0,578117.0,558882.425531,560706.329588],"fc":[734262.2575784414,769687.9188046326,806822.7479205685,845749.2064746025,886553.7345048187,929326.9424876864],"lo":[515340.60944853065,466519.35174796195,436981.9295956515,416608.3037205067,401693.0526638876,390429.5941363012],"hi":[1046183.9277155508,1269871.2071302512,1489679.326475689,1716940.6223172478,1956661.9809631081,2212046.881190074],"fc_yrs":[2026,2027,2028,2029,2030,2031]},"Digital":{"hist_x":[2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025],"hist_y":[40601.0,50016.0,94682.0,126366.0,162205.0,215507.0,255389.0,376110.0,409739.0,600476.0,848594.0,1080535.0,1251333.0,2040158.0,2354697.850382,2663179.0,2825565.16864,3066685.2979064],"fc":[4262470,5924524,8234659,11445579,15908524,22111695],"lo":[2769450,3219711,3902009,4831725,6065776,7689738],"hi":[6560382,10901596,17378126,27112735,41722793,63581760],"fc_yrs":[2026,2027,2028,2029,2030,2031]},"Revistas":{"hist_x":[1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025],"hist_y":[32751.156,35404.709,40055.50916,47905.297016,46349.039184,53527.665106,50546.114343,53647.97818,61775.0,70553.0,83440.0,105912.0,118890.0,108196.0,93488.0,99876.0,109519.0,110206.0,108706.0,103048.0,95061.0,77516.0,71067.0,59988.0,48036.0,19606.0,14732.0,11470.0,10513.0,8622.211773,6839.0],"fc":[6039,5239,4439,3639,2839,2039],"lo":[3687,1913,365,0,0,0],"hi":[8391,8565,8513,8343,8098,7800],"fc_yrs":[2026,2027,2028,2029,2030,2031]},"Exterior":{"hist_x":[2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025],"hist_y":[145738.0,145885.0,130590.0,181973.0,184168.0,209888.0,82238.0,166607.0,274741.0,279346.0,292695.969141,328924.632627],"fc":[305886.48074355954,329613.3951022868,355180.7519140929,382731.31008863286,412418.90201750275,444409.2925189165],"lo":[174439.5388240822,148955.4686423612,134268.9640159272,124469.59769535027,117470.07646782881,112283.2503291327],"hi":[536383.7793451144,729378.9964281908,939557.160173634,1176859.7186333905,1447937.6863937296,1758941.0593141797],"fc_yrs":[2026,2027,2028,2029,2030,2031]},"TOTAL":{"hist_x":[1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025],"hist_y":[254683.146,286994.98899999994,348492.30916000006,604847.282048,565396.923429,641526.626176,678627.084627,729545.866159,1129557.0,1232489.0,1404231.0,1625130.0,1914476.0,1915064.0,1870326.0,2134233.0,2360622.0,2452881.0,2649255.0,2917253.0,2926479.0,2685131.0,2817053.0,3002152.0,3206850.0,2771841.0,4081618.0,4604034.850382,4811707.0,4908762.376894999,5139889.0975694],"fc":[7066546.790901369,7733784.219398384,8464023.535402723,9263213.502668183,10137864.579074735,11095101.952908067],"lo":[4343133.5861998545,3885273.304228146,3642623.662321143,3499077.577415189,3413757.411905772,3367435.1583925863],"hi":[11497708.407281918,15394391.505772797,19667058.97973578,24522784.218862887,30106503.13499635,36556394.27491928],"fc_yrs":[2026,2027,2028,2029,2030,2031]}},"regression":{"x_scatter":[0.226,0.27,0.325,0.379,0.42,0.47100000000000003,0.516,0.5720000000000001,0.63,0.665,0.684,0.7090000000000001,0.72,0.752,0.768,0.773,0.757,0.757],"y_scatter":[40601.0,50016.0,94682.0,126366.0,162205.0,215507.0,255389.0,376110.0,409739.0,600476.0,848594.0,1080535.0,1251333.0,2040158.0,2354697.850382,2663179.0,2825565.16864,3066685.2979064],"yr_scatter":[2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025],"x_line":[0.226,0.23716326530612244,0.2483265306122449,0.25948979591836735,0.2706530612244898,0.2818163265306123,0.2929795918367347,0.30414285714285716,0.3153061224489796,0.32646938775510204,0.33763265306122453,0.34879591836734697,0.3599591836734694,0.3711224489795919,0.38228571428571434,0.3934489795918368,0.4046122448979592,0.41577551020408166,0.4269387755102041,0.43810204081632653,0.449265306122449,0.46042857142857146,0.47159183673469396,0.4827551020408164,0.49391836734693884,0.5050816326530613,0.5162448979591837,0.5274081632653062,0.5385714285714286,0.549734693877551,0.5608979591836736,0.572061224489796,0.5832244897959185,0.5943877551020409,0.6055510204081633,0.6167142857142858,0.6278775510204082,0.6390408163265306,0.6502040816326531,0.6613673469387756,0.6725306122448981,0.6836938775510205,0.694857142857143,0.7060204081632654,0.7171836734693878,0.7283469387755103,0.7395102040816327,0.7506734693877551,0.7618367346938776,0.773],"y_line":[-596891.2337882613,-545352.6639493746,-493814.09411048796,-442275.52427160135,-390736.95443271473,-339198.3845938279,-287659.81475494104,-236121.24491605442,-184582.6750771678,-133044.1052382812,-81505.53539939434,-29966.965560507728,21571.604278378887,73110.17411726573,124648.74395615235,176187.31379503896,227725.88363392558,279264.4534728122,330803.0233116988,382341.5931505854,433880.1629894723,485418.7328283591,536957.3026672457,588495.8725061323,640034.442345019,691573.0121839056,743111.5820227922,794650.1518616788,846188.7217005654,897727.291539452,949265.8613783391,1000804.4312172257,1052343.0010561123,1103881.570894999,1155420.1407338856,1206958.7105727722,1258497.2804116588,1310035.8502505454,1361574.420089432,1413112.9899283191,1464651.5597672062,1516190.1296060928,1567728.6994449794,1619267.269283866,1670805.8391227527,1722344.4089616393,1773882.978800526,1825421.5486394125,1876960.1184782991,1928498.6883171857],"r2":0.6435,"slope":4616800.59,"intercept":-1640288.17,"p_value":6.207531045403789e-05},"corr":[[1.0,0.429,0.903,-0.079,0.297,0.012,0.81,-0.689,0.535,0.807],[0.429,1.0,0.044,-0.898,0.895,-0.545,-0.467,-0.378,-0.855,-0.337],[0.903,0.044,1.0,0.534,-0.129,0.678,0.894,-0.282,0.541,0.926],[-0.079,-0.898,0.534,1.0,-0.943,0.823,0.97,0.496,0.925,0.802],[0.297,0.895,-0.129,-0.943,1.0,-0.604,-0.284,-0.427,-0.508,-0.267],[0.012,-0.545,0.678,0.823,-0.604,1.0,0.9,0.514,0.658,0.612],[0.81,-0.467,0.894,0.97,-0.284,0.9,1.0,-0.433,0.841,0.942],[-0.689,-0.378,-0.282,0.496,-0.427,0.514,-0.433,1.0,-0.399,-0.463],[0.535,-0.855,0.541,0.925,-0.508,0.658,0.841,-0.399,1.0,0.801],[0.807,-0.337,0.926,0.802,-0.267,0.612,0.942,-0.463,0.801,1.0]],"corr_labels":["TV","Prensa","Radio","Digital","Revistas","Exterior","Total","IPC","TRM","Internet"],"metrics":{"TV Nacional":{"aic":-46.0,"bic":-43.1,"rmse":627482,"cagr":5.19},"TV Local":{"aic":-54.3,"bic":-51.4,"rmse":34401,"cagr":3.32},"Prensa":{"aic":567.8,"bic":570.0,"rmse":182290,"cagr":-1.79},"Radio":{"aic":-63.8,"bic":-61.2,"rmse":175120,"cagr":3.44},"Digital":{"aic":-41.1,"bic":-39.3,"rmse":1931391,"cagr":28.97},"Revistas":{"aic":682.4,"bic":685.3,"rmse":64038,"cagr":-5.09},"Exterior":{"aic":-14.0,"bic":-13.0,"rmse":101484,"cagr":7.68},"TOTAL":{"aic":-51.4,"bic":-48.5,"rmse":1557588,"cagr":10.53}},"breaks":[{"year":2002,"delta":192721},{"year":2013,"delta":152783},{"year":2014,"delta":174530},{"year":2017,"delta":274192},{"year":2018,"delta":379246}]}'''
    return json.loads(raw)

D = load_data()

# ─── PALETA ─────────────────────────────────────────────────────
COLORS = {
    'TV Nacional':'#3b82f6','TV Local':'#60a5fa','Prensa':'#f97316',
    'Radio':'#fbbf24','Digital':'#ef4444','Revistas':'#a78bfa',
    'Exterior':'#22d3ee','TOTAL':'#10b981',
    'tv_nac':'#3b82f6','tv_local':'#60a5fa','prensa':'#f97316',
    'radio':'#fbbf24','digital':'#ef4444','revistas':'#a78bfa',
    'exterior':'#22d3ee','total':'#10b981',
    'ipc':'#fb923c','trm':'#818cf8','internet':'#34d399'
}
KK = ['TV Nacional','TV Local','Prensa','Radio','Digital','Revistas','Exterior']
KC = ['tv_nac','tv_local','prensa','radio','digital','revistas','exterior']

# Layout base para Plotly
def base_layout(height=340, **kwargs):
    layout = dict(
        paper_bgcolor='#101d30', plot_bgcolor='#0b1627',
        font=dict(family='DM Sans, sans-serif', color='#d8e8f5', size=11),
        margin=dict(t=28, b=52, l=65, r=18),
        xaxis=dict(gridcolor='#152035', zerolinecolor='#152035', linecolor='#1c2e47'),
        yaxis=dict(gridcolor='#152035', zerolinecolor='#152035', linecolor='#1c2e47'),
        legend=dict(bgcolor='rgba(0,0,0,0)', bordercolor='#1c2e47', borderwidth=1, font=dict(size=9.5)),
        hoverlabel=dict(bgcolor='#0c1825', bordercolor='#1c2e47', font=dict(size=11)),
        height=height
    )
    layout.update(kwargs)
    return layout

def fmt(v):
    if v >= 1e6: return f"{v/1e6:.2f}M"
    if v >= 1e3: return f"{v/1e3:.0f}K"
    return f"{v:.0f}"

# ─── HEADER ─────────────────────────────────────────────────────
st.markdown("""
<div style="background: linear-gradient(135deg, #0b1627, #07101f);
            border: 1px solid #152035; border-radius: 16px;
            padding: 2rem 2rem 1.5rem; margin-bottom: 1.5rem">
  <div style="display:flex; gap:.5rem; flex-wrap:wrap; margin-bottom:.9rem">
    <span style="background:rgba(249,115,22,.08);border:1px solid rgba(249,115,22,.22);
                 color:#f97316;font-size:.62rem;font-weight:700;letter-spacing:.1em;
                 text-transform:uppercase;padding:.27rem .72rem;border-radius:2rem">📊 ECAR · IBOPE · IAB Colombia</span>
    <span style="background:rgba(59,130,246,.08);border:1px solid rgba(59,130,246,.2);
                 color:#3b82f6;font-size:.62rem;font-weight:700;letter-spacing:.1em;
                 text-transform:uppercase;padding:.27rem .72rem;border-radius:2rem">🗂 1995–2025 · 31 años</span>
    <span style="background:rgba(16,185,129,.08);border:1px solid rgba(16,185,129,.2);
                 color:#10b981;font-size:.62rem;font-weight:700;letter-spacing:.1em;
                 text-transform:uppercase;padding:.27rem .72rem;border-radius:2rem">🔮 Pronóstico 2026–2031</span>
  </div>
  <h1 style="font-family:Syne,sans-serif;font-weight:800;font-size:clamp(1.4rem,3vw,2.4rem);
             line-height:1.08;letter-spacing:-.03em;margin-bottom:.35rem;
             background:linear-gradient(115deg,#dbeafe 0%,#93c5fd 38%,#fb923c 76%,#f87171 100%);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent">
    Evolución de la Inversión Publicitaria<br>en Medios de Comunicación
  </h1>
  <p style="color:#4e6480;font-size:.85rem">
    Pronóstico y análisis estadístico a 6 años · Series en miles de COP corrientes · Colombia
  </p>
</div>
""", unsafe_allow_html=True)

# ─── KPIs ───────────────────────────────────────────────────────
total_vals = D['hist']['total']
last, prev = total_vals[-1], total_vals[-2]
yoy = (last - prev) / prev * 100
dig_last = D['hist']['digital'][-1]
dig_pct = dig_last / last * 100
fc_2031 = D['forecast']['TOTAL']['fc'][5]

col1,col2,col3,col4,col5,col6 = st.columns(6)
kpis = [
    (col1, "Inversión Total 2025", f"{fmt(last)} COP", "Miles corrientes", "#f97316"),
    (col2, "Crecimiento YoY",      f"+{yoy:.1f}%",    "vs 2024",          "#10b981"),
    (col3, "Participación Digital",f"{dig_pct:.1f}%", "del total 2025",   "#ef4444"),
    (col4, "CAGR Total 30 años",   f"+{D['cagr']['TOTAL']}%","1995–2025 anual","#3b82f6"),
    (col5, "CAGR Digital",         f"+{D['cagr']['Digital']}%","2008–2025 anual","#22d3ee"),
    (col6, "Proyección 2031",      f"{fmt(fc_2031)} COP","Central IC 95%",  "#a78bfa"),
]
for col, label, value, sub, color in kpis:
    with col:
        st.markdown(f"""
        <div class="metric-card" style="color:{color}">
          <div style="font-size:.6rem;text-transform:uppercase;letter-spacing:.1em;color:#4e6480;margin-bottom:.28rem">{label}</div>
          <div style="font-family:Syne,sans-serif;font-size:1.2rem;font-weight:700;line-height:1">{value}</div>
          <div style="font-size:.63rem;color:#4e6480;margin-top:.15rem">{sub}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── TABS ───────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Tendencias", "🔮 Pronóstico", "📺 Por Medios",
    "🌐 Digital", "🔗 Correlaciones", "🧮 Modelos"
])

# ══════════════════════════════════════════════════════════════
# TAB 1 – TENDENCIAS
# ══════════════════════════════════════════════════════════════
with tab1:
    st.markdown("#### Inversión Publicitaria Total — Colombia")
    chart_type = st.radio("Tipo de gráfico:", ["Línea", "Área", "Barras"], horizontal=True, key="tt")

    x, y = D['hist']['years'], D['hist']['total']
    if chart_type == "Barras":
        fig = go.Figure(go.Bar(x=x, y=y,
            marker_color=[f"rgba(249,115,22,{0.35+0.65*i/len(x):.2f})" for i in range(len(x))],
            hovertemplate="<b>%{x}</b><br>%{y:,.0f}<extra></extra>"))
    else:
        fill = 'tozeroy' if chart_type == "Área" else 'none'
        fig = go.Figure(go.Scatter(x=x, y=y, mode='lines+markers', fill=fill,
            line=dict(color='#f97316', width=2.8),
            fillcolor='rgba(249,115,22,0.07)',
            marker=dict(size=4, color='#f97316'),
            hovertemplate="<b>%{x}</b><br>%{y:,.0f}<extra></extra>"))

    for brk in D['breaks'][:2]:
        yr_idx = D['hist']['years'].index(brk['year'])
        fig.add_annotation(x=brk['year'], y=D['hist']['total'][yr_idx],
            text=f"Ruptura {brk['year']}", showarrow=True, arrowhead=2,
            arrowcolor='rgba(239,68,68,.45)', font=dict(size=8, color='#f87171'),
            bgcolor='rgba(239,68,68,.07)', bordercolor='rgba(239,68,68,.22)', borderpad=3)

    fig.update_layout(**base_layout(340, yaxis_title='COP Miles', yaxis_tickformat=',', xaxis_title='Año'))
    st.plotly_chart(fig, use_container_width=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### Composición por Medio · Área Apilada")
        fig2 = go.Figure()
        for i, (name, col_key) in enumerate(zip(KK, KC)):
            fig2.add_trace(go.Scatter(x=x, y=D['hist'][col_key], name=name,
                stackgroup='one', fill='tonexty' if i > 0 else 'tozeroy',
                fillcolor=f"rgba({','.join(str(int(COLORS[name][j*2+1:(j+1)*2+1],16)) for j in range(3))},0.72)",
                line=dict(color=COLORS[name], width=0.6),
                hovertemplate='%{x}: %{y:,.0f}<extra>'+name+'</extra>'))
        fig2.update_layout(**base_layout(320, yaxis_title='COP Miles', xaxis_title='Año'))
        st.plotly_chart(fig2, use_container_width=True)

    with col_b:
        st.markdown("#### Participación de Mercado Anual %")
        fig3 = go.Figure()
        for i, (name, col_key) in enumerate(zip(KK, KC)):
            pct_vals = [D['hist'][col_key][j]/D['hist']['total'][j]*100 if D['hist']['total'][j]>0 else 0 for j in range(len(x))]
            fig3.add_trace(go.Bar(x=x, y=pct_vals, name=name,
                marker_color=COLORS[name], hovertemplate='%{x}: %{y:.1f}%<extra>'+name+'</extra>'))
        fig3.update_layout(**base_layout(320, barmode='stack', yaxis=dict(title='%', range=[0,100]), xaxis_title='Año'))
        st.plotly_chart(fig3, use_container_width=True)

    col_c, col_d = st.columns(2)
    with col_c:
        st.markdown("#### Crecimiento Anual YoY %")
        yoy_vals = [None] + [(y[i]-y[i-1])/y[i-1]*100 for i in range(1, len(y))]
        yrs = D['hist']['years'][1:]
        vals = yoy_vals[1:]
        colors_yoy = ['#10b981' if v >= 0 else '#ef4444' for v in vals]
        fig4 = go.Figure(go.Bar(x=yrs, y=vals, marker_color=colors_yoy,
            hovertemplate='%{x}: %{y:.1f}%<extra></extra>'))
        for brk in D['breaks'][:3]:
            fig4.add_vline(x=brk['year'], line_dash="dot", line_color="rgba(239,68,68,.2)", line_width=1.2)
        fig4.update_layout(**base_layout(320, yaxis_title='Crecimiento %', xaxis_title='Año'))
        st.plotly_chart(fig4, use_container_width=True)

    with col_d:
        st.markdown("#### Contexto Macroeconómico")
        fig5 = make_subplots(specs=[[{"secondary_y": True}]])
        fig5.add_trace(go.Scatter(x=x, y=[v*100 for v in D['hist']['ipc']], name='IPC %',
            line=dict(color='#fb923c', width=2), marker=dict(size=3),
            hovertemplate='%{x}: %{y:.1f}%<extra>IPC</extra>'), secondary_y=False)
        fig5.add_trace(go.Scatter(x=x, y=D['hist']['trm'], name='TRM COP/USD',
            line=dict(color='#818cf8', width=2), marker=dict(size=3),
            hovertemplate='%{x}: %{y:,.0f}<extra>TRM</extra>'), secondary_y=True)
        fig5.add_trace(go.Scatter(x=x, y=[v*100 for v in D['hist']['internet']], name='Internet %',
            line=dict(color='#34d399', width=2, dash='dot'), marker=dict(size=3),
            hovertemplate='%{x}: %{y:.1f}%<extra>Internet</extra>'), secondary_y=False)
        fig5.update_layout(**base_layout(320))
        fig5.update_yaxes(title_text="IPC % / Internet %", secondary_y=False, gridcolor='#152035')
        fig5.update_yaxes(title_text="TRM", secondary_y=True, showgrid=False)
        st.plotly_chart(fig5, use_container_width=True)

# ══════════════════════════════════════════════════════════════
# TAB 2 – PRONÓSTICO
# ══════════════════════════════════════════════════════════════
with tab2:
    st.markdown("#### Histórico + Pronóstico por Categoría · IC 95%")
    cat_sel = st.selectbox("Seleccionar categoría:", ['TOTAL'] + KK, key="fcsel")

    fc = D['forecast'][cat_sel]
    col = COLORS.get(cat_sel, '#f97316')
    lastHX, lastHY = fc['hist_x'][-1], fc['hist_y'][-1]

    def hex_rgba(h, a):
        r,g,b = int(h[1:3],16), int(h[3:5],16), int(h[5:7],16)
        return f"rgba({r},{g},{b},{a})"

    fig_fc = go.Figure()
    fig_fc.add_trace(go.Scatter(x=fc['fc_yrs'], y=fc['hi'], mode='lines',
        line=dict(color=col, width=0), showlegend=False, hoverinfo='skip'))
    fig_fc.add_trace(go.Scatter(x=fc['fc_yrs'], y=fc['lo'], mode='lines', name='IC 95%',
        fill='tonexty', fillcolor=hex_rgba(col, .13), line=dict(color=col, width=0),
        hovertemplate='IC 95%: %{y:,.0f}<extra></extra>'))
    fig_fc.add_trace(go.Scatter(x=fc['hist_x'], y=fc['hist_y'], mode='lines+markers', name='Histórico',
        line=dict(color=col, width=2.8), marker=dict(size=3.5),
        hovertemplate='%{x}: %{y:,.0f}<extra>Histórico</extra>'))
    fig_fc.add_trace(go.Scatter(x=[lastHX, fc['fc_yrs'][0]], y=[lastHY, fc['fc'][0]],
        mode='lines', line=dict(color=col, width=1.5, dash='dot'), showlegend=False))
    fig_fc.add_trace(go.Scatter(x=fc['fc_yrs'], y=fc['fc'], mode='lines+markers', name='Pronóstico',
        line=dict(color=col, width=2.2, dash='dash'),
        marker=dict(size=9, symbol='diamond', color=col),
        hovertemplate='%{x}: %{y:,.0f}<extra>Pronóstico</extra>'))
    fig_fc.add_vline(x=2025.5, line_dash="dot", line_color="rgba(237,244,255,.12)", line_width=1)
    fig_fc.update_layout(**base_layout(380, yaxis_title='COP Miles', yaxis_tickformat=',', xaxis_title='Año'))
    st.plotly_chart(fig_fc, use_container_width=True)

    col_e, col_f = st.columns(2)
    with col_e:
        st.markdown("#### CAGR por Categoría · Período Real")
        cats_cagr = list(D['cagr'].keys())
        vals_cagr = list(D['cagr'].values())
        bar_colors = ['#ef4444' if v>10 else '#f97316' if v>4 else '#10b981' if v>=0 else '#64748b' for v in vals_cagr]
        fig_c = go.Figure(go.Bar(x=cats_cagr, y=vals_cagr, marker_color=bar_colors,
            text=[f"+{v:.2f}%" if v>=0 else f"{v:.2f}%" for v in vals_cagr],
            textposition='outside', hovertemplate='%{x}: %{y:.2f}%<extra>CAGR</extra>'))
        fig_c.update_layout(**base_layout(320, yaxis_title='CAGR % anual',
            xaxis=dict(tickangle=-30), margin=dict(t=24,b=85,l=55,r=18)))
        fig_c.add_hline(y=0, line_color='#253549', line_width=1.5)
        st.plotly_chart(fig_c, use_container_width=True)

    with col_f:
        st.markdown("#### Proyección Comparativa 2025–2031")
        fig_fa = go.Figure()
        for k in KK + ['TOTAL']:
            fcd = D['forecast'][k]
            fig_fa.add_trace(go.Scatter(x=fcd['hist_x'], y=fcd['hist_y'], name=k,
                line=dict(color=COLORS[k], width=1.8), legendgroup=k,
                hovertemplate='%{x}: %{y:,.0f}<extra>'+k+'</extra>'))
            fig_fa.add_trace(go.Scatter(
                x=[fcd['hist_x'][-1]] + fcd['fc_yrs'],
                y=[fcd['hist_y'][-1]] + fcd['fc'], name=k+' pron.',
                line=dict(color=COLORS[k], width=1.8, dash='dash'),
                showlegend=False, legendgroup=k,
                hovertemplate='%{x}: %{y:,.0f}<extra>'+k+' Pron.</extra>'))
        fig_fa.add_vline(x=2025.5, line_dash="dot", line_color="rgba(237,244,255,.1)")
        fig_fa.update_layout(**base_layout(320, yaxis_title='COP Miles', xaxis_title='Año',
            legend=dict(font=dict(size=8.5))))
        st.plotly_chart(fig_fa, use_container_width=True)

    st.markdown("#### Tabla de Proyección 2026–2031 con Intervalos de Confianza 95%")
    keys_tbl = ['TOTAL','TV Nacional','Prensa','Radio','Digital','Exterior']
    rows = []
    for i in range(6):
        yr = D['forecast']['TOTAL']['fc_yrs'][i]
        row = {'Año': yr}
        for k in keys_tbl:
            fcd = D['forecast'][k]
            row[k] = f"{fmt(fcd['fc'][i])} [{fmt(fcd['lo'][i])}–{fmt(fcd['hi'][i])}]"
        rows.append(row)
    df_tbl = pd.DataFrame(rows).set_index('Año')
    st.dataframe(df_tbl, use_container_width=True)

# ══════════════════════════════════════════════════════════════
# TAB 3 – POR MEDIOS
# ══════════════════════════════════════════════════════════════
with tab3:
    st.markdown("#### Series Históricas por Medio")
    selected_medios = st.multiselect("Seleccionar medios:", KK,
        default=['TV Nacional','Prensa','Radio','Digital'], key="medios_sel")

    if selected_medios:
        fig_m = go.Figure()
        for k in selected_medios:
            fig_m.add_trace(go.Scatter(x=D['hist']['years'], y=D['hist'][KC[KK.index(k)]],
                name=k, mode='lines+markers', line=dict(color=COLORS[k], width=2.2),
                marker=dict(size=3.5), hovertemplate='%{x}: %{y:,.0f}<extra>'+k+'</extra>'))
        fig_m.update_layout(**base_layout(340, yaxis_title='COP Miles', yaxis_tickformat=',', xaxis_title='Año'))
        st.plotly_chart(fig_m, use_container_width=True)

    col_g, col_h = st.columns(2)
    with col_g:
        st.markdown("#### Cambio Estructural de Participación")
        snap_yr = st.select_slider("Año de corte:", [2008, 2016, 2025], value=2025, key="snap")
        idx = D['hist']['years'].index(snap_yr)
        vals_pie = [max(D['hist'][c][idx] or 0, 0) for c in KC]
        fig_p = go.Figure(go.Pie(labels=KK, values=vals_pie, hole=0.42,
            marker=dict(colors=[COLORS[k] for k in KK], line=dict(color='#0b1627', width=1.5)),
            textinfo='label+percent', textfont=dict(size=9),
            hovertemplate='%{label}: %{value:,.0f}<extra></extra>'))
        fig_p.update_layout(**base_layout(320, showlegend=False, title=f"Año {snap_yr}",
            margin=dict(t=40, b=20, l=10, r=10)))
        st.plotly_chart(fig_p, use_container_width=True)

    with col_h:
        st.markdown("#### Ranking Inversión 2025")
        idx25 = D['hist']['years'].index(2025)
        data25 = sorted([(k, D['hist'][KC[i]][idx25] or 0) for i,k in enumerate(KK)], key=lambda x: -x[1])
        fig_b = go.Figure(go.Bar(
            x=[d[1] for d in data25], y=[d[0] for d in data25], orientation='h',
            marker_color=[COLORS[d[0]] for d in data25],
            text=[fmt(d[1]) for d in data25], textposition='outside',
            hovertemplate='%{y}: %{x:,.0f}<extra></extra>'))
        fig_b.update_layout(**base_layout(320, xaxis_title='COP Miles', xaxis_tickformat=',',
            margin=dict(t=20, b=50, l=92, r=82)))
        st.plotly_chart(fig_b, use_container_width=True)

# ══════════════════════════════════════════════════════════════
# TAB 4 – DIGITAL
# ══════════════════════════════════════════════════════════════
with tab4:
    di = next(i for i,v in enumerate(D['hist']['digital']) if v > 0)
    pct_dig = [D['hist']['digital'][i]/D['hist']['total'][i]*100 if D['hist']['total'][i]>0 else 0
               for i in range(len(D['hist']['years']))]

    col_i, col_j = st.columns(2)
    with col_i:
        st.markdown(f"#### Digital vs Penetración Internet · R²={D['regression']['r2']}")
        xs, ys, yrs_sc = D['regression']['x_scatter'], D['regression']['y_scatter'], D['regression']['yr_scatter']
        nc = [(y-yrs_sc[0])/(yrs_sc[-1]-yrs_sc[0]) for y in yrs_sc]
        fig_sc = go.Figure()
        fig_sc.add_trace(go.Scatter(x=xs, y=ys, mode='markers+text', text=[str(y) for y in yrs_sc],
            textposition='top center', textfont=dict(size=7.5, color='rgba(216,232,245,.5)'),
            marker=dict(size=10, color=nc, colorscale=[[0,'#f97316'],[.5,'#ef4444'],[1,'#a78bfa']],
                showscale=True, colorbar=dict(title=dict(text='Año'), len=.65, thickness=10,
                    tickmode='array', tickvals=[0,.5,1], ticktext=[str(yrs_sc[0]),'~2016',str(yrs_sc[-1])]),
                line=dict(color='rgba(255,255,255,.1)',width=1)),
            name='Observado', hovertemplate='<b>%{text}</b><br>Internet: %{x:.1%}<br>Digital: %{y:,.0f}<extra></extra>'))
        fig_sc.add_trace(go.Scatter(x=D['regression']['x_line'], y=D['regression']['y_line'],
            mode='lines', name=f"R²={D['regression']['r2']}",
            line=dict(color='#3b82f6', width=2.2, dash='dash')))
        fig_sc.update_layout(**base_layout(320, xaxis=dict(title='Penetración Internet', tickformat='.0%'),
            yaxis=dict(title='Inversión Digital (COP Miles)', tickformat=',')))
        st.plotly_chart(fig_sc, use_container_width=True)

    with col_j:
        st.markdown("#### Crecimiento Digital Histórico 2008–2025")
        fig_dh = go.Figure(go.Scatter(
            x=D['hist']['years'][di:], y=D['hist']['digital'][di:],
            fill='tozeroy', fillcolor='rgba(239,68,68,.09)',
            line=dict(color='#ef4444', width=2.8), marker=dict(size=4),
            hovertemplate='%{x}: %{y:,.0f}<extra>Digital</extra>'))
        fig_dh.update_layout(**base_layout(320, yaxis_title='COP Miles', yaxis_tickformat=',', xaxis_title='Año'))
        st.plotly_chart(fig_dh, use_container_width=True)

    col_k, col_l = st.columns(2)
    with col_k:
        st.markdown("#### Participación Digital del Total (%)")
        pct_colors = ['#ef4444' if v>50 else '#f97316' if v>30 else '#fbbf24' if v>15 else '#3b82f6' for v in pct_dig[di:]]
        fig_dp = go.Figure(go.Bar(
            x=D['hist']['years'][di:], y=pct_dig[di:], marker_color=pct_colors,
            text=[f"{v:.1f}%" for v in pct_dig[di:]], textposition='outside',
            hovertemplate='%{x}: %{y:.1f}%<extra></extra>'))
        fig_dp.update_layout(**base_layout(320, yaxis_title='% del Total', xaxis_title='Año'))
        st.plotly_chart(fig_dp, use_container_width=True)

    with col_l:
        st.markdown("#### Penetración Internet vs Participación Digital")
        fig_di = make_subplots(specs=[[{"secondary_y": True}]])
        fig_di.add_trace(go.Scatter(x=D['hist']['years'], y=[v*100 for v in D['hist']['internet']],
            name='Internet %', line=dict(color='#34d399', width=2.2), marker=dict(size=3.5),
            hovertemplate='%{x}: %{y:.1f}%<extra>Internet</extra>'), secondary_y=False)
        fig_di.add_trace(go.Scatter(x=D['hist']['years'], y=pct_dig,
            name='Digital/Total %', line=dict(color='#ef4444', width=2.2), marker=dict(size=3.5),
            hovertemplate='%{x}: %{y:.1f}%<extra>Digital</extra>'), secondary_y=True)
        fig_di.update_layout(**base_layout(320))
        fig_di.update_yaxes(title_text="Internet %", secondary_y=False, gridcolor='#152035')
        fig_di.update_yaxes(title_text="Digital/Total %", secondary_y=True, showgrid=False)
        st.plotly_chart(fig_di, use_container_width=True)

# ══════════════════════════════════════════════════════════════
# TAB 5 – CORRELACIONES
# ══════════════════════════════════════════════════════════════
with tab5:
    st.markdown("#### Mapa de Calor — Matriz de Correlaciones Pearson r")
    lbls = D['corr_labels']
    z = D['corr']
    z_rev = list(reversed(z))
    lbls_rev = list(reversed(lbls))
    fig_h = go.Figure(go.Heatmap(
        z=z_rev, x=lbls, y=lbls_rev,
        text=[[f"{v:.2f}" for v in row] for row in z_rev],
        texttemplate='%{text}', textfont=dict(size=11),
        colorscale=[[0,'#b91c1c'],[.2,'#ea580c'],[.38,'#1e3a5f'],[.5,'#0b1627'],[.62,'#1e3a5f'],[.8,'#1d4ed8'],[1,'#06b6d4']],
        zmid=0, zmin=-1, zmax=1, showscale=True, xgap=3, ygap=3,
        colorbar=dict(title=dict(text='r', font=dict(size=9.5)), len=.88, thickness=16,
            tickvals=[-1,-.5,0,.5,1], ticktext=['−1','−.5','0','.5','+1'], tickfont=dict(size=8.5)),
        hovertemplate='<b>%{y} ↔ %{x}</b><br>r = %{z:.3f}<extra></extra>'))
    fig_h.update_layout(**base_layout(460, margin=dict(t=22,b=105,l=95,r=28),
        xaxis=dict(tickangle=-40, tickfont=dict(size=10.5)),
        yaxis=dict(tickfont=dict(size=10.5))))
    st.plotly_chart(fig_h, use_container_width=True)

    col_m, col_n, col_o = st.columns(3)
    with col_m:
        st.markdown("#### TRM vs Inversión Total")
        fig_trm = go.Figure(go.Scatter(x=D['hist']['trm'], y=D['hist']['total'],
            mode='markers', text=[str(y) for y in D['hist']['years']],
            marker=dict(size=9, color=D['hist']['years'], colorscale='Plasma', showscale=True,
                colorbar=dict(title=dict(text='Año'),len=.6,thickness=10),
                line=dict(color='rgba(255,255,255,.1)',width=1)),
            hovertemplate='<b>%{text}</b><br>TRM: %{x:,.0f}<br>Total: %{y:,.0f}<extra></extra>'))
        fig_trm.update_layout(**base_layout(280, xaxis_title='TRM (COP/USD)', xaxis_tickformat=',', yaxis_title='Total'))
        st.plotly_chart(fig_trm, use_container_width=True)

    with col_n:
        st.markdown("#### IPC vs Inversión Total")
        fig_ipc = go.Figure(go.Scatter(x=[v*100 for v in D['hist']['ipc']], y=D['hist']['total'],
            mode='markers', text=[str(y) for y in D['hist']['years']],
            marker=dict(size=9, color=D['hist']['years'], colorscale='Viridis', showscale=True,
                colorbar=dict(title=dict(text='Año'),len=.6,thickness=10),
                line=dict(color='rgba(255,255,255,.1)',width=1)),
            hovertemplate='<b>%{text}</b><br>IPC: %{x:.1f}%<br>Total: %{y:,.0f}<extra></extra>'))
        fig_ipc.update_layout(**base_layout(280, xaxis_title='IPC (%)', yaxis_title='Total'))
        st.plotly_chart(fig_ipc, use_container_width=True)

    with col_o:
        st.markdown("#### Correlaciones vs Total · Ranking")
        tot_idx = D['corr_labels'].index('Total')
        corr_rank = [(l, D['corr'][tot_idx][i]) for i,l in enumerate(D['corr_labels']) if l!='Total']
        corr_rank.sort(key=lambda x: abs(x[1]), reverse=True)
        fig_cb = go.Figure(go.Bar(
            x=[c[1] for c in corr_rank], y=[c[0] for c in corr_rank], orientation='h',
            marker_color=['#3b82f6' if c[1]>0 else '#ef4444' for c in corr_rank],
            text=[f"{c[1]:.2f}" for c in corr_rank], textposition='outside',
            hovertemplate='%{y}: r=%{x:.3f}<extra></extra>'))
        fig_cb.add_vline(x=0, line_color='#253549', line_width=1.5)
        fig_cb.update_layout(**base_layout(280, xaxis=dict(title='r', range=[-1.1,1.1]),
            margin=dict(t=20,b=50,l=82,r=60)))
        st.plotly_chart(fig_cb, use_container_width=True)

# ══════════════════════════════════════════════════════════════
# TAB 6 – MODELOS
# ══════════════════════════════════════════════════════════════
with tab6:
    st.markdown("""
    <div style="background:linear-gradient(135deg,rgba(59,130,246,.05),rgba(249,115,22,.04));
                border:1px solid rgba(59,130,246,.18);border-radius:12px;padding:1.3rem;margin-bottom:1rem">
      <h3 style="font-family:Syne,sans-serif;margin-bottom:.4rem">🏆 Recomendación: ARIMAX (Total) + Prophet (Digital)</h3>
      <p style="color:#4e6480;font-size:.8rem;line-height:1.65">
        Las series muestran <strong>tendencias heterogéneas</strong>: Digital crece +28.97% anual,
        Radio y Exterior moderados, Prensa y Revistas declinan. La ruptura 2020 (COVID) afecta todas.
        Para el <strong>TOTAL</strong>, ARIMAX con IPC, TRM e Internet captura mejor los shocks macroeconómicos.
        Para <strong>Digital</strong>, Prophet maneja múltiples changepoints automáticamente.
      </p>
    </div>""", unsafe_allow_html=True)

    # Metrics table
    PERIODS={'TV Nacional':'1995–2025','TV Local':'1995–2025','Prensa':'2003–2025',
             'Radio':'1998–2025','Digital':'2008–2025','Revistas':'1995–2025',
             'Exterior':'2014–2025','TOTAL':'1995–2025'}
    rows_m = []
    for k, m in D['metrics'].items():
        cg = m['cagr']
        rows_m.append({
            'Categoría': k, 'Período': PERIODS.get(k,''),
            'AIC': m['aic'] or '—', 'BIC': m['bic'] or '—',
            'RMSE': fmt(m['rmse']) if m['rmse'] else '—',
            'CAGR': f"+{cg:.2f}%" if cg>=0 else f"{cg:.2f}%",
            'Tendencia': '📈 Creciente' if cg>5 else '↗ Leve alza' if cg>0 else '↘ Leve baja' if cg>-3 else '📉 Declinante'
        })
    df_m = pd.DataFrame(rows_m).set_index('Categoría')
    st.dataframe(df_m, use_container_width=True)

    col_p, col_q, col_r = st.columns(3)
    with col_p:
        st.markdown("#### AIC por Categoría")
        cats_m = list(D['metrics'].keys())
        aics_m = [D['metrics'][k]['aic'] or 0 for k in cats_m]
        fig_aic = go.Figure(go.Bar(x=cats_m, y=aics_m,
            marker_color=[COLORS.get(k,'#4e6480') for k in cats_m],
            text=[f"{v:.1f}" for v in aics_m], textposition='outside',
            hovertemplate='%{x}: AIC=%{y:.1f}<extra></extra>'))
        fig_aic.update_layout(**base_layout(280, yaxis_title='AIC',
            xaxis=dict(tickangle=-35), margin=dict(t=24,b=85,l=50,r=18)))
        st.plotly_chart(fig_aic, use_container_width=True)

    with col_q:
        st.markdown("#### RMSE Backtest (escala log)")
        rmses_m = [D['metrics'][k]['rmse'] or 1 for k in cats_m]
        fig_rmse = go.Figure(go.Bar(x=cats_m, y=rmses_m,
            marker_color=[COLORS.get(k,'#4e6480') for k in cats_m],
            text=[fmt(v) for v in rmses_m], textposition='outside',
            hovertemplate='%{x}: RMSE=%{y:,.0f}<extra></extra>'))
        fig_rmse.update_layout(**base_layout(280, yaxis=dict(title='RMSE (log)', type='log'),
            xaxis=dict(tickangle=-35), margin=dict(t=24,b=85,l=50,r=18)))
        st.plotly_chart(fig_rmse, use_container_width=True)

    with col_r:
        st.markdown("#### Proyección 2031 + IC 95%")
        ci_data = [(k, D['forecast'][k]['fc'][5], D['forecast'][k]['lo'][5], D['forecast'][k]['hi'][5])
                   for k in cats_m]
        fig_ci = go.Figure(go.Bar(
            x=[c[0] for c in ci_data], y=[c[1] for c in ci_data],
            error_y=dict(type='data', symmetric=False,
                array=[c[3]-c[1] for c in ci_data],
                arrayminus=[c[1]-c[2] for c in ci_data],
                color='rgba(237,244,255,.3)', thickness=2.5, width=7),
            marker_color=[COLORS.get(c[0],'#4e6480') for c in ci_data],
            text=[fmt(c[1]) for c in ci_data], textposition='outside',
            hovertemplate='%{x}: %{y:,.0f}<extra>2031</extra>'))
        fig_ci.update_layout(**base_layout(280, yaxis=dict(title='COP Miles 2031 (log)', type='log'),
            xaxis=dict(tickangle=-35), margin=dict(t=24,b=85,l=50,r=18)))
        st.plotly_chart(fig_ci, use_container_width=True)

# FOOTER
st.markdown("""
<div style="text-align:center;color:#253549;font-size:.69rem;padding:1.5rem 1rem;
            border-top:1px solid #152035;margin-top:1rem;line-height:2.1">
  <strong style="color:#4e6480">Dashboard Inversión Publicitaria — Colombia</strong> ·
  Fuentes: ECAR / IBOPE / IAB · 1995–2025<br>
  Metodología: Regresión Log-Lineal por período real · IC Bootstrap 95% · Validación leave-last-3-out<br>
  Python · NumPy · SciPy · Plotly · Streamlit · 2025
</div>""", unsafe_allow_html=True)
