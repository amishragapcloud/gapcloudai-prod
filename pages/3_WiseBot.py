import streamlit as st
import streamlit.components.v1 as components

# Set page config and add logo
st.set_page_config(
    page_title="GapcloudAI - Conversations with your Data",
    page_icon="🤖",
    layout="wide"
)

logo_url = "https://media.licdn.com/dms/image/C560BAQGeCieaiSruPg/company-logo_200_200/0/1630669521343/gapcloud_logo?e=2147483647&v=beta&t=jFkQ6l0vG434rsZTMywindOO_6FkdrH4FYhE0W6Xj0Q"
logo_html = f"""
<div style="position: absolute; top: 10px; right: 10px; z-index: 1000;">
    <img src="{logo_url}" alt="Logo" style="width: 100px; height: 100px;">
</div>
"""
st.markdown(logo_html, unsafe_allow_html=True)

# Title
st.markdown('<h1 class="title" style="color: Black; display: inline;">GapcloudAI</h1>'
            '<h3 style="color: Pink; display: inline;">Actions on your Data</h3>', 
            unsafe_allow_html=True)

st.markdown("      ") 

def run():
    iframe_src = "https://gapcloudtestsynapse.blob.core.windows.net/$web/index.html?sp=r&st=2024-06-23T20:55:18Z&se=2024-06-24T04:55:18Z&spr=https&sv=2022-11-02&sr=b&sig=g5o922XhkzCbFTKjPK4W7kj130zxD2Ou5Q9l5YJWk0w%3D"
    components.iframe(iframe_src, height=900, width=1200)
   # You can add height and width to the component of course.

if __name__ == "__main__":
    run()