import streamlit as st
import psutil
import time
import pandas as pd

st.title("Surveillance de l'application")

cpu_values = []
ram_values = []

chart = st.line_chart(pd.DataFrame({"CPU": [], "RAM": []}))
metrics = st.empty()

def get_streamlit_process():
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = " ".join(proc.info['cmdline']).lower()

            if "streamlit" in cmdline and "app.py" in cmdline:
                return psutil.Process(proc.info['pid'])

        except:
            continue

    return None

process = get_streamlit_process()

if process is None:
    st.error("Application Streamlit non trouvée. Lance 'streamlit run app.py'")
else:
    while True:
        cpu = process.cpu_percent(interval=1)
        ram = process.memory_info().rss / 1024 / 1024  # en MB

        cpu_values.append(cpu)
        ram_values.append(ram)

        new_data = pd.DataFrame({
            "CPU": [cpu],
            "RAM": [ram]
        })

        chart.add_rows(new_data)

        with metrics.container():
            st.metric("CPU processus (%)", round(cpu, 2))
            st.metric("RAM processus (MB)", round(ram, 2))

        time.sleep(2)