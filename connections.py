import streamlit as st

sql_connection_string = ("mysql+pymysql://{}:{}@{}:{}/{}".format
                         (st.secrets["database_connection"]["user"],
                          st.secrets["database_connection"]["password"],
                          st.secrets["database_connection"]["host"],
                          st.secrets["database_connection"]["port"],
                          st.secrets["database_connection"]["database_name"]))


google_sheet_credit_nails = {
    "type": st.secrets["gs_credit_nails"]["type"],
    "project_id": st.secrets["gs_credit_nails"]["project_id"],
    "private_key_id": st.secrets["gs_credit_nails"]["private_key_id"],
    "private_key": st.secrets["gs_credit_nails"]["private_key"],
    "client_email": st.secrets["gs_credit_nails"]["client_email"],
    "client_id": st.secrets["gs_credit_nails"]["client_id"],
    "auth_uri": st.secrets["gs_credit_nails"]["auth_uri"],
    "token_uri": st.secrets["gs_credit_nails"]["token_uri"],
    "auth_provider_x509_cert_url": st.secrets["gs_credit_nails"]["auth_provider_x509_cert_url"],
    "client_x509_cert_url": st.secrets["gs_credit_nails"]["client_x509_cert_url"]}