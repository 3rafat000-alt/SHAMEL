# شامل / SHAMEL — مصنع المشاريع: طريقة البناء الموحّدة

**التاريخ:** 2026-07-10 · **الوثيقة:** تصميم ملزم (design spec) لطبقة المشاريع في نظام شامل · **الموطن المستقبلي:** `~/Desktop/SHAMEL/`
**المصادر المسنودة:** `06-projects-structure.md` (تدقيق PRJ-SAKK الحي) · `08-COMPARISON-MATRIX.md` (§3 البنود 19–20) · `09-GAP-ANALYSIS.md` (GAP-01/03/04/09/12/13)
**المبدأ الحاكم:** مصدر حقيقة واحد لكل concern · الكود هو الحقيقة (أرقام الدماغ تُولَّد لا تُكتب) · لا ادعاء بلا إنفاذ آلي fail-closed · كل مشروع ريبو git خاص منذ اللحظة صفر.

---

## 0) النطاق وخريطة المسارات

نظام شامل يفصل فصلاً قاطعاً بين **ريبو الإطار** (framework) و**ريبوات المشاريع** (products):

```
~/Desktop/SHAMEL/                  ← ريبو الإطار (git واحد: العقيدة، الوكلاء، الأدوات)
├── .gitignore                     ← يحوي سطر  /projects/  (المشاريع ليست ملفاته)
└── projects/                      ← الجذر الفيزيائي الوحيد للمشاريع
    ├── PRJ-SAKK/    (.git خاص)   ← كل مشروع ريبو git مستقل كامل
    ├── PRJ-ALPHA/   (.git خاص)
    └── README.md                  ← مؤشر فقط (كيف تنشئ/تستورد مشروعاً)
```

**قانون حلّ المسار (يخلف `paths.py` — علاج GAP-09):** سُلّم صريح **fail-loud**:

1. `SHAMEL_PROJECTS_DIR` (env) إن ضُبط — ويُتحقق من وجوده فعلياً.
2. `~/Desktop/SHAMEL/projects/` إن وُجد.
3. **لا fallback ثالث صامت.** غياب الاثنين = خطأ صريح `exit ≠ 0` برسالة `projects root not found — set SHAMEL_PROJECTS_DIR`. (الدرس: `projects_dir()` في v6 كان يرجع مساراً معدوماً بصمت فعمِيت كل الأدوات عن المشروع الوحيد الحي — تقرير 06 §الصحة.)

قاعدة worktrees: الحلّ يجري من **جذر الإطار الحقيقي** (`git rev-parse --git-common-dir`) لا من جذر الـ worktree — فلا يتكرر عمى v6.

---

## 1) الهيكل القانوني (canonical) لكل PRJ-XXXX

### 1.1 الاصطلاح السداسي المحسّن

ستة مجلدات قانونية ثابتة + واحد شرطي + اثنان خدميان. **لا اجتهاد في المستوى الأعلى** — أي مجلد آخر في الجذر يفشل فحص `shamel folder-map --check` في CI:

| # | المجلد | الوضع | المحتوى |
|---|--------|-------|---------|
| 1 | `_context/` | إلزامي | دماغ المشروع + سجل artifacts البوابات |
| 2 | `backend/` | إلزامي (لمنتج له خادم) | Laravel — **والويب داخله افتراضياً** (Blade+Vue) |
| 3 | `frontend/` | **شرطي** | SPA مستقل فقط — لا يوجد بلا ADR (انظر §1.2) |
| 4 | `mobile/` | شرطي (حسب النطاق) | Flutter feature-first |
| 5 | `docs/` | إلزامي | 8 مقاطع قياسية + `FOLDER-MAP.md` (§5) |
| 6 | `deploy/` | إلزامي | كل ما يلزم لتشغيل المنتج خارج جهاز المطور (§7) |
| 7 | `tests/` | إلزامي | الاختبارات **العابرة للطبقات** فقط: e2e / integration / load |
| — | `_scratch/` | خدمي، gitignored | سكربتات مؤقتة، تُطهَّر عند إغلاق كل بوابة |
| — | `.github/` | خدمي، tracked | CI workflows داخل المشروع (§7) |

ملاحظتان تصحيحيتان على واقع v6 (تقرير 06 §نقاط الضعف 3):

- **يُلغى مستوى `src/`** — سكافولدر v6 كان يولّد `src/{backend,frontend,mobile}` بينما SAKK الفعلي بمستوى أعلى مباشرة؛ الشكل القانوني الواحد هو المستوى الأعلى المباشر (`backend/` لا `src/backend/`). scaffold = واقع = خريطة، بلا استثناء.
- اختبارات unit تسكن **داخل طبقتها** (`backend/tests/`, `mobile/test/`) بأدوات الطبقة نفسها؛ `tests/` الجذري حصراً لما يعبر الطبقات. مجلد فارغ فيه (كما كانت `integration/` و`load/` في SAKK) = فشل فحص FOLDER-MAP، لا وعد معلّق.

### 1.2 قرار الويب — Pattern A (افتراضي) مقابل Pattern B (بـ ADR فقط)

الدرس من SAKK: ثلاث روايات للويب كلها ≠ الكود (IMPORTED.md «Next.js 16» — معدوم؛ STATE «Blade+Vue3» — صفر ملف `.vue`؛ الفعلي Blade+Tailwind) — GAP-12. شامل يقفل الباب بقاعدة ثنائية حاسمة:

**Pattern A — Monolith (الافتراضي، بلا قرار):**
الويب يعيش داخل `backend/resources/` كـ **Blade + Vue 3 (جزر تفاعلية) + Tailwind عبر Vite**. deployable واحد، `composer.json` + `package.json` واحدان، جلسة auth واحدة.
**متى:** الحالة العامة — لوحات إدارة، منتجات server-rendered، أي مشروع لا يستوفي شرطاً من شروط B. (واقع SAKK — 38 Blade view تعمل — يثبت كفايته.)

**Pattern B — `frontend/` مستقل:**
SPA/PWA له `package.json` وbuild pipeline وdeployable خاص، يستهلك **عقد OpenAPI المجمّد** تماماً كما يستهلكه `mobile/` (typed client، لا وصول مباشر لقاعدة البيانات).
**متى (يكفي شرط واحد):** متطلب offline/PWA أو client-state ثقيل مثبت في `GATE2-UX-ARCH` · إيقاع إصدار مستقل عن الـ backend · squad ويب منفصل يعمل بالتوازي خلف العقد المجمّد · backend غير Laravel.

**قواعد الإنفاذ:**

1. القرار يُتخذ عند **Gate 3** بيد `arc-system-architect`، ويُسجَّل ADR في `_context/DECISIONS.md` **قبل** أن يظهر مجلد `frontend/` على القرص. مجلد `frontend/` بلا ADR = فشل `folder-map --check`. **استثناء يوم-الصفر الوحيد:** `shamel new --web B` يكتب `ADR-000 (web_pattern: B)` في `DECISIONS.md` تلقائياً **قبل** إنشاء المجلد، بمصدر إلزامي (`--adr-source`: قرار مالك صريح، أو تقرير `shamel import scan` في مسار الاستيراد §6)؛ بلا مصدر يُرفض `--web B` كله قبل إنشاء أي شيء. `arc-system-architect` يصادق على ADR-000 أو ينقضه عند Gate 3 — فالقاعدة تبقى أحادية القراءة: لا `frontend/` على القرص إلا وADR يسبقه.
2. **لا ازدواج شاشات أبداً:** الشاشة الواحدة تُبنى في A أو B، لا كليهما — مصدر حقيقة واحد لكل شاشة.
3. `STATE.md` يحمل حقلاً مولّداً `web_pattern: A|B` يفحصه سكربت الحقائق (§1.4) ضد القرص الفعلي (وجود `.vue` داخل backend أم `frontend/package.json`) — فلا تتكرر رواية «Vue 3» فوق صفر ملف vue.

### 1.3 الشجرة الكاملة المشروحة

```
PRJ-XXXX/                              ← ريبو git مستقل (قانون §2)
├── .git/                              ← يوم-صفر، ينشئه السكافولدر نفسه
├── .gitignore                         ← يولَّد قياسياً (انظر أدناه)
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                     ← lint→test→build→scan (§7) — بوابة Gate 5/6
│   │   └── deploy.yml                 ← staging/prod (يُفعَّل عند Gate 6)
│   └── shamel/                        ← سكربتا الفحص المستقلان folder_map.py · facts.py (§7.1)
├── README.md                          ← هوية المشروع + أوامر التشغيل الثلاثة الأولى
│
├── _context/                          ← الدماغ (يُصدَّر مع المشروع — في ريبو المشروع نفسه)
│   ├── STATE.md                       ← الحالة الحية: gate/branch/head_sha/domain (frontmatter §3.4)
│   ├── FOUNDATIONS.md                 ← التعاليم مثبّتة على هذا المشروع (من قالب الإطار)
│   ├── CONTEXT.md                     ← حقائق دائمة append-only؛ الأرقام فيه مولّدة لا مكتوبة
│   ├── DECISIONS.md                   ← سجل ADR — قرار لا رجعة فيه = سطر هنا أولاً
│   ├── HANDOFFS.md                    ← طابور التذاكر (TKT-NNN بعقد consume/produce/route)
│   ├── LOCKS.md                       ← ادعاءات المسارات المشتركة (claim/release)
│   ├── LESSONS.md                     ← ذاكرة إجرائية — يولَّد فارغاً يوم-صفر (سدّ GAP-11)
│   └── features/                      ← سجل artifacts البوابات المجمّدة (أنجح نمط في SAKK)
│       ├── GATE0-INCEPTION.md         ←   الاسم القياسي: GATE<n>-<ARTIFACT>.<ext>
│       ├── GATE1-JOURNEY-MAP.md       ←   المجمّد هنا هو النسخة الوحيدة — docs/ يشير إليه ولا ينسخه
│       ├── GATE3-OPENAPI.yaml
│       └── ...                        ←   الجدول الكامل في §4
│
├── backend/                           ← Laravel (المستوى الأعلى مباشرة — لا src/)
│   ├── app/  routes/  database/       ←   Models/Controllers/Services · migrations لها down() مُختبَر
│   ├── resources/                     ←   Pattern A: views/ (Blade) + js/ (Vue islands) + css/ (Tailwind)
│   ├── tests/                         ←   unit + feature (PHPUnit) — اختبارات الطبقة داخل الطبقة
│   ├── composer.json + composer.lock  ←   الـ lock ملزم tracked (درس Dockerfile SAKK — GAP-13)
│   └── .env.example                   ←   كل مفتاح بيئة موثّق؛ .env نفسه gitignored أبداً
│
├── frontend/                          ← [شرطي — Pattern B فقط، بعد ADR في Gate 3]
│   ├── src/                           ←   typed client مولّد من GATE3-OPENAPI.yaml
│   ├── package.json + lockfile
│   └── tests/
│
├── mobile/                            ← Flutter — بنية feature-first (نمط SAKK الناجح: lib/{core,features,shared})
│   ├── lib/core/                      ←   theme/network/router/services — والـ API base **يُحقن بـ --dart-define
│   │                                  ←   بلا افتراضي إنتاجي** (علاج ثغرة SAKK: prod URL مثبّت — GAP-13)
│   ├── lib/features/<feature>/        ←   شريحة عمودية لكل feature
│   ├── test/
│   └── pubspec.yaml + pubspec.lock
│
├── docs/                              ← 8 مقاطع قياسية + FOLDER-MAP.md — التفصيل في §5
│
├── deploy/                            ← النشر كله داخل المشروع (§7) — لا شيء منه في ريبو الإطار
│   ├── Dockerfile                     ←   multi-stage، fail-closed (لا `|| true`)، ينسخ الـ locks
│   ├── docker-compose.yml             ←   التشكيلة المرجعية (app + db + redis)
│   ├── Caddyfile                      ←   نطاق الإنتاج (النطاق المحلي شأن طبقة الإطار، منفصل)
│   ├── deploy.sh + rollback.sh        ←   قابلان للتشغيل ومُتدرَّب عليهما قبل إعلان Gate 6
│   └── supervisord.conf
│
├── tests/                             ← عابر الطبقات فقط
│   ├── e2e/                           ←   browser-eyes وأشباهه — الاعتمادات من env، لا hardcoded أبداً
│   ├── integration/                   ←   backend↔mobile↔frontend ضد العقد المجمّد
│   └── load/                          ←   k6 — ميزانيات الأداء (TTI < 2s) قابلة للتشغيل
│
└── _scratch/                          ← gitignored — سكربتات tmp_<role>_<purpose>.py، تُطهَّر عند إغلاق البوابة
```

**`.gitignore` المولَّد قياسياً (يوم-صفر، قبل أول commit):**

```gitignore
# SHAMEL project — generated by shamel new (day-zero)
/_scratch/
.env
.env.*.local
/backend/vendor/
/backend/node_modules/
/backend/storage/*.key
/backend/storage/logs/
/backend/public/build/
/frontend/node_modules/
/frontend/dist/
/mobile/.dart_tool/
/mobile/build/
*.log
```

(vendor=90MB + node_modules=63MB كانت جاثمة داخل شجرة SAKK غير المُصدَّرة — تقرير 06 §الجرد 2.)

### 1.4 قواعد الثبات (invariants) — يفحصها CI في كل مشروع

1. **الشكل = العقد:** `shamel folder-map --check` يقارن القرص بـ `docs/FOLDER-MAP.md` المولَّد — أي انحراف (مجلد دخيل بالجذر، `frontend/` بلا ADR، مقطع docs ناقص) = فشل.
2. **الكود هو الحقيقة:** `shamel facts PRJ-XXXX` سكربت عدّ (models/controllers/migrations/tests/features/coverage) يكتب كتلة `facts:` المولَّدة في `STATE.md`؛ **يُمنع** كتابة هذه الأرقام يدوياً. علاج مباشر لـ GAP-12 (STATE قال 43 اختباراً وCONTEXT قال 38 والفعلي كان ثالثاً).
3. **دماغ في الريبو:** `_context/` tracked في ريبو المشروع نفسه — `shamel checkpoint` بلا `.git` محلي = **فشل صريح** لا تحذير (كان تحذيراً فتسرّب — تقرير 06 §ما يُرحَّل 4).
4. **لا أسرار في الشجرة:** secret-scan (gitleaks) في pre-commit hook للمشروع + في CI — درس اعتمادات admin المضمّنة في `browser-eyes.sh` (GAP-13).

---

## 2) قانون VCS الملزم — «لا مشروع بلا git ولو لدقيقة»

### 2.1 نص القانون

1. **يوم-صفر:** `git init` + أول commit جزء لا يتجزأ من السكافولدر نفسه (§3). المشروع لا «يولد ثم يُصدَّر لاحقاً» — يولد مُصدَّراً. السكافولدر الذي يفشل في خطوة git يفشل كله (`set -euo pipefail` + trap يحذف نصف السكافولد).
2. **remote خلال 24 ساعة:** أول commit محلي يكفي للولادة، لكن `STATE.md` يحمل `remote: (pending)` وأي `shamel gate-check` لبوابة > 0 **يفشل** ما دام pending. بديل مؤقت مقبول عند غياب الشبكة: mirror محلي bare خارج شجرة Desktop (`git clone --mirror` إلى قرص/مسار ثانٍ) مسجّل في STATE.
3. **ريبو الإطار لا يحتضن كود منتج:** `/projects/` يبقى متجاهَلاً في `.gitignore` الإطار — لكن الآن عن حق، لأن كل مشروع يحمل `.git` خاصاً. **يُلغى نهائياً** نمط v6 «فرع `prj/<ID>` في ريبو الإطار» — الفرع الذي لا يستطيع أن يحوي المشروع الذي سُمّي باسمه (تقرير 06 §نقاط الضعف 2).
4. **حُرّاس checkpoint تُرحَّل كما هي** من v6 (`gitops.checkpoint()`: conventional-commit إجباري، فحص مسارات محظورة secrets/`_scratch/` مع unstage بلا `--hard`، trailer، ختم `head_sha` في STATE) — فوق ريبو المشروع الحقيقي هذه المرة، مع تشديد واحد: «no brain to checkpoint» = فشل.
5. **trailer موحّد:** كل commit في ريبو مشروع يحمل `SHAMEL: PRJ-XXXX · TKT-NNN · gate<N> · <agent-id>`.

### 2.2 نموذج الفروع داخل ريبو المشروع

```
main                        ← فرع التكامل الوحيد؛ الحقيقة القابلة للنشر
gate4/<squad>               ← فروع worktrees للـ squads المتوازية خلف حزمة Gate-3 المجمّدة
fix/<TKT-NNN>               ← إصلاح معزول قصير العمر
tags:  gate0-done … gate8-done   ← وسوم إغلاق البوابات، immutable (shamel gate-tag)
```

Worktrees الـ squads تُنشأ من ريبو **المشروع** (`shamel worktree PRJ-XXXX gate4-bck`) وتقبع خارج أي مجلد تهيئة (لا تحت `.claude/` — درس نزيف الـ palette، قرار 08 §5.4). الدمج حصراً `gate-merge --no-ff` بيد الـ lead عند إغلاق البوابة.

### 2.3 خطر PRJ-SAKK غير المُصدَّر — خطة التصحيح الآمنة

**الوضع (GAP-01، CRITICAL):** منصّة fintech كاملة (25 model · 38 controller · 136 ملف dart · أموال/KYC/2FA) + دماغها الحي، بلا `.git` ولا remote ولا نسخة ثانية — والخطر متحقق سابقاً مرتين (xo-game وheart-clinic تبخّرا؛ wipe موثَّق بتاريخ 2026-07-09 شمل git history).

**الترتيب أدناه ملزم — تحديداً: تطهير الأسرار قبل أول `git add`، لأن ما يدخل التاريخ يبقى فيه:**

```bash
# 0) تأمين لقطة خارج الشجرة أولاً — قبل لمس أي شيء (snapshot-first)
tar -czf ~/backup-PRJ-SAKK-$(date +%Y%m%d).tar.gz \
    --exclude='backend/vendor' --exclude='backend/node_modules' \
    -C ~/Desktop/Lorka/projects PRJ-SAKK
# تُنسَخ فوراً إلى وسيط ثانٍ (قرص خارجي/سحابة خاصة)

# 1) تطهير الأسرار من ملفات العمل (قبل أي staging — GAP-13)
#    - tests/e2e/browser-eyes.sh:13-14 : نقل اعتمادات admin إلى متغيرات بيئة
#      (ADMIN_EMAIL/ADMIN_PASSWORD من .env — السكربت يفشل صراخاً إن غابت)
#    - فحص شامل:  gitleaks detect --source . --no-git   ← يجب أن يخرج نظيفاً

# 2) كتابة .gitignore القياسي (§1.3) — يستبعد vendor/node_modules/.env/_scratch

# 3) الولادة
cd ~/Desktop/Lorka/projects/PRJ-SAKK
git init -b main
git add -A
git diff --cached --stat        # مراجعة بشرية: لا vendor، لا .env، لا أسرار
gitleaks detect --source . --staged   # حارس ثانٍ fail-closed
git commit -m "chore(rescue): PRJ-SAKK day-zero import — code + brain under VCS

SHAMEL: PRJ-SAKK · TKT-RESCUE · gate4 · ops-lead"

# 4) النسخة الثانية خلال الجلسة نفسها
git remote add origin <private-remote-url>
git push -u origin main
#    (لا remote متاح؟ mirror محلي bare على وسيط ثانٍ + تسجيله في STATE.md)

# 5) تصحيح الدماغ فوق الحقيقة الجديدة
#    - shamel facts PRJ-SAKK  → أرقام STATE/CONTEXT تُولَّد من الكود (25/38/10…)
#    - stack يُصحَّح: web = Blade+Tailwind (لا Vue/Next) · mobile = Riverpod (يوثَّق ADR للانحراف عن Bloc أو قرار توحيد)
#    - إعادة التصنيف الرسمية: gate 6 → gate 4/5 (GAP-04: لا CI ولا deploy.sh — البوابة كانت خيالاً)
#    - ختم branch/head_sha في STATE.md (كانا فارغين رغم gate 6)
git add _context/ && git commit -m "docs(brain): regenerate facts from code; reclassify gate 6→4"
```

بعد هذه الخطوات فقط يعود SAKK مشروعاً شرعياً في المصنع: البوابات تتقدم بـ artifacts قابلة للتشغيل (workflow موجود + rollback مُتدرَّب) يفحصها `shamel gate-check` fail-closed.

---

## 3) دورة السكافولد — `shamel new` (خليفة new-project.sh)

### 3.1 الواجهة

```bash
shamel new PRJ-XXXX "عنوان المشروع" PRIORITY [--date YYYY-MM-DD] \
           [--slug sakk] [--web A|B] [--mobile yes|no] [--remote <url>] \
           [--adr-source owner:"<قرار المالك>"|import-scan:<report.json>]
```

الافتراضيات: `--web A` (monolith) · `--mobile no` · بلا `--remote` → تحذير صاخب + `remote: (pending)` في STATE. **`--web B` يستلزم `--adr-source`** (منه يُكتب `ADR-000` تلقائياً — §1.2)؛ بلا مصدر = رفض فوري قبل إنشاء أي شيء.

### 3.2 ماذا ينشئ بالضبط — الخطوات مفاهيمياً (كلها fail-closed، فشل أي خطوة = تراجع كامل)

| # | الخطوة | التفصيل | الفرق عن v6 |
|---|--------|---------|--------------|
| 1 | حلّ الجذر | سُلّم §0 — فشل صريح إن غاب الجذر | v6 كان يبني مساراً معدوماً بصمت |
| 2 | حارس الوجود | `PRJ-XXXX/` موجود؟ رفض فوري (كما v6 — يُحتفظ به) | — |
| 3 | الشجرة القانونية | §1.3 بالمستوى الأعلى المباشر؛ `frontend/` فقط مع `--web B` — وبعد كتابة `ADR-000` في `DECISIONS.md` أولاً (§1.2)، فلا يولد مشروع في حالة فشل `folder-map --check` | v6 ولّد `src/{...}` المخالف للواقع، و`frontend` دائماً |
| 4 | `.gitignore` + `.gitattributes` | القالب القياسي §1.3 | v6 لم يولّد أياً منهما |
| 5 | الدماغ الأولي | 7 ملفات §3.4 من قوالب الإطار (`sed s/PRJ-XXXX/$ID/`) — **بإضافة `LESSONS.md`** فارغاً بترويسة؛ مع `--web B`: `DECISIONS.md` يولد حاملاً `ADR-000` لا فارغاً | v6 ولّد 6 بلا LESSONS (GAP-11: لا LESSONS لأي مشروع قط) |
| 6 | `_context/features/` | README يشرح اصطلاح `GATE<n>-<ARTIFACT>.<ext>` + جدول §4 | v6 لم يعرف المجلد أصلاً (SAKK ابتدعه يدوياً — ونجح) |
| 7 | `docs/` الثمانية | §5 + **توليد** `FOLDER-MAP.md` بسكربت من الشجرة الفعلية | FOLDER-MAP في SAKK كان يدوياً فكذب (React 19 معدوم) |
| 8 | `deploy/` + `tests/` | هياكل skeleton قابلة للتشغيل: Dockerfile قياسي fail-closed، compose، deploy.sh/rollback.sh قوالب، `tests/{e2e,integration,load}/README` بعقد واضح | v6 لم يولّدهما إطلاقاً (SAKK رقّعهما يدوياً) |
| 9 | CI | `.github/workflows/ci.yml` القياسي (§7) **+ سكربتا الفحص المستقلان** `.github/shamel/{folder_map.py,facts.py}` (§7.1) — بهما يعمل الـ CI من أول push بلا اعتماد على ريبو الإطار | v6: لا CI — فأُعلنت Gate 6 فوق workflows فارغة (GAP-04) |
| 10 | **git يوم-صفر** | `git init -b main` **داخل مجلد المشروع** + pre-commit hook (gitleaks + conventional-commit) + `git add -A` + أول commit بموضوع `chore(scaffold): PRJ-XXXX day-zero` وترايلر SHAMEL | **الفجوة القاتلة في v6:** لا git init أبداً؛ فرع `prj/<ID>` في ريبو الإطار الذي يتجاهل projects/ |
| 11 | remote | `--remote` مُمرَّر → `git remote add origin && git push -u`؛ غائب → تسجيل `remote: (pending)` + تذكير أن أي gate-check > 0 سيفشل | لا مفهوم remote في v6 |
| 12 | النطاق المحلي | `shamel domain register PRJ-XXXX <slug>` → `<slug>.local` في `/etc/hosts` بوسم `# shamel-domain`، وختم `local_domain`/`local_port` في STATE (يُرحَّل من v6 كما هو — التكامل الوحيد المُثبت حياً في SAKK) | يُحتفظ به |
| 13 | الخاتمة | طباعة: مسار المشروع · حالة git/remote · الدومين · التذكرة الأولى TKT-001 · الأمر التالي (`shamel sync PRJ-XXXX`) | — |

### 3.3 النطاق المحلي — القانون كما هو

كل مشروع URL محلي نظيف `<slug>.local` لا `127.0.0.1:PORT` عارياً. التسجيل تلقائي في الخطوة 12؛ أول squad يشغّل التطبيق ينفّذ `shamel domain up PRJ-XXXX`. التهيئة الأحادية `shamel domain init` تبقى شرطاً مسبقاً على مستوى الجهاز. Caddyfile الإنتاجي في `deploy/` منفصل تماماً عن هذه الطبقة (فصل صحيح أثبته SAKK).

### 3.4 الدماغ الأولي — `STATE.md` بصيغة `key: value` صرفة (بلا frontmatter — استثناء `BRAIN.md` §2.3 المقصود، يُقرأ بـ parser حتمي لا YAML lib)

```markdown
# STATE — PRJ-XXXX
prj: PRJ-XXXX
title: عنوان المشروع
gate: 0            # Inception
track: (declared at gate 0 — fast_track | deep_audit)
priority: HIGH
status: in_progress
branch: main       # فرع ريبو المشروع نفسه — لا فرع إطار
head_sha: (set at first checkpoint)
remote: (pending | <url>)
web_pattern: A     # يفحصه shamel facts ضد القرص
local_domain: http://<slug>.local
local_port: (set by shamel domain up)
public_url: none
counts_sha: (set by shamel facts)   # بصمة آخر توليد أرقام (BRAIN §7.4)
facts_generated_at: null            # ← مفاتيح facts_* كتلة مولَّدة حصراً بـ `shamel facts` — الكتابة اليدوية فيها محظورة
facts_models: 0
facts_controllers: 0
facts_migrations: 0
facts_tests: 0
facts_coverage: null
updated_by: shamel-new
blockers: none
next: TKT-001 (gate 0 — str-product-strategist)
```

و`HANDOFFS.md` يولد بتذكرة TKT-001 جاهزة (from: brd-ceo → to: str-product-strategist، produce: `_context/features/GATE0-INCEPTION.md` + وثائق docs/PRD) — لا جلسة أولى عمياء.

---

## 4) ربط البوابات بالمجلدات — أين يسكن كل artifact

**القاعدة:** الـ artifact المجمّد للبوابة نسخة **واحدة** في `_context/features/GATE<n>-<NAME>.<ext>` (يُختم بوسم `gate<n>-done`)؛ وثائق العمل الحية التي أنتجته تسكن مقطع `docs/` المالك وتشير إليه — **لا نسخ مزدوج أبداً**. الأسماء أدناه هي القياس الملزم (المُثبت في SAKK + gates.yaml):

| Gate | الغرفة المالكة | الـ artifacts المجمّدة في `_context/features/` | مواطن العمل والكود |
|------|----------------|-----------------------------------------------|---------------------|
| **0 Inception** | str | `GATE0-INCEPTION.md` (problem statement + 5 أسئلة + risk register + track) | `docs/PRD/` (Blueprint, Risk-Register) |
| **1 Discovery** | res | `GATE1-PERSONAS.md` · `GATE1-JOURNEY-MAP.md` (حقيقة التصميم) · `GATE1-RESEARCH.md` · `GATE1-COMPETITOR-ANALYSIS.md` | `docs/PRD/` |
| **2 Design** | dsn | `GATE2-UX-ARCH.md` · `GATE2-UI-SPEC.md` · `GATE2-DESIGN-TOKENS.md` · `GATE2-UX-COPY.md` (+`Content_Strings.json`) · `GATE2-A11Y-MATRIX.md` | `docs/DESIGN/` |
| **3 Architecture** | arc + dat + sec | `GATE3-SYSTEM-ARCH.md` · `GATE3-DATA-ARCH.md` (schema+ERD) · `GATE3-OPENAPI.yaml` (العقد المجمّد) · `GATE3-THREAT-MODEL.md` · `GATE3-PII-MAP.md` (عند وجود بيانات شخصية) · ADR قرار الويب A/B في `DECISIONS.md` | `docs/ARCHITECTURE/` |
| **4 Build** | bck · fnt · mob | لا artifact وثائقي مجمّد — **الكود هو الـ artifact**: `backend/**` (+tests) · `frontend/**` (Pattern B) · `mobile/**` (+tests) · migrations بـ down() مُختبَر | worktrees `gate4/<squad>` → دمج `--no-ff` في main؛ ملاحظات البناء في `docs/BUILD/` |
| **5 Quality** | qa + sec | `GATE5-QUALITY-REPORT.md` (verdict واحد PASS/BLOCK + coverage ≥90%) · `GATE5-DESIGN-AUDIT.md` · `GATE5-SECURITY-AUDIT.md` · `GATE5-PERF-REPORT.md` (k6/Lighthouse/TTI) | `tests/{e2e,integration,load}/` قابلة للتشغيل + `docs/QUALITY/` |
| **6 Staging/UAT** | ops | `GATE6-DEPLOY-CONFIG.md` (يستشهد **حصراً بملفات موجودة**: Dockerfile، compose، workflow، rollback.sh — يفحصها gate-check وجوداً وتشغيلاً) | `deploy/**` + `.github/workflows/deploy.yml` + runbook في `docs/OPS/` |
| **7 Prod** | ops | `GATE7-RELEASE.md` (سجل الإصدار + دليل بروفة rollback على بيانات staging + Blue/Green) | `deploy/` + وسم git إصدار |
| **8 Observe** | obs | `GATE8-OBSERVE-CONFIG.md` (SLI/SLO + خريطة alerts↔runbooks) | تهيئة المراقبة في `deploy/observability/` + `docs/OPS/` |

**بند الإنفاذ (علاج GAP-04):** `shamel gate-check PRJ-XXXX <n>` ميكانيكي fail-closed: وجود الـ artifacts أعلاه بالاسم القياسي + كتلة evidence في التذكرة (cmd + exit code) + لبوابة 6 تحديداً: workflow موجود **وله run أخضر** وrollback.sh نُفّذ ببروفة موثّقة. الحكم النهائي دائماً للفحص العدائي fresh-context (gatekeeper) — المنفّذ لا يصحّح لنفسه.

---

## 5) `docs/` القياسي — المقاطع الثمانية + FOLDER-MAP إلزامي

### 5.1 المقاطع (كما استقرت في SAKK — تُرحَّل بالاسم)

```
docs/
├── FOLDER-MAP.md      ← إلزامي — العقد المولَّد (§5.2)
├── PRD/               ← Gates 0–1: Blueprint · Problem-Statement · Risk-Register · Personas · Journey-Map
├── DESIGN/            ← Gate 2: Prototype-Spec · IA/Flows · Tokens · Content-Strings · A11y
├── ARCHITECTURE/      ← Gate 3: Tech-Stack · Schema/ERD · تصدير مقروء للعقد · Threat-Model · Integrations
├── BUILD/             ← Gate 4: ملاحظات البناء · سجلات مراجعات الكود · قرارات تنفيذية غير-ADR
├── QUALITY/           ← Gate 5: استراتيجية الاختبار · تقارير مفصّلة خلف الـ verdict المجمّد
├── OPS/               ← Gates 6–8: runbooks تشغيل ونشر وrollback · SLO · خريطة alerts
├── brain/             ← مساحة ملاحظات الغرف: ملف لكل غرفة لمست المشروع (bck.md, sec.md…) —
│                        مفكرة عمل الغرفة، ليست artifacts ولا نسخاً من _context
└── reports/           ← التقارير المولّدة المدعومة بالأدلة (audit/secure/feature reports) بطابع زمني
```

قاعدتان: (أ) وثيقة العمل تعيش في مقطعها **وتشير** إلى الـ artifact المجمّد في `_context/features/` — الاتجاه الوحيد المسموح؛ (ب) مقطع فارغ يُترك بـ README سطرين يشرح متى يمتلئ — لا يُحذف ولا يُملأ زيفاً.

### 5.2 `FOLDER-MAP.md` — عقد مولَّد لا وثيقة يدوية

الدرس: FOLDER-MAP اليدوي في SAKK أعلن `frontend/` React 19 وملفات deploy معدومة — خيال رسمي (تقرير 06). في شامل:

- **يولَّد** بـ `shamel folder-map PRJ-XXXX` من الشجرة الفعلية: لكل مجلد أعلى — الغرض، الغرفة المالكة، البوابة، العدّ الفعلي للملفات، وحالة Pattern الويب من ADR.
- **يُفحص** بـ `shamel folder-map --check` في CI (وفي gate-check): قرص ≠ خريطة = فشل build. الخريطة لا تكذب لأنها لا تُكتب.
- رأس الملف المولّد: `<!-- GENERATED by shamel folder-map — DO NOT EDIT (edits fail CI) -->`.

---

## 6) بروتوكول استيراد مشروع خارجي قائم — «كما حدث مع SAKK، لكن الصحيح»

أخطاء استيراد SAKK المرجعية: بلا git، دماغ بأرقام وstack مخترعة (ثلاث روايات للويب)، gate مُعلنة فوق واقع معدوم، أسرار مضمّنة، ومشروعان سابقان تبخّرا بلا أثر. البروتوكول الملزم:

**المرحلة 0 — التأمين (قبل أي لمس):** لقطة `tar` للمصدر خارج الشجرة + نسخة على وسيط ثانٍ. لا خطوة تالية قبلها.

**المرحلة 1 — الجرد الآلي:** `shamel import scan <src-path>` (سكربت، لا انطباعات): كشف stack فعلي من lock/manifest files (composer.lock, pubspec.yaml, package.json) · عدّ models/controllers/tests · **secret-scan كامل** (gitleaks) · قائمة ما سيُستبعد (vendor/node_modules/build). خرجه تقرير JSON هو **المصدر الوحيد** لكل ما سيُكتب لاحقاً في الدماغ — لا رواية بشرية.

**المرحلة 2 — الولادة القانونية:** `shamel new PRJ-XXXX ... --web <حسب الجرد> --adr-source import-scan:<تقرير المرحلة 1>` — عند SPA مستورد (`--web B`) يُستولد `ADR-000` آلياً من تقرير الجرد (§1.2) فلا يولد المشروع فاشلاً في CI؛ المشروع المستقبِل يولد كاملاً (repo + دماغ + CI + دومين) **قبل** دخول أي ملف مستورد.

**المرحلة 3 — التطهير ثم النقل:** إزالة الأسرار من ملفات المصدر (إلى env/`.env.example`) **قبل** النسخ · النقل وفق جدول ربط `مصدر → مجلد قانوني` يُكتب في `docs/reports/IMPORT-PRJ-XXXX.md` (بما فيه ما استُبعد ولماذا) · `.gitignore` القياسي فعّال أثناء النسخ فلا يدخل vendor.

**المرحلة 4 — الحقيقة المولَّدة:** `shamel facts` يملأ STATE/CONTEXT من الكود المنقول · `shamel folder-map` يولّد الخريطة · انحرافات الـ stack عن افتراضات الشركة (مثل Riverpod بدل Bloc) تُسجَّل ADR صريحاً: توحيد أو قبول موثَّق — لا تجاهل.

**المرحلة 5 — تصنيف البوابة بالإثبات لا بالإعلان:** المشروع المستورد يدخل عند البوابة التي **تثبتها artifacts موجودة** يفحصها gatekeeper بسياق نظيف (V2). ما لا دليل عليه من تاريخه يُعلَّم `GATE<n>: UNVERIFIED-LEGACY` في STATE — **يُمنع اختراع artifacts بأثر رجعي**؛ تُستولد لاحقاً هندسةً عكسية حيث يمكن (OpenAPI من routes، schema من migrations) وتُختم حينها فقط.

**المرحلة 6 — الإغلاق:** commit + push (remote إلزامي لمشروع مستورد — لا فترة سماح: هو موجود مسبقاً فخطره فوري) · سطر في `DECISIONS.md` (المصدر، التاريخ، الجدول، الاستثناءات) · سجل مركزي `projects/IMPORTED.md` يُحدَّث — وأي حذف لاحق لمشروع لا يقع إلا بـ ADR + أرشفة (لا تبخّر صامت كما xo-game وheart-clinic).

---

## 7) CI/deploy القياسي — داخل المشروع، لا في ريبو الإطار

**القانون:** ريبو الإطار لا يحمل CI لأي منتج؛ كل مشروع مكتفٍ ذاتياً بنشره واختباره. (يقتل تبعية «الأدوات في worktree والمشاريع في MAIN» التي عمّت v6.)

### 7.1 `ci.yml` القياسي (يولَّد يوم-صفر، يعمل من أول push)

```yaml
name: ci
on: { push: { branches: [main, "gate4/**", "fix/**"] }, pull_request: {} }

jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: shivammathur/setup-php@v2
        with: { php-version: "8.3", coverage: xdebug }
        # coverage driver صريح — بدونه يسقط `--coverage` على runner عارٍ
      - run: composer install --working-dir=backend --no-interaction --prefer-dist
        # لا `|| true` في أي سطر — درس Dockerfile SAKK: ابتلاع الفشل محظور
      - run: composer --working-dir=backend exec pint -- --test
      - run: cp backend/.env.example backend/.env && php backend/artisan key:generate
        # تهيئة بيئة الاختبار داخل الـ runner — APP_KEY من .env.example (كل مفتاح موثّق §1.3)
      - run: php backend/artisan test --coverage --min=90
        env: { DB_CONNECTION: sqlite, DB_DATABASE: ":memory:" }
        # عتبة التغطية ≥90% تُنفَّذ هنا آلياً — لا في وثيقة
      - run: |
          # حارس الأسرار في كل push — تثبيت مثبَّت الإصدار؛ الـ runner لا يحمل gitleaks افتراضاً
          curl -sSfL https://github.com/gitleaks/gitleaks/releases/download/v8.18.4/gitleaks_8.18.4_linux_x64.tar.gz | tar -xz gitleaks
          ./gitleaks detect --source . --no-git

  mobile:
    if: ${{ hashFiles('mobile/pubspec.yaml') != '' }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
      - run: flutter test
        working-directory: mobile

  contract:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python3 .github/shamel/folder_map.py --check && python3 .github/shamel/facts.py --check
        # السكربتان المستقلان المولَّدان يوم-صفر داخل المشروع (انظر «آلية التوزيع» أدناه) —
        # لا استدعاء لأداة ريبو الإطار على الـ runner
        # انحراف الشكل أو أرقام دماغ مكتوبة يدوياً = فشل build
```

**آلية توزيع الفحوص إلى CI المشروع (سدّ التبعية الخفية):** `shamel` أداة ريبو الإطار ولا وجود لها على runner المشروع — لذلك يولّد السكافولدر يوم-صفر (§3.2 خطوة 9) نسختين standalone بلا أي تبعية خارج مكتبة بايثون القياسية: `.github/shamel/folder_map.py` و`.github/shamel/facts.py` (موطنهما القانوني `.github/` الخدمي المتتبَّع — لا مجلد دخيل بالجذر)، وكلٌّ منهما يحمل ختم `SHAMEL_CHECKS_VERSION` في رأسه. أمرا الإطار `shamel folder-map` / `shamel facts` يستدعيان محلياً **السكربتين نفسيهما** — منطق واحد، مصدره قالب الإطار؛ و`shamel doctor` يكشف انحراف نسخة المشروع عن القالب ويعرض تحديثها بـ commit صريح في ريبو المشروع (لا مزامنة صامتة). بهذا يصدق الادعاءان معاً: CI يعمل من أول push، والمشروع مكتفٍ ذاتياً فعلاً بلا تثبيت للإطار.

### 7.2 `deploy/` القياسي

- **Dockerfile** multi-stage (composer → node/vite → php-fpm+nginx+supervisord — نمط SAKK المتّسق يُرحَّل) مع إصلاحين ملزمين: `COPY composer.json composer.lock ./` (الـ lock دائماً) و`composer install --no-dev` **بلا** `|| true` — build غير قابل لإعادة الإنتاج مرفوض في أي مشروع، فكيف بمنتج مالي (GAP-13).
- **docker-compose.yml** التشكيلة المرجعية للتشغيل staging/محلي.
- **deploy.sh / rollback.sh** قابلان للتشغيل فعلياً؛ **بروفة rollback على بيانات staging شرط دخول Gate 7** — لا «runbook يستشهد بأربعة ملفات معدومة» بعد اليوم (تقرير 06 §الصحة).
- **deploy.yml** (workflow) يُفعَّل عند Gate 6: يبني الصورة، ينشر إلى staging، ينتظر موافقة، ثم Blue/Green إلى prod — ولا يُعلن Gate 6/7 إلا وله run أخضر يفحصه gate-check.
- نمط الشبكة المرجعي: `Cloudflare TLS → Caddy reverse-proxy → حاوية` (المُثبت في SAKK).

---

## 8) خلاصة القوانين الملزمة (checklist المصنع)

1. مشروع = ريبو git خاص منذ السطر الأول من السكافولدر؛ remote خلال 24h وإلا تتجمد البوابات.
2. الشكل القانوني: `_context/ · backend/ · [frontend/] · mobile/ · docs/ · deploy/ · tests/` بالمستوى الأعلى — يفحصه `folder-map --check` في CI.
3. الويب داخل `backend/` (Pattern A) افتراضاً؛ `frontend/` مستقل لا يوجد إلا وADR يسبقه (`ADR-000` آلياً عند `--web B` بمصدر ملزم، وإلا قرار Gate 3)؛ لا شاشة تُبنى مرتين.
4. artifacts البوابات نسخة واحدة في `_context/features/GATE<n>-<NAME>` بالأسماء القياسية؛ docs/ يشير ولا ينسخ.
5. أرقام الدماغ مولّدة بـ `shamel facts` حصراً — الكود هو الحقيقة.
6. `FOLDER-MAP.md` مولَّد، تحريره اليدوي يفشل CI.
7. لا بوابة بلا artifacts قابلة للتشغيل يفحصها gate-check fail-closed + حكم gatekeeper بسياق نظيف — المنفّذ لا يصحّح لنفسه.
8. لا أسرار في الشجرة أو التاريخ: gitleaks في pre-commit وCI؛ التطهير **قبل** أول add دائماً.
9. الاستيراد: تأمين → جرد آلي → ولادة قانونية → تطهير فنقل → حقيقة مولّدة → تصنيف بالإثبات → ADR — ولا حذف مشروع بلا ADR وأرشفة.
10. CI/deploy داخل المشروع حصراً؛ فحوص CI (folder-map/facts) سكربتات standalone مولّدة داخله (§7.1) — لا استدعاء لأداة الإطار من الـ runner؛ ريبو الإطار للعقيدة والأدوات فقط، و`/projects/` متجاهَل فيه عن حق.
