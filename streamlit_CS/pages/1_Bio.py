import streamlit as st

st.title("👋 My Bio")

# ---------- TODO: Replace with your own info ----------
NAME = "Benjamin Hislop"
PROGRAM = "Bachelor of Science in Computer Science"
INTRO = (
    "I work full time, and I have an 8 year old son, so school has been my hobby lately. However, I do love hiking and skiing."
    "I'm currently a full stack developer and I lead the AI inovation team at work. I'm working on my degree so that I can further progress in my career."
)
FUN_FACTS = [
    "I love reading sci-fi novels",
    "I’m learning data visualization and machine learning",
    "I want to build productivity, and pipeline related tools to accelerate the work I do",
]
PHOTO_PATH = "your_photo.jpg"  # Put a file in repo root or set a URL

# ---------- Layout ----------
col1, col2 = st.columns([1, 2], vertical_alignment="center")

with col1:
    try:
        st.image(PHOTO_PATH, caption=NAME, use_container_width=True)
    except Exception:
        st.info("Add a photo named `your_photo.jpg` to the repo root, or change PHOTO_PATH.")
with col2:
    st.subheader(NAME)
    st.write(PROGRAM)
    st.write(INTRO)

st.markdown("### Fun facts")
for i, f in enumerate(FUN_FACTS, start=1):
    st.write(f"- {f}")

st.divider()
st.caption("Edit `pages/1_Bio.py` to customize this page.")
