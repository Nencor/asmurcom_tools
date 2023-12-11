import streamlit as st 
from backend import * 

reset_state()

linknya = {
    'moc':'https://asuransimurni.com/produk/asuransi-kesehatan/maestro-optima-care/',
    'website':'https://asuransimurni.com',
    'linkedin':'https://www.linkedin.com/in/nencor',
    'twitter':'https://twitter.com/asmurcom',
    'looker':'https://lookerstudio.google.com/reporting/1687e67d-6dbe-4bac-bacd-988cf433bebe/page/NpqcD',
    'foto':'https://pbs.twimg.com/profile_images/1638728562814640129/s902CLPl_400x400.jpg',
    'alamat_klaim':"""STO Telkom Gambir
Lantai 3, Jl. Medan Merdeka Sel. No.12, RT.11/RW.2
Gambir, Kecamatan Gambir, Kota Jakarta Pusat, 
Daerah Khusus Ibukota Jakarta 10110""",
    'whatsapp':'https://wa.me/6281210429617'
}

checkbox_kurir = ['JNE','JNT','TIKI','POS Indonesia','SAP','SiCepat','JET']
menunya = ['Upgrade Downgrade Kamar'
        ,'Pertanyaan Kesehatan MOC'
        ,'Klaim Reimbursement MOC']

kelengkapan_klaim = {
    'suket_dokter':{
        'name':'[Surat Keterangan Dokter]({})'.format(linknya['looker']),
        'key':'kelengkapan_klaim_suket_dokter',
        'help':'Surat Keterangan Dokter wajib diisi oleh dokter dan disign oleh dokter serta stempel Rumah Sakit'
    },
    'invoice':{
        'name':'Invoice / Tagihan Rumah Sakit',
        'key':'kelengkapan_klaim_invoice',
        'help':None
    },
    'kwitansi':{
        'name':'Kwitansi / Official Receipt / Bukti Bayar',
        'key':'kelengkapan_klaim_kwitansi',
        'help':None
    },
    'tax_invoice':{
        'name':'Tax Invoice (bila ada. Bila tidak ada maka tetap diceklis)',
        'key':'kelengkapan_klaim_tax_invoice',
        'help':'Pembayaran pajak dapat ditagihkan ke Penanggung'
    },
    'resume_medis':{
        'name':'Resume Medis / Discharge Summary',
        'key':'kelengkapan_klaim_resume_medis',
        'help':"Dapat diminta ke bagian Admisi Rumah Sakit."
    },
    'billing_details':{
        'name':'Rincian biaya, perawatan, dan obat-obatan selama Rawat Inap',
        'key':'kelengkapan_klaim_billing_details',
        'help':"Dapat diminta ke bagian Admisi Rumah Sakit"
    },
    'hasil_lab':{
        'name':'Hasil Laboratorium dan analisa dokter (baca rontgen, MRI,CT Scan, dll)',
        'key':'kelengkapan_klaim_hasil_lab',
        'help':"Dapat diminta ke bagian Admisi Rumah Sakit"
    }
    ,'ktp':{
        'name':'Copy KTP Tertanggung',
        'key':'kelengkapan_klaim_ktp_tertanggung',
        'help':"Untuk keperluan verifikasi data TErtanggung"
    },
    'rekening':{
        'name':'Copy Buku Rekening Tabungan untuk pembayaran klaim',
        'key':'kelengkapan_klaim_buku_rekening',
        'help':"Masukkan nomor rekening yang masih aktif"
    }

}


penyakit_eligible_moc = [
    'Kanker'
    ,'Hepatitis B'
    ,'Hepatitis C'
    ,'Diabetes'
    ,'Penyakit Jantung'
    ,'Gagal Ginjal'
    ,'Hipertensi'
    ,'Penyakit Paru Obstruktif Kronis'
    ,'Sirosis Hati / Liver'
    ,'Stroke'
    ,'Tidak ada'

]

obat_rutin_eligible_moc = [
    'Ya'
    ,'Tidak'
]

with st.sidebar:
    st.title("[Asuransimurni.com](https://Asuransimurni.com) Tools")
    st.write("Membantu nasabah dalam mendapatkan informasi terkait Klaim maupun Administrasi terkait Asuransi AXA Financial Indonesia.")
    st.selectbox("Menu",menunya,key='menu')
    st.write(f"[Butuh bantuan?]({linknya['whatsapp']})")

tab1,tab2 = st.tabs(['Home','Debug'])

with tab1:
    if st.session_state['menu'] == 'Upgrade Downgrade Kamar':
            st.subheader("Perhitungan Upgrade Downgrade Kamar [Maestro Optima Care]({})".format(linknya['moc']))
            st.write("Menu ini bertujuan untuk menghitung estimasi biaya tagihan Rumah Sakit yang excess diakibatkan oleh upgrade kamar.")
            st.selectbox("Plan saat ini",config_kamar.keys(),index=2,key='cur_plan')
            st.selectbox("Berobat di",['Indonesia','Luar Indonesia'],index=0,key='cur_negara')
            st.number_input("Masukkan harga per malam kamar rawat inap {} bed per room termurah di Rumah Sakit".format(config_kamar[st.session_state['cur_plan']]['jumlah_bed']),min_value=0,key='cur_kamar_rs',on_change=calc_kamar)
            if st.session_state['cur_kamar_rs']:
                st.write("Harga Kamar yang akan diperhitungkan adalah {:,}".format(st.session_state['max_harga_kamar']))
            st.number_input("Masukkan harga kamar per malam yang dituju",min_value=0,key='cur_kamar_tujuan_rs',on_change=calc_kamar)
            
            if st.session_state['cur_kamar_rs']>0 and st.session_state['cur_kamar_tujuan_rs']:
                if st.session_state['cur_kamar_increment']<=0.2 and st.session_state['cur_negara']=='Indonesia':
                    st.number_input("Estimasi jumlah hari dirawat",min_value=0,key='cur_jumlah_hari',on_change=calc_kamar)
                    if st.session_state['cur_jumlah_hari']>0:
                        st.write("Total harga kamar: {:,} ".format(st.session_state['max_harga_kamar']))
                        st.write("Total harga kamar yang dituju: {:,}".format(st.session_state['cur_kamar_tujuan_rs']))
                        st.write(":exclamation: Selisih harga kamar: {:,}".format(st.session_state['selisih_kamar']))
                        st.write("Total hari dirawat: {} hari".format(st.session_state['cur_jumlah_hari']))
                        st.write(":exclamation: Total dana minimal yang perlu disiapkan: {:,} X {} hari = {:,} ".format(st.session_state['selisih_kamar']
                                                                                                        ,st.session_state['cur_jumlah_hari']
                                                                                                        ,st.session_state['total_billing_subsidi']
                                                                                                        ))
                else:
                    st.write("Harga kamar tujuan ialah {:,} dan kenaikan harga kamar sama dengan {}% dari harga kamar yang diperhitungkan {:,}, maka akan dikenakan perhitungan prorata dari total tagihan Rumah Sakit".format(st.session_state['cur_kamar_tujuan_rs']
                                                                                                        ,round(st.session_state['cur_kamar_increment']*100)
                                                                                                        ,st.session_state['max_harga_kamar']))
                    st.number_input("Masukkan estimasi total Billing Rumah Sakit",min_value=0,help="Angka ini dapat dikonfirmasi melalui bagian Admisi / Asuransi tiap Rumah Sakit",key='cur_tagihan_rs',on_change=calc_kamar)
                    if st.session_state['cur_tagihan_rs']>0:
                        st.write("Estimasi Total Tagihan Rumah Sakit: {:,} (100%)".format(st.session_state['cur_tagihan_rs']))
                        st.write(":white_check_mark: Estimasi Total Billing yang dicover Asuransi: {:,} ({}%)".format(st.session_state['cur_tagihan_rs_moc_paid'],st.session_state['%_moc_paid']))
                        st.write(":exclamation: Estimasi Total Billing yang dicover diri sendiri: {:,} ({}%)".format(st.session_state['cur_tagihan_self_paid'],st.session_state['%_self_paid']))
    
    elif st.session_state['menu'] == 'Pertanyaan Kesehatan MOC':
        st.subheader("Pertanyaan Kesehatan [Maestro Optima Care](https://asuransimurni.com/produk/asuransi-kesehatan/maestro-optima-care/)")
        st.write("Tools ini bertujuan untuk mengetahui apakah anda eligible untuk membeli Asuransi Kesehatan Maestro Optima Care.")
        st.number_input("1. Masukkan Usia (tahun)",min_value=1,on_change=calc_eligible_moc,key='eligible_usia')
        st.radio("2. Apakah pernah terdiagnosa penyakit di bawah ini?",penyakit_eligible_moc,on_change=calc_eligible_moc,index=10,key='eligible_penyakit')
        st.radio("3. Apakah saat ini sedang konsumsi obat/rawat jalan / kontrol dokter secara rutin",obat_rutin_eligible_moc,on_change=calc_eligible_moc,index=1,key='eligible_rutin')
        if st.button("Cek Eligible",'eligible_button'):
            if st.session_state['check_eligible_usia'] and st.session_state['check_eligible_penyakit'] and st.session_state['check_eligible_rutin']:
                st.success(":white_check_mark: Anda lulus dan diperkenankan membeli Asuransi Kesehatan Maestro Optima Care. Hubungi [agen](https://asuransimurni.com/produk/asuransi-kesehatan/maestro-optima-care/) sekarang.")
            else:
                st.error(":exclamation: Mohon maaf anda tidak diperkenankan untuk membeli Asuransi Kesehatan Maestro Optima Care.")
    elif st.session_state['menu'] == 'Klaim Reimbursement MOC':
        st.subheader("Klaim Reimbursement [Maestro Optima Care]({})".format(linknya['moc']))
        st.write("Menu ini bertujuan untuk melakukan verifikasi apakah dokumen Klaim sudah lengkap sebelum dikirim")
        st.write("Mohon untuk melengkapi dokumen di bawah ini:")
        
        st.session_state['kelengkapan_score']=0
        
        for item in kelengkapan_klaim:
            st.checkbox(kelengkapan_klaim[item]['name']
                        ,key=kelengkapan_klaim[item]['key']
                        ,help=kelengkapan_klaim[item]['help']
                        ,on_change=calc_kelengkapan_klaim)        
        my_bar = st.progress(st.session_state['progress_value'], text="Kelengkapan Dokumen")
        if st.session_state['progress_value']==1:
            st.success("Terima kasih. Dokumen telah lengkap. Mohon untuk mengirimkan seluruh berkas dan dokumen untuk keperluan Klaim via ekspedisi yang memiliki nomor resi seperti JNE, JNT, TIKI, dsb ke alamat di bawah ini:")
            st.code(linknya['alamat_klaim'])
            st.checkbox("Saya telah mengirimkan dokumen Klaim ke alamat tersebut",key="klaim_sent")
            if st.session_state['klaim_sent']:
                col1,col2,col3 = st.columns(3)
                with col1:
                    st.text_input("Nomor Polis",key='klaim_no_polis',help="cth: 570-9999999")
                with col2:
                    st.selectbox("Pilih Kurir / Jasa Ekspedisi",checkbox_kurir,index=0,key='klaim_kurir',on_change=calc_kelengkapan_klaim)
                with col3:
                    st.text_input("Nomor Resi",key='klaim_resi')

                if st.session_state['klaim_no_polis'] and st.session_state['klaim_sent'] and st.session_state['klaim_resi']:
                    st.markdown(f"[Kirim Nomor Resi via Whatsapp](https://api.whatsapp.com/send/?phone={linknya['whatsapp']}&text=dokumen%20klaim%20nomor%20polis%20{st.session_state['klaim_no_polis']}%20telah%20dikirim%20menggunakan%20{str(st.session_state['klaim_kurir']).replace(' ','%20') }%20dengan%20nomor%20resi%20{st.session_state['klaim_resi']}&type=phone_number&app_absent=0)")
                else:
                    st.error("Lengkapi Nomor Polis / Nomor Resi terlebih dahulu untuk mengirimkan nomor resi pengiriman via Whatsapp.")
                    
with tab2:
    st.session_state