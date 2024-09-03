import streamlit as st
import pandas as pd

# 데이터 불러오기
uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요", type=["xlsx"])

if uploaded_file is not None:
    # 업로드된 파일을 데이터프레임으로 읽기
    data = pd.read_excel(uploaded_file, header=2, sheet_name='생산추적(3차 수정_240823)')

    # 열 이름 변경
    data = data.rename(columns={
        'Unnamed: 0': 'No.',
        'Unnamed: 1': 'Labeling',
        'DM5-1.건조균막 두께/표준편차(mm)': 'DM5-1.건조균막 두께(mm)',
        'Unnamed: 47': '두께/표준편차(mm)',
        'DM5-2.건조균막 인장강도/표준편차(MPa)': 'DM5-2.건조균막 인장강도(MPa)',
        'Unnamed: 49': '인장강도/표준편차(MPa)',
        'DM5-3.건조균막 신율/표준편차(%)': 'DM5-3.건조균막 신율(%)',
        'Unnamed: 51': '신율/표준편차(%)'
    })

    st.write("업로드된 데이터:")
    st.dataframe(data)

    # 검색 조건 입력 받기
    labeling = st.text_input("Labeling을 입력하세요:")
    min_thickness = st.number_input("최소 건조균막 두께 (mm):", min_value=0.0, value=0.0)
    min_thickness_2 = st.number_input("신율/표준편차(%):", min_value=0.0, value=0.0)

    # 조건에 맞게 데이터 필터링
    if labeling:
        filtered_data = data[
            (data['Labeling'].str.contains(labeling, na=False)) &
            (data['DM5-1.건조균막 두께(mm)'] >= min_thickness) &
        (data['신율/표준편차(%)'] >= min_thickness)
        ]
    else:
        filtered_data = data[data['DM5-1.건조균막 두께(mm)'] >= min_thickness]

    # 필터링된 데이터 표시
    st.write("필터링된 데이터:")
    st.dataframe(filtered_data)

    # 엑셀 파일로 저장할 수 있는 버튼 생성
    if st.button('엑셀 파일로 저장'):
        filtered_data.to_excel('filtered_data.xlsx', index=False)
        st.success('엑셀 파일이 저장되었습니다!')

    # 파일 다운로드 링크 제공
    @st.cache_data
    def convert_df(df):
        return df.to_csv().encode('utf-8')

    csv = convert_df(filtered_data)

    st.download_button(
        label="CSV 파일로 다운로드",
        data=csv,
        file_name='filtered_data.csv',
        mime='text/csv',
    )
