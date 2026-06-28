import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import base64
from io import BytesIO

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="ECOSORT - Intelligent Waste AI",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Helper function to convert PIL images to base64 so they render inline perfectly
def img_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

# -----------------------------
# HIGH-CONTRAST HACKATHON THEME ENGINE
# -----------------------------
current_theme = {
    "bg": "linear-gradient(135deg, #0f172a 0%, #020617 100%)", 
    "card_bg": "rgba(15, 23, 42, 0.9)",
    "text_primary": "#ffffff",
    "text_secondary": "#94a3b8",
    "accent": "#38bdf8",
    "accent_light": "rgba(56, 189, 248, 0.15)",
    "shadow": "rgba(56, 189, 248, 0.2)",
    "icons": ["♻️", "🌍", "🌱", "🗑️", "🌿"]
}

THEMES = {
    "battery": {
        "bg": "linear-gradient(135deg, #450a0a 0%, #0f0505 100%)",
        "card_bg": "rgba(28, 7, 7, 0.95)",
        "text_primary": "#ffffff",
        "text_secondary": "#fca5a5",
        "accent": "#ff3333", 
        "accent_light": "rgba(255, 51, 51, 0.2)",
        "shadow": "rgba(255, 51, 51, 0.45)",
        "icons": ["🔋", "⚡", "⚠️", "🔌", "🔋"]
    },
    "biological": {
        "bg": "linear-gradient(135deg, #064e3b 0%, #022c22 100%)",
        "card_bg": "rgba(2, 44, 34, 0.95)",
        "text_primary": "#ffffff",
        "text_secondary": "#6ee7b7",
        "accent": "#00ff88", 
        "accent_light": "rgba(0, 255, 136, 0.2)",
        "shadow": "rgba(0, 255, 136, 0.45)",
        "icons": ["🌱", "🍎", "🍌", "🌿", "🍁"]
    },
    "cardboard": {
        "bg": "linear-gradient(135deg, #7c2d12 0%, #1c1917 100%)",
        "card_bg": "rgba(43, 21, 14, 0.95)",
        "text_primary": "#ffffff",
        "text_secondary": "#fdba74",
        "accent": "#ff7b00", 
        "accent_light": "rgba(255, 123, 0, 0.2)",
        "shadow": "rgba(255, 123, 0, 0.45)",
        "icons": ["📦", "📦", "🪵", "🏷️", "📦"]
    },
    "clothes": {
        "bg": "linear-gradient(135deg, #2e1b4b 0%, #0f0e26 100%)",
        "card_bg": "rgba(23, 13, 41, 0.95)",
        "text_primary": "#ffffff",
        "text_secondary": "#c084fc",
        "accent": "#c084fc", 
        "accent_light": "rgba(192, 132, 252, 0.2)",
        "shadow": "rgba(192, 132, 252, 0.45)",
        "icons": ["👕", "👗", "🧦", "🧣", "👖"]
    },
    "glass": {
        "bg": "linear-gradient(135deg, #164e63 0%, #083344 100%)",
        "card_bg": "rgba(11, 46, 61, 0.95)",
        "text_primary": "#ffffff",
        "text_secondary": "#67e8f9",
        "accent": "#00e5ff", 
        "accent_light": "rgba(0, 229, 255, 0.2)",
        "shadow": "rgba(0, 229, 255, 0.45)",
        "icons": ["🍾", "🍷", "🥛", "🧪", "💎"]
    },
    "metal": {
        "bg": "linear-gradient(135deg, #374151 0%, #111827 100%)",
        "card_bg": "rgba(31, 41, 55, 0.95)",
        "text_primary": "#ffffff",
        "text_secondary": "#d1d5db",
        "accent": "#e5e7eb", 
        "accent_light": "rgba(229, 231, 235, 0.2)",
        "shadow": "rgba(229, 231, 235, 0.35)",
        "icons": ["🥫", "🔩", "🔧", "🔨", "📎"]
    },
    "paper": {
        "bg": "linear-gradient(135deg, #1e293b 0%, #0f172a 100%)",
        "card_bg": "rgba(30, 41, 59, 0.95)",
        "text_primary": "#ffffff",
        "text_secondary": "#cbd5e1",
        "accent": "#38bdf8", 
        "accent_light": "rgba(56, 189, 248, 0.2)",
        "shadow": "rgba(56, 189, 248, 0.35)",
        "icons": ["📄", "📰", "📚", "📝", "✉️"]
    },
    "plastic": {
        "bg": "linear-gradient(135deg, #1e3a8a 0%, #172554 100%)",
        "card_bg": "rgba(23, 37, 84, 0.95)",
        "text_primary": "#ffffff",
        "text_secondary": "#93c5fd",
        "accent": "#3b82f6", 
        "accent_light": "rgba(59, 130, 246, 0.2)",
        "shadow": "rgba(59, 130, 246, 0.45)",
        "icons": ["🥤", "🧴", "🛍️", "🧪", "🥤"]
    },
    "shoes": {
        "bg": "linear-gradient(135deg, #581c87 0%, #2e1065 100%)",
        "card_bg": "rgba(46, 16, 101, 0.95)",
        "text_primary": "#ffffff",
        "text_secondary": "#f472b6",
        "accent": "#ec4899", 
        "accent_light": "rgba(236, 72, 153, 0.2)",
        "shadow": "rgba(236, 72, 153, 0.45)",
        "icons": ["👟", "🥾", "👠", "👞", "👟"]
    },
    "trash": {
        "bg": "linear-gradient(135deg, #27272a 0%, #09090b 100%)",
        "card_bg": "rgba(24, 24, 27, 0.92)",
        "text_primary": "#ffffff",
        "text_secondary": "#a1a1aa",
        "accent": "#f4f4f5", 
        "accent_light": "rgba(244, 244, 245, 0.15)",
        "shadow": "rgba(244, 244, 245, 0.35)",
        "icons": ["🗑️", "🚮", "🖤", "💨", "🗑️"]
    }
}

# -----------------------------
# MULTI-LANGUAGE TRANSLATION MATRICES
# -----------------------------
from gtts import gTTS

LANG_UI = {
    "English": {
        "title": "♻️ ECOSORT AI",
        "subtitle": "Computer Vision & Environmental Intelligence Infrastructure",
        "drop_zone": "📤 Drop waste image here to run deep vision classification...",
        "impact_title": "⚠️ Environmental Impact Profile",
        "disposal_title": "🚛 Recommended Disposal Method",
        "steps_title": "🛠️ Actionable Handling Steps",
        "voice_btn": "🔊 Read Outcomes Out Loud",
        "lang_code": "en",
        "audio_prefix": "Material identified as",
        "audio_impact": "Environmental impact status:",
        "audio_disposal": "Recommended disposal action:",
        "audio_steps": "Follow these handling steps:"
    },
    "తెలుగు (Telugu)": {
        "title": "♻️ ఎకోసార్ట్ AI",
        "subtitle": "కంప్యూటర్ విజన్ & పర్యావరణ ఇంటెలిజెన్స్ ఇన్ఫ్రాస్ట్రక్చర్",
        "drop_zone": "📤 డీప్ విజన్ వర్గీకరణను ప్రారంభించడానికి వ్యర్థాల చిత్రాన్ని ఇక్కడ వేయండి...",
        "impact_title": "⚠️ పర్యావరణ ప్రభావ ప్రొఫైల్",
        "disposal_title": "🚛 సిఫార్సు చేయబడిన పారవేసే పద్ధతి",
        "steps_title": "🛠️ ఆచరణాత్మక నిర్వహణ దశలు",
        "voice_btn": "🔊 ఫలితాలను వినండి",
        "lang_code": "te",
        "audio_prefix": "గుర్తించబడిన వ్యర్థ పదార్థం",
        "audio_impact": "పర్యావరణ ప్రభావం:",
        "audio_disposal": "సిఫార్సు చేయబడిన పారవేసే పద్ధతి:",
        "audio_steps": "ఈ క్రింది దశలను అనుసరించండి:"
    },
    "தமிழ் (Tamil)": {
        "title": "♻️ எகோசார்ட் AI",
        "subtitle": "கம்ப்யூட்டர் விஷன் & சுற்றுச்சூழல் நுண்ணறிவு உள்கட்டமைப்பு",
        "drop_zone": "📤 ஆழ்ந்த பார்வை வகைப்பாட்டைத் தொடங்க கழிவுப் படத்தை இங்கே பதிவேற்றவும்...",
        "impact_title": "⚠️ சுற்றுச்சூழல் பாதிப்பு சுயவிவரம்",
        "disposal_title": "🚛 பரிந்துரைக்கப்பட்ட அகற்றல் முறை",
        "steps_title": "🛠️ நடைமுறை கையாளுதல் படிகள்",
        "voice_btn": "🔊 முடிவுகளை உரக்கக் கேளுங்கள்",
        "lang_code": "ta",
        "audio_prefix": "கண்டறியப்பட்ட கழிவுப்பொருள்",
        "audio_impact": "சுற்றுச்சூழல் பாதிப்பு:",
        "audio_disposal": "பரிந்துரைக்கப்பட்ட அகற்றல் முறை:",
        "audio_steps": "பின்வரும் வழிமுறைகளைப் பின்பற்றவும்:"
    },
    "മലയാളം (Malayalam)": {
        "title": "♻️ എക്കോസോർട്ട് AI",
        "subtitle": "കമ്പ്യൂട്ടർ വിഷൻ & എൻവയോൺമെന്റൽ ഇന്റലിജൻസ് ഇൻഫ്രാസ്ട്രക്ചർ",
        "drop_zone": "📤 വർഗ്ഗീകരണം ആരംഭിക്കുന്നതിന് മാലിന്യത്തിന്റെ ചിത്രം ഇവിടെ അപ്‌ലോഡ് ചെയ്യുക...",
        "impact_title": "⚠️ പാരിസ്ഥിതിക ആഘാത വിവരണം",
        "disposal_title": "🚛 ശുപാർശ ചെയ്ത സംസ്കരണ രീതി",
        "steps_title": "🛠️ പ്രായോഗിക നടപടികൾ",
        "voice_btn": "🔊 ഫലം ഉച്ചത്തിൽ കേൾക്കുക",
        "lang_code": "ml",
        "audio_prefix": "കണ്ടെത്തിയ മാലിന്യ വസ്തു",
        "audio_impact": "പാരിസ്ഥിതിക ആഘാതം:",
        "audio_disposal": "ശുപാർശ ചെയ്ത സംസ്കരണ രീതി:",
        "audio_steps": "താഴെ പറയുന്ന നടപടികൾ സ്വീകരിക്കുക:"
    },
    "ಕನ್ನಡ (Kannada)": {
        "title": "♻️ ಎಕೋಸಾರ್ಟ್ AI",
        "subtitle": "ಕಂಪ್ಯೂಟರ್ ವಿಷನ್ ಮತ್ತು ಎನ್ವಿರಾನ್ಮೆಂಟಲ್ ಇಂಟೆಲಿಜೆನ್ಸ್ ಇನ್ಫ್ರಾಸ್ಟ್ರಕ್ಚರ್",
        "drop_zone": "📤 ಆಳವಾದ ದೃಷ್ಟಿ ವರ್ಗೀಕರಣವನ್ನು ಚಲಾಯಿಸಲು ತ್ಯಾಜ್ಯದ ಚಿತ್ರವನ್ನು ಇಲ್ಲಿ ಬಿಡಿ...",
        "impact_title": "⚠️ ಪರಿಸರ ಪ್ರಭಾವದ ಪ್ರೊಫೈಲ್",
        "disposal_title": "🚛 ಶಿಫಾರಸು ಮಾಡಲಾದ ವಿಲೇವಾರಿ ವಿಧಾನ",
        "steps_title": "🛠️ ಕ್ರಿಯಾತ್ಮಕ ನಿರ್ವಹಣಾ ಹಂತಗಳು",
        "voice_btn": "🔊 ಫಲಿತಾಂಶಗಳನ್ನು ಆಲಿಸಿ",
        "lang_code": "kn",
        "audio_prefix": "ಪತ್ತೆಯಾದ ತ್ಯಾಜ್ಯ ವಸ್ತು",
        "audio_impact": "ಪರಿಸರ ಪ್ರಭಾವ:",
        "audio_disposal": "ಶಿಫಾರಸು ಮಾಡಲಾದ ವಿಲೇವಾರಿ ವಿಧಾನ:",
        "audio_steps": "ಈ ಕೆಳಗಿನ ಹಂತಗಳನ್ನು ಅನುಸರಿಸಿ:"
    },
    "हिन्दी (Hindi)": {
        "title": "♻️ इकोसॉर्ट AI",
        "subtitle": "कंप्यूटर विज़न और पर्यावरणीय इंटेलिजेंस इन्फ्रास्ट्रक्चर",
        "drop_zone": "📤 डीप विज़न वर्गीकरण शुरू करने के लिए कचरे की छवि को यहाँ ड्रॉप करें...",
        "impact_title": "⚠️ पर्यावरणीय प्रभाव प्रोफ़ाइल",
        "disposal_title": "🚛 अनुशंसित निपटान विधि",
        "steps_title": "🛠️ व्यावहारिक हैंडलिंग कदम",
        "voice_btn": "🔊 परिणाम को जोर से सुनें",
        "lang_code": "hi",
        "audio_prefix": "पहचाना गया कचरा सामग्री है",
        "audio_impact": "पर्यावरण प्रभाव:",
        "audio_disposal": "अनुशंसित निपटान विधि:",
        "audio_steps": "इन व्यावहारिक कदमों का पालन करें:"
    }
}

# High-visibility text wrapper rules for your dropdown layout
# -------------------------------------------------------------
# FIXED MAX-WIDTH LANGUAGE SELECTOR CONTAINER
# -------------------------------------------------------------
st.markdown("""
<style>
    /* Centers the picker container box and restricts its maximum scaling size */
    .lang-picker-wrapper {
        max-width: 300px;
        margin: 0 auto 15px auto;
        text-align: left;
    }
    .lang-picker-label {
        color: #ffffff; 
        font-weight: 600; 
        margin-bottom: 6px; 
        font-size: 14px;
    }
</style>
<div class="lang-picker-wrapper">
    <div class="lang-picker-label">🌐 Choose Language</div>
</div>
""", unsafe_allow_html=True)

# Wrap the actual selectbox column block to keep it small
col_left, col_mid, col_right = st.columns([1, 2, 1])
with col_mid:
    selected_lang = st.selectbox(
        "LANGUAGE_SELECTOR", 
        list(LANG_UI.keys()), 
        index=0, 
        label_visibility="collapsed"
    )
text = LANG_UI[selected_lang]

CLASSES = ["battery", "biological", "cardboard", "clothes", "glass", "metal", "paper", "plastic", "shoes", "trash"]

WASTE_INFO = {
    "battery": {
        "impact": "Contains heavy metals capable of severe soil leaching and water ecosystem toxicity.",
        "disposal": "Must be routed exclusively to designated Hazardous E-Waste Collections.",
        "suggestions": ["Segregate safely in a dry container", "Do not mix with household trash", "Drop off at e-waste kiosks"]
    },
    "biological": {
        "impact": "Decomposes anaerobically in landfills producing methane gas. Highly valuable when composted.",
        "disposal": "Direct to organic processing loops or backyard composting assemblies.",
        "suggestions": ["Separate liquids from solids", "Use biodegradable bin liners", "Utilize for nutrient-rich composting"]
    },
    "cardboard": {
        "impact": "Recycling saves timber forests, minimizes processing energy usage, and mitigates landfill mass.",
        "disposal": "Flatten thoroughly, protect from liquid structural damage, and stack into fiber bins.",
        "suggestions": ["Break down structural boxes flat", "Remove excessive heavy adhesive tapes", "Keep dry to protect paper fibers"]
    },
    "clothes": {
        "impact": "Decomposition of synthetic fibers can take centuries while releasing greenhouse gases.",
        "disposal": "Route to textile reuse platforms, localized donation pipelines, or fiber down-cycling.",
        "suggestions": ["Wash thoroughly before processing", "Separate high-quality wearable clothes", "Send scraps to textile regenerators"]
    },
    "glass": {
        "impact": "Infinitely recyclable without molecular integrity loss, downscaling production emissions.",
        "disposal": "Rinse clean of residues and deposit gently into color-sorted containment streams.",
        "suggestions": ["Rinse food matrices thoroughly", "Sort by tint profile if available", "Handle structurally broken glass safely"]
    },
    "metal": {
        "impact": "Extremely high energy-savings yield compared to virgin raw resource extraction operations.",
        "disposal": "Clean out alternative compound materials and deliver directly to scrap collection networks.",
        "suggestions": ["Wash cans clean of juices", "Remove plastic wrapper seals", "Compress soft aluminum items"]
    },
    "paper": {
        "impact": "Fibers can be re-pulped multiple times, saving significant fresh-water volumes.",
        "disposal": "Discard into dry paper collection structures. Avoid mixing with grease.",
        "suggestions": ["Ensure zero liquid or chemical contact", "Segregate highly soiled grease-paper", "Shred highly sensitive documentation"]
    },
    "plastic": {
        "impact": "Fractures into destructive microplastics that poison marine and land lifecycles.",
        "disposal": "Check local resin codes, clean residue, and drop into polymer recycle facilities.",
        "suggestions": ["Crush bottles to minimize air volume", "Rinse remaining liquid contents", "Separate films from rigid structures"]
    },
    "shoes": {
        "impact": "Complex blended assembly of rubber, leather, and polymers makes decomposition footprint massive.",
        "disposal": "Donate functional footwear assemblies or forward to specialized athletic grind programs.",
        "suggestions": ["Tie pairs securely together", "Scrub heavy soil off outsoles", "Extract completely non-fixed inner insoles"]
    },
    "trash": {
        "impact": "Destination is strictly long-term land burial or energy incineration plants.",
        "disposal": "Drop securely sealed into standard residue management collection pipelines.",
        "suggestions": ["Re-inspect for misclassified items", "Seal bags securely against pests", "Optimize volume footprint before dropping"]
    }
}

# -----------------------------
# AI MODEL INFERENCE ENGINE
# -----------------------------
MODEL_PATH = "waste_classifier.h5"

@st.cache_resource
def load_model():
    return tf.keras.models.load_model(MODEL_PATH)

try:
    model = load_model()
except Exception as e:
    st.error(f"Inference Engine Error: {e}")

# -----------------------------
# MULTI-LANGUAGE TRANSLATION MATRICES (EVERY SINGLE UI VALUE & BACKEND OUTCOME)
# -----------------------------
from gtts import gTTS


WASTE_DATA_LOCALIZED = {
    "English": {
        "cardboard": {"class": "Cardboard", "impact": "Recycling saves timber forests, minimizes processing energy usage, and mitigates landfill mass.", "disposal": "Flatten thoroughly, protect from liquid structural damage, and stack into fiber bins.", "suggestions": ["Break down structural boxes flat", "Remove excessive heavy adhesive tapes", "Keep dry to protect paper fibers"]},
        "battery": {"class": "Battery", "impact": "Contains heavy metals capable of severe soil leaching and water ecosystem toxicity.", "disposal": "Must be routed exclusively to designated Hazardous E-Waste Collections.", "suggestions": ["Segregate safely in a dry container", "Do not mix with household trash", "Drop off at e-waste kiosks"]},
        "biological": {"class": "Biological", "impact": "Decomposes anaerobically in landfills producing methane gas. Highly valuable when composted.", "disposal": "Direct to organic processing loops or backyard composting assemblies.", "suggestions": ["Separate liquids from solids", "Use biodegradable bin liners", "Utilize for nutrient-rich composting"]},
        "clothes": {"class": "Clothes", "impact": "Decomposition of synthetic fibers can take centuries while releasing greenhouse gases.", "disposal": "Route to textile reuse platforms, localized donation pipelines, or fiber down-cycling.", "suggestions": ["Wash thoroughly before processing", "Separate high-quality wearable clothes", "Send scraps to textile regenerators"]},
        "glass": {"class": "Glass", "impact": "Infinitely recyclable without molecular integrity loss, downscaling production emissions.", "disposal": "Rinse clean of residues and deposit gently into color-sorted containment streams.", "suggestions": ["Rinse food matrices thoroughly", "Sort by tint profile if available", "Handle structurally broken glass safely"]},
        "metal": {"class": "Metal", "impact": "Extremely high energy-savings yield compared to virgin raw resource extraction operations.", "disposal": "Clean out alternative compound materials and deliver directly to scrap collection networks.", "suggestions": ["Wash cans clean of juices", "Remove plastic wrapper seals", "Compress soft aluminum items"]},
        "paper": {"class": "Paper", "impact": "Fibers can be re-pulped multiple times, saving significant fresh-water volumes.", "disposal": "Discard into dry paper collection structures. Avoid mixing with grease.", "suggestions": ["Ensure zero liquid or chemical contact", "Segregate highly soiled grease-paper", "Shred highly sensitive documentation"]},
        "plastic": {"class": "Plastic", "impact": "Fractures into destructive microplastics that poison marine and land lifecycles.", "disposal": "Check local resin codes, clean residue, and drop into polymer recycle facilities.", "suggestions": ["Crush bottles to minimize air volume", "Rinse remaining liquid contents", "Separate films from rigid structures"]},
        "shoes": {"class": "Shoes", "impact": "Complex blended assembly of rubber, leather, and polymers makes decomposition footprint massive.", "disposal": "Donate functional footwear assemblies or forward to specialized athletic grind programs.", "suggestions": ["Tie pairs securely together", "Scrub heavy soil off outsoles", "Extract completely non-fixed inner insoles"]},
        "trash": {"class": "Trash", "impact": "Destination is strictly long-term land burial or energy incineration plants.", "disposal": "Drop securely sealed into standard residue management collection pipelines.", "suggestions": ["Re-inspect for misclassified items", "Seal bags securely against pests", "Optimize volume footprint before dropping"]}
    },
    "తెలుగు (Telugu)": {
        "cardboard": {"class": "కార్డ్‌బోర్డ్", "impact": "రీసైక్లింగ్ చేయడం ద్వారా కలప అడవులు రక్షించబడతాయి మరియు ల్యాండ్‌ఫిల్ వ్యర్థాలు తగ్గుతాయి.", "disposal": "కార్డ్‌బోర్డ్‌ను పూర్తిగా ఫ్లాట్‌గా చేసి, తడి తగలకుండా ఫైబర్ బిన్లలో వేయండి.", "suggestions": ["బాక్సులను పూర్తిగా ఫ్లాట్‌గా మడవండి", "దట్టమైన అంటుకునే టేపులను తొలగించండి", "పేపర్ ఫైబర్ దెబ్బతినకుండా పొడిగా ఉంచండి"]},
        "battery": {"class": "బ్యాటరీ", "impact": "ఇందులో ఉండే భారీ లోహాలు నేల మరియు నీటి పర్యావరణ వ్యవస్థలను తీవ్రంగా కలుషితం చేస్తాయి.", "disposal": "దీనిని ఖచ్చితంగా ఇ-వేస్ట్ కలెక్షన్ కేంద్రాలకు మాత్రమే పంపాలి.", "suggestions": ["పొడి కంటైనర్‌లో సురక్షితంగా వేరు చేయండి", "ఇంటి చెత్తతో కలపవద్దు", "ఇ-వేస్ట్ కియోస్క్‌లలో అందజేయండి"]},
        "biological": {"class": "జీవ వ్యర్థాలు", "impact": "ఇవి కుళ్ళిపోయినప్పుడు మిథేన్ వాయువును విడుదల చేస్తాయి. కంపోస్ట్ చేస్తే చాలా విలువైనవిగా మారుతాయి.", "disposal": "సేంద్రీయ ప్రాసెసింగ్ లేదా పెరటి కంപോస్టింగ్ కోసం ఉపయోగించండి.", "suggestions": ["ద్రవాలను ఘనపదార్థాల నుండి వేరు చేయండి", "బయోడిగ్రేడబుల్ బ్యాగులను వాడండి", "పోషకాలతో కూడిన కంపోస్ట్ కోసం उपयोगించండి"]},
        "clothes": {"class": "దుస్తులు", "impact": "సింథటిక్ ఫైబర్స్ కుళ్ళిపోవడానికి శతాబ్దాలు పడుతుంది మరియు గ్రీన్‌హౌస్ వాయువులను విడుదల చేస్తుంది.", "disposal": "టెక్స్‌టైల్ పునర్వినియోగ ప్లాట్‌ఫారమ్‌లు లేదా విరాళాల పైప్‌లైన్‌లకు పంపండి.", "suggestions": ["ప్రాసెస్ చేయడానికి ముందు完全に ఉతకండి", "ధరించగలిగే నాణ్యమైన బట్టలను వేరు చేయండి", "పాత ముక్కలను టెక్స్‌టైల్ రీజెనరేటర్లకు పంపండి"]},
        "glass": {"class": "గాజు", "impact": "నాణ్యత కోల్పోకుండా ఎన్నిసార్లయినా రీసైకిల్ చేయవచ్చు, దీనివల్ల ఉద్గారాలు తగ్గుతాయి.", "disposal": "వ్యర్థాలను శుభ్రం చేసి, రంగుల ఆధారంగా నిర్దేశిత బిన్లలో వేయండి.", "suggestions": ["ఆహార అవశేషాలను పూర్తిగా కడగాలి", "అందుబాటులో ఉంటే రంగుల ఆధారంగా వేరు చేయండి", "పగిలిన గాజును సురక్షితంగా నిర్వహించండి"]},
        "metal": {"class": "లోహం", "impact": "కొత్త ఖనిజాల వెలికితీతతో పోలిస్తే రీసైక్లింగ్ ద్వారా విపరీతమైన ఇంధన ఆదా అవుతుంది.", "disposal": "ఇతర పదార్థాలను తొలగించి నేరుగా స్క్రాప్ సేకరణ నెట్‌వర్క్‌లకు అందించండి.", "suggestions": ["క్యాన్లను పూర్తిగా కడగాలి", "ప్లాస్టిక్ రేపర్లను తొలగించండి", "మృదువైన అల్యూమినియం వస్తువులను కుదించండి"]},
        "paper": {"class": "కాగితం", "impact": "కాగితపు ఫైబర్‌లను బహుళ సార్లు రీ-పల్ప్ చేయవచ్చు, ఇది గణనీయమైన నీటిని ఆదా చేస్తుంది.", "disposal": "పారవేయడానికి పొడి కాగితపు సేకరణ బిన్లను వాడండి. నూనె మరకలు లేకుండా చూసుకోండి.", "suggestions": ["ద్రవాలు లేదా రసాయనాలు తగలకుండా చూసుకోండి", "నూనె మరకల కాగితాలను వేరు చేయండి", "సున్నితమైన పత్రాలను ముక్కలు చేయండి"]},
        "plastic": {"class": "ప్లాస్టిక్", "impact": "ఇది మైక్రోప్లాస్టిక్‌లుగా మారి జల మరియు భూ చరాల జీవన చక్రాన్ని విషపూరితం చేస్తుంది.", "disposal": "స్థానిక రెసిన్ కోడ్‌లను తనిఖీ చేసి, పాలిమర్ రీసైకిల్ సౌకర్యాలలో వేయండి.", "suggestions": ["సీసాలను నలిపి పరిమాణాన్ని తగ్గించండి", "మిగిలి ఉన్న ద్రవాలను కడగాలి", "ప్లాస్టిక్ ఫిల్మ్‌లను గట్టి నిర్మాణాల నుండి వేరు చేయండి"]},
        "shoes": {"class": "షూస్", "impact": "రబ్బరు, తోలు మరియు పాలిమర్‌ల మిశ్రమం కావడం వల్ల ఇవి కుళ్ళిపోవడానికి చాలా కాలం పడుతుంది.", "disposal": "పనిచేసే పాదరక్షలను దానం చేయండి లేదా ప్రత్యేక అథ్లెటిక్ గ్రైండ్ ప్రోగ్రామ్‌లకు పంపండి.", "suggestions": ["జతలను సురక్షితంగా కలపండి", "అరికాళ్ళపై ఉన్న భారీ మట్టిని శుభ్రం చేయండి", "లోపలి ఇన్సోల్స్ పూర్తిగా తొలగించండి"]},
        "trash": {"class": "చెత్త", "impact": "ఇది నేరుగా ల్యాండ్‌ఫిల్‌కు లేదా ఇంధన దహన ప్లాంట్‌లకు వెళుతుంది.", "disposal": "ప్రామాణిక అవశేషాల నిర్వహణ సేకరణ పైప్‌లైన్లలో సురక్షితంగా సీల్ చేసి వేయండి.", "suggestions": ["పొరపాటున వేరే వస్తువులు పడకుండా తనిఖీ చేయండి", "క్రిమికీటకాలు చేరకుండా బ్యాగులను సీల్ చేయండి", "పారవేయడానికి ముందు వాల్యూమ్‌ను కుదించండి"]}
    },
    "தமிழ் (Tamil)": {
        "cardboard": {"class": "அட்டைப்பெட்டி", "impact": "மறுசுழற்சி செய்வதால் மரக்காடுகள் பாதுகாக்கப்படுகின்றன மற்றும் குப்பைக்கிடங்கின் அளவு குறைகிறது.", "disposal": "நன்கு தட்டையாக்கி, திரவ பாதிப்புகளிலிருந்து பாதுகாத்து, ஃபைபர் தொட்டிகளில் அடுக்கவும்.", "suggestions": ["பெட்டிகளை முழுமையாக தட்டையாக்கவும்", "அதிகப்படியான ஒட்டும் டேப்புகளை அகற்றவும்", "காகித நார்களைப் பாதுகாக்க உலர வைக்கவும்"]},
        "battery": {"class": "மின்கலன்", "impact": "மண்ணிலும் நீரிலும் கடுமையான நச்சுத்தன்மையை ஏற்படுத்தக்கூடிய கன உலோகங்களைக் கொண்டுள்ளது.", "disposal": "ஆபத்தான மின்-கழிவு சேகரிப்பு மையங்களுக்கு மட்டுமே அனுப்பப்பட வேண்டும்.", "suggestions": ["உலர்ந்த கொள்கலனில் নিরাপதாக பிரிக்கவும்", "வீட்டுக் குப்பைகளுடன் கலக்க வேண்டாம்", "மின்-கழிவு மையங்களில் ஒப்படைக்கவும்"]},
        "biological": {"class": "உயிரினக் கழிவுகள்", "impact": "குப்பைக் கிடங்குகளில் மீத்தேன் வாயுவை உருவாக்குகிறது. உரமாக மாற்றினால் அதிக மதிப்புடையது.", "disposal": "இயற்கை உரம் தயாரிப்பிற்கு அல்லது வீட்டுத் தோட்ட உரமாகப் பயன்படுத்தவும்.", "suggestions": ["திரவங்களை திடப்பொருட்களிலிருந்து பிரிக்கவும்", "மட்கும் குப்பைப்பைகளை பயன்படுத்தவும்", "ஊட்டச்சத்து நிறைந்த உரமாக மாற்றவும்"]},
        "clothes": {"class": "துணிகள்", "impact": "செயற்கை நார்கள் மட்குவதற்கு பல நூற்றாண்டுகள் ஆகும், மேலும் இது பசுமை இல்ல வாயுக்களை வெளியிடுகிறது.", "disposal": "ஜவுளி மறுசுழற்சி மையங்கள் அல்லது தொண்டு நிறுவனங்களுக்கு வழங்கவும்.", "suggestions": ["செயலாக்கத்திற்கு முன் நன்கு துவைக்கவும்", "அணியக்கூடிய நல்ல துணிகளை பிரிக்கவும்", "பழைய துணிகளை ஜவுளி மறுசுழற்சிக்கு அனுப்பவும்"]},
        "glass": {"class": "கண்ணாடி", "impact": "தர இழப்பின்றி எண்ணற்ற முறை மறுசுழற்சி செய்யப்படலாம், இதனால் உற்பத்தி உமிழ்வு குறைகிறது.", "disposal": "எச்சங்களை கழுவி சுத்தம் செய்து, நிற வாரியாக பிரிக்கப்பட்ட தொட்டிகளில் போடவும்.", "suggestions": ["உணவு எச்சங்களை நன்கு கழுவவும்", "நிறத்தின் அடிப்படையில் வரிசைப்படுத்தவும்", "உடைந்த கண்ணாடியை பாதுகாப்பாக கையாளவும்"]},
        "metal": {"class": "உலோகம்", "impact": "புதிய தாதுக்களை எடுப்பதை விட மறுசுழற்சி மூலம் மிக அதிக ஆற்றல் சேமிக்கப்படுகிறது.", "disposal": "இதர பொருட்களை நீக்கிவிட்டு நேரடியாக ஸ்க್ರಾப் சேகரிப்பு மையங்களுக்கு அனுப்பவும்.", "suggestions": ["டின்களை நன்கு கழுவி சுத்தம் செய்யவும்", "பிளாஸ்டிக் மூடிகளை அகற்றவும்", "மென்மையான அலுமினிய பொருட்களை நசுக்கவும்"]},
        "paper": {"class": "காகிதம்", "impact": "காகித நார்களை பலமுறை கூழாக்கலாம், ಇದು கணிசமான அளவு தண்ணீரை சேமிக்கிறது.", "disposal": "உலர்ந்த காகித சேகரிப்பு தொட்டிகளில் போடவும். எண்ணெய் பசை இல்லாமல் பார்த்துக் கொள்ளவும்.", "suggestions": ["ஈரப்பதம் அல்லது இரசாயன தொடர்பு இல்லாமல் பார்த்துக் கொள்ளவும்", "எண்ணெய் படிந்த காகிதங்களை பிரிக்கவும்", "முக்கிய ஆவணங்களை நறுக்கி அழிக்கவும்"]},
        "plastic": {"class": "நெகிழி", "impact": "கடல் மற்றும் நிலப்பரப்பு உயிரினங்களை நச்சுப்படுத்தும் நுண்-பிளாஸ்டிக்குகளாக உடைகிறது.", "disposal": "உள்ளூர் பிளாஸ்டிக் குறியீடுகளை சரிபார்த்து மறுசுழற்சி மையங்களில் போடவும்.", "suggestions": ["பாட்டில்களை நசுக்கி அளவைக் குறைக்கவும்", "மீதமுள்ள திரவங்களை கழுவவும்", "பிளாஸ்டிக் தாள்களை கடினமான அமைப்புகளிலிருந்து பிரிக்கவும்"]},
        "shoes": {"class": "காலணிகள்", "impact": "ரப்பர், தோல் மற்றும் பாலிமர்களின் கலவை என்பதால் இது மட்குவதற்கு நீண்ட காலம் எடுக்கும்.", "disposal": "பயன்படுத்தக்கூடிய காலணிகளை தானம் செய்யுங்கள் அல்லது விளையாட்டு மறுசுழற்சி மையங்களுக்கு அனுப்பவும்.", "suggestions": ["ஜோடிகளை பாதுகாப்பாக ஒன்றாக கட்டவும்", "அடிப்பகுதியில் உள்ள மண்ணை சுத்தம் செய்யவும்", "உள் உள்ளமைப்புகளை முழுமையாக அகற்றவும்"]},
        "trash": {"class": "பொதுக் குப்பை", "impact": "இதன் இறுதி இலக்கு நீண்ட கால நிலப்பரப்பு புதைப்பு அல்லது எரிப்பு ஆலைகள் ஆகும்.", "disposal": "நிலையான கழிவு மேலாண்மை சேகரிப்பு குழாய்களில் பாதுகாப்பாக சீல் வைத்து போடவும்.", "suggestions": ["தவறான பொருட்கள் ஏதேனும் உள்ளதா என சரிபார்க்கவும்", "பூச்சிகள் வராமல் தடுக்க பைகளை நன்கு சீல் செய்யவும்", "போடுவதற்கு முன் அளவை சுருக்கவும்"]}
    },
    "മലയാളം (Malayalam)": {
        "cardboard": {"class": "കാർഡ്ബോർഡ്", "impact": "പുനരുപയോഗം വനങ്ങളെ സംരക്ഷിക്കുകയും ലാൻഡ്ഫിൽ മാലിന്യങ്ങൾ കുറയ്ക്കുകയും ചെയ്യുന്നു.", "disposal": "പൂർണ്ണമായും പരത്തി, ഈർപ്പത്തിൽ നിന്ന് സംരക്ഷിച്ച് ഫൈബർ ബിന്നുകളിൽ സൂക്ഷിക്കുക.", "suggestions": ["പെട്ടികൾ പൂർണ്ണമായും പരത്തുക", "അമിതമായ പശ ടേപ്പുകൾ മാറ്റുക", "പേപ്പർ ഫൈബറുകൾ കേടുവരാതെ ഉണക്കി സൂക്ഷിക്കുക"]},
        "battery": {"class": "ബാറ്ററി", "impact": "മണ്ണിലും ജലത്തിലും കടുത്ത വിഷാംശം കലർത്താൻ ശേഷിയുള്ള കനത്ത ലോഹങ്ങൾ അടങ്ങിയിരിക്കുന്നു.", "disposal": "അപകടകരമായ ഇ-മാലിന്യ ശേഖരണ കേന്ദ്രങ്ങളിലേക്ക് മാത്രം അയക്കുക.", "suggestions": ["ഉണങ്ങിയ പാത്രത്തിൽ സുരക്ഷിതമായി മാറ്റുക", "വീട്ടുമാലിന്യങ്ങളുമായി കലർത്തരുത്", "ഇ-മാലിന്യ കിയോസ്കുകളിൽ ഏൽപ്പിക്കുക"]},
        "biological": {"class": "ജൈവമാലിന്യം", "impact": "ലാൻഡ്ഫില്ലുകളിൽ കിടന്ന് മീഥെയ്ൻ വാതകം ഉത്പാദിപ്പിക്കുന്നു. കമ്പോസ്റ്റ് ചെയ്താൽ വളരെ മൂല്യവത്താണ്.", "disposal": "ജൈവ പ്രോസസിംഗിനോ കമ്പോസ്റ്റിംഗിനോ ആയി ഉപയോഗിക്കുക.", "suggestions": ["ദ്രാവകങ്ങൾ ഖരമാലിന്യങ്ങളിൽ നിന്ന് മാറ്റുക", "ബയോഡീഗ്രേഡബിൾ ബാഗുകൾ ഉപയോഗിക്കുക", "പോഷകസമൃദ്ധമായ കമ്പോസ്റ്റിനായി ഉപയോഗിക്കുക"]},
        "clothes": {"class": "വസ്ത്രങ്ങൾ", "impact": "സിന്തറ്റിക് നാരുകൾ നശിക്കാൻ നൂറ്റാണ്ടുകളെടുക്കും, ഒപ്പം ഹരിതഗൃഹ വാതകങ്ങൾ പുറത്തുവിടുകയും ചെയ്യും.", "disposal": "ടെക്സ്റ്റൈൽ പുനരുപയോഗ പ്ലാറ്റ്‌ഫോമുകൾക്കോ ​​സംഭാവനകൾക്കോ നൽകുക.", "suggestions": ["അലക്കിയ ശേഷം മാത്രം പുനരുപയോഗത്തിന് നൽകുക", "ഉപയോഗപ്രദമായ നല്ല വസ്ത്രങ്ങൾ മാറ്റിവെക്കുക", "ബാക്കി ഭാഗങ്ങൾ ടെക്സ്റ്റൈൽ റീജനറേറ്ററുകളിലേക്ക് അയക്കുക"]},
        "glass": {"class": "കണ്ണാടി", "impact": "ഗുണമേന്മ നഷ്ടപ്പെടാതെ എത്ര തവണ വേണമെങ്കിലും പുനരുപയോഗിക്കാം, ഇത് ഉൽപ്പാദന മലിനീകരണം കുറയ്ക്കുന്നു.", "disposal": "അവശിഷ്ടങ്ങൾ കഴുകി വൃത്തിയാക്കി നിറം തിരിച്ചുള്ള ബിന്നുകളിൽ നിക്ഷേപിക്കുക.", "suggestions": ["ഭക്ഷണ അവശിഷ്ടങ്ങൾ പൂർണ്ണമായും കഴുകുക", "നിറത്തിന്റെ അടിസ്ഥാനത്തിൽ തരംതിരിക്കുക", "പൊട്ടിയ ഗ്ലാസ് സുരക്ഷിതമായി കൈകാര്യം ചെയ്യുക"]},
        "metal": {"class": "ലോഹം", "impact": "പുതിയ ലോഹങ്ങൾ ഖനനം ചെയ്യുന്നതിനേക്കാൾ പുനരുപയോഗം വഴി വലിയ തോതിൽ ഊർജ്ജം ലാഭിക്കാം.", "disposal": "മറ്റ് വസ്തുക്കൾ മാറ്റി നേരിട്ട് സ്ക്രാപ്പ് ശേഖരണ ശൃംഖലകളിൽ എത്തിക്കുക.", "suggestions": ["കാനുകൾ കഴുകി വൃത്തിയാക്കുക", "പ്ലാസ്റ്റിക് റേപ്പറുകൾ മാറ്റുക", "അലുമിനിയം വസ്തുക്കൾ അമർത്തി ചെറുതാക്കുക"]},
        "paper": {"class": "പേപ്പർ", "impact": "പേപ്പർ നാരുകൾ പലതവണ പുനരുപയോഗിക്കാം, ഇത് വലിയ തോതിൽ ജലം ലാഭിക്കാൻ സഹായിക്കുന്നു.", "disposal": "ഉണങ്ങിയ പേപ്പർ ശേഖരണ ബിന്നുകളിൽ നിക്ഷേപിക്കുക. എണ്ണമയം ഒഴിവാക്കുക.", "suggestions": ["ദ്രാവകങ്ങളോ രാസവസ്തുക്കളോ തട്ടാതെ സൂക്ഷിക്കുക", "എണ്ണമയമുള്ള പേപ്പറുകൾ വേർതിരിക്കുക", "രഹസ്യരേഖകൾ കീറി നശിപ്പിക്കുക"]},
        "plastic": {"class": "പ്ലാസ്റ്റിക്", "impact": "കടൽ-കര ജീവികളെ നശിപ്പിക്കുന്ന മൈക്രോപ്ലാസ്റ്റിക്കുകളായി ഇവ മാറുന്നു.", "disposal": "പ്ലാസ്റ്റിക് കോഡുകൾ പരിശോധിച്ച് റീസൈക്ലിംഗ് സെന്ററുകളിൽ നിക്ഷേപിക്കുക.", "suggestions": ["കുപ്പികൾ അമർത്തി വലിപ്പം കുറയ്ക്കുക", "ബാക്കിയുള്ള ദ്രാവകങ്ങൾ കഴുകിക്കളയുക", "പ്ലാസ്റ്റിക് ഫിലിമുകൾ കട്ടിപ്പുള്ള ഭാഗങ്ങളിൽ നിന്ന് മാറ്റുക"]},
        "shoes": {"class": "ഷൂസുകൾ", "impact": "റബ്ബർ, ലെതർ, പോളിമർ എന്നിവയുടെ മിശ്രിതമായതിനാൽ ഇവ നശിക്കാൻ വലിയ സമയമെടുക്കും.", "disposal": "ഉപയോഗപ്രദമായ പാദരക്ഷകൾ സംഭാവന ചെയ്യുക അല്ലെങ്കിൽ റീസൈക്ലിംഗ് കേന്ദ്രങ്ങളിലേക്ക് നൽകുക.", "suggestions": ["ജോഡികൾ സുരക്ഷിതമായി ഒന്നിച്ച് കെട്ടുക", "അടിഭാഗത്തെ മണ്ണ് കഴുകി വൃത്തിയാക്കുക", "അകത്തെ ഇൻസോളുകൾ പൂർണ്ണമായും മാറ്റുക"]},
        "trash": {"class": "മാലിന്യം", "impact": "ഇവ ലാൻഡ്ഫില്ലുകളിലേക്കോ വലിയ സംസ്കരണ പ്ലാന്റുകളിലേക്കോ മാത്രമാണ് പോകുന്നത്.", "disposal": "മാലിന്യ ബാഗുകളിൽ സുരക്ഷിതമായി അടച്ച് സാധാരണ കളക്ഷൻ പൈപ്പ് ലൈനുകളിൽ നിക്ഷേപിക്കുക.", "suggestions": ["മാറിപ്പോയ വസ്തുക്കൾ ഇല്ലെന്ന് ഉറപ്പാക്കുക", "കീടങ്ങൾ വരാതിരിക്കാൻ ബാഗുകൾ നന്നായി അടയ്ക്കുക", "നിക്ഷേപിക്കുന്നതിന് മുൻപ് വലിപ്പം കുറയ്ക്കുക"]}
    },
    "ಕನ್ನಡ (Kannada)": {
        "cardboard": {"class": "ಕಾರ್ಡ್‌ಬೋರ್ಡ್", "impact": "ಮರುಬಳಕೆಯಿಂದ ಅರಣ್ಯ ನಾಶ ತಪ್ಪುತ್ತದೆ ಮತ್ತು ಕಸದ ರಾಶಿಯ ಪ್ರಮಾಣ ಕಡಿಮೆಯಾಗುತ್ತದೆ.", "disposal": "ಸಂಪೂರ್ಣವಾಗಿ ಚಪ್ಪಟೆ ಮಾಡಿ, ತೇವದಿಂದ ರಕ್ಷಿಸಿ ಫೈಬರ್ ಬಿನ್‌ಗಳಲ್ಲಿ ಜೋಡಿಸಿ.", "suggestions": ["ಪೆಟ್ಟಿಗೆಗಳನ್ನು ಸಂಪೂರ್ಣವಾಗಿ ಚಪ್ಪಟೆ ಮಾಡಿ", "ಅತಿಯಾದ ಅಂಟು ಟೇಪ್‌ಗಳನ್ನು ತೆಗೆದುಹಾಕಿ", "ಪೇಪರ್ ಫೈಬರ್ ರಕ್ಷಿಸಲು ಒಣದಾಗಿಡಿ"]},
        "battery": {"class": "ಬ್ಯಾಟರಿ", "impact": "ಮಣ್ಣು ಮತ್ತು ನೀರಿನ ಪರಿಸರ ವ್ಯವಸ್ಥೆಗೆ ತೀವ್ರ ನಂಜು ಉಂಟುಮಾಡುವ ಭಾರಿ ಲೋಹಗಳನ್ನು ಹೊಂದಿರುತ್ತದೆ.", "disposal": "ಇದನ್ನು ಕೇವಲ ಇ-ತ್ಯಾಜ್ಯ ಸಂಗ್ರಹಣಾ ಕೇಂದ್ರಗಳಿಗೆ ಮಾತ್ರ ಕಳುಹಿಸಬೇಕು.", "suggestions": ["ಒಣ ಕಂಟೇನರ್‌ನಲ್ಲಿ ಸುರಕ್ಷಿತವಾಗಿ ಬೇರ್ಪಡಿಸಿ", "ಮನೆಯ ಕಸದೊಂದಿಗೆ ಬೆರೆಸಬೇಡಿ", "ಇ-ತ್ಯಾಜ್ಯ ಕೇಂದ್ರಗಳಲ್ಲಿ ಹಸ್ತಾಂತರಿಸಿ"]},
        "biological": {"class": "ಜೈವಿಕ ತ್ಯಾಜ್ಯ", "impact": "ಇದು ಕೊಳೆಯುವಾಗ ಮಿಥೇನ್ ಅನಿಲವನ್ನು ಬಿಡುగಡೆ ಮಾಡುತ್ತದೆ. ಗೊಬ್ಬರ ಮಾಡಿದರೆ ತುಂಬಾ ಉಪಯುಕ್ತ.", "disposal": "ಸಾವಯವ ಸಂಸ್ಕರಣೆ ಅಥವಾ ಮನೆಯ ಗೊಬ್ಬರ ತಯಾರಿಕೆಗೆ ಬಳಸಿ.", "suggestions": ["ದ್ರವಗಳನ್ನು ಘನವಸ್ತುಗಳಿಂದ ಬೇರ್ಪಡಿಸಿ", "ಬಯೋಡಿಗ್ರೇಡಬಲ್ ಬ್ಯಾಗ್‌ಗಳನ್ನು ಬಳಸಿ", "ಪೋಷಕಾಂಶ ಭರಿತ ಗೊಬ್ಬರಕ್ಕಾಗಿ ಬಳಸಿ"]},
        "clothes": {"class": "ಬಟ್ಟೆಗಳು", "impact": "ಸಿಂಥೆಟಿಕ್ ನಾರುಗಳು ಕೊಳೆಯಲು ಶತಮಾನಗಳು ಬೇಕಾಗುತ್ತವೆ ಮತ್ತು ಹಸಿರುಮನೆ ಅನಿಲಗಳನ್ನು ಬಿಡುగಡೆ ಮಾಡುತ್ತವೆ.", "disposal": "ಜವಳಿ ಮರುಬಳಕೆ中心ಗಳು ಅಥವಾ ದಾನ ಸಂಸ್ಥೆಗಳಿಗೆ ನೀಡಿ.", "suggestions": ["ಸಂಸ್ಕರಣೆಯ ಮೊದಲು ಸಂಪೂರ್ಣವಾಗಿ ತೊಳೆಯಿರಿ", "ಧರಿಸಬಹುದಾದ ಉತ್ತಮ ಬಟ್ಟೆಗಳನ್ನು ಬೇರ್ಪಡಿಸಿ", "ಹಳೆಯ ಚೂರುಗಳನ್ನು ಜವಳಿ ಮರುಬಳಕೆಗೆ ಕಳುಹಿಸಿ"]},
        "glass": {"class": "ಗಾಜು", "impact": "ಗುಣಮಟ್ಟ ಕಳೆದುಕೊಳ್ಳದೆ ಎಷ್ಟು ಬಾರಿಯಾದರೂ ಮರುಬಳಕೆ ಮಾಡಬಹುದು, ಇದರಿಂದ ಮಾಲಿನ್ಯ ಕಡಿಮೆಯಾಗುತ್ತದೆ.", "disposal": "ತ್ಯಾಜ್ಯವನ್ನು ತೊಳೆದು ಸ್ವಚ್ಛಗೊಳಿಸಿ, ಬಣ್ಣದ ಆಧಾರದ ಬಿನ್‌ಗಳಲ್ಲಿ ಹಾಕಿ.", "suggestions": ["ಆಹಾರದ ಅವಶೇಷಗಳನ್ನು ಸಂಪೂರ್ಣವಾಗಿ ತೊಳೆಯಿರಿ", "ಬಣ್ಣದ ಪ್ರೊಫೈಲ್ ಆಧಾರದ ಮೇಲೆ ವಿಂಗಡಿಸಿ", "ಒಡೆದ ಗಾಜನ್ನು ಸುರಕ್ಷಿತವಾಗಿ ನಿರ್ವಹಿಸಿ"]},
        "metal": {"class": "ಲೋಹ", "impact": "ಹೊಸ ಅದಿರು ತೆಗೆಯುವುದಕ್ಕಿಂತ ಮರುಬಳಕೆಯಿಂದ ಹೆಚ್ಚಿನ ಇಂಧನ ಉಳಿತಾಯವಾಗುತ್ತದೆ.", "disposal": "ಇತರ ವಸ್ತುಗಳನ್ನು ತೆಗೆದುಹಾಕಿ ನೇರವಾಗಿ ಸ್ಕ್ರ್ಯಾಪ್ ಸಂಗ್ರಹಣಾ ಕೇಂದ್ರಗಳಿಗೆ ನೀಡಿ.", "suggestions": ["ಟನ್‌ಗಳನ್ನು ಸ್ವಚ್ಛವಾಗಿ ತೊಳೆಯಿರಿ", "ಪ್ಲಾಸ್ಟಿಕ್ ಹೊದಿಕೆಗಳನ್ನು ತೆಗೆದುಹಾಕಿ", "ಮೃದುವಾದ ಅಲ್ಯೂಮಿನಿಯಂ ವಸ್ತುಗಳನ್ನು ಕುಗ್ಗಿಸಿ"]},
        "paper": {"class": "ಕಾಗದ", "impact": "ಕಾಗದದ ನಾರುಗಳನ್ನು ಹಲವು ಬಾರಿ ಮರುಬಳಕೆ ಮಾಡಬಹುದು, ಇದು ಗಣನೀಯವಾಗಿ ನೀರನ್ನು ಉಳಿಸುತ್ತದೆ.", "disposal": "ಒಣ ಕಾಗದ ಸಂಗ್ರಹಣಾ ಬಿನ್‌ಗಳಲ್ಲಿ ಹಾಕಿ. ಎಣ್ಣೆ ಜಿಡ್ಡು ಇಲ್ಲದಂತೆ ನೋಡಿಕೊಳ್ಳಿ.", "suggestions": ["ತೇವ ಅಥವಾ ರಾಸಾಯನಿಕ ಸಂಪರ್ಕವಿಲ್ಲದಂತೆ ನೋಡಿಕೊಳ್ಳಿ", "ಎಣ್ಣೆ ಜಿಡ್ಡಿನ ಕಾಗದಗಳನ್ನು ಬೇರ್ಪಡಿಸಿ", "ಸೂಕ್ಷ್ಮ ದಾಖಲೆಗಳನ್ನು ಕತ್ತರಿಸಿ ನಾಶಮಾಡಿ"]},
        "plastic": {"class": "ಪ್ಲಾಸ್ಟಿಕ್", "impact": "ಇದು ಮೈಕ್ರೋಪ್ಲಾಸ್ಟಿಕ್ ಆಗಿ ಬದಲಾಗಿ ಜಲ ಮತ್ತು ಭೂಮಿಯ ಜೀವಿಗಳ ಜೀವನ ಚಕ್ರವನ್ನು ವಿಷಗೊಳಿಸುತ್ತದೆ.", "disposal": "ಸ್ಥಳೀಯ ಪ್ಲಾಸ್ಟಿಕ್ ಕೋಡ್‌ಗಳನ್ನು ಪರಿಶೀಲಿಸಿ ಮರುಬಳಕೆ ಕೇಂದ್ರಗಳಿಗೆ ಹಾಕಿ.", "suggestions": ["ಬಾಟಲಿಗಳನ್ನು ಜಜ್ಜಿ ಗಾತ್ರವನ್ನು ಕಡಿಮೆ ಮಾಡಿ", "ಉಳಿದಿರುವ ದ್ರವಗಳನ್ನು ತೊಳೆದು ಸ್ವಚ್ಛಗೊಳಿಸಿ", "ಪ್ಲಾಸ್ಟಿಕ್ ಫಿಲ್ಮ್‌ಗಳನ್ನು ಗಟ್ಟಿಯಾದ भागಗಳಿಂದ ಬೇರ್ಪಡಿಸಿ"]},
        "shoes": {"class": "ಪಾದರಕ್ಷೆಗಳು", "impact": "ರಬ್ಬರ್, ಚರ್ಮ ಮತ್ತು ಪಾಲಿಮರ್‌ಗಳ ಮಿಶ್ರಣವಾಗಿರುವುದರಿಂದ ಇವು ಕೊಳೆಯಲು ದೀರ್ಘಕಾಲ ತೆಗೆದುಕೊಳ್ಳುತ್ತದೆ.", "disposal": "ಬಳಸಬಹುದಾದ ಪಾದರಕ್ಷೆಗಳನ್ನು ದಾನ ಮಾಡಿ ಅಥವಾ ಮರುಬಳಕೆ ಕಾರ್ಯಕ್ರಮಗಳಿಗೆ ಕಳುಹಿಸಿ.", "suggestions": ["ಜೋಡಿಗಳನ್ನು ಸುರಕ್ಷಿತವಾಗಿ ಒಟ್ಟಿಗೆ ಕಟ್ಟಿ", "ಅಡಿಭಾಗದಲ್ಲಿರುವ ಮಣ್ಣನ್ನು ಸ್ವಚ್ಛಗೊಳಿಸಿ", "ಒಳಗಿನ ಇನ್ಸೋಲ್‌ಗಳನ್ನು ಸಂಪೂರ್ಣವಾಗಿ ತೆಗೆದುಹಾಕಿ"]},
        "trash": {"class": "ಸಾಮಾನ್ಯ ಕಸ", "impact": "ಇದರ ಅಂತಿಮ ಗುರಿ ದೀರ್ಘಕಾಲದ ಭೂಹೂತ ಅಥವಾ ಕಸದ ದಹನ ಸ್ಥಾವರಗಳು ಮಾತ್ರ.", "disposal": "ತ್ಯಾಜ್ಯ ನಿರ್ವಹಣಾ ಸಂಗ್ರಹಣಾ ಪೈಪ್‌ಲೈನ್‌ಗಳಲ್ಲಿ ಸುರಕ್ಷಿತವಾಗಿ ಸೀಲ್ ಮಾಡಿ ಹಾಕಿ.", "suggestions": ["ತಪ್ಪಾದ ವಸ್ತುಗಳು ಸೇರಿಲ್ಲವೆಂಬುದನ್ನು ಪರಿಶೀಲಿಸಿ", "ಕೀಟಗಳು ಬರದಂತೆ ಬ್ಯಾಗ್‌ಗಳನ್ನು ಚೆನ್ನಾಗಿ ಸೀಲ್ ಮಾಡಿ", "ಹಾಕುವ ಮುನ್ನ ಗಾತ್ರವನ್ನು ಕುಗ್ಗಿಸಿ"]}
    },
    "हिन्दी (Hindi)": {
        "cardboard": {"class": "गत्ता", "impact": "रीसाइक्लिंग से जंगलों की रक्षा होती है और लैंडफिल का कचरा कम होता है।", "disposal": "पूरी तरह से फ्लैट करें, नमी से बचाएं और फाइबर बिन में व्यवस्थित रखें।", "suggestions": ["बक्सों को पूरी तरह से फ्लैट मोड़ें", "अत्यधिक चिपचिपे टेप हटा दें", "कागज के रेशों को बचाने के लिए सूखा रखें"]},
        "battery": {"class": "बैटरी", "impact": "इसमें भारी धातुएं होती हैं जो मिट्टी और पानी को गंभीर रूप से दूषित करती हैं।", "disposal": "इसे विशेष रूप से केवल ई-कचरा संग्रह केंद्रों पर ही भेजा जाना चाहिए।", "suggestions": ["सूखे कंटेनर में सुरक्षित रूप से अलग करें", "घरेलू कचरे के साथ न मिलाएं", "ई-कचरा कियोस्क पर जमा करें"]},
        "biological": {"class": "जैविक कचरा", "impact": "लैंडफिल में मीथेन गैस पैदा करता है। खाद बनाने पर यह अत्यधिक मूल्यवान है।", "disposal": "जैविक प्रसंस्करण या घरेलू खाद बनाने के लिए उपयोग करें।", "suggestions": ["तरल पदार्थों को ठोस कचरे से अलग करें", "बायोडिग्रेडेबल बैग का उपयोग करें", "पोषक तत्वों से भरपूर खाद के लिए उपयोग करें"]},
        "clothes": {"class": "कपड़े", "impact": "सिंथेटिक फाइबर को नष्ट होने में सदियों लग जाते हैं और यह ग्रीनहाउस गैसें छोड़ता है।", "disposal": "कपड़ा पुनर्चक्रण मंचों या दान केंद्रों को भेजें।", "suggestions": ["प्रसंस्करण से पहले पूरी तरह से धो लें", "पहनने योग्य अच्छे कपड़ों को अलग करें", "पुराने कपड़ों को कपड़ा पुनर्चक्रण में भेजें"]},
        "glass": {"class": "कांच", "impact": "गुणवत्ता खोए बिना अनगिनत बार रीसायकल किया जा सकता है, जिससे प्रदूषण कम होता है।", "disposal": "अवशेषों को साफ करें और रंग के आधार पर निर्धारित डिब्बे में डालें।", "suggestions": ["खाद्य अवशेषों को पूरी तरह से धो लें", "रंग के आधार पर क्रमबद्ध करें", "टूटे हुए कांच को सुरक्षित रूप से संभालें"]},
        "metal": {"class": "धातु", "impact": "नए खनिजों को निकालने की तुलना में रीसाइक्लिंग से भारी मात्रा में ऊर्जा की बचत होती है।", "disposal": "अन्य सामग्रियों को हटाकर सीधे कबाड़ संग्रह नेटवर्क को दें।", "suggestions": ["कैन को पूरी तरह से धो लें", "प्लास्टिक रैपर हटा दें", "नरम एल्युमिनियम की वस्तुओं को संकुचित करें"]},
        "paper": {"class": "कागज", "impact": "कागज के रेशों को कई बार री-पल्प किया जा सकता है, जिससे पानी की भारी बचत होती है।", "disposal": "सूखे कागज संग्रह डिब्बे में डालें। तेल के दाग न होने दें।", "suggestions": ["नमी या रासायनिक संपर्क से दूर रखें", "तैलीय कागज को अलग करें", "संवेदनशील दस्तावेजों को नष्ट कर दें"]},
        "plastic": {"class": "प्लास्टिक", "impact": "यह माइक्रोप्लास्टिक में बदलकर समुद्री और स्थलीय जीवों के जीवन चक्र को जहरीला बनाता है।", "disposal": "स्थानीय प्लास्टिक कोड की जांच करें और रीसायकल केंद्रों में डालें।", "suggestions": ["बोतलों को कुचलकर आकार कम करें", "बचे हुए तरल पदार्थों को साफ करें", "प्लास्टिक फिल्मों को सख्‍त संरचनाओं से अलग करें"]},
        "shoes": {"class": "जूते", "impact": "रबर, चमड़े और पॉलिमर का मिश्रण होने के कारण इन्हें नष्ट होने में लंबा समय लगता है।", "disposal": "उपयोग करने योग्य जूते दान करें या पुनर्चक्रण कार्यक्रमों को भेजें।", "suggestions": ["जोड़ों को सुरक्षित रूप से एक साथ बांधें", "तलवों पर लगी मिट्टी को साफ करें", "अंदर के इनसोल को पूरी तरह से हटा दें"]},
        "trash": {"class": "सामान्य कचरा", "impact": "इसका अंतिम गंतव्य केवल दीर्घकालिक लैंडफिल या कचरा दहन संयंत्र हैं।", "disposal": "कचरा प्रबंधन संग्रह पाइपलाइनों में सुरक्षित रूप से सील करके डालें।", "suggestions": ["जांचें कि कोई गलत वस्तु तो नहीं छूटी", "कीड़ों से बचाने के लिए बैग को अच्छी तरह सील करें", "डालने से पहले आकार को संकुचित करें"]}
    }
}


# -----------------------------
# CONTROL FLOW & IMAGE PROCESSING
# -----------------------------
st.markdown(f"""
<div class="header-wrapper">
    <div class="app-title">{text['title']}</div>
    <div class="app-subtitle">{text['subtitle']}</div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("DROP_ZONE", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

computed_output = None
if uploaded_file:
    raw_image = Image.open(uploaded_file).convert("RGB")
    processed_matrix = raw_image.resize((224, 224))
    processed_matrix = np.array(processed_matrix, dtype=np.float32)
    processed_matrix = processed_matrix / 127.5 - 1.0
    processed_matrix = np.expand_dims(processed_matrix, axis=0)

    prediction_logits = model.predict(processed_matrix, verbose=0)[0]
    probabilities = prediction_logits / np.sum(prediction_logits)
    target_index = np.argmax(probabilities)
    
    detected_class = CLASSES[target_index]
    
    # 🌟 This pulls the translated sentences based on the language dropdown selection
    translated_info = WASTE_DATA_LOCALIZED[selected_lang][detected_class]
    
    # 🌟 This maps all keys correctly to match the UI container blocks at the bottom
    computed_output = {
        "class_raw": detected_class,
        "class_title": translated_info["class"],
        "impact": translated_info["impact"],
        "disposal": translated_info["disposal"],
        "suggestions": translated_info["suggestions"], 
        "raw_img": raw_image,
        "b64": img_to_base64(raw_image)
    }
    current_theme = THEMES[detected_class]

# -----------------------------
# RENDERING INTERFACE ENVIRONMENT
# -----------------------------
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');

    .stApp {{
        background: {current_theme['bg']};
        background-image:
            radial-gradient(circle at 10% 20%, rgba(255,255,255,0.08) 0%, transparent 24%),
            radial-gradient(circle at 90% 15%, rgba(255,255,255,0.06) 0%, transparent 20%),
            radial-gradient(circle at 80% 80%, rgba(255,255,255,0.05) 0%, transparent 24%),
            linear-gradient(135deg, {current_theme['bg']} 0%, rgba(255,255,255,0.02) 100%);
        background-size: 220% 220%;
        animation: themeFlow 20s ease infinite;
        font-family: 'Plus Jakarta Sans', sans-serif;
        transition: background 0.8s cubic-bezier(0.25, 1, 0.5, 1);
    }}

    header, [data-testid="stHeader"], [data-testid="stToolbar"] {{
        visibility: hidden; height: 0; display: none;
    }}

    /* Full Background Ambient Animation Flow Canvas */
    .floating-canvas {{
        position: fixed; width: 100%; height: 100%; top:0; left:0; pointer-events: none; z-index: 1; overflow: hidden;
    }}
    .floating-canvas::before {{
        content: "";
        position: absolute;
        inset: -12% -10% 20% -10%;
        background:
            radial-gradient(circle at 12% 20%, rgba(255,255,255,0.16) 0%, transparent 28%),
            radial-gradient(circle at 82% 16%, rgba(255,255,255,0.12) 0%, transparent 24%),
            radial-gradient(circle at 24% 78%, rgba(255,255,255,0.10) 0%, transparent 26%),
            radial-gradient(circle at 84% 78%, rgba(255,255,255,0.12) 0%, transparent 24%);
        filter: blur(28px);
        animation: ambientGlow 14s ease-in-out infinite alternate;
        pointer-events: none;
    }}
    .floating-canvas::after {{
        content: "";
        position: absolute;
        inset: 0;
        background-image: linear-gradient(rgba(255,255,255,0.045) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.045) 1px, transparent 1px);
        background-size: 60px 60px;
        mask-image: linear-gradient(to bottom, rgba(0,0,0,0.8), transparent 95%);
        animation: gridShift 16s linear infinite;
        opacity: 0.45;
        pointer-events: none;
    }}
    .ambient-orb {{
        position: absolute;
        border-radius: 50%;
        filter: blur(34px);
        opacity: 0.28;
        animation: orbDrift 18s ease-in-out infinite;
    }}
    .soft-wave {{
        position: absolute;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(255,255,255,0.12) 0%, rgba(255,255,255,0.03) 38%, transparent 70%);
        filter: blur(18px);
        animation: softWaveDrift 20s ease-in-out infinite;
        opacity: 0.7;
    }}
    .float-card {{
        position: absolute; 
        font-size: 54px;
        opacity: 0.18;
        filter: drop-shadow(0px 0px 12px {current_theme['accent']});
        animation: globalMatrixDrift 13s infinite ease-in-out;
    }}
    @keyframes themeFlow {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}
    @keyframes globalMatrixDrift {{
        0% {{ transform: translateY(0px) translateX(0px) rotate(0deg) scale(1); }}
        50% {{ transform: translateY(-70px) translateX(40px) rotate(200deg) scale(1.25); opacity: 0.34; }}
        100% {{ transform: translateY(0px) translateX(0px) rotate(360deg) scale(1); }}
    }}
    @keyframes ambientGlow {{
        0% {{ transform: translate3d(-2%, -1%, 0) scale(1); opacity: 0.72; }}
        50% {{ transform: translate3d(2%, 2%, 0) scale(1.08); opacity: 1; }}
        100% {{ transform: translate3d(-1%, 1%, 0) scale(0.95); opacity: 0.84; }}
    }}
    @keyframes gridShift {{
        0% {{ background-position: 0 0; }}
        100% {{ background-position: 70px 70px; }}
    }}
    @keyframes orbDrift {{
        0% {{ transform: translate3d(0, 0, 0) scale(1); }}
        50% {{ transform: translate3d(48px, -38px, 0) scale(1.16); }}
        100% {{ transform: translate3d(-26px, 30px, 0) scale(0.94); }}
    }}
    @keyframes softWaveDrift {{
        0% {{ transform: translate3d(0, 0, 0) scale(0.9); opacity: 0.35; }}
        25% {{ transform: translate3d(24px, -24px, 0) scale(1.05); opacity: 0.55; }}
        50% {{ transform: translate3d(10px, -60px, 0) scale(1.18); opacity: 0.72; }}
        75% {{ transform: translate3d(-18px, -38px, 0) scale(1.04); opacity: 0.5; }}
        100% {{ transform: translate3d(0, 0, 0) scale(0.9); opacity: 0.35; }}
    }}

    .header-wrapper {{
        text-align: center;
        margin-top: 30px;
        margin-bottom: 20px;
        z-index: 10;
        position: relative;
    }}
    .app-title {{
        font-size: 50px; font-weight: 800; letter-spacing: -1.5px;
        color: #ffffff; margin-bottom: 4px;
        text-shadow: 0 4px 20px rgba(0,0,0,0.7);
    }}
    .app-subtitle {{
        font-size: 15px; color: {current_theme['text_secondary']}; font-weight: 400;
        text-shadow: 0 2px 10px rgba(0,0,0,0.5);
    }}

    /* Master Box Container */
    .master-container {{
        max-width: 740px;
        margin: 20px auto;
        background: {current_theme['card_bg']};
        border: 2.5px solid {current_theme['accent']};
        border-radius: 28px;
        padding: 40px;
        box-shadow: 0 35px 80px {current_theme['shadow']};
        backdrop-filter: blur(40px);
        -webkit-backdrop-filter: blur(40px);
        text-align: center;
        z-index: 10;
        position: relative;
    }}

    .earth-showcase {{
        max-width: 900px;
        margin: 32px auto 18px auto;
        padding: 24px 22px 26px 22px;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 24px;
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        position: relative;
        z-index: 10;
        overflow: hidden;
    }}
    .earth-showcase::before {{
        content: "";
        position: absolute;
        inset: -30% auto auto -20%;
        width: 140%;
        height: 70px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
        transform: translateX(-100%);
        animation: sweepLine 6s linear infinite;
    }}
    .earth-caption {{
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 1.6px;
        text-transform: uppercase;
        color: {current_theme['accent']};
        text-align: center;
        margin-bottom: 12px;
    }}
    .earth-stage {{
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 290px;
    }}
    .earth-globe {{
        width: 240px;
        height: 240px;
        border-radius: 50%;
        position: relative;
        background: radial-gradient(circle at 30% 30%, #2dd4bf 0%, #14532d 35%, #0f172a 100%);
        border: 2px solid rgba(255,255,255,0.16);
        box-shadow: 0 20px 70px rgba(0,0,0,0.35);
        overflow: hidden;
        animation: earthFloat 5.5s ease-in-out infinite;
    }}
    .earth-globe::before {{
        content: "";
        position: absolute;
        inset: 0;
        border-radius: 50%;
        background: radial-gradient(circle at 20% 20%, rgba(255,255,255,0.22), transparent 30%),
                    radial-gradient(circle at 80% 30%, rgba(255,255,255,0.16), transparent 25%),
                    linear-gradient(135deg, rgba(255,255,255,0.12), transparent 70%);
        pointer-events: none;
    }}
    .earth-waste-layer {{
        position: absolute;
        inset: 0;
        border-radius: 50%;
        background:
            linear-gradient(135deg, #475569 0%, #0f172a 85%);
        opacity: 1;
        transform: scale(1);
        animation: wasteFade 7s ease-in-out infinite;
    }}
    .earth-clean-layer {{
        position: absolute;
        inset: 0;
        border-radius: 50%;
        background:
            radial-gradient(circle at 24% 24%, rgba(255,255,255,0.22) 0 8%, transparent 9%),
            radial-gradient(circle at 70% 30%, rgba(255,255,255,0.16) 0 8%, transparent 9%),
            linear-gradient(135deg, #34d399 0%, #166534 70%);
        opacity: 0;
        transform: scale(0.94);
        animation: cleanRise 7s ease-in-out infinite;
    }}
    .earth-biomass {{
        position: absolute;
        width: 68px;
        height: 68px;
        border-radius: 18px;
        background: linear-gradient(135deg, #64748b 0%, #334155 100%);
        box-shadow: inset 0 0 16px rgba(255,255,255,0.16);
        opacity: 0.95;
        animation: wasteDrift 7s ease-in-out infinite;
    }}
    .earth-biomass.one {{ top: 24%; left: 18%; }}
    .earth-biomass.two {{ top: 58%; left: 28%; width: 54px; height: 54px; }}
    .earth-biomass.three {{ top: 28%; left: 64%; width: 58px; height: 58px; }}
    .earth-biomass.four {{ top: 66%; left: 64%; width: 48px; height: 48px; }}
    .earth-leaf {{
        position: absolute;
        width: 54px;
        height: 54px;
        border-radius: 60% 0 60% 0;
        background: linear-gradient(135deg, #86efac 0%, #16a34a 100%);
        transform: rotate(45deg);
        opacity: 0;
        animation: leafBloom 7s ease-in-out infinite;
    }}
    .earth-leaf.one {{ top: 20%; left: 28%; }}
    .earth-leaf.two {{ top: 62%; left: 56%; }}
    .earth-leaf.three {{ top: 34%; left: 72%; }}
    .earth-ring {{
        position: absolute;
        inset: -18px;
        border: 1px solid rgba(255,255,255,0.18);
        border-radius: 50%;
        transform: rotate(-12deg);
        animation: ringSpin 8s linear infinite;
    }}
    @keyframes wasteFade {{
        0%, 45% {{ opacity: 1; transform: scale(1); }}
        60%, 100% {{ opacity: 0; transform: scale(0.94); }}
    }}
    @keyframes cleanRise {{
        0%, 45% {{ opacity: 0; transform: scale(0.94); }}
        60%, 100% {{ opacity: 1; transform: scale(1); }}
    }}
    @keyframes wasteDrift {{
        0%, 50% {{ transform: translate3d(0,0,0) rotate(0deg); }}
        60%, 100% {{ transform: translate3d(8px,-12px,0) rotate(8deg); }}
    }}
    @keyframes leafBloom {{
        0%, 45% {{ opacity: 0; transform: rotate(45deg) scale(0.7); }}
        55%, 100% {{ opacity: 0.95; transform: rotate(45deg) scale(1); }}
    }}
    @keyframes earthFloat {{
        0%, 100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-10px); }}
    }}
    @keyframes ringSpin {{
        0% {{ transform: rotate(-12deg) scale(0.98); }}
        50% {{ transform: rotate(148deg) scale(1.02); }}
        100% {{ transform: rotate(360deg) scale(0.98); }}
    }}
    @keyframes sweepLine {{
        0% {{ transform: translateX(-120%); }}
        100% {{ transform: translateX(120%); }}
    }}

    /* Modified Image Presentation Style to force 100% full box scaling */
    .display-image-render {{
        width: 100%;
        max-height: 380px;
        border-radius: 20px;
        border: 3px solid #ffffff;
        box-shadow: 0 12px 30px rgba(0,0,0,0.5);
        margin: 5px auto 25px auto;
        display: block;
        object-fit: cover;
    }}

    .verdict-badge {{
        background: {current_theme['accent_light']};
        color: {current_theme['accent']};
        border: 2px solid {current_theme['accent']};
        padding: 10px 36px; border-radius: 50px; display: inline-block;
        font-weight: 800; font-size: 24px; text-transform: uppercase;
        letter-spacing: 2px; margin-bottom: 25px;
        text-shadow: 0 0 15px rgba(0,0,0,0.5);
        box-shadow: 0 0 25px {current_theme['accent_light']};
    }}

    /* SINGLE UNIFIED OUTCOMES CONTAINER BOX */
    .single-outcome-box {{
        margin-top: 25px;
        padding: 30px;
        background: rgba(0, 0, 0, 0.5);
        border-radius: 20px;
        border: 2px solid {current_theme['accent']};
        text-align: left;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.6);
    }}

    .section-block {{
        margin-bottom: 24px;
    }}
    .section-block:last-child {{
        margin-bottom: 0;
    }}

    .row-title {{
        font-size: 14px; font-weight: 800; text-transform: uppercase;
        letter-spacing: 1.2px; color: {current_theme['accent']}; margin-bottom: 8px;
    }}
    .row-desc {{
        font-size: 15px; line-height: 1.6; color: {current_theme['text_primary']};
    }}

    .step-number-label {{
        color: {current_theme['accent']};
        font-weight: 800;
        font-size: 16px;
        margin-top: 12px;
        margin-bottom: 2px;
    }}
    .step-text-content {{
        font-size: 15px;
        color: {current_theme['text_primary']};
        margin-bottom: 6px;
    }}

    [data-testid="stFileUploaderDropzone"] {{
        background: rgba(255,255,255,0.03) !important;
        border: 2px dashed rgba(255,255,255,0.15) !important;
        border-radius: 16px !important;
    }}
    div[data-testid="stFileUploader"] {{
        max-width: 740px; margin: 0 auto;
    }}
    
    div[data-testid="stSelectbox"] {{
        max-width: 300px !important;
        margin: 0 auto !important;
    }}
    div[data-testid="stSelectbox"] > div {{
        border-radius: 12px !important;
    }}
    

    /* Enhanced Particle Behavior: Floating + Weaving + Scaling */
    .eco-dust-particle {{
        position: absolute;
        background: radial-gradient(circle, rgba(255,255,255,0.8) 0%, rgba(255,255,255,0) 70%);
        border-radius: 50%;
        pointer-events: none;
        /* Adds an glow halo that works with any background color */
        box-shadow: 0 0 14px rgba(255, 255, 255, 0.6);
        animation: quantumSwarmDrift 18s infinite ease-in-out;
    }}

    @keyframes gridMovement {{
        0% {{ background-position: 0 0; }}
        100% {{ background-position: 40px 80px; }}
    }}

    /* 🌟 NEW HACKATHON-TIER ANIMATION MATH: Weaves left/right while scaling up and down */
    @keyframes quantumSwarmDrift {{
        0% {{ 
            transform: translateY(105vh) translateX(0px) scale(0.3); 
            opacity: 0; 
        }}
        15% {{ 
            opacity: 0.7; 
        }}
        50% {{ 
            transform: translateY(50vh) translateX(60px) scale(1.2); 
            opacity: 0.4;
        }}
        75% {{ 
            transform: translateY(25vh) translateX(-40px) scale(0.6); 
            opacity: 0.8;
        }}
        100% {{ 
            transform: translateY(-10vh) translateX(20px) scale(1); 
            opacity: 0; 
        }}
    }}
</style>
</style>
""", unsafe_allow_html=True)

# -----------------------------
# STAGE CANVAS ANIMATION MATRIX
# -----------------------------
st.markdown(f"""
<div class="floating-canvas">
    <div class="ambient-orb" style="top: 8%; left: 8%; width: 280px; height: 280px; background: radial-gradient(circle, {current_theme['accent_light']} 0%, transparent 78%); animation-delay: 0s;"></div>
    <div class="ambient-orb" style="top: 62%; left: 74%; width: 340px; height: 340px; background: radial-gradient(circle, rgba(255,255,255,0.13) 0%, transparent 70%); animation-delay: 5s;"></div>
    <div class="ambient-orb" style="top: 34%; left: 42%; width: 200px; height: 200px; background: radial-gradient(circle, {current_theme['accent_light']} 0%, transparent 76%); animation-duration: 20s;"></div>
    <div class="soft-wave" style="top: 10%; left: 12%; width: 260px; height: 260px; animation-delay: 0s;"></div>
    <div class="soft-wave" style="top: 24%; left: 68%; width: 300px; height: 300px; animation-delay: 4s;"></div>
    <div class="soft-wave" style="top: 56%; left: 22%; width: 240px; height: 240px; animation-delay: 8s;"></div>
    <div class="soft-wave" style="top: 70%; left: 72%; width: 280px; height: 280px; animation-delay: 12s;"></div>
    <div class="float-card" style="top: 12%; left: 6%; animation-delay: 0s;">{current_theme['icons'][0]}</div>
    <div class="float-card" style="top: 20%; left: 30%; animation-delay: 3s;">{current_theme['icons'][1]}</div>
    <div class="float-card" style="top: 14%; left: 58%; animation-delay: 1.5s;">{current_theme['icons'][2]}</div>
    <div class="float-card" style="top: 16%; left: 84%; animation-delay: 4s;">{current_theme['icons'][3]}</div>
    <div class="float-card" style="top: 48%; left: 7%; animation-delay: 6s;">{current_theme['icons'][4]}</div>
    <div class="float-card" style="top: 55%; left: 89%; animation-delay: 2.5s;">{current_theme['icons'][0]}</div>
    <div class="float-card" style="top: 76%; left: 5%; animation-delay: 5s;">{current_theme['icons'][1]}</div>
    <div class="float-card" style="top: 84%; left: 28%; animation-delay: 1s;">{current_theme['icons'][2]}</div>
    <div class="float-card" style="top: 72%; left: 62%; animation-delay: 7s;">{current_theme['icons'][3]}</div>
    <div class="float-card" style="top: 78%; left: 86%; animation-delay: 3.5s;">{current_theme['icons'][4]}</div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# CONSOLIDATED SYSTEM CONTAINER WITH INSTANT CACHED TTS VOICE
# -----------------------------
if computed_output:
    steps_html = "".join([
        f'<div class="step-number-label">{i}</div><div class="step-text-content">{step}</div>'
        for i, step in enumerate(computed_output["suggestions"], start=1)
    ])

    html_layout = f"""
<div class="master-container">
    <img class="display-image-render" src="data:image/jpeg;base64,{computed_output['b64']}" alt="Target Waste Image" />
    <div class="verdict-badge">🎯 {computed_output['class_title'].upper()}</div>
    <div class="single-outcome-box">
        <div class="section-block">
            <div class="row-title">{text['impact_title']}</div>
            <div class="row-desc">{computed_output['impact']}</div>
        </div>
        <div class="section-block">
            <div class="row-title">{text['disposal_title']}</div>
            <div class="row-desc">{computed_output['disposal']}</div>
        </div>
        <div class="section-block">
            <div class="row-title">{text['steps_title']}</div>
            {steps_html}
        </div>
    </div>
</div>
"""
    st.markdown(html_layout, unsafe_allow_html=True)

    # 🌟 PRE-GENERATE THE AUDIO STREAM TO ELIMINATE CLOUD SERVER LAG
    if "cached_audio" not in st.session_state or st.session_state.get("last_class") != computed_output["class_raw"] or st.session_state.get("last_lang") != selected_lang:
        try:
            suggestions_joined = ", ".join(computed_output["suggestions"])
            full_narration_script = (
                f"{text['audio_prefix']} {computed_output['class_title']}. "
                f"{text['audio_impact']} {computed_output['impact']} "
                f"{text['audio_disposal']} {computed_output['disposal']} "
                f"{text['audio_steps']} {suggestions_joined}."
            )
            
            tts = gTTS(text=full_narration_script, lang=text['lang_code'], slow=False)
            audio_fp = BytesIO()
            tts.write_to_fp(audio_fp)
            audio_fp.seek(0)
            
            # Save audio memory to state engine for zero-latency retrieval
            st.session_state["cached_audio"] = audio_fp.getvalue()
            st.session_state["last_class"] = computed_output["class_raw"]
            st.session_state["last_lang"] = selected_lang
        except Exception:
            st.session_state["cached_audio"] = None

    # High-performance button execution layout structure
    if st.button(text['voice_btn'], use_container_width=True):
        if st.session_state.get("cached_audio"):
            st.audio(st.session_state["cached_audio"], format="audio/mp3", autoplay=True)
        else:
            st.error("Audio stream compilation failed or timed out.")