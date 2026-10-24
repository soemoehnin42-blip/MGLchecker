import google.generativeai as genai
from PIL import Image
import streamlit as st

st.set_page_config(page_title="MGL Slip & Sheet Checker", layout="centered")

st.title("MGL စလစ်နှင့် ငွေဝင်ဇယား တိုက်စစ်ဆေးရေး")
st.write(
    "MGL စလစ်ပုံနှင့် ငွေစာရင်းဇယားပုံကို တင်၍ AI ဖြင့် အလိုအလျောက်"
    " တိုက်စစ်ဆေးပါ။"
)

api_key = st.text_input("Google Gemini API Key ထည့်ပါ", type="password")

uploaded_slip = st.file_uploader(
    "MGL စလစ်ပုံ တင်ရန် (Slip)", type=["png", "jpg", "jpeg"]
)
uploaded_sheet = st.file_uploader(
    "ငွေဝင်ဇယားပုံ တင်ရန် (Sheet)", type=["png", "jpg", "jpeg"]
)

if st.button("စစ်ဆေးမည်"):
  if not api_key:
    st.error("ကျေးဇူးပြု၍ API Key အရင်ထည့်ပေးပါရှင်။")
  elif not uploaded_slip or not uploaded_sheet:
    st.error("စလစ်ပုံနှင့် ဇယားပုံ နှစ်ခုလုံး တင်ပေးပါရှင်။")
  else:
    try:
      genai.configure(api_key=api_key)
      model = genai.GenerativeModel("gemini-2.5-flash")

      slip_img = Image.open(uploaded_slip)
      sheet_img = Image.open(uploaded_sheet)

      prompt = (
          "ನೀವು ငွေစာရင်းစစ်ဆေးရေး AI ဖြစ်ပါတယ်။ ပေးထားသော MGL"
          " ငွေလွှဲစလစ်ပုံ (Slip) နှင့် ဘဏ်ငွေဝင်ဇယား (Sheet) တို့ကို"
          " အသေးစိတ် နှိုင်းယှဉ်တိုက်စစ်ဆေးပေးပါ။"
          " 1. ငွေပမာဏ (Amount) တူညီမှု ရှိမရှိ၊ 2. အမည် သို့မဟုတ် အကောင့်နံပါတ်"
          " 3. အချိန်နှင့် ရက်စွဲများကို စစ်ဆေးပေးပြီး"
          " ကိုက်ညီမှု ရှိမရှိကို မြန်မာဘာသာဖြင့် ရှင်းလင်းတိကျစွာ"
          " ရလဒ်ထုတ်ပေးပါ။"
      )

      with st.spinner("AI ဖြင့် စစ်ဆေးနေပါပြီ... ခဏစောင့်ပေးပါရှင်..."):
        response = model.generate_content([prompt, slip_img, sheet_img])

      st.success("စစ်ဆေးမှု ပြီးစီးပါပြီ!")
      st.markdown("### တိုက်စစ်ဆေးချက် ရလဒ်:")
      st.write(response.text)

    except Exception as e:
      st.error(f"မှားယွင်းမှု တစ်စုံတစ်ရာ ရှိနေပါသည်: {e}")

