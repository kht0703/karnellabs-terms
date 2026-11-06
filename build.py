"""Karnel Labs 앱별 이용약관 페이지 생성기.

src/<slug>.md (한국어 {#ko} + 영어 {#en}) → <slug>/index.html
사용: python -I build.py   (이 저장소 루트에서)
수정은 src/*.md만 하고, 다시 빌드해 생성된 html까지 커밋한다.
"""
import html
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent
APPS = [
    # (slug, 페이지 제목, 패키지)
    ("bitey", "Bitey 이용약관 / Terms of Service", "com.karnellabs.bitey"),
    ("block-slide", "Block Slide 이용약관 / Terms of Service", "com.karnellabs.block_slide_puzzle"),
    ("block-reveal", "블록소녀 이용약관 / Terms of Service", "com.karnellabs.block_reveal_puzzle"),
]

CSS = """
:root{--bg:#ffffff;--fg:#1f2329;--muted:#6b7280;--line:#e5e7eb;--accent:#2563eb;--card:#f6f7f9}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#121316;--fg:#eceef2;--muted:#9ca3af;--line:#2a2d33;--accent:#7aa7ff;--card:#1b1d22}}
:root[data-theme="dark"]{--bg:#121316;--fg:#eceef2;--muted:#9ca3af;--line:#2a2d33;--accent:#7aa7ff;--card:#1b1d22}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.75 -apple-system,BlinkMacSystemFont,"Segoe UI","Apple SD Gothic Neo","Malgun Gothic",Roboto,sans-serif;word-break:keep-all;overflow-wrap:anywhere}
.wrap{max-width:760px;margin:0 auto;padding:24px 16px 56px}
.lang{display:flex;gap:8px;margin-bottom:8px}
.lang a{font-size:14px;padding:4px 12px;border:1px solid var(--line);border-radius:999px;text-decoration:none;color:var(--muted)}
h1{font-size:25px;line-height:1.35;margin:16px 0 8px;scroll-margin-top:16px}
h2{font-size:18px;margin:30px 0 8px}
p,li{margin:7px 0}
ul{padding-left:22px}
a{color:var(--accent)}
hr{border:0;border-top:1px solid var(--line);margin:48px 0}
.table{overflow-x:auto;margin:10px 0;border:1px solid var(--line);border-radius:10px}
table{border-collapse:collapse;width:100%;font-size:15px}
th,td{text-align:left;vertical-align:top;padding:9px 12px;border-bottom:1px solid var(--line)}
th{background:var(--card);font-weight:600;white-space:nowrap}
tr:last-child td{border-bottom:0}
footer{color:var(--muted);font-size:13px;margin-top:40px}
"""

URL_RE = re.compile(r'(?<![="\'>])(https?://[^\s<)]+)')


def render(md_text: str) -> str:
    body = markdown.markdown(md_text, extensions=["tables", "attr_list"], output_format="html")
    body = body.replace("<table>", '<div class="table"><table>').replace("</table>", "</table></div>")
    return URL_RE.sub(lambda m: f'<a href="{m.group(1)}">{m.group(1)}</a>', body)


def main() -> None:
    for slug, title, package in APPS:
        md_text = (ROOT / "src" / f"{slug}.md").read_text(encoding="utf-8")
        out = ROOT / slug / "index.html"
        out.parent.mkdir(exist_ok=True)
        out.write_text(f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<style>{CSS}</style>
</head>
<body><div class="wrap">
<nav class="lang"><a href="#ko">한국어</a><a href="#en">English</a></nav>
{render(md_text)}
<footer>© Karnel Labs · {package}</footer>
</div></body>
</html>
""", encoding="utf-8")
    (ROOT / "index.html").write_text(
        '<!doctype html><html lang="ko"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1"><title>Karnel Labs Terms</title>'
        f"<style>{CSS}</style></head><body><div class=wrap><h1>Karnel Labs 이용약관 / Terms of Service</h1><ul>"
        + "".join(f'<li><a href="{s}/">{html.escape(t)}</a></li>' for s, t, _ in APPS)
        + "</ul></div></body></html>",
        encoding="utf-8",
    )
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")
    print("built", ", ".join(s for s, _, _ in APPS))


if __name__ == "__main__":
    main()
