import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title('데이터 대시보드')

uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")
if uploaded_file is not None:
    data_load_state = st.text('Loading data...')
    
    @st.cache_data
    def load_data(uploaded_file):
        data = pd.read_excel(uploaded_file)
        data['datetime'] = pd.to_datetime(data['Date'].astype(str) + ' ' + data['Time'].astype(str))
        data.set_index('datetime', inplace=True)
        data.drop(columns=['Date', 'Time'], inplace=True)
        return data

    data = load_data(uploaded_file)
    data_load_state.text('Done! (using st.cache_data)')

    # 1. 날짜별 평균 온도
    st.subheader('Daily Average Temperature')
    daily_avg_temp = data['온도'].resample('D').mean()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=daily_avg_temp.index, y=daily_avg_temp, mode='lines', name='Daily Average Temperature', line=dict(color='blue')))
    fig.update_layout(title='Daily Average Temperature', xaxis_title='Date', yaxis_title='Temperature')
    st.plotly_chart(fig)

    # 2. 날짜 선택을 통한 시간대별 시각화
    st.subheader('Select a Date for Detailed Analysis')
    selected_date = st.date_input("Choose a date", value=pd.to_datetime(data.index.date).min(), min_value=pd.to_datetime(data.index.date).min(), max_value=pd.to_datetime(data.index.date).max())

    # 선택된 날짜에 해당하는 데이터 필터링
    filtered_data = data[data.index.date == pd.to_datetime(selected_date).date()]

    if not filtered_data.empty:
        st.subheader(f'Temperature, Humidity, and CO2 on {selected_date}')

        color_map = {'온도': 'rgba(0,0,255,1)', '습도': 'rgba(0,255,0,1)', 'CO2': 'rgba(255,0,0,1)'}
        for measurement in ['온도', '습도', 'CO2']:
            color = color_map[measurement]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=filtered_data.index, y=filtered_data[measurement], mode='lines+markers', name=f'{measurement}', line=dict(color=color)))
            fig.update_layout(title=f'{measurement} on {selected_date}', xaxis_title='Time', yaxis_title=measurement)
            st.plotly_chart(fig)

        st.write("Filtered Data:")
        st.dataframe(filtered_data)
    else:
        st.write("No data available for the selected date.")
else:
    st.error("Please upload an Excel file.")

