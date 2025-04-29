import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import const
import os


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

IMG_PATH = "imgs/"+str(st.session_state["name"])

if not os.path.exists(IMG_PATH):
    # ディレクトリが存在しない場合、ディレクトリを作成する
    os.makedirs(IMG_PATH)

def list_imgs():
    # IMG_PATH 内の画像ファイルを列挙
    return [
        filename
        for filename in os.listdir(IMG_PATH)
        if filename.split('.')[-1] in ['csv', 'xlsx', 'xls']
    ]

if st.session_state['authentication_status']:
    with st.sidebar:
        st.markdown(f'## ようこそ！ *{st.session_state["name"]}さん*')
        authenticator.logout('Logout', 'sidebar')
        st.divider()
    st.header('原稿のアップロード＆ダウンロード')
    file = st.file_uploader('原稿をアップロードしてください。', type=['csv', 'xlsx', 'xls'])
    if file:
        st.markdown(f'{file.name}をアップロードしました。')
        img_path = os.path.join(IMG_PATH, file.name)
        # 画像を保存する
        with open(img_path, 'wb') as f:
            f.write(file.read())

    filename = st.selectbox('ダウンロードする原稿を選択', list_imgs())
    # ダウンロード
    if os.listdir(IMG_PATH):
        st.download_button(
            'ダウンロード',
            open(os.path.join(IMG_PATH, filename), 'br'),
            filename
        )


else:
    st.warning("**ログイン画面からログインしてください**")