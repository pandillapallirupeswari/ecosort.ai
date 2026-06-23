import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# -----------------------------

# PAGE CONFIG

# -----------------------------

st.set_page_config(
page_title="ECOSORT - AI",
page_icon="♻️",
layout="wide"
)

# -----------------------------

# CUSTOM CSS

# -----------------------------

st.markdown("""

<style>

.stApp{
background: linear-gradient(135deg,#e8fff1,#d9ffe8,#f5fff8);
}

/* REMOVE WHITE TOP BAR */
header{
    visibility:hidden;
}

[data-testid="stHeader"]{
    background:transparent;
    height:0rem;
}

[data-testid="stToolbar"]{
    display:none;
}

[data-testid="stAppViewContainer"]{
    background: linear-gradient(135deg,#e8fff1,#d9ffe8,#f5fff8);
}

.main-title{
font-size:42px;
font-weight:700;
color:#0f5132;
text-align:center;
}

.sub-title{
text-align:center;
color:#198754;
font-size:18px;
}

.result-card{
background:white;
padding:20px;
border-radius:15px;
box-shadow:0 4px 12px rgba(0,0,0,0.1);
margin-top:15px;
}

.logo{
width:90px;
}

.bg-icons{
position:fixed;
top:0;
left:0;
width:100%;
height:100%;
pointer-events:none;
opacity:0.3;
font-size:45px;
z-index:0;

color: rgba(0, 150, 80, 0.25);
}

</style>

""", unsafe_allow_html=True)

# -----------------------------

# BACKGROUND ICONS

# -----------------------------
st.markdown("""
<style>
.bg-icon{
    position:fixed;
    font-size:45px;
    opacity:0.18;
    z-index:0;
}
</style>

<div class="bg-icon" style="top:5%; left:8%;">♻️</div>
<div class="bg-icon" style="top:15%; left:75%;">🌱</div>
<div class="bg-icon" style="top:30%; left:20%;">🗑️</div>
<div class="bg-icon" style="top:45%; left:85%;">🔋</div>
<div class="bg-icon" style="top:60%; left:10%;">📦</div>
<div class="bg-icon" style="top:75%; left:65%;">👕</div>
<div class="bg-icon" style="top:20%; left:50%;">🍾</div>
<div class="bg-icon" style="top:55%; left:40%;">🔩</div>
<div class="bg-icon" style="top:85%; left:25%;">📄</div>
<div class="bg-icon" style="top:35%; left:70%;">🧴</div>
<div class="bg-icon" style="top:90%; left:80%;">👟</div>
<div class="bg-icon" style="top:10%; left:35%;">🌍</div>
<div class="bg-icon" style="top:65%; left:90%;">♻️</div>
<div class="bg-icon" style="top:40%; left:5%;">🌿</div>

""", unsafe_allow_html=True)
# -----------------------------

# LOGO

# -----------------------------

colA, colB = st.columns([4, 1])

with colA:
    st.markdown(
        '<div class="main-title">♻️ ECOSORT - AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">AI Powered Waste Detection & Disposal Recommendation</div>',
        unsafe_allow_html=True
    )

with colB:
    try:
       from PIL import Image

       img = Image.open("ecosort.jpeg")
       st.image(img, width=160)
    except:
        pass
# -----------------------------

# MODEL

# -----------------------------

MODEL_PATH = "waste_classifier.h5"

@st.cache_resource
def load_model():
 return tf.keras.models.load_model(MODEL_PATH)

model = load_model()

# -----------------------------

# CLASSES

# -----------------------------
CLASSES = [
    "battery",
    "biological",
    "cardboard",
    "clothes",
    "glass",
    "metal",
    "paper",
    "plastic",
    "shoes",
    "trash"
]

# 👇 PLACE WASTE_INFO HERE (OUTSIDE LOOP)
WASTE_INFO = {

"battery":{
    "impact":"Batteries contain toxic chemicals and heavy metals that can contaminate soil and water if improperly disposed.",
    "disposal":"Take batteries to an authorized e-waste or battery recycling center. Never dispose of them in regular household waste.",
    "suggestions":[
        "Do not throw in regular bins",
        "Take to battery recycling points",
        "Avoid breaking batteries"
    ]
},

"biological":{
    "impact":"Organic waste can be converted into nutrient-rich compost and biogas.",
    "disposal":"Compost the waste at home or send it to a composting facility to produce organic fertilizer.",
    "suggestions":[
        "Separate wet and dry waste",
        "Convert organic waste into compost",
        "Use organic recycling methods"
    ]
},

"cardboard":{
    "impact":"Cardboard is highly recyclable and helps reduce landfill waste and deforestation.",
    "disposal":"Flatten cardboard boxes and send them to a paper or cardboard recycling facility.",
    "suggestions":[
        "Keep cardboard dry",
        "Flatten boxes before recycling",
        "Reuse boxes whenever possible"
    ]
},

"clothes":{
    "impact":"Textile waste can often be reused, donated, or recycled into new products.",
    "disposal":"Donate usable clothes or send damaged textiles to a textile recycling center.",
    "suggestions":[
        "Donate wearable clothes",
        "Reuse old fabrics",
        "Recycle damaged textiles"
    ]
},

"glass":{
    "impact":"Glass can be recycled repeatedly without losing quality, reducing environmental impact.",
    "disposal":"Clean glass items and send them to a glass recycling facility. Handle broken glass carefully.",
    "suggestions":[
        "Separate glass by color if possible",
        "Handle broken glass carefully",
        "Recycle clean glass containers"
    ]
},

"metal":{
    "impact":"Metal recycling saves energy and reduces the need for mining natural resources.",
    "disposal":"Send metal waste to a scrap metal collection and recycling center.",
    "suggestions":[
        "Separate metal items from other waste",
        "Sell scrap metal for recycling",
        "Clean metal containers before disposal"
    ]
},

"paper":{
    "impact":"Paper recycling reduces deforestation, water consumption, and energy usage.",
    "disposal":"Keep paper clean and dry and send it to a paper recycling facility.",
    "suggestions":[
        "Keep paper dry",
        "Avoid food contamination",
        "Reuse one-sided paper"
    ]
},

"plastic":{
    "impact":"Plastic can take hundreds of years to decompose and may pollute land and oceans.",
    "disposal":"Clean and separate plastic items before sending them to a plastic recycling facility.",
    "suggestions":[
        "Wash plastic containers",
        "Reduce single-use plastics",
        "Separate plastic types"
    ]
},

"shoes":{
    "impact":"Footwear can often be reused, repaired, donated, or recycled into new materials.",
    "disposal":"Donate reusable shoes or send worn-out shoes to a footwear recycling program.",
    "suggestions":[
        "Donate reusable shoes",
        "Repair shoes if possible",
        "Recycle worn-out footwear"
    ]
},

"trash":{
    "impact":"General waste usually ends up in landfills and contributes to environmental pollution.",
    "disposal":"Dispose of non-recyclable waste through municipal waste collection services.",
    "suggestions":[
        "Check for recyclable parts first",
        "Reduce landfill waste",
        "Segregate waste properly"
    ]
}

}

# -----------------------------

# UPLOAD

# -----------------------------


uploaded_files = st.file_uploader(
"Upload Waste Images",
type=["jpg","jpeg","png"],
accept_multiple_files=True
)

# -----------------------------

# PREDICTION

# -----------------------------

if uploaded_files:

    for file in uploaded_files:

        st.markdown("---")

        image = Image.open(file).convert("RGB")

        col1, col2 = st.columns([1, 2])

        # =========================
        # PREPROCESS
        # =========================
        img = image.resize((224, 224))
        img = np.array(img, dtype=np.float32)

        img = img / 127.5
        img = img - 1.0

        img = np.expand_dims(img, axis=0)

        # =========================
        # PREDICTION
        # =========================
        prediction = model.predict(img, verbose=0)[0]

        prob = prediction / np.sum(prediction)

        # =========================
        # IRRELEVANT IMAGE FILTER
        # =========================
        top1 = np.max(prob)
        top2 = np.partition(prob, -2)[-2]

        confidence = top1 * 100
        margin = top1 - top2

        if confidence < 80: 
           with col2:
                st.warning("⚠️ The uploaded image may not be relevant to waste classification. Please upload a clear image of waste.")

        is_mixed = confidence < 80 or margin < 0.30

        # =========================
        # CLASSIFICATION
        # =========================
        top_index = np.argmax(prob)
        waste_type = CLASSES[top_index]

        # =========================
        # DISPLAY IMAGE
        # =========================
        with col1:
            st.image(image, caption=file.name, use_container_width=True)

        # =========================
        # WASTE INFO
        # =========================
        with col2:
           
           if not is_mixed:

               info = WASTE_INFO[waste_type] 

               st.success(f"✅ Detected Waste Type: **{waste_type.upper()}**")

               st.markdown("### ♻ Disposal Method")
               st.success(info["disposal"])
        
               st.markdown("### 💡 How to Handle This Waste")
               st.success(info["impact"])

               st.markdown("### 🛠 Suggestions")
               for i, item in enumerate(info["suggestions"], start=1):
                 st.markdown(f"""
                    **Step {i}:** {item}
                """)
        