import streamlit as st
st.title('hola 나이 첫 웹사이트!!')
name = st.text_input('당신의 이름 : ')
menu = st.selectbox('좋아하는 나라을 선택해주세요:', ['스페인','미국'])
if st.button('인사말 생성') : 
  st.write(name+'님! 당신이 좋아하는 나라는 '+menu+'이군요?! 저도 좋아요!!')
