# تقرير شامل 05 — جرد الوكلاء عبر الأجيال (Agents Inventory Audit)

**التاريخ:** 2026-07-10 · **المدقّق:** وكيل جرد الوكلاء (SHAMEL) · **النطاق:** READ-ONLY
**الأشجار:** MAIN=`/home/es3dlll/Desktop/Lorka` (فرع `prj/PRJ-SAKK` @ `483d355`) · WT=`/home/es3dlll/Desktop/Lorka/.claude/worktrees/org-rooms-100` · المرجع المدموج `origin/main`.

---

## الجرد

### العدّ الفعلي (أوامر منفّذة، لا تقديرات)

| # | الجرد | المسار | العدّ الفعلي | نظام التسمية | الشكل |
|---|-------|--------|--------------|---------------|-------|
| A | spawnables v6 | `WT/.claude/agents/*.md` | **105** ملف flat | `<roomcode>-<role>.md` (مثل `bck-api-engineer`) | RCCF كامل ~43 سطراً |
| B | specs v6 | `WT/company/rooms/*/agents/*.md` | **105** عبر 15 غرفة | نفس IDs جرد A (أسماء الملفات متطابقة 105/105 — `diff` = فارغ) | persona + Operating Prompt ~57 سطراً |
| C | org-rooms personas | `WT/org-rooms/*.md` | **100** persona في 10 ملفات + `README.md` (مجموع 2217 سطراً) | `STR-01…KNB-10` غرفة/ملف، كل persona عنوان `## N. اسم بشري كامل` (`grep -c '^## '` = 10 لكل ملف) | قالب HR سداسي (أ–و) عربي |
| D | جيل claude-team على MAIN | `MAIN/.claude/agents/` | **105** ملف داخل **15 مجلد غرفة** — وليس 15 وكيلاً (تصحيح لخريطة المهمة: `find -type f` = 105) | نفس 105 IDs جرد A حرفياً (`diff` أسماء = IDENTICAL) | stub مصغّر ~6 أسطر |
| E | جيل OpenCode | `MAIN/.opencode/agents/` | **68** ملف: 10 مجلدات غرف (6–7 وكلاء لكلٍّ = 67) + `translator/translator.md` | `<room>-<NN>-<role>.md` (مثل `bkd-05-api-developer`) | frontmatter opencode + persona عربية سداسية |

**تصحيح لخريطة الأجيال:** الادعاء «MAIN فيه `.claude/agents=15` فقط» غير دقيق — الـ15 مجلدات غرف لا ملفات وكلاء؛ `git -C MAIN ls-tree -r HEAD .claude/agents` = 105 مسار متداخل (أولها `arc/arc-api-architect.md`)، والشجرة نظيفة (`git status .claude/agents` فارغ). أما `origin/main` فيعتمد المسار **المسطّح**: `git ls-tree -r origin/main` = 105 `.claude/agents/*.md` flat + 11 `org-rooms/` + 105 `company/rooms/*/agents/` — أي أن origin/main يجمع A+B+C، وجرد D يعيش فقط على فرع `prj/PRJ-SAKK`.

### بنية الملف — عيّنات مقروءة

- **A** (`WT/.claude/agents/bck-api-engineer.md`): frontmatter `name/description/tools/model` (السطور 1–12، `model: sonnet` سطر 11) ثم `# 📮 Priya Nair — API Engineer · Room 05-backend · Gate 4` (سطر 13) وأقسام 🎭Role · 📂Context · 🎯Command · 📐Format · ↪Handoff. توزيع الموديلات في الـ105: `sonnet`=72 · `inherit`=18 · `haiku`=15؛ و21 وكيلاً فقط يحمل `WebSearch: true`.
- **B** (`WT/company/rooms/05-backend/agents/bck-api-engineer.md:1-11`): frontmatter آلي غني — `agent/persona_name/title/room/reports_to/gate/experience/route{model,effort,caveman,budget}/success_metric` — ثم 10 أقسام: Who they are · How their mind works · Mission · Mastery · How they work · Activates·Consumes·Produces · Operating Prompt · Handoff · Definition of Done · Non-negotiables.
- **C** (`WT/org-rooms/STR-01.md:8-39`): قالب سداسي كامل — أ. رأس المال البشري (اسم/عمر/موقع سوري/تكوين نفسي/أكاديمي) · ب. سياق مهني · ج. أسلوب حياة · د. منظومة تقنية · هـ. مهارات ناعمة · و. **حوكمة الصلاحيات** (سلطة/مال/فيتو/اعتماديات). **تفاوت داخلي:** STR-01/UXR-02 = 354 سطراً وDSN-03 = 344 (قالب مفصّل)، والسبعة الباقية مضغوطة بفقرات **أ.**–**و.** (163–164 سطراً، مثل `BKD-05.md:10-20`).
- **D** (`MAIN/.claude/agents/bck/bck-api-engineer.md` — 6 أسطر كاملة): `description: "Endpoints per frozen contract — 422-JSON rule, no redirects."` + `model: inherit` + فقرة واحدة «You are the API Engineer…». لا tools ولا persona ولا RCCF.
- **E** (`MAIN/.opencode/agents/bkd-05/bkd-05-api-developer.md:1-10`): `mode: subagent` · `model: opencode/big-pickle` (68/68 بنفس الموديل) · `permission: {edit: allow, bash: ask}` ثم `# كريم فاروق — مطور APIs` بالقالب السداسي العربي.

---

## الصحة

1. **Parity A↔B↔registry = 105↔105↔105 مثبتة آلياً:** أسماء ملفات A وB متطابقة (`diff` فارغ)، و`WT/company/nexus/registry.yaml` يسجّل 105 `- id:` بنمط الغرف الـ15.
2. **عيّنة parity 15 وكيلاً عبر كل الغرف الـ15 — 15/15 ناجحة:** `brd-cso, str-roadmap-planner, res-journey-architect, dsn-a11y-specialist, arc-review-architect, bck-queue-engineer, fnt-vue-engineer, mob-state-engineer, dat-privacy-officer, sec-pentester, qa-lead, ops-release-manager, obs-sre, knw-reflector, gtw-gatekeeper` — الملفان موجودان، `persona_name` متطابق (Priya Nair، Emeka Obi، Tomasz Wójcik…)، والـgate متطابق بعد تحقق يدوي من 3 حالات بدت مختلفة بسبب grep (مثل `arc-review-architect`: spec=`"cross"` وعنوان الـspawnable فعلاً «Gate cross»؛ `ops-release-manager`: spec=`"6-7"` والعنوان «Gates 6–7»). consume/produce متسقة نصياً في العيّنتين المفحوصتين (`bck-queue-engineer`: نفس `Infra_Topology.md` والـasync sections؛ `sec-pentester`: نفس staging build/OpenAPI/Threat_Model → نفس `Pentest_Report.md`).
3. **قادة الغرف:** B = 15/15 غرفة فيها قائد (boardroom قائدها `brd-ceo`؛ **استثناء تسموي**: غرفة 14-gateway بلا ملف `gtw-lead.md` — القيادة عند `gtw-dispatcher` بعنوان `title: Room Lead / Dispatcher — Nexus Bus`, `gate: cross`). C = 10/10 قادة مسمّون (`org-rooms/README.md:9-18`). E = 10/10 ملفات `-lead`.
4. **تلوّث نصي حقيقي في جرد E:** 14 من 68 ملفاً تحوي محارف CJK صينية داخل النص العربي (`grep -rlP '[\x{4e00}-\x{9fff}]'`) — كامل `bkd-05/` (7 ملفات)، كامل `gtw-06/` (6)، و`mob-04-animation-specialist.md`. أمثلة حرفية من `bkd-05-api-developer.md:25,35`: «ي感兴趣的 في تطوير…» و«لا ي执着 برأيه»، وعنوان مشوّه سطر 21: «## السياق المهني.TextEdit». الجيل ميّت وظيفياً (الموديل `opencode/big-pickle` والمنصة أُزيلا).
5. **جرد D سليم داخلياً (committed نظيف @ `483d355`) لكنه جيل موازٍ حي بمحتوى مغاير جذرياً لجرد A رغم تطابق الأسماء** — انظر «التداخل».

---

## نقاط القوة

- **الاكتمال العددي المثلّث:** 105 spawnable = 105 spec = 105 registry entry، وعدّة كل غرفة تطابق CLAUDE.md (brd·7, dsn·8, bck·8, mob·6, gtw·6…) — أعيد عدّها غرفة-غرفة وطابقت 15/15.
- **جرد B هو الأغنى آلياً:** frontmatter قابل للاستعلام (`route: {model, effort, caveman, budget}` + `success_metric` + `gate` + `reports_to`) يتيح التوجيه الاقتصادي والتحقق الآلي دون parsing نصّي.
- **جرد A يفرض least-privilege فعلياً:** tools grants صريحة لكل وكيل (21 فقط بـWebSearch — يطابق «Devs stay on the frozen contract»)، وmodel مثبّت بالملف (72 sonnet/15 haiku) بدل inherit شامل كما في D.
- **جرد C هو الأغنى بشرياً:** حوكمة صلاحيات per-person لا نظير لها في A/B (فيتو الرئيس وحده؛ «حق رفض دمج محدود بنطاق مهمته + تصعيد للرئيس» — `BKD-05.md:36`)، أسماء وجغرافيا سورية متماسكة، وقسم اعتماديات بينية يرسم شبكة الغرف (`BKD-05.md:20`: ارتباط بـ GTW-06/SEC-09/OPS-08).
- **استمرارية persona بين E وC عند مستوى القادة:** قادة opencode الأربعة المفحوصون (طارق الجندي str، رانيا الحسين knb، سارة الحلبي uxr، يوسف حداد bkd) هم أنفسهم قادة org-rooms — أي أن C توثيق موسّع (6–7→10 لكل غرفة) لنفس المنظمة لا منظمة جديدة.

---

## نقاط الضعف

- **ثلاثة أسماء بشرية لدور وظيفي واحد — لا canon موحّد:** مهندس API الخلفي = **Priya Nair** (A/B) و**عمّار خضّور** (`org-rooms/BKD-05.md:24-36`) و**كريم فاروق** (`.opencode/agents/bkd-05/bkd-05-api-developer.md:10`). جردا A/B كونٌ دولي (هندية/نيجيري/بولندي…) وجردا C/E كونٌ سوري — بلا أي جدول ربط.
- **جرد C غير موصول بأي طبقة آلية:** لا ID يربط «عمّار خضّور» بـ`bck-api-engineer`؛ personas الـ100 توثيق HR معلّق بلا spawnable ولا registry entry — 100 ملف-دور بلا ذراع تنفيذية.
- **تفاوت قالب C غير مكتمل التوحيد:** 3 غرف بالصيغة المفصّلة (~350 سطراً) و7 بالمضغوطة (~164) — نفس الأقسام الستة بعمق غير متساوٍ.
- **فجوات تغطية في منظمة الغرف العشر (C):** لا boardroom، لا architecture مستقلة (مدموجة في قائد BKD-05)، **لا web-frontend implementer إطلاقاً** (ذكر Vue/React الوحيد في DSN-03 تصميمي)، **لا غرفة QA** (الاختبار مبعثر: `MOB-04` #9 on-device perf tester، `DSN-03` #10 component QA، `KNB-10` #10 linguistic QA)، **لا observability** (شظية وحيدة: `GTW-06` #8 Latency/Observability Engineer).
- **stubs جرد D بلا عمق:** 6 أسطر، `model: inherit` للـ105 كلها (لا توجيه اقتصادي)، لا tools grants (وراثة كاملة — عكس least-privilege)، لا persona ولا evidence contract.
- **جرد E مشوّه ومهجور:** 14/68 ملوّثة CJK، موديل ميت واحد للجميع، ومكدّسه (Go microservices في `BKD-05.md:3`) يخالف stack defaults الحالية.

---

## التداخل مع الطبقات الأخرى

1. **أخطر تداخل — تعريفان حيّان لنفس 105 IDs يتبدّلان حسب الشجرة:** جلسة على MAIN (`prj/PRJ-SAKK`) تحمّل stubs جرد D (وصف `bck-api-engineer` القصير هو الظاهر فعلاً في قائمة الوكلاء المحمّلة لهذه الجلسة)، بينما جلسة على WT/origin/main تحمّل RCCF الكامل. نفس الاستدعاء `@bck-api-engineer` = وكيل مختلف السلوك والموديل (inherit vs sonnet) حسب الفرع — انحراف صامت.
2. **تصادم كود GTW الدلالي:** v6 `gtw` = مشغّلو الـNexus (dispatcher/router/gatekeeper/budget-warden — حوكمة داخلية)؛ C/E `GTW-06` = هندسة API Gateway خارجية (Kong، OAuth2/JWT، rate-limit، Stripe payments، webhooks، load balancing — `org-rooms/GTW-06.md` العناوين 1–10). نفس الاختصار، وظيفتان غير مترابطتين؛ وظيفة GTW-06 تقع في v6 عند `arc-integration-architect` + `bck-integration-engineer` + `sec-authn-engineer`.
3. **انزياح دلالي MOB:** v6 `mob` = هندسة Flutter/Bloc (بناء Gate 4)؛ C `MOB-04` = تصميم واجهات موبايل ونمذجة حركية (Lottie/gestures/prototyping) — التقاطع الوحيد «Flutter Handoff Specialist» (#5).
4. **تسميتان لوظيفة واحدة:** `res` ↔ `UXR-02` (أبحاث المستخدم) و`knw` ↔ `KNB-10` (المعرفة) — تطابق وظيفي شبه كامل باسمين.
5. **يتيم بلا غرفة:** `translator.md` في E (Semantic Gateway يحوّل المدخل الخام إلى JSON للـCEO — frontmatter:1-2) — وظيفته ورثها `gtw-dispatcher` في v6 لكن الملف بلا نظير معلن.
6. **تكامل A/B مع بقية v6 سليم:** كل spawnable يشير لملف spec الصحيح وroute في `routing.yaml` وcharter غرفته (`bck-api-engineer.md:16,23-24`) — الربط agents↔nexus↔constitution متماسك.

### مصفوفة تطابق الغرف — v6 (15) × org-rooms (10)

| غرفة v6 | org-rooms | نوع التطابق |
|---------|-----------|-------------|
| brd boardroom | — | **v6 فقط** (قيادة C موزّعة: قائد STR-01 «CPO & ECD»، قائد SEC-09 «CISO» — `README.md:9,17`) |
| str strategy | STR-01 | تطابق مباشر (BA/market/monetization/roadmap/risk في الجهتين) |
| res research | UXR-02 | نفس الوظيفة — **تسمية مختلفة فقط** (v6 أوسع: web-scout/fact-checker) |
| dsn design | DSN-03 | تطابق مباشر (tokens/brand/a11y/content) |
| arc architecture | — | **v6 فقط** (مدموجة في قائد BKD-05 «Chief Backend Architect» + system/database architects في E) |
| bck backend | BKD-05 | تطابق + BKD تبتلع arc وجزء dat وتضيف Go microservices |
| fnt frontend | — | **v6 فقط** — لا web-frontend implementer في الغرف العشر (فجوة) |
| mob mobile | MOB-04 | **جزئي** — v6 هندسة Flutter، C تصميم حركي/نمذجة |
| dat data | DAT-07 | تطابق (ميْل C للتحليل السلوكي/BI؛ v6 تضيف cache/ETL/migrations) |
| sec security | SEC-09 | تطابق مباشر (CISO) |
| qa quality | — | **v6 فقط** — الاختبار في C مبعثر بلا غرفة (فجوة) |
| ops devops | OPS-08 | تطابق (+DR engineer في C؛ لا monitoring فيها) |
| obs observability | — | **v6 فقط** — شظية وحيدة في GTW-06 #8 (فجوة) |
| knw knowledge | KNB-10 | نفس الوظيفة — **تسمية مختلفة فقط** (kn**w** ↔ KN**B**) |
| gtw gateway/Nexus | GTW-06 | **تصادم**: نفس الكود، وظيفتان مختلفتان كلياً (حوكمة داخلية vs API gateway خارجية) |

---

## ما يُرحَّل لنظام شامل

1. **من B (الأغنى للآلة):** صيغة الـspec الكاملة — frontmatter الآلي (`route/success_metric/gate/reports_to/persona_name`) + Consumes/Produces + Definition of Done + Non-negotiables. هذا **العمود الفقري** لسجل وكلاء شامل: ملف واحد queryable آلياً ومقروء بشرياً.
2. **من A:** انضباط الـspawnable — tools grants صريحة per-agent (least-privilege) + model مثبّت بالملف + بنية RCCF المطابقة للـWork Order؛ ونمط التسمية flat `<room>-<role>` (الأسهل استدعاءً وdiffاً).
3. **من C (الأغنى للبشر):** طبقة **حوكمة الصلاحيات السداسية** (سلطة تشغيلية/مالية/فيتو/تصعيد/اعتماديات per-person — لا نظير لها في A/B) + الكانون العربي-السوري للأسماء إن أراد شامل هوية محلية — بشرط بناء **جدول ربط ID↔persona** يُنهي ازدواج الكانونين.
4. **من D:** لا محتوى — لكن **الدرس المعماري**: نسخة stub خفيفة تُحمَّل بالسياق (اقتصاد tokens) مع إحالة للـspec الكامل؛ شامل يولّدها آلياً من frontmatter جرد B بدل صيانة جيلين يدوياً.
5. **من E:** فكرتان فقط — وكيل **translator** (بوابة دلالية قبل CEO) ونموذج `permission: {edit, bash}` per-agent في frontmatter؛ الباقي superseded ومشوّه — **يُؤرشف ولا يُرحَّل**.
6. **قرارات دمج واجبة قبل الترحيل:** حسم تصادم GTW (إعادة تسمية أحدهما)، اعتماد خريطة الغرف (15 أم 10 — والـ15 أكمل تغطيةً)، وسدّ فجوات fnt/qa/obs إن اعتُمدت العشر، وإلغاء أحد التعريفين الحيّين للـ105 IDs (توحيد MAIN على نسخة origin/main).

---

## الحكم

**DEGRADED** — نواة v6 سليمة تماماً (A↔B↔registry = 105↔105↔105 مع parity عيّنة 15/15)، لكن الطبقة ككل تحمل تعريفين حيّين متعارضين لنفس الـ105 IDs (stubs على `prj/PRJ-SAKK` vs RCCF على origin/main)، وكانونَي personas منفصلين بلا جدول ربط (دولي A/B vs سوري C/E)، وتصادم GTW الدلالي، وجرد opencode ميتاً ومشوّهاً بمحارف CJK في 14/68 ملفاً.
