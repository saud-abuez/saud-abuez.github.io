# -*- coding: utf-8 -*-
"""
مولّد موقع «ديوان قصيد» — شغّله بالأمر:  python build.py
المصدر الوحيد للنصوص هو الملف data/poems.json (عدّل فيه أي كلمة ثم أعد التشغيل).
يمكنك تغيير الإعدادات من الأعلى أو عبر متغيرات البيئة SITE_URL و EMAIL.
"""
import json, os, html, datetime, shutil

# ───────── الإعدادات ─────────
SITE_NAME = "ديوان قصيد"
POET      = "محمد بن علي آل عمره المري"
NICK      = "راعي اللبل"                      # كما هو مكتوب في الديوان
SITE_URL  = os.environ.get("SITE_URL", "https://YOUR-DOMAIN.com").rstrip("/")
EMAIL     = os.environ.get("EMAIL", "YOUR_EMAIL@example.com")
OUT       = os.path.dirname(os.path.abspath(__file__))
LONG_MIN  = 4   # القصيدة التي فيها هذا العدد من الأبيات فأكثر تأخذ صفحة مستقلة
TODAY     = datetime.date.today()
MONTHS    = ["يناير","فبراير","مارس","أبريل","مايو","يونيو","يوليو","أغسطس","سبتمبر","أكتوبر","نوفمبر","ديسمبر"]
TODAY_AR  = f"{TODAY.day} {MONTHS[TODAY.month-1]} {TODAY.year}"

DESC = {
 "nasaeh":    "قصائد في النصح والحكمة وتجارب الحياة.",
 "qasira":    "أبيات قصيرة ونصائح مركّزة في قصائد موجزة.",
 "ibil":      "قصائد عن الإبل وأهلها ومواقف راعيها.",
 "wataniyat": "قصائد وطنية في حب الوطن وقيادته.",
 "jeeb":      "قصائد عن الجيب والسفر به.",
 "madh":      "قصائد مدح وتقدير لأهل الفضل.",
 "amma":      "قصائد متنوعة في موضوعات عامة.",
}

esc = html.escape
data = json.load(open(os.path.join(OUT, "data", "poems.json"), encoding="utf-8"))
sections = data["sections"]

def n_poems(n):
    return "قصيدة واحدة" if n == 1 else "قصيدتان" if n == 2 else f"{n} قصائد" if n <= 10 else f"{n} قصيدة"
def n_verses(n):
    return "بيت واحد" if n == 1 else "بيتان" if n == 2 else f"{n} أبيات" if n <= 10 else f"{n} بيتًا"

for s in sections:
    for p in s["poems"]:
        p["long"] = len(p["verses"]) >= LONG_MIN
        p["section"] = s
        p["url"] = f"poems/{p['id']:03d}.html" if p["long"] else f"sections/{s['slug']}.html#p{p['id']}"
    s["long"] = [p for p in s["poems"] if p["long"]]

all_poems = [p for s in sections for p in s["poems"]]
TOTAL_POEMS = len(all_poems)
TOTAL_VERSES = sum(len(p["verses"]) for p in all_poems)

# ───────── القالب العام ─────────
def layout(title, desc, body, root, path, jsonld=None, og_image=True):
    canon = f"{SITE_URL}/{path}" if path else f"{SITE_URL}/"
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    img = f'<meta property="og:image" content="{SITE_URL}/assets/portrait.jpg">' if og_image else ""
    nav = f"""
      <a href="{root}index.html">الرئيسية</a>
      <a href="{root}index.html#sections">الأقسام</a>
      <a href="{root}about.html">عن الشاعر</a>
      <a href="{root}contact.html">اتصل بنا</a>"""
    sec_links = "".join(f'<li><a href="{root}sections/{s["slug"]}.html">{esc(s["title"])}</a></li>' for s in sections)
    return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:locale" content="ar_AR">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canon}">
{img}
<meta name="theme-color" content="#2e5b4c">
<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&amp;family=Tajawal:wght@400;500;700&amp;display=swap">
<link rel="stylesheet" href="{root}assets/style.css">
<!-- AdSense: بعد قبول الموقع الصق هنا كود Google AdSense الذي يعطيك إياه (انظر README.md) -->
{ld}
</head>
<body>
<a class="skip" href="#main">تخطَّ إلى المحتوى</a>
<header class="site-header">
  <div class="wrap bar">
    <a class="brand" href="{root}index.html">{SITE_NAME}</a>
    <nav aria-label="القائمة الرئيسية">{nav}
    </nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap foot-grid">
    <div>
      <strong class="foot-brand">{SITE_NAME}</strong>
      <p>ديوان الشاعر {esc(POET)} ({esc(NICK)}) — قصائده مرتبة في أقسام لتسهيل القراءة.</p>
    </div>
    <div>
      <h2>الأقسام</h2>
      <ul>{sec_links}</ul>
    </div>
    <div>
      <h2>الموقع</h2>
      <ul>
        <li><a href="{root}about.html">عن الشاعر والديوان</a></li>
        <li><a href="{root}contact.html">اتصل بنا</a></li>
        <li><a href="{root}privacy.html">سياسة الخصوصية</a></li>
        <li><a href="{root}terms.html">الشروط وإخلاء المسؤولية</a></li>
      </ul>
    </div>
  </div>
  <p class="copy">© {TODAY.year} {SITE_NAME} — حقوق القصائد محفوظة لأصحابها.</p>
</footer>
<script src="{root}assets/site.js" defer></script>
</body>
</html>
"""

def write(path, content):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full) or OUT, exist_ok=True)
    open(full, "w", encoding="utf-8").write(content)

def verse_html(v):
    cls = {"pair": "verse", "triple": "verse triple", "stack": "verse stack"}[v["layout"]]
    return f'<div class="{cls}">' + "".join(f"<p>{esc(l)}</p>" for l in v["lines"]) + "</div>"

def verses_html(p):
    return '<div class="poem-body">' + '<div class="orn" aria-hidden="true">❖</div>'.join(verse_html(v) for v in p["verses"]) + "</div>"

def notes_html(p):
    return "".join(f'<aside class="note"><strong>عن القصيدة</strong><p>{esc(n)}</p></aside>' for n in p["notes"])

def preview(p):
    return p["verses"][0]["lines"][1] if len(p["verses"][0]["lines"]) > 1 else ""

def crumbs(items):
    out = []
    for i, (label, href) in enumerate(items):
        out.append(f'<a href="{href}">{esc(label)}</a>' if href else f'<span aria-current="page">{esc(label)}</span>')
    return '<nav class="crumbs" aria-label="مسار التنقل">' + " <i>‹</i> ".join(out) + "</nav>"

# ───────── الصفحة الرئيسية ─────────
featured = [s["long"][0] for s in sections if s["long"]]
cards = ""
for s in sections:
    first = s["poems"][0]
    cards += f"""
    <a class="sec-card" href="sections/{s['slug']}.html">
      <h3>{esc(s['title'])}</h3>
      <p class="muted">{esc(DESC[s['slug']])}</p>
      <p class="sample">«{esc(first['title'])}»</p>
      <span class="count">{n_poems(len(s['poems']))}</span>
    </a>"""
feat = "".join(f"""
    <a class="poem-link" href="{p['url']}">
      <span class="tag">{esc(p['section']['title'])}</span>
      <h3>{esc(p['title'])}</h3>
      <p>{esc(preview(p))}</p>
    </a>""" for p in featured)

home = f"""
<section class="hero">
  <div class="wrap hero-grid">
    <img class="portrait" src="assets/portrait.jpg" width="320" height="320" alt="الشاعر {esc(POET)}">
    <div>
      <p class="eyebrow">ديوان شعري</p>
      <h1>{SITE_NAME}</h1>
      <p class="poet">للشاعر <strong>{esc(POET)}</strong> <span>({esc(NICK)})</span></p>
      <p class="lead">قصائد الشاعر مجموعة في ديوان واحد ومرتبة في أقسام: النصح، والإبل، والوطنيات، والجيب، والمدح، وغيرها. تصفّح الأقسام أو ابحث عن أي كلمة أو بيت.</p>
      <ul class="stats" aria-label="إحصاءات الديوان">
        <li><b>{TOTAL_POEMS}</b> قصيدة</li><li><b>{TOTAL_VERSES}</b> بيتًا</li><li><b>{len(sections)}</b> أقسام</li>
      </ul>
    </div>
  </div>
</section>

<section class="wrap search-box" aria-labelledby="search-h">
  <h2 id="search-h" class="sr">البحث في الديوان</h2>
  <label for="q">ابحث في الديوان</label>
  <input id="q" type="search" placeholder="اكتب كلمة أو جزءًا من بيت…" autocomplete="off">
  <div id="results" class="results" aria-live="polite"></div>
</section>

<section id="sections" class="wrap block">
  <h2 class="h-sec">أقسام الديوان</h2>
  <div class="grid sec-grid">{cards}
  </div>
</section>

<section class="wrap block">
  <h2 class="h-sec">من قصائد الديوان</h2>
  <div class="grid feat-grid">{feat}
  </div>
</section>

<section class="wrap block about-strip">
  <h2 class="h-sec">عن الديوان</h2>
  <p>«{SITE_NAME}» ديوان يضم قصائد الشاعر {esc(POET)} ({esc(NICK)}). أُنشئ هذا الموقع لحفظ القصائد وتسهيل قراءتها ومشاركتها، وقد نُقلت النصوص كما وردت في الديوان.</p>
  <p><a class="btn" href="about.html">اقرأ المزيد عن الشاعر</a></p>
</section>
"""
ld_home = {"@context": "https://schema.org", "@type": "WebSite", "name": SITE_NAME, "url": SITE_URL + "/", "inLanguage": "ar",
           "about": {"@type": "Person", "name": POET, "alternateName": NICK}}
write("index.html", layout(f"{SITE_NAME} — قصائد {POET}", f"ديوان قصيد للشاعر {POET} ({NICK}): قصائد النصح والإبل والوطنيات والجيب والمدح وغيرها، مرتبة في أقسام مع بحث داخل الديوان.", home, "", "", ld_home))

# ───────── صفحات الأقسام ─────────
for s in sections:
    items = ""
    num = 0
    for p in s["poems"]:
        num += 1
        if p["long"]:
            items += f"""
    <a class="poem-link wide" id="p{p['id']}" href="../{p['url']}">
      <span class="tag">{n_verses(len(p['verses']))}</span>
      <h2>{esc(p['title'])}</h2>
      <p>{esc(preview(p))}</p>
      <span class="more">اقرأ القصيدة كاملة ←</span>
    </a>"""
        else:
            items += f"""
    <article class="poem-card" id="p{p['id']}">
      <span class="tag">قصيدة {num} · {n_verses(len(p['verses']))}</span>
      {notes_html(p)}
      {verses_html(p)}
    </article>"""
    body = f"""
<div class="wrap page-head">
  {crumbs([("الرئيسية","../index.html"),(s['title'],None)])}
  <h1>{esc(s['title'])}</h1>
  <p class="lead">{esc(DESC[s['slug']])} <span class="muted">({n_poems(len(s['poems']))})</span></p>
</div>
<div class="wrap list">{items}
</div>"""
    write(f"sections/{s['slug']}.html", layout(f"{s['title']} | {SITE_NAME}",
        f"{s['title']} من ديوان {POET}: {DESC[s['slug']]} تضم {n_poems(len(s['poems']))}.", body, "../", f"sections/{s['slug']}.html"))

# ───────── صفحات القصائد الطويلة ─────────
for s in sections:
    L = s["long"]
    for i, p in enumerate(L):
        prev_p = L[i-1] if i > 0 else None
        next_p = L[i+1] if i < len(L)-1 else None
        pn = ""
        if prev_p: pn += f'<a class="pn prev" href="{prev_p["id"]:03d}.html"><small>القصيدة السابقة</small>{esc(prev_p["title"])}</a>'
        if next_p: pn += f'<a class="pn next" href="{next_p["id"]:03d}.html"><small>القصيدة التالية</small>{esc(next_p["title"])}</a>'
        more = "".join(f'<li><a href="{q["id"]:03d}.html">{esc(q["title"])}</a></li>' for q in (L[i+1:i+5] or L[:4]) if q is not p)
        body = f"""
<article class="wrap poem-page">
  {crumbs([("الرئيسية","../index.html"),(s['title'],f"../sections/{s['slug']}.html"),("القصيدة",None)])}
  <header class="poem-head">
    <p class="tag">{esc(s['title'])} · {n_verses(len(p['verses']))}</p>
    <h1>{esc(p['title'])}</h1>
    <p class="muted">للشاعر {esc(POET)}</p>
  </header>
  {notes_html(p)}
  {verses_html(p)}
  <p class="center"><button class="btn ghost" id="copy-link" type="button">نسخ رابط القصيدة</button></p>
  <div class="pn-row">{pn}</div>
  <section class="more-list"><h2>المزيد من {esc(s['title'])}</h2><ul>{more}</ul>
    <p><a href="../sections/{s['slug']}.html">عرض كل قصائد القسم ←</a></p></section>
</article>"""
        desc = " — ".join(p["verses"][0]["lines"][:2]) + f" | من ديوان {POET}"
        ld = {"@context": "https://schema.org", "@type": "CreativeWork", "name": p["title"], "inLanguage": "ar",
              "genre": "شعر", "author": {"@type": "Person", "name": POET}, "isPartOf": {"@type": "Book", "name": SITE_NAME}}
        write(f"poems/{p['id']:03d}.html", layout(f"{p['title']} | {s['title']} | {SITE_NAME}", desc, body, "../", f"poems/{p['id']:03d}.html", ld))

# ───────── فهرس البحث ─────────
idx = [{"t": p["title"], "s": p["section"]["title"], "u": p["url"], "x": " | ".join(l for v in p["verses"] for l in v["lines"])} for p in all_poems]
write("assets/search-index.js", "window.DIWAN_INDEX=" + json.dumps(idx, ensure_ascii=False) + ";")
hp = open(os.path.join(OUT, "index.html"), encoding="utf-8").read()
hp = hp.replace('<script src="assets/site.js" defer></script>', '<script src="assets/search-index.js" defer></script>\n<script src="assets/site.js" defer></script>')
write("index.html", hp)

# ───────── عن الشاعر ─────────
sec_list = "".join(f'<li><a href="sections/{s["slug"]}.html">{esc(s["title"])}</a> — {n_poems(len(s["poems"]))}</li>' for s in sections)
about = f"""
<div class="wrap page-head">
  {crumbs([("الرئيسية","index.html"),("عن الشاعر",None)])}
  <h1>عن الشاعر والديوان</h1>
</div>
<div class="wrap prose about-grid">
  <img class="portrait" src="assets/portrait.jpg" width="320" height="320" loading="lazy" alt="الشاعر {esc(POET)}">
  <div>
    <h2>الشاعر</h2>
    <p>الشاعر <strong>{esc(POET)}</strong>، ويُعرف بلقب <strong>({esc(NICK)})</strong>.</p>
    <h2>الديوان</h2>
    <p>«{SITE_NAME}» مجموعة قصائد الشاعر، جُمعت في ديوان واحد وقُسّمت إلى أقسام بحسب موضوعاتها. يضم الديوان {n_poems(TOTAL_POEMS)} و{n_verses(TOTAL_VERSES)}.</p>
    <h2>أقسام الديوان</h2>
    <ul>{sec_list}</ul>
    <h2>عن الموقع</h2>
    <p>أُنشئ هذا الموقع لحفظ قصائد الشاعر وتسهيل قراءتها والبحث فيها ومشاركتها. نُقلت النصوص كما وردت في الديوان، وقد يختلف الإملاء في بعض الكلمات عن الفصحى لأن القصائد مكتوبة باللهجة العامية.</p>
    <p>لتصحيح خطأ طباعي أو للتواصل معنا زر صفحة <a href="contact.html">اتصل بنا</a>.</p>
  </div>
</div>"""
write("about.html", layout(f"عن الشاعر والديوان | {SITE_NAME}", f"نبذة عن الشاعر {POET} ({NICK}) وعن ديوان قصيد وأقسامه.", about, "", "about.html"))

# ───────── اتصل بنا ─────────
contact = f"""
<div class="wrap page-head">
  {crumbs([("الرئيسية","index.html"),("اتصل بنا",None)])}
  <h1>اتصل بنا</h1>
</div>
<div class="wrap prose narrow">
  <p>يسعدنا تواصلك معنا لأي من الأمور التالية:</p>
  <ul>
    <li>الإبلاغ عن خطأ طباعي أو كلمة تختلف عن الديوان الأصلي.</li>
    <li>الاستفسار عن القصائد أو طلب الإذن بإعادة نشرها.</li>
    <li>الملاحظات والاقتراحات لتحسين الموقع.</li>
  </ul>
  <p>راسلنا على البريد الإلكتروني:</p>
  <p><a class="btn" href="mailto:{EMAIL}">{EMAIL}</a></p>
  <p class="muted">نحاول الرد خلال أيام قليلة.</p>
</div>"""
write("contact.html", layout(f"اتصل بنا | {SITE_NAME}", f"طرق التواصل مع موقع {SITE_NAME}: الإبلاغ عن خطأ، الاستفسار، أو الاقتراحات.", contact, "", "contact.html"))

# ───────── سياسة الخصوصية ─────────
privacy = f"""
<div class="wrap page-head">
  {crumbs([("الرئيسية","index.html"),("سياسة الخصوصية",None)])}
  <h1>سياسة الخصوصية</h1>
  <p class="muted">آخر تحديث: {TODAY_AR}</p>
</div>
<div class="wrap prose narrow">
  <h2>مقدمة</h2>
  <p>نحترم خصوصية زوّار موقع «{SITE_NAME}». توضح هذه الصفحة أنواع المعلومات التي قد تُجمع عند زيارتك للموقع وكيف تُستخدم.</p>
  <h2>المعلومات التي نجمعها</h2>
  <p>لا يطلب الموقع التسجيل ولا يجمع بيانات شخصية مباشرة منك. وكما هو معتاد في المواقع، قد تسجّل خدمة الاستضافة بيانات تقنية قياسية مثل عنوان IP ونوع المتصفح والصفحات التي زرتَها ووقت الزيارة، وذلك لأغراض التشغيل والأمان.</p>
  <h2>ملفات تعريف الارتباط (Cookies)</h2>
  <p>ملفات تعريف الارتباط ملفات صغيرة تُحفظ على جهازك. قد يستخدمها الموقع أو شركاؤه لتحسين التجربة وعرض الإعلانات. يمكنك التحكم فيها أو حذفها من إعدادات متصفحك.</p>
  <h2>الإعلانات وGoogle AdSense</h2>
  <p>قد نعرض إعلانات عبر خدمة Google AdSense. تستخدم Google وشركاؤها ملفات تعريف الارتباط لعرض إعلانات بناءً على زياراتك السابقة لهذا الموقع أو لمواقع أخرى. ويتيح استخدام ملف DART لـ Google ولشركائها عرض إعلانات لك بناءً على زيارتك لهذا الموقع و/أو مواقع أخرى على الإنترنت.</p>
  <p>يمكنك إيقاف الإعلانات المخصصة من <a href="https://adssettings.google.com" rel="noopener" target="_blank">إعدادات إعلانات Google</a>، أو زيارة <a href="https://www.aboutads.info" rel="noopener" target="_blank">aboutads.info</a>. ولمعرفة المزيد عن كيفية استخدام Google للبيانات راجع <a href="https://policies.google.com/technologies/ads" rel="noopener" target="_blank">سياسة إعلانات Google</a>.</p>
  <h2>خدمات الأطراف الثالثة</h2>
  <p>يحمّل الموقع الخطوط من خدمة Google Fonts، وقد تتلقى Google عنوان IP الخاص بك عند تحميلها. وقد تحتوي الصفحات على روابط لمواقع خارجية لا نتحكم في سياسات الخصوصية فيها.</p>
  <h2>خصوصية الأطفال</h2>
  <p>لا يستهدف الموقع الأطفال دون سن 13 عامًا، ولا نجمع عمدًا بيانات شخصية منهم.</p>
  <h2>حقوقك</h2>
  <p>إن كنت من المقيمين في المنطقة الاقتصادية الأوروبية أو المملكة المتحدة فقد تُعرض عليك رسالة للموافقة على ملفات تعريف الارتباط الخاصة بالإعلانات، ويحق لك سحب موافقتك في أي وقت.</p>
  <h2>التغييرات على هذه السياسة</h2>
  <p>قد نحدّث هذه السياسة من حين لآخر، وسيظهر تاريخ آخر تحديث أعلى الصفحة.</p>
  <h2>التواصل</h2>
  <p>لأي استفسار عن الخصوصية راسلنا عبر <a href="contact.html">صفحة اتصل بنا</a> أو على البريد <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
</div>"""
write("privacy.html", layout(f"سياسة الخصوصية | {SITE_NAME}", f"سياسة الخصوصية لموقع {SITE_NAME}: المعلومات التي تُجمع وملفات تعريف الارتباط وإعلانات Google AdSense.", privacy, "", "privacy.html"))

# ───────── الشروط ─────────
terms = f"""
<div class="wrap page-head">
  {crumbs([("الرئيسية","index.html"),("الشروط وإخلاء المسؤولية",None)])}
  <h1>الشروط وإخلاء المسؤولية</h1>
  <p class="muted">آخر تحديث: {TODAY_AR}</p>
</div>
<div class="wrap prose narrow">
  <h2>حقوق المحتوى</h2>
  <p>قصائد هذا الموقع هي من نظم الشاعر {esc(POET)}، وحقوقها محفوظة لأصحابها. يُسمح بالقراءة ومشاركة روابط الصفحات، ويجوز الاقتباس القصير مع ذكر اسم الشاعر والموقع. ولا يجوز إعادة نشر الديوان أو أجزاء كبيرة منه أو استخدامه تجاريًا دون إذن كتابي.</p>
  <h2>دقة النصوص</h2>
  <p>نُقلت القصائد كما وردت في الديوان. وما قد يظهر من اختلاف في الإملاء عن الفصحى سببه أن القصائد مكتوبة باللهجة العامية كما نظمها الشاعر. وإن لاحظت خطأً طباعيًا فنرجو إبلاغنا عبر <a href="contact.html">صفحة اتصل بنا</a>.</p>
  <h2>إخلاء المسؤولية</h2>
  <p>المحتوى مقدَّم للقراءة والاطلاع الأدبي، وما يرد في القصائد من آراء ونصائح يعبّر عن الشاعر ولا يُعدّ استشارة مهنية. نبذل جهدنا لدقة المعلومات لكننا لا نضمن خلو الموقع من الأخطاء أو استمرار توفره دون انقطاع.</p>
  <h2>الإعلانات والروابط الخارجية</h2>
  <p>قد يعرض الموقع إعلانات من أطراف ثالثة، ولسنا مسؤولين عن محتوى المعلنين أو المواقع الخارجية المرتبطة بالموقع. للتفاصيل راجع <a href="privacy.html">سياسة الخصوصية</a>.</p>
  <h2>التعديلات</h2>
  <p>نحتفظ بحق تعديل هذه الشروط في أي وقت، ويُعدّ استمرارك في استخدام الموقع موافقةً على النسخة المحدّثة.</p>
</div>"""
write("terms.html", layout(f"الشروط وإخلاء المسؤولية | {SITE_NAME}", f"شروط استخدام موقع {SITE_NAME} وحقوق المحتوى وإخلاء المسؤولية.", terms, "", "terms.html"))

# ───────── 404 ─────────
nf = """
<div class="wrap page-head center">
  <h1>الصفحة غير موجودة</h1>
  <p class="lead">ربما تغيّر الرابط أو حُذفت الصفحة.</p>
  <p><a class="btn" href="/">العودة إلى الرئيسية</a></p>
</div>"""
write("404.html", layout(f"الصفحة غير موجودة | {SITE_NAME}", "الصفحة المطلوبة غير موجودة.", nf, "/", "404.html", og_image=False).replace('href="/assets', 'href="/assets').replace('href="//', 'href="/'))

# ───────── sitemap / robots / ads.txt ─────────
urls = [""] + [f"sections/{s['slug']}.html" for s in sections] + [f"poems/{p['id']:03d}.html" for p in all_poems if p["long"]] + ["about.html","contact.html","privacy.html","terms.html"]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"  <url><loc>{SITE_URL}/{u}</loc><lastmod>{TODAY.isoformat()}</lastmod></url>\n" for u in urls) + "</urlset>\n"
write("sitemap.xml", sm)
write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")
write("ads.txt", "# بعد قبول الموقع في AdSense استبدل هذا السطر بالسطر الذي يعطيك إياه AdSense، مثال:\n# google.com, pub-0000000000000000, DIRECT, f08c47fec0942fa0\n")
write(".nojekyll", "")

print(f"OK: {len(urls)} صفحة | {TOTAL_POEMS} قصيدة | {TOTAL_VERSES} بيت | صفحات قصائد مستقلة: {sum(len(s['long']) for s in sections)}")
