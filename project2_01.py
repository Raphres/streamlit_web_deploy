import streamlit as st
from st_pages import Page, show_pages, add_page_title
from PIL import Image

st.set_page_config(
      page_title="갈릴레오 프로젝트",
      page_icon="./Galileo.jpg",
      layout="wide"
)
image = Image.open('header4.jpg')
st.image(image)
st.subheader("")
st.title(":bookmark_tabs: 프로젝트명: 갈릴레오 프로젝트")
st.header(':ballot_box_with_check: Mission: 자유 낙하 운동 분석하기', divider='violet')
video_file = open('갈릴레이 실험1.mp4', 'rb')
video_bytes = video_file.read()
st.video(video_bytes)
st.divider()

st.subheader(':question: 질량이 다른 두 물체를 동시에 떨어뜨릴때 먼저 땅에 닿는 물체는?', divider='violet')

# contents 추가할 떄 마다 비율 나누기
con1,con2 = st.columns([1.0,2.2])

image = Image.open('갈릴레이 실험.jpg')
con1.image(image, caption='자유 낙하에 대한 두 가지 생각')

con2.subheader("자유 낙하 운동 논쟁: 아리스토텔레스 VS 갈릴레오")
with con2:
      st.markdown('질량이 다른 두 물체를 같은 높이에서 동시에 떨어뜨릴 때, 당시 대부분의 사람은 아리스토텔레스의 이론대로 질량이 큰 물체가 먼저 떨어진다고 생각했지만 갈릴레오는 물체에 작용하는 중력의 가속도는 물체의 질량과는 관계없이 일정하기 때문에 질량이 다른 두 물체는 같은 속도로 낙하하며 동시에 떨어질 것이라고 주장했다. 결과는 어땠을까?')
st.divider()

st.subheader(':brain: 생각해보기: 나의 예상은?', divider='violet')
with st.form(key='my_form'):
        st.markdown('##### :smile: 실험 결과를 예측해보자!')
        prediction = st.radio(
        "", 
        ["**갈릴레오가 맞다(동시에 떨어진다)**", "**아리스토텔레스가 맞다(질량이 큰 물체가 먼저 떨어진다)**"],
        captions = ["낙하하는데 걸리는 시간은 같으므로 중력 가속도는 질량에 관계 없이 같다.", "질량이 큰 물체의 낙하 시간이 짧으므로 중력 가속도는 질량이 큰 물체가 크다."])

        submitted = st.form_submit_button("나의 예상은?")
if submitted:
    st.write("나는 질량이 다른 두 물체의 자유낙하 결과 ", prediction, "고 생각해!") 
st.divider()
st.subheader(":eyes: 눈으로 확인하기: 누가 맞았을까?", divider='violet')
video_file = open('갈릴레이 실험3.mp4', 'rb')
video_bytes = video_file.read()
st.video(video_bytes)

st.markdown("#### **:bulb: 데이터로 검증하기: ':chart_with_upwards_trend: 프로젝트 1'로 가서 우리도 직접 확인해보자! :heavy_check_mark:**")

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
show_pages(
    [
        Page("project2_01.py", "갈릴레오 프로젝트", ":bookmark_tabs:"),
        Page("project2_02.py", "프로젝트 1: 가속도 확인", ":chart_with_upwards_trend:"),
        Page("project2_03.py", "프로젝트 2: 역학적 에너지 보존 확인", ":bar_chart:"),
    ]
)