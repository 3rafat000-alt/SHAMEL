# تدقيق شامل ٠٦ — نظام المشاريع وطريقة بنائها (من الحاوية إلى داخل المنتج)

**التاريخ:** 2026-07-10 · **المدقّق:** SHAMEL audit agent · **النطاق:** `/home/es3dlll/Desktop/Lorka/projects/` + السكافولدر في worktree v6 · **الوضع:** READ-ONLY

---

## الجرد

### 1) الحاوية `projects/`
| عنصر | الواقع | الدليل |
|---|---|---|
| المحتوى | `PRJ-SAKK/` + `README.md` + `IMPORTED.md` فقط | `ls /home/es3dlll/Desktop/Lorka/projects/` |
| `IMPORTED.md` | يوثّق **3** مشاريع مستوردة (PRJ-SAKK · xo-game · heart-clinic) — **موجود واحد فقط**؛ xo-game وheart-clinic اختفيا بلا أثر ولا ADR للحذف | `projects/IMPORTED.md:7-9` |
| حالة git | `/projects/` متجاهَل صراحةً في repo الأم | `.gitignore:20` → `/projects/`؛ `git ls-files projects/` → **0 ملف متتبَّع** |
| repo خاص بالمشروع | **غير موجود** — لا `.git` داخل PRJ-SAKK | `ls -a PRJ-SAKK/` → لا `.git` |
| `README.md` | يشير لسكافولدر بمسار v5 قديم `sofi/bin/new-project.sh` (المسار الحقيقي `company/os/bin/`) | `projects/README.md:3` |

### 2) PRJ-SAKK — الاصطلاح الفعلي (سداسي + `.github` فارغ)
`_context/ · backend/ · mobile/ · docs/ · deploy/ · tests/ · .github/workflows/ (فارغ تماماً)`

**`_context/`** — `STATE.md`(25 سطر) · `CONTEXT.md`(14) · `DECISIONS.md`(6) · `HANDOFFS.md`(56) · `features/` = **19 artifact بوابات** (GATE0-INCEPTION → GATE8-OBSERVE-CONFIG، ومنها `GATE3-OPENAPI.yaml`). لا `FOUNDATIONS.md` ولا `LOCKS.md` ولا `LESSONS.md`.

**`STATE.md` (كامل):** `gate: 6 (Deploy)` · `branch:` **فارغ** · `head_sha:` **فارغ** (`STATE.md:8-10`) · `local_domain: http://sakk.local` + `local_port: 8001` (مسجّل فعلاً في `/etc/hosts:23`). يدّعي «43 اختبار (78 assertion) ALL GREEN» `[unverified — لم أشغّل الاختبارات]` و«ادفع إلى main ← GitHub Actions ينشر تلقائياً» (`STATE.md:26`) — **لا يوجد أي workflow**.

**`backend/` (Laravel):** Models=**25** · Controllers=**38** · Services=**6** · Migrations=**10** (كلها 2026-07-09) · اختبارات PHPUnit=**10 ملفات**. `composer.json`: `php ^8.3` · `laravel/framework ^13.8` (المثبّت فعلياً **v13.19.0** حسب `composer.lock`) · `laravel/sanctum ^4.0` (v4.3.2) · phpunit ^12.5 · pint · pail. **vendor=90MB + node_modules=63MB مثبّتة داخل الشجرة غير المُصدَّرة** (يناقض ادعاء `IMPORTED.md:3` «excluded by design»). `.env.example` موجود.

**الويب (تأكيد النقطة 4):** `package.json` = Vite ^8 + Tailwind ^4 + Sass — **لا يوجد `vue` إطلاقاً** في dependencies. `find resources/js -name '*.vue'` = **0**؛ `resources/js/app.js` شبه فارغ (سطر تعليق واحد)؛ Blade views=**38**؛ Alpine (`x-data`) في ملفّين فقط. إذن الويب فعلياً = **Blade + Tailwind4 + Sass عبر Vite** — ليس Next.js كما يدّعي `IMPORTED.md:7` («Next.js 16 (TS)») **وليس حتى Vue 3** كما يدّعي `STATE.md:3` و`CONTEXT.md:5` («Blade + Vue 3»). ثلاث روايات، كلها ≠ الكود.

**`mobile/` (Flutter `sakk_wallet` v1.0.3+4):** deps رئيسة: `flutter_riverpod ^2.6.1` (**Riverpod لا Bloc** — يخالف stack defaults في CLAUDE.md) · `go_router` · `dio` · `flutter_secure_storage` · `hive_flutter` · `local_auth` (`pubspec.yaml`). البنية `lib/{core,features,shared}` نظيفة: core=7 أقسام (theme/network/router/services/…) · **features=25** (auth·kyc·wallets·transfer·gold·cards·qr·bills·cashback·agents·chat…) · **136 ملف dart**. الـ API الافتراضي إنتاجي: `https://sakk.zanjour.com/api/v1` مع override بـ `--dart-define` (`lib/core/constants/api_constants.dart:9-11`).

**`docs/`** — `FOLDER-MAP.md` (الخريطة الرسمية) + أقسام: ARCHITECTURE=**4** · BUILD=**3** · DESIGN=**5** · OPS=**2** · PRD=**5** · QUALITY=**3** · reports=**3** · brain=**14** (مجرد README placeholder لكل غرفة).

**`deploy/`** — `Caddyfile` (لنطاق الإنتاج `sakk.zanjour.com` + trusted_proxies لـ Cloudflare — **ليس** لـ `sakk.local`؛ الدومين المحلي تديره طبقة sofi-domain خارج المشروع) · `Dockerfile` (multi-stage: composer→node→php:8.4-fpm + nginx + supervisord) · `supervisord.conf` (php-fpm + nginx). متّسق كبنية `Cloudflare → Caddy → Docker` المعلنة في `STATE.md:20`.

**`tests/`** — **5 ملفات فقط**: README + `e2e/browser-eyes.sh` (سكربت لقطات شاشة للـ admin) + لقطتا PNG + `report.md`. **`integration/` و`load/` فارغتان تماماً** رغم أن README يعد بـ k6/artillery.

### 3) السكافولدر (worktree v6)
`company/os/bin/new-project.sh` ينشئ: `_context/{STATE,FOUNDATIONS,LOCKS,CONTEXT,DECISIONS,HANDOFFS}.md` + `docs/` + **`src/{backend,frontend,mobile}`** + `_scratch/` + symlink `shared → ../../shared-packages` + `README.md`، ثم ينشئ فرع `prj/<ID>` **في repo الإطار** (السطور 107-115) ويسجّل الدومين المحلي (117-124). **لا يعمل `git init` داخل مجلد المشروع أبداً.**

`sofi_tools/paths.py`: حلّ جذر المشاريع = `SOFI_PROJECTS_DIR` → وإلا `~/Desktop/projects` إن وُجد → وإلا `<repo>/projects` (`paths.py:55-61`). و`project_repo()` يصعد من مجلد المشروع حتى أول `.git` (`paths.py:64-72`).

---

## الصحة

- **تشغيل حي للحلّال من الـ worktree:** `projects_dir()` = `<worktree>/projects` — **غير موجود**، و`list_projects()` = `[]`. أي أن **أدوات v6 كلها عمياء عن PRJ-SAKK** ما لم يُضبط `SOFI_PROJECTS_DIR` (و`~/Desktop/projects` غير موجود أصلاً رغم أن doctrine الـ CLAUDE.md يعتبره الافتراضي).
- **`sofi checkpoint` مكسور بنيوياً لهذا المشروع:** `checkpoint()` يستدعي `project_repo()` (`gitops.py:130`)؛ بلا `.git` في PRJ-SAKK يصعد الصعود إلى repo الإطار `/home/es3dlll/Desktop/Lorka/.git` حيث `/projects/` متجاهَل — فلا يُلتقط أي brain. الأثر ظاهر: `branch`/`head_sha` فارغان في `STATE.md:9-10` رغم gate 6.
- **الـ brain يناقض نفسه (خرق G5):** `STATE.md` gate=6 و«43 اختبار/78 assertion»؛ `CONTEXT.md:6,12` gate=5 و«38 اختبار/62 assertion» و«9 models · 10 controllers · 13 migrations» — **الفعلي: 25 models · 38 controllers · 10 migrations**.
- **`FOLDER-MAP.md` (الخريطة الرسمية) خيالي جزئياً:** يعلن `frontend/` React 19 SPA (السطور 44-46) — **المجلد غير موجود**؛ ويعلن `deploy/docker-compose.yml · Dockerfile.backend · Dockerfile.frontend · .github/workflows` (57-61) — الفعلي `Caddyfile/Dockerfile/supervisord.conf` و`.github/workflows` فارغ.
- **runbook النشر يستشهد بملفات معدومة:** `HANDOFFS.md:51-56` يسرد `deploy/deploy.sh · sakk.service · docker-compose.yml · .github/workflows/deploy.yml` — البحث `find` أثبت **عدم وجود أيٍّ منها**؛ والخطوة الأولى `git clone <repo-url>` (`HANDOFFS.md:8`) مستحيلة لأن الكود ليس في أي repo أصلاً.
- **Dockerfile هشّ:** `composer install ... || true` (يبتلع فشل التثبيت) وينسخ `composer.json` بدون `composer.lock` → build غير قابل لإعادة الإنتاج.
- سكربت `tests/e2e/browser-eyes.sh:13-14` يضمّن **بيانات دخول admin افتراضية hardcoded** (بريد + كلمة مرور) — لن أقتبس القيمة.

---

## نقاط القوة

1. **الاصطلاح السداسي واضح ومنضبط** (`_context/backend/mobile/docs/deploy/tests`) مع `FOLDER-MAP.md` كفكرة ممتازة: خريطة غرفة→مجلد→بوابة.
2. **سجل بوابات كامل التتبّع:** 19 artifact في `_context/features/` من GATE0 حتى GATE8 بأسماء قياسية (بما فيها OpenAPI وTHREAT-MODEL وA11Y-MATRIX) — أفضل تجسيد عملي لدورة الـ 9 بوابات وجدته.
3. **كود المنتج نفسه حيّ ومتماسك:** Laravel 13.19 حديث ببنية fintech جدّية (25 model، migrations موضوعية المجال)، وFlutter clean-architecture بـ 25 feature و136 ملف dart، وdeps أمنية صحيحة (secure_storage، local_auth).
4. **سكافولدر v6 يزرع brain كامل** (STATE/FOUNDATIONS/LOCKS/HANDOFFS مع TKT-001 جاهز) + دومين محلي تلقائي — انطلاقة موحّدة حقيقية.
5. **حُرّاس `checkpoint()` ممتازون بذاتهم:** conventional-commit إجباري، فحص مسارات محظورة (secrets/_scratch) مع unstage بدون `--hard`، trailer `SOFI:`، وختم `head_sha` في STATE (`gitops.py:121-158`).
6. بنية نشر بسيطة وواقعية (Cloudflare TLS → Caddy reverse-proxy → حاوية واحدة supervisord).

---

## نقاط الضعف

1. **[CRITICAL — الخطر الأكبر في المنظومة كلها] كود المنتج غير مُصدَّر إطلاقاً:** `/projects/` متجاهَل في git الأم (`.gitignore:20`)، PRJ-SAKK بلا `.git`، لا remote، لا نسخة ثانية على القرص. **الخطر متحقق فعلاً مرتين:** (أ) xo-game وheart-clinic — مشروعان موثّقان في IMPORTED.md — **تبخّرا نهائياً**؛ (ب) `DECISIONS.md:4-6` يوثّق «Complete wipe and rebuild… code, docs, brain, **git history**» بتاريخ 2026-07-09. منصّة fintech كاملة (منطق أموال/KYC/2FA) تعيش الآن كملفات سائبة قابلة للفناء بأمر `rm -rf` واحد. تقدير الحجم: **فقدان كلي غير قابل للاسترداد لأصل الشركة الأساسي**.
2. **حلقة git مقطوعة ذاتياً:** doctrine يقول «كل PRJ هو repo مستقل» لكن `new-project.sh` لا يعمل `git init`، وفرع `prj/<ID>` يُنشأ في repo الإطار الذي يتجاهل `projects/` — فرع لا يستطيع أن يحوي المشروع الذي سُمّي باسمه.
3. **السكافولدر ≠ الواقع:** يولّد `src/{backend,frontend,mobile}` بينما PRJ-SAKK بمستوى أعلى مباشرة (`backend/`)، ولا يولّد `deploy/` ولا `tests/`؛ وPRJ-SAKK يفتقد FOUNDATIONS/LOCKS/README التي يولّدها. لا شكل قانوني واحد.
4. **توثيق يكذب على ثلاث طبقات:** IMPORTED.md (Next.js 16 — معدوم) · STATE/CONTEXT (Vue 3 — صفر ملف .vue) · FOLDER-MAP (React 19 frontend/ — معدوم) · أرقام العدّ كلها خاطئة.
5. **Gate 6 معلَن والنشر خيال:** لا CI workflow، لا docker-compose، لا deploy.sh — البوابة «مجتازة» بلا artifacts قابلة للتشغيل (خرق V1/V4).
6. **حزام الاختبار شكلي فوق مستوى unit:** integration/ وload/ فارغتان؛ e2e = سكربت لقطات فقط؛ وادعاءات ALL GREEN غير قابلة للتحقق بلا CI.
7. `paths.py` يفشل صامتاً (يرجع مساراً غير موجود بدل خطأ صريح) → عمى الـ worktree عن المشاريع.

---

## التداخل مع الطبقات الأخرى

- **worktree v6 ↔ MAIN:** الأدوات (sofi_tools/new-project.sh) تعيش في الـ worktree، والمشاريع في MAIN — و`projects_dir()` من الـ worktree لا يصل إليها (مُثبت بالتشغيل). MAIN نفسه بلا `company/` (شجرة منزوعة) فلا نسخة عاملة من الأدوات بجوار المشاريع.
- **طبقة sofi-domain:** `sakk.local` مسجّل في `/etc/hosts:23` بوسم `# sofi-domain` — تكامل حي وناجح مع طبقة الدومين المحلي، منفصل صحيحاً عن Caddyfile الإنتاجي.
- **بقايا v5:** `projects/README.md:3` يوجّه لمسار `sofi/bin/` الميت؛ وIMPORTED.md يؤرّخ للحصاد من workspaces قديمة (`SOFI-ENGINEERING`, `SOFI_AI`).
- **CLAUDE.md doctrine ↔ الواقع:** «single physical root ~/Desktop/projects» غير موجود؛ «Flutter/Bloc» والفعلي Riverpod؛ «Blade+Vue3» والفعلي Blade+Tailwind فقط.

---

## ما يُرحَّل لنظام شامل

1. **قانون ملزم يوم-صفر: git init داخل كل مشروع + remote + أول commit كجزء من السكافولدر نفسه** — لا مشروع بلا VCS ولو لدقيقة؛ ورفع تجاهل `/projects/` أو استبداله بـ submodule/repo مستقل حقيقي. (الدرس المدفوع الثمن: مشروعان ضائعان + wipe موثّق.)
2. **نمط `_context/features/GATE0..GATE8`** — سجل artifacts البوابات القياسي؛ أنجح فكرة في PRJ-SAKK.
3. **FOLDER-MAP كعقد مُولَّد لا كوثيقة يدوية:** السكافولدر يولّد الشكل القانوني الواحد (سداسي: `_context/docs/backend|frontend|mobile/deploy/tests`) ويولّد الخريطة منه — يقتل انحراف scaffold≠واقع≠خريطة.
4. **حُرّاس `gitops.checkpoint()`** (conventional-commit، فحص المسارات المحظورة، trailer، ختم head_sha) — تُرحَّل كما هي فوق repos مشاريع حقيقية، مع تحويل «no brain to checkpoint» من تحذير إلى **فشل صريح**.
5. **`paths.py` كمصدر مسارات وحيد** — يُرحَّل بعد إصلاحين: فشل صاخب عند غياب الجذر، وحلّ صريح للـ worktrees.
6. **قاعدة «الكود هو الحقيقة»:** كل أرقام الـ brain (عدد models/tests/migrations) تُولَّد بسكربت عدّ لا تُكتب يدوياً — درس تناقضات STATE/CONTEXT/FOLDER-MAP الثلاثية.
7. نمط النشر Cloudflare→Caddy→حاوية واحدة + فكرة `browser-eyes` للفحص البصري (بعد نزع الاعتمادات المضمّنة) + بنية Flutter feature-first (25 feature) كمرجع.

---

## الحكم

**DEGRADED** — كود المنتج نفسه حديث ومتماسك والاصطلاح السداسي وسجل البوابات ممتازان، لكن المنظومة حوله مقطوعة: صفر VCS لأصل fintech كامل (مع سابقتي فقدان متحققتين)، أدوات v6 لا ترى المشاريع أصلاً، الـ brain والخرائط تناقض الكود في الـ stack والأرقام، وGate 6 معلن فوق نشر وCI غير موجودين.
