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

def init_state(init_sessions,valuenya=0):
    for session in init_sessions:
        if session not in st.session_state:
            st.session_state[session]=valuenya

def reset_state():
    init_state(init_sessions=['cur_kamar_increment'
                          ,'cur_tagihan_rs_moc_paid'
                          ,'cur_tagihan_self_paid'
                          ,'cur_tagihan_rs'
                          ,'cur_jumlah_hari'
                          ,'%_moc_paid'
                          ,'%_self_paid'
                          ,'max_harga_kamar'
                          ,'eligible_moc_score'
                          ,'kelengkapan_score'
                          ,'progress_value'
                          ,'klaim_no_polis'
                          ,'klaim_kurir'])
    init_state(['check_eligible_usia'
                ,'check_eligible_penyakit'
                ,'check_eligible_rutin'],valuenya=True)

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

def calc_eligible_moc():
    init_state(['check_eligible_usia','check_eligible_penyakit','check_eligible_rutin'],valuenya=False)
    st.session_state['check_eligible_usia'] = True if st.session_state['eligible_usia']<=80 else False
    st.session_state['check_eligible_penyakit'] = True if st.session_state['eligible_penyakit'] =='Tidak ada' else False
    st.session_state['check_eligible_rutin'] = True if st.session_state['eligible_rutin']=='Tidak' else False

def calc_kelengkapan_klaim():
    count_true = 0 #to have it presented in st.progress
    count_checkbox=0 # count_true / count_checkbox
    for item in st.session_state:        
        if 'kelengkapan_klaim' in item: #this is where st.checkbox is
            count_checkbox+=1
            if st.session_state[item] is True:
                count_true+=1 
    st.session_state['progress_value'] = count_true/count_checkbox
    print("Klaim Kurir is {}".format(str(st.session_state['klaim_kurir']).replace(" ","%20")))