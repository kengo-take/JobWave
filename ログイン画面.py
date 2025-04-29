import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import const

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

st.set_page_config(page_icon="📝")
st.markdown(const.HIDE_ST_STYLE, unsafe_allow_html=True)

# Pre-hashing all plain text passwords once
# stauth.Hasher.hash_passwords(config['credentials'])

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

try:
    authenticator.login()
except Exception as e:
    st.error(e)

if st.session_state["authentication_status"]:
    ## ログイン成功
    with st.sidebar:
        st.markdown(f'## ようこそ！ *{st.session_state["name"]}さん*')
        authenticator.logout('Logout', 'sidebar')
        st.divider()
    st.write('# ログインしました!')
elif st.session_state['authentication_status'] is False:
    st.error('ユーザー名またはパスワードが正しくありません')
elif st.session_state['authentication_status'] is None:
    st.warning('ユーザー名とパスワードを入力してください')