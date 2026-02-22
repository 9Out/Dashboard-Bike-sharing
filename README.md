# Submission Dicoding "Proyek Analisis Data"

## Project Analisis Data

Repository ini berisi proyek data analytics yang saya kerjakan. Deployment in **Streamlit** <img src="https://user-images.githubusercontent.com/7164864/217935870-c0bc60a3-6fc0-4047-b011-7b4c59488c91.png" alt="Streamlit logo"></img>

## Deskripsi

Proyek ini bertujuan untuk menganalisis data pada Bike Sharing Dataset. Tujuan akhirnya adalah untuk menghasilkan wawasan dan informasi yang berguna dari data yang dianalisis.

## Struktur Direktori

- **/Data**: Direktori ini berisi data awal yang digunakan dalam proyek, dalam format .csv .
- **/Dashboard**: Direktori ini berisi app.py yang digunakan untuk membuat dashboard hasil analisis data.
- **Proyek_Analisis_Data_Done.ipynb**: File ini yang digunakan untuk melakukan analisis data.

## Instalasi

1. Clone repository ini ke komputer lokal Anda menggunakan perintah berikut:

   ```shell
   git clone https://github.com/9Out/Dashboard-Bike-sharing.git
   ```

2. Pastikan Anda memiliki lingkungan Python yang sesuai dan pustaka-pustaka yang diperlukan. Anda dapat menginstal pustaka-pustaka tersebut dengan menjalankan perintah berikut:

    ```shell
    python -m venv env
    .\env\Scripts\Activate.ps1
    pip install streamlit
    pip install -r requirements.txt
    ```

## Penggunaan
1. Masuk ke direktori proyek (Local):

    ```shell
    cd Dashboard-Bike-sharing/Dashboard/
    streamlit run app.py
    ```
    Atau bisa dengan kunjungi website ini [Project Data Analytics](https://dashboard-bikes-data.streamlit.app/)