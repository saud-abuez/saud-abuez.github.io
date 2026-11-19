# موقع «ديوان قصيد» — دليل النشر على GitHub Pages

## 1) النشر
1. أنشئ مستودعًا (Repository) جديدًا على GitHub، ثم ارفع **كل محتويات هذا المجلد** إلى الفرع `main`.
2. من **Settings ← Pages** اختر: Branch = `main` و Folder = `/ (root)` ثم Save.
3. بعد دقيقة يظهر الرابط في نفس الصفحة.

## 2) ثلاث تعديلات لازمة قبل التقديم على AdSense
ابحث في كل الملفات (VS Code: ‏Ctrl+Shift+H) واستبدل:
- `https://YOUR-DOMAIN.com` ← رابط موقعك الفعلي (النطاق الخاص).
- `YOUR_EMAIL@example.com` ← بريدك الإلكتروني الحقيقي (مطلوب في صفحة اتصل بنا وسياسة الخصوصية).

أو شغّل بدلًا من ذلك: `SITE_URL=https://نطاقك EMAIL=بريدك python build.py`

## 3) نطاق خاص (مهم جدًا لقبول AdSense)
- تفيد التقارير بأن مواقع `username.github.io` بدون نطاق خاص يصعب قبولها في AdSense، والأفضل شراء نطاق (مثل `diwan-qasid.com`).
- في Settings ← Pages ← Custom domain اكتب النطاق وفعّل Enforce HTTPS، وأنشئ سجل DNS حسب تعليمات GitHub.

## 4) بعد الرفع
- أضف الموقع إلى Google Search Console وأرسل `sitemap.xml`.
- قدّم طلب AdSense، ثم الصق كود AdSense في وسم `<head>` (يوجد تعليق يحدد المكان في `build.py` داخل دالة `layout`)، وحدّث `ads.txt`.

## 5) تعديل النصوص
كل نصوص القصائد في `data/poems.json`. عدّل الكلمة هناك ثم شغّل `python build.py` لتُحدَّث جميع الصفحات.
