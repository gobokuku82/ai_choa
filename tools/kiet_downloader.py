import requests, re, os
from bs4 import BeautifulSoup

BASE_PAGE = "https://www.kiet.re.kr/trends/indbriefList"
BASE_DOWNLOAD = "https://www.kiet.re.kr/common/file/userDownload"

def get_latest_pdf_url() -> str:
    res = requests.get(BASE_PAGE)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    # 첫 번째 다운로드 버튼 찾기
    tag = soup.find("a", class_="down pdf")
    if not tag or "onclick" not in tag.attrs:
        raise ValueError("❌ PDF 다운로드 링크를 찾을 수 없음")

    # onclick 속성 파싱
    onclick = tag["onclick"]
    m = re.search(r"filedownload\('(.+?)',\s*'(.+?)',\s*'(.+?)',\s*'(.+?)'\)", onclick)
    if not m:
        raise ValueError("❌ 파일다운로드 인자 파싱 실패")

    atch_no, menu_cd, lang, no = m.groups()

    # 실제 PDF URL 생성
    return f"{BASE_DOWNLOAD}?atch_no={atch_no}&menu_cd={menu_cd}&lang={lang}&no={no}"

def download_pdf_from_url(url: str, save_dir: str = "downloads") -> str | None:
    try:
        res = requests.get(url)
        res.raise_for_status()

        # 파일명 추출
        cd = res.headers.get("Content-Disposition", "")
        filename = re.search(r'filename="?(.+?)"?$', cd)
        if not filename:
            return None

        from urllib.parse import unquote
        decoded_name = unquote(filename.group(1))

        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, decoded_name)

        with open(save_path, "wb") as f:
            f.write(res.content)

        return save_path
    except Exception as e:
        print("❌ 다운로드 실패:", e)
        return None

def get_latest_titles(limit: int = 10) -> list[str]:
    res = requests.get("https://www.kiet.re.kr/trends/indbriefList")
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")
    items = soup.select("div.rpt_tit strong")
    return [item.text.strip() for item in items[:limit]]
