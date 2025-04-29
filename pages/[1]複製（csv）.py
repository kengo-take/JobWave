import streamlit as st
import numpy as np
import pandas as pd
import const
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

st.set_page_config(page_icon="📝")
st.markdown(const.HIDE_ST_STYLE, unsafe_allow_html=True)


authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

if st.session_state["authentication_status"]:
    ## ログイン成功
    with st.sidebar:
        st.markdown(f'## ようこそ！ *{st.session_state["name"]}さん*')
        authenticator.logout('Logout', 'sidebar')
        st.divider()

    st.header('複製（csv）')

    # ファイルアップロード
    st.error('※csvファイルの場合はコチラ')
    uploaded_files = st.file_uploader('複製する原稿をアップロードしてください。', type='csv')

    # ファイルがアップロードされた場合
    if uploaded_files is not None:
        try:
            df = pd.read_csv(uploaded_files, encoding='shift-jis')
            st.success("ファイルが正常に読み込まれました。")
            st.write(df)
        except Exception as e:
            st.error(f"エラー: {e}")
    
        # 簡単なデータ処理
        processed_df = df.loc[df.index.repeat(df[df.columns[0]])]
        processed_df = processed_df.drop(df.columns[0], axis = 1)

    
        # 処理結果をCSVとしてダウンロード
        csv = processed_df.to_csv(index = False).encode('shift-jis')
        st.download_button(
            label="複製した原稿をダウンロードする",
            data=csv,
            file_name='processed_data.csv',
            mime='text/csv',
        )
else:
    st.warning("**ログイン画面からログインしてください**")