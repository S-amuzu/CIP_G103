README Streamlit Project:

We created the Streamlit app separately from the main Notebook, which is why all necessary files are included in this folder.

Since the app loads several files, please be patient as it may take a moment to start.
Once loaded, you will see some of the same plots that we also created in the Notebook.

This Streamlit app serves as a small bonus for us (it was kept very simple), we built it because we wanted to experiment and explore Streamlit for ourselve.


File Descriptions

Dashboard.py        - Main Streamlit app file. Run this to launch the dashboard. (streamlit run Dashboard.py)
out_es.xlsx         - Output dataset for Spain for the year 2013.
out_es_2014.xlsx    - Output dataset for Spain for the year 2014. (league)
out_es_2015.xlsx    - Output dataset for Spain for the year 2015.
out_pl.xlsx         - Output dataset for Prem for the year 2013.
out_pl_2014.xlsx    - Output dataset for Prem for the year 2014. (league)
out_pl_2015.xlsx    - Output dataset for Prem for the year 2015.
transfer_es1.xlsx   - Transfer dataset related to spanish league (es1).
transfer_gb1.xlsx   - Transfer dataset related to premier league (gb1).

How to Run the Dashboard

1. Install dependencies:
   pip install streamlit pandas openpyxl

2. Start the Streamlit app:
   streamlit run Dashboard.py

3. Open your browser and go to:
   http://localhost:8501 or click the Link in the IDE

Folder Structure

Streamlit/
│
├── Dashboard.py
├── out_es.xlsx
├── out_es_2014.xlsx
├── out_es_2015.xlsx
├── out_pl.xlsx
├── out_pl_2014.xlsx
├── out_pl_2015.xlsx
├── transfer_es1.xlsx
└── transfer_gb1.xlsx
