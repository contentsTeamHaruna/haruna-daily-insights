#!/usr/bin/env python3
"""
index.html의 헤더 바로 아래에 '🗂️ 인스타 그리드 무드 체크 열기' 버튼을 주입합니다.
매일 생성되는 index.html이 버튼을 포함하지 않을 때,
.github/workflows/preserve-grid-button.yml이 이 스크립트를 호출해 자동 복구합니다.
"""
import pathlib
import re

SNIPPET = """
  <div id="toolLinks" style="text-align:center;margin:-8px 0 28px;">
    <a href="./grid_mood_check.html" style="display:inline-flex;align-items:center;gap:8px;padding:11px 22px;background:#1a1815;color:#fff;border-radius:24px;text-decoration:none;font-size:14px;font-weight:600;box-shadow:0 4px 12px rgba(26,24,21,0.15);transition:transform 0.15s, box-shadow 0.15s;" onmouseover="this.style.transform='translateY(-1px)';this.style.boxShadow='0 6px 18px rgba(26,24,21,0.22)';" onmouseout="this.style.transform='';this.style.boxShadow='0 4px 12px rgba(26,24,21,0.15)';">
      🗂️ 인스타 그리드 무드 체크 열기
      <span style="opacity:0.6;font-size:13px;">→</span>
    </a>
  </div>

"""


def inject(html: str) -> str:
    if "grid_mood_check.html" in html:
        return html

    # 1순위: 헤더 </div> 닫히고 바로 뒤 <div class="tabs" id="tabs">가 오는 지점
    pattern = re.compile(
        r'(</div>\s*)(<div class="tabs" id="tabs">)', re.DOTALL
    )
    new_html, n = pattern.subn(r"\1" + SNIPPET + r"  \2", html, count=1)
    if n == 0:
        # fallback: <body> 바로 다음에 삽입
        new_html = html.replace("<body>", "<body>\n" + SNIPPET, 1)
    return new_html


def main():
    path = pathlib.Path("index.html")
    html = path.read_text(encoding="utf-8")
    new_html = inject(html)
    if new_html == html:
        print("button already present, no change")
        return
    path.write_text(new_html, encoding="utf-8")
    print("button injected into index.html")


if __name__ == "__main__":
    main()
