import pickle
import streamlit as st
import pandas as pd
import locale

model = pickle.load(open('estimasi_mobil.sav', 'rb'))

# Set locale untuk Indonesia
#locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')



# Load the data
df = pd.read_csv('toyota.csv')

# Menambahkan judul yang menarik
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🚗 Estimasi Harga Mobil Toyota Bekas di Wilayah Inggris</h1>", unsafe_allow_html=True)


# Additional option to filter by model
unique_models = sorted(df['model'].unique())
selected_model = st.sidebar.multiselect('Pilih Model Mobil:', unique_models)

# Tombol Estimasi Harga dinonaktifkan jika belum ada model yang dipilih
button_disabled = not bool(selected_model)

 
# Menampilkan selectbox untuk memilih tahun hanya jika ada model yang dipilih
if selected_model:
    filtered_data_by_model = df[df['model'].isin(selected_model)]
    
    # Menampilkan selectbox untuk memilih tahun
    unique_years = sorted(filtered_data_by_model['year'].unique())
    selected_year = st.sidebar.selectbox('Pilih Tahun:', unique_years)

    # Menampilkan data sesuai model dan tahun yang dipilih
    if selected_year:
        filtered_data_by_year = filtered_data_by_model[filtered_data_by_model['year'] == selected_year ]
    
    # Menampilkan selectbox untuk memilih KM
        unique_mileage = sorted(filtered_data_by_year['mileage'].unique())
        selected_km = st.sidebar.selectbox('Pilih KM:', unique_mileage)

         # Menampilkan data sesuai model, tahun, dan KM yang dipilih
        if selected_km:
            filtered_data_by_tax = filtered_data_by_year[filtered_data_by_year['mileage'] == selected_km]
            
            # Menampilkan selectbox untuk memilih Pajak
            unique_tax = sorted(filtered_data_by_tax['tax'].unique())
            selected_pajak = st.sidebar.selectbox('Pilih Pajak:', unique_tax)
        
            # Menampilkan data sesuai model, tahun, KM, dan pajak yang dipilih
            if selected_pajak:
                filtered_data_by_mpg = filtered_data_by_tax[filtered_data_by_tax['tax'] == selected_pajak]

                # Menampilkan selectbox untuk memilih bahan bakar
                unique_mpg = sorted(filtered_data_by_mpg['mpg'].unique())
                selected_mpg = st.sidebar.selectbox('Pilih Bahan Bakar:', unique_mpg)
            
                # Menampilkan data sesuai model, tahun, KM, pajak dan bahan bakar yang dipilih
                if selected_mpg:
                    filtered_data_by_ukuran = filtered_data_by_mpg[filtered_data_by_mpg['mpg'] == selected_mpg]

                    # Menampilkan selectbox untuk memilih ukuran mesin
                    unique_ukuran = sorted(filtered_data_by_ukuran['engineSize'].unique())
                    selected_ukuran = st.sidebar.selectbox('Pilih Ukuran Mesin:', unique_ukuran)
                    
                    # Menampilkan data sesuai model, tahun, KM, pajak, bahan bakar dan ukuran mesin
                    if selected_ukuran:
                        final_filtered_data = filtered_data_by_ukuran[filtered_data_by_ukuran['engineSize'] == selected_ukuran]
                        
                        # Menampilkan informasi yang dipilih
                        st.markdown(f"<h2 style='text-align: center; color: #FF5733;'>Menampilkan Data untuk:</h2>", unsafe_allow_html=True)
                        st.markdown(f"<h3 style='text-align: center;'>Model: {', '.join(selected_model)}, Tahun: {selected_year}, KM: {selected_km}, Pajak:{selected_pajak}, Bahan Bakar:{selected_mpg}, dan Ukuran Mesin:{selected_ukuran}</h3>", unsafe_allow_html=True)

                        # Menampilkan data dalam expander untuk tampilan yang lebih rapi
                        with st.expander("Klik untuk melihat data lengkap"):
                            st.dataframe(final_filtered_data)
  
                    else:
                        st.write("Data Tidak ada.")
    
else:
    st.markdown("<p style='text-align: center;'>Silakan pilih satu atau lebih model mobil untuk memulai.</p>", unsafe_allow_html=True)

predict = ''

# Tombol untuk melakukan estimasi harga, aktif jika mobil sudah dipilih           
if st.button('Estimasi Harga', disabled=button_disabled):
    predict = model.predict(
        [[selected_year, selected_km, selected_pajak, selected_mpg, selected_ukuran]]
    )
    # Format hasil estimasi menjadi Pound Sterling
    #formatted_harga = locale.currency(predict, grouping=True, symbol=True)
    
    # Format hasil estimasi menjadi Pound Sterling
    # Membulatkan ke bawah (menghapus desimal)
    rounded_harga = int(predict)
    formatted_harga = f"£{rounded_harga:,}"


    # Format angka menjadi Rupiah
    formatted_rupiah = locale.currency(predict*19000, grouping=True, symbol=True)
   
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center; color: #FF5733;'>Hasil Estimasi Harga</h2>", unsafe_allow_html=True)
    st.metric('Estimasi Harga Mobil Bekas dalam Ponds :', formatted_harga)
    st.metric('Estimasi Harga Mobil Bekas dalam IDR', formatted_rupiah)
   

   