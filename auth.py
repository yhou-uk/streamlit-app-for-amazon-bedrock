import streamlit as st
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.exceptions import (CredentialsError,
                                                          ForgotError,
                                                          LoginError,
                                                          RegisterError,
                                                          ResetError,
                                                          UpdateError)

import yaml
from yaml.loader import SafeLoader

def authenticate(app_function):
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['pre-authorized']
    )

    # Creating a login widget
    col1, col2, col3 = st.columns([1, 1, 1]) 
    with col2:
        try:
            authenticator.login()
        except LoginError as e:
            st.error(e)

    if st.session_state["authentication_status"]:
        authenticator.logout()
        st.write(f'Welcome *{st.session_state["name"]}*')
        app_function()
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')

    # Creating a new user registration widget
    with col2:
        if not st.session_state["authentication_status"]:
            try:
                (email_of_registered_user,
                 username_of_registered_user,
                 name_of_registered_user) = authenticator.register_user(pre_authorization=False)
                if email_of_registered_user:
                    st.success('User registered successfully')
            except RegisterError as e:
                st.error(e)

    # Saving config file
    with open('config.yaml', 'w', encoding='utf-8') as file:
        yaml.dump(config, file, default_flow_style=False)