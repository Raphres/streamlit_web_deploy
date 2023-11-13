import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
from PIL import Image

image = Image.open('header4.jpg')
st.image(image)
st.title(':chart_with_upwards_trend: 프로젝트1: 자유낙하 운동 분석(가속도)')
st.subheader("")

# 글자체 특징
path = os.getcwd() + '/NanumGothic.ttf'
fontprop = fm.FontProperties(fname = path)

# 1번 구역
st.subheader('1. 자유낙하 운동 실험 과정 안내 :clipboard:', divider='violet')
st.markdown('##### **다음 과정에 따라 실험해 봅시다.**')
st.markdown(" 1. 플레이스토어(또는 앱스토어)에서 '**phyphox**' 앱을 다운받는다.")
st.markdown(" 2. 앱을 실행하고 '**Raw Sensors**'의 '**Acceleration without g**' 를 실행한다.")
st.markdown(" 3. 재생 버튼을 누르고 스마트폰을 **자유 낙하**시킨다.")
st.markdown(" 4. 바닥에 닿으면 일시 정지 버튼을 눌러 실행을 종료한다.")
st.markdown(" 5. 오른쪽 위의 '**점 세 개**'-'**Export Data**'-'**CSV(Comma, decimal point)**'를 누르고 OK를 눌러 CSV 파일을 폰으로 받는다.")
st.image('phyphox.png')
st.markdown(" 6. 아래 '**자유낙하 운동 실험 결과**'에 조 이름과 질량을 입력한 후 폰으로 받은 CSV 파일을 업로드한다.")
st.markdown(" 7. '**데이터 바탕으로 그래프 그리기**' 버튼을 눌러서 그래프를 생성한다.")
st.markdown(" 8. 그래프를 확인하고 '**그린 그래프 제출하기**' 버튼을 눌러 그래프를 제출한다.")
st.markdown(" 9. '**갈릴레오 도감**'에서 모든 조의 실험 결과 그래프를 비교하여 실험 결과를 해석한다.")
st.divider()

# 2번 구역
st.subheader('2. 자유낙하 운동 실험 결과 :chart_with_upwards_trend:', divider='violet')

# CSV 파일 구분을 위한 조 이름 입력
group_name = st.text_input(':busts_in_silhouette: **조 이름을 입력해주세요.**')

# 컨텐츠1(CSV 업로드), 컨텐츠2(질량 입력)
con1, con2 = st.columns([0.6,0.4])
with con1: 
    #  파일 저장하는 함수 정의
    def save_uploaded_file(directory, file):
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(os.path.join(directory, file.name),'wb') as f: 
            f.write(file.getbuffer())

        return st.success('파일 업로드 성공')

    # csv 파일 업로드 부분
    csv_file = st.file_uploader(':file_folder: **Phyphox에서 다운로드 받은 .csv 파일을 업로드 하세요.**', type = ['csv'])

    if csv_file is not None:
        if group_name is None:
            st.warning('조 이름을 입력해주세요.')
        
        else:
            filename = group_name + '.csv'
            csv_file.name = filename
            df = pd.read_csv(csv_file)

            # 속도 데이터 프레임 생성 (★생성 방식 논의 필요)
            selected_columns = ['Time (s)', 'Absolute acceleration (m/s^2)']
            filtered_df = df[selected_columns]

            continuous_duration = 0.1  # 최소 지속 시간 (초)
            continuous_rows = []
            current_duration = 0
            for index, row in filtered_df.iterrows():
                if 9.0 <= row['Absolute acceleration (m/s^2)'] < 10.0:
                    current_duration += 0.1  # 0.1초 간격으로 계산
                else:
                    if current_duration >= continuous_duration:
                        continuous_rows.extend(list(range(index - int(current_duration * 10), index)))
                    current_duration = 0

            vel_df = filtered_df.loc[continuous_rows]
            vel_df['velocity (m/s)'] = vel_df['Absolute acceleration (m/s^2)'].cumsum() * 0.01
        

            save_uploaded_file('csv', csv_file)

    else:
        st.warning('파일을 업로드하지 않았습니다.')

with con2: 
    # 질량 값 입력 부분
    mass = st.number_input(':pencil: **실험에 사용한 물체의 질량을 (g)단위로 입력하세요:**', min_value=0.0)

    st.write('**실험 물체 질량:**', mass)

    # 그래프 세부 세팅
    selected_color = st.color_picker("그래프의 색상을 선택하세요.", "#ff5733")
    markers = ['o', 's', '^', 'D', 'v', ',', '<', '>', 'p', 'h', 'd', '_', '1']


# 컨텐츠3(원본 데이터 그래프 그리기), 컨텐츠4(v-t 가공 그래프 그리기)
if st.button('데이터 바탕으로 그래프 그리기', use_container_width = True):
    if csv_file is not None:
        if group_name is not None:
            
            con3, con4 = st.columns([0.5,0.5])
            with con3: 
                # 원본 데이터 그래프
                x = df['Time (s)'].to_numpy()
                y = df['Absolute acceleration (m/s^2)'].to_numpy()
                plt.figure(figsize=(8, 6))
                plt.scatter(x, y, marker = 'x', alpha = 0.22)
                plt.xlabel('시간(s)', fontproperties = fontprop)
                plt.ylabel('가속도($ \mathrm{m/s^2}$)', fontproperties = fontprop)
                plt.title('내가 수집한 자유낙하 운동 데이터의 원본 그래프' + '(질량 =' + str(mass) + 'g)', fontproperties = fontprop)
                st.set_option('deprecation.showPyplotGlobalUse', False)
                st.pyplot()

            with con4:
                # 가공 데이터 그래프 (그래프 가공 코드 미완성)
                x = vel_df['Time (s)'].to_numpy()
                y = vel_df['velocity (m/s)'].to_numpy()

                # 선형회귀 (싸이킷 런 오류떠서 직접 연산 처리)
                x_mean = np.mean(x)
                y_mean = np.mean(y)

                numerator = np.sum((x - x_mean) * (y - y_mean))
                denominator = np.sum((x - x_mean)**2)

                slope = numerator / denominator
                intercept = y_mean - slope * x_mean

                fig, ax = plt.subplots()
                ax.scatter(x, y, c = selected_color, marker = np.random.choice(markers), alpha = 0.5)
            
                ax.plot(x, slope * x + intercept, color= 'red', linewidth=2)
                
                plt.xlabel('시간(s)', fontproperties = fontprop)
                plt.ylabel('속도($ \mathrm{m/s}$)', fontproperties = fontprop)
                plt.title('내가 수집한 자유낙하 운동 데이터의 시간에 따른 속력 그래프' + '(질량 =' + str(mass) + 'g)', fontproperties = fontprop)
                plt.grid(True)
                st.set_option('deprecation.showPyplotGlobalUse', False)
                st.pyplot()
                    
        else: 
            st.warning('조 이름을 입력해주세요.')
    else: 
        st.warning('파일을 업로드하지 않았습니다.')

# 그래프 추가하기 (수정 예정)
with st.form(key = 'form'):
    name = group_name
    submit = st.form_submit_button(label = '그린 그래프 제출하기', use_container_width = True)
    
    if submit:
        x = vel_df['Time (s)'].to_numpy()
        y = vel_df['velocity (m/s)'].to_numpy()

        # 선형회귀 (싸이킷 런 오류떠서 직접 연산 처리)
        x_mean = np.mean(x)
        y_mean = np.mean(y)

        numerator = np.sum((x - x_mean) * (y - y_mean))
        denominator = np.sum((x - x_mean)**2)

        slope = numerator / denominator
        intercept = y_mean - slope * x_mean

        fig, ax = plt.subplots()
        ax.scatter(x, y, c = selected_color, marker = np.random.choice(markers), alpha = 0.5)
        ax.plot(x, slope * x + intercept, color= 'red', linewidth=2)
        
        plt.xlabel('시간(s)', fontproperties = fontprop)
        plt.ylabel('속도($ \mathrm{m/s}$)', fontproperties = fontprop)
        plt.title('내가 수집한 자유낙하 운동 데이터의 시간에 따른 속력 그래프' + '(질량 =' + str(mass) + 'g)', fontproperties = fontprop)
        plt.grid(True)
        plt.savefig('img' + '/' + group_name + '조' + '시간-속력 그래프', dpi = 300)

        if not name:
            st.error('조 이름을 입력해주세요.')

        else:
            st.success('그래프가 제출되었습니다.')
            
st.divider()

# 3번 구역
st.subheader('3. 갈릴레이 도감: 모든 조의 자유낙하 운동 실험 결과 :grinning:', divider='violet')

# 그래프 모음집 업데이트
cols = st.columns(3)

image_folder = os.getcwd() + '/img'
files = os.listdir(image_folder)
image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
print(image_files) # 점검용
my_range = range(len(image_files))


for i in my_range:
    with cols[i % 3]:
        st.image('img' + '/' + image_files[int(i)], caption = image_files[int(i)])

# 4번 구역: 실험 정리
st.subheader('4. 프로젝트1 보고서: 실험 결과 해석하기 :bookmark_tabs:', divider='violet')

with st.form(key='my_form1'):
    st.markdown('**1. 자유 낙하 운동 실험 결과 물체가 자유낙하할 때, 가속도는?**')
    question1 = st.radio(
        "",
        ["질량이 클수록 가속도는 커진다.", "질량에 관계 없이 가속도는 일정하다."]
    )
    answer1 = st.form_submit_button("정답 제출")

if answer1:
    if question1 == "질량에 관계 없이 가속도는 일정하다.":
        st.write("정답입니다! :clap:")
    else:
        st.write("갈릴레이 도감을 보고 다시 풀어보세요. :sweat_smile:")

with st.form(key='my_form2'):
    st.markdown('**2. (1번의 답에 의하면) 질량이 다른 두 물체를 같은 높이에서 동시에 자유낙하할 때, 결과는?**')
    question2 = st.radio(
        "",
        ["질량이 클수록 먼저 떨어진다.", "질량에 관계 없이 동시에 떨어진다."]
    )
    answer2 = st.form_submit_button("정답 제출")

if answer2:
    if question2 == "질량에 관계 없이 동시에 떨어진다.":
        st.write("정답입니다! :clap:")
    else:
        st.write("다시 풀어보세요. :sweat_smile:")

with st.form(key='my_form3'):
    st.markdown('**3. 프로젝트1 보고서: 실험 결과 한줄로 정리하기** :pencil:')
    student_result = st.text_input("**위의 문제를 참고해서 자유 낙하 실험 결과를 한줄로 정리해보세요!** :blush:")

    if st.form_submit_button('한줄 보고서 제출'):
        st.write(f"**'{student_result}'** 라고 정리했군요! 수고했어요 :clap:")

st.divider()
st.subheader(':white_check_mark: 프로젝트1 Clear!!! :tada:')
st. markdown("#### ':bar_chart: 프로젝트2'로 가서 자유 낙하 운동에서 역학적 에너지를 분석해보자! :heavy_check_mark:")