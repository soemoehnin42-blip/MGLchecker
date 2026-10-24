import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="MGL Slip & Sheet Checker", layout="centered")

st.title("MGL စလစ်နှင့် ငွေဝင်ဇယား တိုက်စစ်ဆေးရေး")
st.write("MGL စလစ်ပုံနှင့် ငွေစာရင်းဇယားပုံကို တင်၍ AI ဖြင့် အလိုအလျောက် တိုက်စစ်ပါ၊")

api_key = st.text_input("Google Gemini API Key ထည့်ပါ", type="password")

uploaded_slip = st.file_uploader("MGL စလစ်ပုံ တင်ပါ", type=["jpg", "jpeg", "png"])
uploaded_sheet = st.file_uploader("ငွေဝင်ဇယားပုံ တင်ပါ", type=["jpg", "jpeg", "png"])

if st.button("စစ်ဆေးမည်"):
    if not api_key:
        st.error("ကျေးဇူးပြု၍ API Key အရင်ထည့်ပေးပါ၊")
    elif not uploaded_slip or not uploaded_sheet:
        st.error("စလစ်ပုံနှင့် ဇယားပုံ နှစ်ခုလုံး တင်ပေးပါ၊")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            slip_img = Image.open(uploaded_slip)
            sheet_img = Image.open(uploaded_sheet)
            
            prompt = """
            ကျေးဇူးပြု၍ ပေးထားသော MGL စလစ်ပုံနှင့် ငွေဝင်ဇယားပုံကို သေချာတိုက်စစ်ပေးပါ။
            ၁။ စလစ်ထဲက ပမာဏ၊ ရက်စွဲ၊ အကောင့်အမည်/နံပါတ်တို့သည် ငွေဝင်ဇယားထဲက အချက်အလက်နှင့် ကိုက်ညီမှု ရှိမရှိ စစ်ပေးပါ။
            ၂။ ကိုက်ညီပါက 'မှန်ကန်သည်' ဟု ဖော်ပြပြီး၊ လွဲမှားနေပါက လွဲမှားနေသည့် အချက်များကို အသေးစိတ် ရှင်းပြပေးပါ။
            """
            
            with st.spinner("AI မှ တိုက်စစ်နေပါသည်... ခေတ္တစောင့်ပါ..."):
                response = model.generate_content([prompt, slip_img, sheet_img])
                st.success("စစ်ဆေးမှု ပြီးစီးပါပြီ!")
                st.markdown(response.text)
        except Exception as e:
            st.error(f"အမှားအယွင်း ဖြစ်ပေါ်ခဲ့သည်: {e}")
