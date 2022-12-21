import streamlit as st
import base64
from cogniflow_utils import cogniflow_request

st.set_page_config(
    page_title="Cogniflow Image Recognition",
    page_icon="https://uploads-ssl.webflow.com/60510407e7726b268293da1c/60ca08f7a2abc9c7c79c4dac_logo_ico256x256.png",
)

def _max_width_():
    max_width_str = f"max-width: 1200px;"
    st.markdown(
        f"""
    <style>
    .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )

_max_width_()

st.title('Image Recognition')
st.markdown("Powered by [Cogniflow](https://www.cogniflow.ai)")

model = st.secrets["model_url"]
api_key = st.secrets["api_key"]

if not "image/classification/predict/" in model:
    st.error("Error validating model url. Please make sure you are using an image classification model")
    st.stop()

file = st.file_uploader("Upload a picture", type=['jpg', 'png', 'jpeg'])

st.session_state['enableBtn'] = not (file is not None and model != "" and api_key != "")

click = st.button("✨ Get prediction from AI", disabled=st.session_state.enableBtn)

if click:
    if file is not None and model != "" and api_key != "":    
        image_format = file.type.replace("image/", "")
        bytes_data = file.getvalue()
        image_b64 = base64.b64encode(bytes_data).decode()

        with st.spinner("Predicting..."):
            result = cogniflow_request(model, api_key, image_b64, image_format)

        score_str = "Between 0 and 1, the higher the better"

        col1, col2 = st.columns(2, gap="large")

        col1.write("Image:")
        col1.image(file)
        col2.write("Prediction:")
        col2.metric(label="Result", value=result['result'])
        col2.metric(label="Score", value=result['confidence_score'], help=score_str)

        st.balloons()                
    else:
        st.warning("fill every input")

