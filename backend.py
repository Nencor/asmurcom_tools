import streamlit as st

config_kamar = {
    'Opal':{
        'harga_kamar':500000,
        'jumlah_bed':2
    },
    'Emerald Blue':{
        'harga_kamar':500000,
        'jumlah_bed':2
    },
    'Emerald':{
        'harga_kamar':1000000,
        'jumlah_bed':1
    },
    'Ruby Blue':{
        'harga_kamar':500000,
        'jumlah_bed':2
    },
    'Ruby':{
        'harga_kamar':1200000,
        'jumlah_bed':1
    },
    'Diamond':{
        'harga_kamar':1500000,
        'jumlah_bed':1
    }
}

def init_state(init_sessions):
    for session in init_sessions:
        if session not in st.session_state:
            st.session_state[session]=0

def calc_kamar():
    st.session_state['max_harga_kamar'] = st.session_state['cur_kamar_rs'] if st.session_state['cur_kamar_rs'] >= config_kamar[st.session_state['cur_plan']]['harga_kamar'] else config_kamar[st.session_state['cur_plan']]['harga_kamar']
    st.session_state['cur_kamar_increment'] = (st.session_state['cur_kamar_tujuan_rs'] - st.session_state['max_harga_kamar'])/st.session_state['max_harga_kamar']
    #calc subsidi:
    if st.session_state['cur_jumlah_hari']>0:
        st.session_state['selisih_kamar'] = st.session_state['cur_kamar_tujuan_rs']-st.session_state['max_harga_kamar']
        st.session_state['total_billing_subsidi'] = st.session_state['selisih_kamar'] * st.session_state['cur_jumlah_hari']
    #calc prorata
    if st.session_state['cur_tagihan_rs']>0:
        st.session_state['cur_tagihan_self_paid'] = int((st.session_state['cur_kamar_rs']*st.session_state['cur_tagihan_rs'])/st.session_state['cur_kamar_tujuan_rs'])
        st.session_state['%_self_paid'] = int((st.session_state['cur_tagihan_self_paid']/st.session_state['cur_tagihan_rs'])*100)
        st.session_state['cur_tagihan_rs_moc_paid'] = int(st.session_state['cur_tagihan_rs'] - st.session_state['cur_tagihan_self_paid'])
        st.session_state['%_moc_paid'] = int((st.session_state['cur_tagihan_rs_moc_paid']/st.session_state['cur_tagihan_rs'])*100)