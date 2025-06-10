# app.py

import streamlit as st
from tools.kiet_downloader import (
    get_latest_pdf_url,
    download_pdf_from_url,
    get_latest_titles,
)
import os

st.set_page_config(page_title="KIET 브리프 자동 다운로드", page_icon="📄")
st.title("📄 KIET 산업동향 브리프 자동 다운로드")

# ⬇️ 최신 PDF 다운로드 영역
st.subheader("⬇️ 최신 브리프 다운로드")
st.markdown("가장 최근에 등록된 KIET 산업동향 브리프 PDF를 자동으로 다운로드합니다.")

if st.button("📥 최신 PDF 1개 다운로드"):
    try:
        with st.spinner("🔍 최신 파일 정보 가져오는 중..."):
            url = get_latest_pdf_url()

        with st.spinner("⬇️ 다운로드 중..."):
            path = download_pdf_from_url(url)

        if path:
            filename = os.path.basename(path)
            st.success(f"✅ 다운로드 완료: `{filename}`")
            with open(path, "rb") as f:
                st.download_button("📂 다운로드한 파일 열기", f, file_name=filename)
        else:
            st.error("❌ 다운로드 실패: 파일 저장에 실패했습니다.")
    except Exception as e:
        st.error(f"❌ 오류 발생: {e}")

# 📃 최신 10개 목록 표시
st.markdown("---")
st.subheader("📝 최근 등록된 KIET 브리프 목록 (상위 10개)")

try:
    titles = get_latest_titles(limit=10)
    for i, title in enumerate(titles, 1):
        st.write(f"{i}. {title}")
except Exception as e:
    st.error(f"❌ 제목 목록을 불러오지 못했습니다: {e}")
