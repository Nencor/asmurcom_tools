import streamlit as st 
from backend import * 

init_state(init_sessions=['cur_kamar_increment'
                          ,'cur_tagihan_rs_moc_paid'
                          ,'cur_tagihan_self_paid'
                          ,'cur_tagihan_rs'
                          ,'cur_jumlah_hari'
                          ,'%_moc_paid'
                          ,'%_self_paid'])

with st.sidebar:
    st.title("[Asuransimurni.com](https://Asuransimurni.com) Tools")
    st.write("Membantu nasabah dalam mendapatkan informasi terkait Klaim maupun Administrasi terkait Asuransi AXA Financial Indonesia.")
    st.selectbox("Menu",['Upgrade Downgrade Kamar'],key='menu')

tab1,tab2 = st.tabs(['Home','Debug'])

with tab1:
    match st.session_state['menu']:
        case 'Upgrade Downgrade Kamar':
            st.subheader("Perhitungan Upgrade Downgrade Kamar [Maestro Optima Care](https://asuransimurni.com/produk/asuransi-kesehatan/maestro-optima-care/)")
            st.write("Menu ini bertujuan untuk menghitung estimasi biaya tagihan Rumah Sakit yang excess diakibatkan oleh upgrade kamar.")
            st.write("Saat ini hanya berlaku khusus nasabah Maestro Optima Care dengan Plan Emerald.")
            st.selectbox("Plan saat ini",["Emerald"],key='cur_plan')
            st.number_input("Masukkan harga per malam kamar rawat inap 1 bed per room termurah di Rumah Sakit",min_value=0,key='cur_kamar_rs',on_change=calc_kamar)
            st.number_input("Masukkan harga kamar per malam yang dituju",min_value=0,key='cur_kamar_tujuan_rs',on_change=calc_kamar)
            
            if st.session_state['cur_kamar_rs']>0 and st.session_state['cur_kamar_tujuan_rs']:
                if st.session_state['cur_kamar_increment']<=0.2:
                    st.number_input("Estimasi jumlah hari dirawat",min_value=0,key='cur_jumlah_hari',on_change=calc_kamar)
                    if st.session_state['cur_jumlah_hari']>0:
                        st.write("Total harga kamar: {:,} ".format(st.session_state['cur_kamar_rs']))
                        st.write("Total harga kamar yang dituju: {:,}".format(st.session_state['cur_kamar_tujuan_rs']))
                        st.write(":exclamation: Selisih harga kamar: {:,}".format(st.session_state['selisih_kamar']))
                        st.write("Total hari dirawat: {} hari".format(st.session_state['cur_jumlah_hari']))
                        st.write(":exclamation: Total dana minimal yang perlu disiapkan: {:,} X {} hari = {:,} ".format(st.session_state['selisih_kamar']
                                                                                                        ,st.session_state['cur_jumlah_hari']
                                                                                                        ,st.session_state['total_billing_subsidi']
                                                                                                        ))
                else:
                    st.write("Harga kamar tujuan ialah {:,} dan kenaikan harga kamar sama dengan {}% dari harga kamar asal {:,}, maka akan dikenakan perhitungan prorata dari total tagihan Rumah Sakit".format(st.session_state['cur_kamar_tujuan_rs']
                                                                                                        ,round(st.session_state['cur_kamar_increment']*100)
                                                                                                        ,st.session_state['cur_kamar_rs']))
                    st.number_input("Masukkan estimasi total Billing Rumah Sakit",min_value=0,help="Angka ini dapat dikonfirmasi melalui bagian Admisi / Asuransi tiap Rumah Sakit",key='cur_tagihan_rs',on_change=calc_kamar)
                    if st.session_state['cur_tagihan_rs']>0:
                        st.write("Estimasi Total Tagihan Rumah Sakit: {:,} (100%)".format(st.session_state['cur_tagihan_rs']))
                        st.write(":white_check_mark: Estimasi Total Billing yang dicover Asuransi: {:,} ({}%)".format(st.session_state['cur_tagihan_rs_moc_paid'],st.session_state['%_moc_paid']))
                        st.write(":exclamation: Estimasi Total Billing yang dicover diri sendiri: {:,} ({}%)".format(st.session_state['cur_tagihan_self_paid'],st.session_state['%_self_paid']))

        case _:
            st.subheader("Kamu belum memilih menu")
with tab2:
    st.session_state