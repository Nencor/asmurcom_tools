import streamlit as st

def init_state(init_sessions):
    for session in init_sessions:
        if session not in st.session_state:
            st.session_state[session]=0

def calc_kamar():
    st.session_state['cur_kamar_increment'] = (st.session_state['cur_kamar_tujuan_rs'] - st.session_state['cur_kamar_rs'])/st.session_state['cur_kamar_rs']
    #calc subsidi:
    if st.session_state['cur_jumlah_hari']>0:
        st.session_state['selisih_kamar'] = st.session_state['cur_kamar_tujuan_rs']-st.session_state['cur_kamar_rs']
        st.session_state['total_billing_subsidi'] = st.session_state['selisih_kamar'] * st.session_state['cur_jumlah_hari']
    #calc prorata
    if st.session_state['cur_tagihan_rs']>0:
        st.session_state['cur_tagihan_self_paid'] = (st.session_state['cur_kamar_rs']*st.session_state['cur_tagihan_rs'])/st.session_state['cur_kamar_tujuan_rs']
        st.session_state['%_self_paid'] = int((st.session_state['cur_tagihan_self_paid']/st.session_state['cur_tagihan_rs'])*100)
        st.session_state['cur_tagihan_rs_moc_paid'] = st.session_state['cur_tagihan_rs'] - st.session_state['cur_tagihan_self_paid']
        st.session_state['%_moc_paid'] = int((st.session_state['cur_tagihan_rs_moc_paid']/st.session_state['cur_tagihan_rs'])*100)