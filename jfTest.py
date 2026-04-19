import streamlit as st
import gspread
import streamlit as st
import base64
from oauth2client.service_account import ServiceAccountCredentials
from collections import defaultdict




def set_bg_from_local(image_file):
  with open(image_file, "rb") as f:
      encoded = base64.b64encode(f.read()).decode()
  st.markdown(
      f"""
      <style>
      .stApp {{
          background-image: url("data:image/png;base64,{encoded}");
          background-size: cover;
          background-repeat: no-repeat;
          background-position: top;
      }}
      </style>
      """,
      unsafe_allow_html=True
  )




# 背景画像を設定
set_bg_from_local("IMG_0064.PNG")




# ---------------------- 🌸 フォントとスタイル ----------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:wght@700&display=swap');




#ダークモードでも常に黒字に
html, body, [class*="css"], .stApp {
  color: #111111 !important;
}




#/* グラデ背景 */
#.stApp {
  #background: linear-gradient(135deg, #ffe4e1, #add8e6);
  #background-attachment: fixed;
  #background-size: cover;
#}




/* 半透明カード */
.transparent-card {
  background-color: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 30px;
  margin: 20px 0;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  text-align: center;
  transition: transform 0.3s ease;
  font-family: 'Libre Baskerville', serif;
}




.transparent-card:hover {
  transform: scale(1.02);
}




.transparent-card h2, .transparent-card h3, .transparent-card p {
  font-family: 'Libre Baskerville', serif;
  font-weight: 700;  /* ここで全体を太字に */
}




.transparent-card h2 {
  font-size: 32px;
  margin-bottom: 10px;
  color: #333;
}




.transparent-card h3 {
  font-size: 28px;
  margin: 5px 0;
}




.transparent-card p {
  font-size: 20px;
  margin: 5px 0;
}




/* h1タグにフォントと太字適用 */
h1 {
  font-family: 'Libre Baskerville', serif !important;
  font-weight: 700 !important;
  color: #333 !important;
  text-align: center !important;
  font-size: 36px !important;  /* サイズ調整 */
}
</style>
""", unsafe_allow_html=True)




# ---------------------- 🌱 データ処理 ----------------------
if "gcp_service_account" not in st.secrets:
  st.error("Google認証情報が設定されていません。")
  st.stop()




creds_dict = st.secrets["gcp_service_account"]
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)




spreadsheet_name = "Japanese Festival 2025"
try:
  sheet = client.open(spreadsheet_name).sheet1
except gspread.exceptions.SpreadsheetNotFound:
  st.error(f"スプレッドシート '{spreadsheet_name}' が見つかりません。")
  st.stop()




data = sheet.get_all_records()
category_totals = defaultdict(float)
total_co2_reduction = 0.0




if not data:
  st.write("データがありません。")
else:
  for record in data:
      category = record.get("Category", "").strip().lower()
      weight = record.get("Weight (kg)", 0)
      co2 = record.get("CO2 Reduction (kg)", 0)




      try:
          weight = float(weight)
          category_totals[category] += weight
      except ValueError:
          st.warning(f"無効な重量データ: {weight}")

      try:
          co2 = float(co2)
          total_co2_reduction += co2
      except ValueError:
          st.warning(f"無効なCO2削減データ: {co2}")






total_weight = category_totals.get("recycle", 0) + category_totals.get("compost", 0)




# ---------------------- 💖 表示 ----------------------
st.markdown("<h1>🌸 Our Recycling Efforts Results 💙</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
  if "compost" in category_totals:
      st.markdown(f"""
      <div class="transparent-card">
           <h2>🌱 Compost</h2>
           <h3>{category_totals['compost']:.2f} kg</h3>
      </div>
      """, unsafe_allow_html=True)

with col2:
  if "recycle" in category_totals:
      st.markdown(f"""
      <div class="transparent-card">
          <h2>♻️ Recyclables</h2>
          <h3>{category_totals['recycle']:.2f} kg</h3>
      </div>
      """, unsafe_allow_html=True)

# 🌟ここを追加：CO2削減量の表示用カード
st.markdown(f"""
<div class="transparent-card" style="background-color: rgba(200, 255, 200, 0.6);">
  <h2>🌍 Total CO2 Reduced</h2>
  <h3>{total_co2_reduction:.3f} kg-CO2</h3>
</div>
""", unsafe_allow_html=True)

# 元々あった総重量のカード
st.markdown(f"""
<div class="transparent-card">
  <h2>📊 Total Waste Reduced</h2>
  <h3>{total_weight:.2f} kg</h3>
  <p>Thank you for your cooperation! 💖</p>
</div>
""", unsafe_allow_html=True)












