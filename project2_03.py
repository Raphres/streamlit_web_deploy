import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from PIL import Image
import random
from wordcloud import WordCloud

image = Image.open('header4.jpg')
st.image(image)

# 글자체 특징
path = os.getcwd() + '/NanumGothic.ttf'
fontprop = fm.FontProperties(fname = path).get_name()

# Streamlit 앱의 제목 설정
st.title(':bar_chart: 프로젝트2: 자유낙하 운동 분석(에너지)')
st.subheader("")

# 1번 구역
st.subheader('1. 자유낙하 운동의 역학적 에너지 분석 실험 과정 안내 :clipboard:', divider='rainbow')
st.markdown('##### **다음 과정에 따라 실험해 봅시다.**')
st.markdown(" 1. 플레이스토어(또는 앱스토어)에서 '**phyphox**' 앱을 다운받는다.")
st.markdown(" 2. 앱을 실행하고 '**Raw Sensors**'의 '**Acceleration without g**' 를 실행한다.")
st.markdown(" 3. 재생 버튼을 누르고 스마트폰을 **자유 낙하**시킨다.")
st.markdown(" 4. 바닥에 닿으면 일시 정지 버튼을 눌러 실행을 종료한다.")
st.markdown(" 5. 오른쪽 위의 '**점 세 개**'-'**Export Data**'-'**CSV(Comma, decimal point)**'를 누르고 OK를 눌러 CSV 파일을 폰으로 받는다.")
st.markdown(" 6. 아래 '**자유낙하 운동의 역학적 에너지 그래프 그리기**'에 폰으로 받은 CSV 파일을 업로드한다.")
st.markdown(" 7. 조 이름을 입력하고 '**그린 그래프 제출하기**' 버튼을 눌러 그래프를 제출한다.")
st.markdown(" 8. '**에너지 도감**'에서 모든 조의 실험 결과 그래프를 비교하여 실험 결과를 해석한다.")
st.divider()

# 2번 구역
st.subheader('2. 자유낙하 운동의 역학적 에너지 그래프 그리기 :bar_chart:', divider='rainbow')

# CSV 파일 업로드 위젯
uploaded_file = st.file_uploader(":file_folder: **Phyphox에서 다운로드 받은 .csv 파일을 업로드 하세요.**", type=["csv"])

# 탭은 selectbox로 설정(radio보다 깔끔)
tabs = ["역학적 에너지 그래프", "운동에너지 그래프", "위치에너지 그래프"]
selected_tab = st.selectbox(":white_check_mark: **그래프 유형을 선택하세요**", tabs)

# CSV 파일 업로드되면 실행
if uploaded_file is not None:
    # 업로드된 CSV 파일을 데이터프레임으로 변환
    df = pd.read_csv(uploaded_file)

    # phyphox 앱의 csv 파일에서 필요한 열만 선택 (Time (s)과 Absolute acceleration (m/s^2))
    selected_columns = ['Time (s)', 'Absolute acceleration (m/s^2)']
    filtered_df = df[selected_columns]

    # 물체의 질량 입력 받기(스마트폰 무게 고려해서 최대 최소 설정)
    mass_g = st.number_input("물체의 질량(g)을 입력하세요", min_value=100, max_value=1000, step=1)
    mass = mass_g/1000


    # 데이터 전처리: 가속도 값이 9.0 이상인 구간 중 최소 0.1초 이상 지속되는 구간 선택
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
    filtered_df = filtered_df.loc[continuous_rows]



    # 가속도를 적분하여 속도 계산 (v = ∫a dt, 초기 속도는 0으로 가정)
    filtered_df['속도(m/s)'] = filtered_df['Absolute acceleration (m/s^2)'].cumsum() * 0.01  # 0.01초 간격으로 적분


    # 위치에너지 계산
    height = st.number_input("높이(m)를 입력하세요", min_value=0.10, max_value=2.0, step=0.01)
    velocity_integral = filtered_df['속도(m/s)'].cumsum() * 0.01
    filtered_df['위치에너지'] = mass * filtered_df['Absolute acceleration (m/s^2)'] * (height - velocity_integral)


    # 운동에너지 계산
    filtered_df['운동에너지'] = 0.5 * mass * (filtered_df['속도(m/s)'] ** 2)

    # 역학적 에너지 계산
    filtered_df['역학적에너지'] = filtered_df['위치에너지'] + filtered_df['운동에너지']




    # 탭에 따라 그래프 그리기
    if selected_tab == "운동에너지 그래프":
        plot_df = filtered_df[['Time (s)', '운동에너지']]
        ylabel = '운동에너지'
        color = 'b'
    elif selected_tab == "위치에너지 그래프":
        plot_df = filtered_df[['Time (s)', '위치에너지']]
        ylabel = '위치에너지'
        color = 'r'
    else:
        plot_df = filtered_df[['Time (s)', '위치에너지', '운동에너지', '역학적에너지']]
        ylabel = '에너지'
        color = ['r', 'b', 'g']

    # 그래프 그리기
    plt.rc('font', family = fontprop)
    fig, ax = plt.subplots(figsize=(10, 6))
    if isinstance(color, list):
        ax.plot(plot_df['Time (s)'], plot_df['위치에너지'], marker='.', markersize=1, color=color[0], label='위치에너지')
        ax.plot(plot_df['Time (s)'], plot_df['운동에너지'], marker='.', markersize=1, color=color[1], label='운동에너지')
        ax.plot(plot_df['Time (s)'], plot_df['역학적에너지'], marker='.', markersize=1, color=color[2], label='역학적에너지')
    else:
        ax.plot(plot_df['Time (s)'], plot_df[ylabel], marker='o', color=color, label=ylabel)
    ax.set_xlabel('시간 (s)')
    ax.set_ylabel(ylabel)
    ax.set_title(f'시간에 따른 물체의 {ylabel} 그래프')
    ax.legend()
    st.pyplot(fig)
   
    # 정답 계산 함수
    def calculate_answer(mass, height):
        return float(mass * 10.0 * height)  # 중력가속도는 10.0 m/s^2

    tolerance = 1e-6  # 허용 오차, ==으로 answer값을 판별이 어려워서 넣었습니다. 
    with st.form("위치에너지 계산"):
        user_answer = st.number_input("처음 위치에너지 값 입력 (단위 J)", min_value=0.1, format="%.1f")
        st.caption(r'중력가속도 값은 :blue[10 $\mathrm{m}/{s^2}$] 입니다.')
        submit_button = st.form_submit_button("제출하기")
        if submit_button:
            correct_answer = calculate_answer(mass, height)
            if abs(user_answer - correct_answer) < tolerance:
                st.write("정답입니다! :100:")
            else:
                st.write("틀렸습니다. 다시 시도해보세요. :x:")


    # 데이터프레임 출력 (선택사항)
    st.write("전처리된 데이터프레임:")
    st.write(filtered_df)

group_name = st.text_input(':busts_in_silhouette: **조 이름을 입력해주세요.**')

# 그래프 추가하기 (수정 예정)
with st.form(key = 'form'):
    name = group_name
    submit = st.form_submit_button(label = '그린 그래프 제출하기', use_container_width = True)
   
    if submit:
        plt.rc("font", family = fontprop)
        plt.plot(plot_df['Time (s)'], plot_df['역학적에너지'], marker='.', markersize=1, color=color[2], label='역학적에너지')
        plt.title('자유낙하 시간에 따른 역학적에너지 그래프')
        plt.savefig('img2' + '/' + group_name + '조 ' + '시간-역학적에너지 그래프', dpi = 300)

        if not name:
            st.error('조 이름을 입력해주세요.')

        else:
            st.success('그래프가 제출되었습니다.')

st.divider()

# 3번 구역
st.subheader('3. 에너지 도감: 모든 조의 자유낙하 운동의 역학적 에너지 실험 결과 :grinning:', divider='rainbow')
# 그래프 모음집 업데이트
cols = st.columns(3)

image_folder = os.getcwd() + '/img2'
files = os.listdir(image_folder)
image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
print(image_files) # 점검용
my_range = range(len(image_files))

for i in my_range:
    with cols[i % 3]:
        st.image('img2' + '/' + image_files[int(i)], caption = image_files[int(i)])


st.divider()

# # 4번 구역
# st.subheader('4. 에너지 계산해보기 :pencil2:', divider='rainbow')
# st.caption(r'중력가속도 값은 :blue[9.8 $\mathrm{m}/{s^2}$] 입니다.')



# # 질량과 속력 random으로 받기
# def random_values():
#     mass = random.randrange(2, 11, 2)
#     velocity = random.randint(1, 10)
#     height = random.randint(1, 10)
#     return mass, velocity, height


# if 'stage' not in st.session_state:
#     st.session_state.stage = 0
#     st.session_state.mass, st.session_state.velocity, st.session_state.height = random_values()
   
# def set_state(i):
#     st.session_state.stage = i
#     # 아래 st.sesstion_state를 해야 '문제 다시 만들기'에서 random_value 초기화됨.
#     if i == 0:
#         st.session_state.mass, st.session_state.velocity, st.session_state.height = random_values()

# if st.button('문제 풀어보기', on_click=set_state, args=[1]):
#     pass

# if st.session_state.stage >= 1:
#     st.write(f"물체의 질량: {st.session_state.mass} kg")
#     st.write(f"물체의 속도: {st.session_state.velocity} m/s")
#     st.write(f"물체의 높이: {st.session_state.height} m")
#     answer = st.number_input('운동에너지 계산(단위 J)', min_value=0, on_change=set_state, args=[2])

# if st.session_state.stage >= 2:
#     correct_answer = 0.5 * st.session_state.mass * (st.session_state.velocity**2)
#     st.write(f'정답이 {answer} J 맞는지 확인할게요!')
#     st.button('운동에너지 정답 확인', on_click=set_state, args=[3])

# if st.session_state.stage >= 3:
#     if answer == correct_answer:
#         st.write(f'정답입니다 :100:')
#     else:
#         st.write(f'다시 해볼게요! :sweat_smile:')
#     answer_Ep = st.number_input('위치에너지 계산(단위 J)', min_value=0.0, on_change=set_state, args=[4])

# if st.session_state.stage >= 4:
#     correct_answer_Ep = st.session_state.mass * 9.8 * st.session_state.height
#     st.button('위치에너지 정답 확인', on_click=set_state, args=[5])

# if st.session_state.stage >= 5:
#     if answer_Ep == correct_answer_Ep:
#         st.write(f'위치에너지 정답입니다 :100:')
#     else:
#         st.write(f'위치에너지 다시 해볼게요! :sweat_smile:')
#     st.button('문제 다시 만들기', on_click=set_state, args=[0])

# st.divider()

# 4번 구역
st.subheader('4. 프로젝트2 보고서: 실험 결과 한줄로 정리하기 :pencil:', divider='rainbow')

# 학생의 답안 입력 받기
student_result = st.text_input("**역학적 에너지와 운동에너지, 위치에너지의 관계를 포함하여 실험 결과를 한줄로 정리해보세요!** :blush:")

# 학생의 답안 보여주기
if st.button('한줄 보고서 제출'):
    st.write(f"**'{student_result}'** 라고 정리했군요! 수고했어요 :clap:")

st.divider()

# 5번 구역
st.subheader('[더 생각해보기] 오차는 무엇 때문일까? :upside_down_face:', divider='rainbow')



# 라디오 버튼으로 선택할 수 있는 옵션들
options = ['질량', '공기저항', '높이', '기타']

# 사용자가 라디오 버튼으로 선택
choice = st.radio("**실제 실험 결과를 보면 '역학적 에너지가 일정하게 보존된다'는 결론에서 벗어나는 오차가 나타나요. 오차의 이유로 생각되는 요인을 선택하세요. 우리 반 친구들의 의견은 어떨까요? 단어가 크면 응답횟수가 많다는 뜻이에요!**", options)

# 선택 사항의 클릭 수 추적
if 'click_count' not in st.session_state:
    st.session_state['click_count'] = {option: 0 for option in options}

st.session_state['click_count'][choice] += 1

# 선택된 응답을 클릭 수만큼 반복하여 워드 클라우드에 전달
if 'text' not in st.session_state:
    st.session_state.text = ''

st.session_state['text'] += ' '.join([choice] * st.session_state['click_count'][choice]) + ' '

# 워드 클라우드 생성
wordcloud = WordCloud(width=800, height=400, font_path= 'NanumGothic.ttf', background_color='white').generate(st.session_state['text'])

plt.figure(figsize=(8, 4))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")

# 워드 클라우드 이미지를 스트림릿에 표시
st.pyplot(plt)
st. divider()

st.header(':white_check_mark: Mission Clear!!! :tada:')
st. markdown('##### 자유 낙하 운동의 가속도부터 역학적 에너지 보존까지 완벽하게 분석했군요! 수고했어요 :clap:')