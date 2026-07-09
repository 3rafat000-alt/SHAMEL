# شامل / SHAMEL — 10: تقرير الاتساق النهائي (Cross-Document Consistency)

**التاريخ:** 2026-07-10 · **الفاحص:** حارس الاتساق (fresh-context) · **النطاق:** التناقضات **بين** الوثائق العشر حصراً: `08-COMPARISON-MATRIX` · `09-GAP-ANALYSIS` · `PRD` · `ARCHITECTURE` · `BRAIN` · `PROTOCOL` · `AUTOMATION` · `PROJECT-STRUCTURE` · `MASTER-PLAN` · `MIGRATION` (قراءة كاملة لكل وثيقة؛ doc-vs-disk خارج النطاق).
**مرجع التحكيم:** بند PROTOCOL «عند أي تعارض بنيوي يحسم ARCHITECTURE (الـ Design Record الحاكم)» + ADR-006 (MASTER-PLAN Phase 2.3) الذي حسم خمسة تعارضات مسبقاً.

**الحصيلة: 25 تناقضاً — CRITICAL 2 (أُصلحا مباشرة) · HIGH 6 · MEDIUM 10 (منها 5 محسومة سلفاً بـ ADR-006 بانتظار commit التصحيح) · LOW 7.**

---

## 1) جدول التناقضات

| # | الخطورة | الوثيقتان (الموضع) | التعارض | الأصح | التصحيح بسطر |
|---|---------|---------------------|----------|-------|----------------|
| C1 | 🔴 CRITICAL | PROJECT-STRUCTURE §3.4 ↔ BRAIN §2.3 (+MASTER-PLAN 5.7) | STATE.md قالب frontmatter YAML مقابل قانون BRAIN الملزم «key: value صرفة بلا frontmatter، parser حتمي لا YAML lib» — doctor مرحلة 5 كان سيرسّب كل مشروع يولده سكافولد مرحلة 7 | BRAIN (سلطة معمارية الذاكرة، وMASTER-PLAN يتبناها) | **أُصلح ✅** — PS §3.4 حُوّل إلى صيغة flat (مع تسطيح facts إلى `facts_*` + إضافة `counts_sha`) |
| C2 | 🔴 CRITICAL | BRAIN §6 المرحلة-0 ↔ PROJECT-STRUCTURE §2.3 + MIGRATION §0-8 + MASTER-PLAN 0.1 | سكربت إنقاذ SAKK في BRAIN يعمل add/commit/push **قبل** تطهير الأسرار (يُدخل اعتمادات browser-eyes.sh لتاريخ لا يُمحى — يكسر قبول Phase-0 `gitleaks = 0` بلا علاج لأن إعادة كتابة التاريخ محظورة) ويدفع لفرع `master` بدل `main` | PS §2.3 (التسلسل المعلَن ملزماً حرفياً في MASTER-PLAN 0.1) | **أُصلح ✅** — BRAIN §6: gitleaks قبل add + `git init -b main` + push إلى main + إحالة لـ PS §2.3 |
| H1 | 🟠 HIGH | PRD FR-10 (+معيار قبوله §9) ↔ BRAIN §6-3a + MASTER-PLAN 5.1/قبولها ↔ ARCHITECTURE §2 | عدد قوالب الدماغ: PRD «السبعة» مقابل 8 (ستة v6 + FOLDER-MAP + LOCKS) مقابل 6 مسرودة في شجرة ARCHITECTURE — معيارا قبول متعارضان (7 vs `wc -l = 8`) | 8 (BRAIN + MASTER-PLAN) | PRD FR-10 → «القوالب الثمانية» ومعيار القبول `= 8`؛ سرد شجرة ARCHITECTURE يستكمل LOCKS + FOLDER-MAP |
| H2 | 🟠 HIGH | PRD §4.3 + FR-32/33 ↔ ARCHITECTURE §2/§3.3 ↔ AUTOMATION §2.4 | موطن المحرك الخارجي والـ oracle: `automation/{pipeline,oracle,logs}/` (PRD) مقابل `engine/shamel_tools/pipeline/` + `net/oracle.py` (ARCHITECTURE — تتبعه MASTER-PLAN 3.8/9.4) مقابل `orchestrator/` بالجذر (AUTOMATION) — ثلاثة بيوت لنفس الـ concern وADR-006 لا يسمّيه | ARCHITECTURE | توسيع ADR-006 ببند (و): موطن pipeline/oracle = `engine/shamel_tools/{pipeline,net}` وتصحيح PRD/AUTOMATION في commit 2.3 |
| H3 | 🟠 HIGH | PRD §4.3 (الشجرة) ↔ ARCHITECTURE §2 | PRD يضع `constitution/ nexus/ rooms/ os/` في الجذر؛ ARCHITECTURE تحت `core/` و`engine/` — شجرتان قانونيتان متخالفتان في المرجع الأم | ARCHITECTURE (بند التحكيم في PROTOCOL + MASTER-PLAN 2.2 «حرفياً من ARCHITECTURE §2») | تحديث شجرة PRD §4.3 ضمن commit تصحيح الوثائق (Phase 2.3) |
| H4 | 🟠 HIGH | ARCHITECTURE §2 + PRD §4.3 + MASTER-PLAN 10.8 ↔ BRAIN §2.2/§6 (+MIGRATION §9.3 يتبعه) | موطن المقبرة: `archive/` بجذر شامل مقابل `brain/archive/` — وجهات دفن BRAIN §6 (v5-engine، opencode-memory…) تخالف `archive/INDEX.md` الجذري | ARCHITECTURE (المقبرة أصل تنظيمي لا ملف ذاكرة) | وجهات BRAIN §6 وMIGRATION §9.3 → `archive/<name>/`؛ `brain/archive/` يُشطب من شجرة BRAIN |
| H5 | 🟠 HIGH | PROTOCOL §8.1 + §3.1 (gate-0/5) + مثال STATE في BRAIN §2.3 ↔ PROJECT-STRUCTURE §2.2/§3.2 + MASTER-PLAN 7.1 | فرع عمل ريبو المشروع: `prj/<PRJ-ID>` (PROTOCOL/BRAIN) مقابل `main` فرع التكامل الوحيد + `gate4/<squad>` + `fix/<TKT>` (PS، وقانون المصنع `git init -b main`) | PROJECT-STRUCTURE (نمط prj/ أُلغي نصاً وMASTER-PLAN يتبعه) | PROTOCOL §8.1 وsnapshot البوابات ومثال BRAIN → `main` داخل ريبو المشروع |
| H6 | 🟠 HIGH | BRAIN §7.4 ↔ PROJECT-STRUCTURE §1.4-2 + قبول MASTER-PLAN Phase-8 | موضع كتلة الأرقام المولَّدة: BRAIN يضعها بلوك `<!-- generated:counts -->` في CONTEXT (وSTATE يحمل counts_sha فقط)؛ PS وقبول Phase 8 (`grep generated_at STATE.md`) يضعانها في STATE | STATE (قبول MASTER-PLAN الميكانيكي + PS، وأُبقي عليه في إصلاح C1) | BRAIN §7.4 → «الكتلة في STATE (`facts_*`) وcounts_sha معها؛ CONTEXT يحمل الوقائع لا العدّ» |
| M1 | 🟡 MEDIUM | PRD FR-80 + BRAIN §2.2 + AUTOMATION §2.3/2.4 ↔ ARCHITECTURE + PROTOCOL | مسار الموزّع: `os/bin/shamel` مقابل `engine/bin/shamel` | engine/bin — **محسوم ADR-006(أ)** | تصحيح PRD/BRAIN/AUTOMATION في commit 2.3 (المجدول أصلاً) |
| M2 | 🟡 MEDIUM | BRAIN §2.2/§4.3 (`.claude/memory/`) ↔ AUTOMATION/PROTOCOL §9.4 (`.shamel/`) ↔ ARCHITECTURE (`brain/db/`) ↔ PRD §4.3/FR-13 (`brain/memdb/`) | أربعة أسماء لموطن الـ runtime/memdb الواحد (وسجلاته) | brain/db + brain/db/logs — **محسوم ADR-006(ب)** | توحيد المسارات الأربعة في commit 2.3 (يشمل `taskq.db` لا `tasks.db`) |
| M3 | 🟡 MEDIUM | AUTOMATION §2.4 (`schemadb.py`) ↔ ARCHITECTURE §3.3 + MASTER-PLAN 3.2 (`schemas.py`) | اسم موديول مخططات substrate بعد إعادة التسمية | schemas.py — **محسوم ADR-006(ج)** | تصحيح AUTOMATION §2.4 |
| M4 | 🟡 MEDIUM | PRD FR-31 (`automation/cron.d/*.yaml` manifests) ↔ AUTOMATION §2.3 + PROTOCOL §9.4 (`cron/shamel.crontab` الملف الوحيد) | آليتا جدولة متخالفتان | cron/shamel.crontab — **محسوم ADR-006(د)** (`automation install/status` يعملان عليه) | تصحيح PRD FR-31 ومثال الـ manifest |
| M5 | 🟡 MEDIUM | PRD FR-30/§4.3 + ARCHITECTURE §2/§5 (خمسة hooks) ↔ AUTOMATION §2.2 + MASTER-PLAN 6/قبولها (سبعة) | عدد أحداث hooks الرسمي؛ وPRD FR-30 يدمج اللقاح في SessionStart بينما هو hook مستقل (UserPromptSubmit) | 7 — **محسوم ADR-006(هـ)** | تصحيح PRD/ARCHITECTURE + فصل اللقاح حدثاً مستقلاً في FR-30 |
| M6 | 🟡 MEDIUM | PRD FR-40 (+قبوله: remote إلزامي داخل الذرّية) ↔ PROJECT-STRUCTURE §2.1-2/§3.1 + MASTER-PLAN 7.1 (`remote: (pending)` بمهلة، gate-check>0 يفشل) | إلزامية remote لحظة الولادة مقابل نافذة سماح مضبوطة | PS (الأكثر تفصيلاً والمصدر التنفيذي للمصنع) | PRD FR-40 يعتمد نمط pending-بمهلة وmirror المحلي البديل |
| M7 | 🟡 MEDIUM | ARCHITECTURE §2 (`code_scan.py · verify.py`) ↔ PRD FR-81 + MASTER-PLAN 3.2 (`shamel_scan · shamel_verify`) | اسما الماسحين بعد إعادة التسمية مختلفان بين الوثيقتين | PRD/MASTER-PLAN (حزمة FR-05 sofi→shamel) | شجرة ARCHITECTURE §2 → `shamel_scan.py · shamel_verify.py` |
| M8 | 🟡 MEDIUM | AUTOMATION §2.4 (يبقي `os/substrate/` حزمة منفصلة بجوار `lib/shamel_tools/`) ↔ ARCHITECTURE §3.3 + MASTER-PLAN 3.1 (substrate يندمج داخل `shamel_tools/core/`) | شكلان متخالفان لتوحيد الطبقة الحتمية (انفصال مقابل اندماج) | ARCHITECTURE (ADR-002: مكتبة واحدة) | شجرة AUTOMATION §2.4 تُطابق ARCHITECTURE §3.3 |
| M9 | 🟡 MEDIUM | PROTOCOL §3.1 (artifacts البوابات بمسارات `docs/<PRJ>_*.md`) ↔ PROJECT-STRUCTURE §4 + PRD FR-44 (النسخة المجمّدة الوحيدة في `_context/features/GATE<n>-*` وdocs يشير ولا ينسخ) | موطنا الـ artifact المجمّد متعارضان — وgate-check يقرأ من `_context/features/` | PS/PRD (وPROTOCOL نفسه يعلن الـ snapshot غير مُلزم) | مسارات artifacts في snapshot PROTOCOL → `_context/features/GATE<n>-…` |
| M10 | 🟡 MEDIUM | PRD FR-31 (الحد الأدنى: reflect أسبوعي + **brain-audit يومي** + doctor يومي) ↔ AUTOMATION §2.3 + PROTOCOL §9.4 (crontab: doctor + memdb-compact + reflect + budget — بلا brain-audit) | ادعاء جدولة brain-audit اليومي بلا سطر في ملف الجدولة الوحيد — إعادة إنتاج «أتمتة ورقية» على الورق نفسه | يُحسم بالإضافة (روح GAP-11) | إضافة سطر `shamel brain-audit` يومي إلى `cron/shamel.crontab` أو حذفه من حد PRD الأدنى |
| L1 | 🟢 LOW | ARCHITECTURE §5 (reflect ليلي 03:15 + doctor أسبوعي) ↔ AUTOMATION §2.3/PROTOCOL §9.4 (doctor ليلي + reflect أحد 04:00) ↔ BRAIN §5.2 (reflect أحد 22:00 + doctor 08:00) ↔ PRD FR-31 (اثنين 06:00) | أربعة جداول زمنية مختلفة لنفس الوظيفتين في الأمثلة | ملف `cron/shamel.crontab` هو الحاكم (والإيقاع أسبوعي لـ reflect وفق G-10) | توحيد كل الأمثلة على مرآة AUTOMATION §2.3 |
| L2 | 🟢 LOW | PRD FR-62 + MASTER-PLAN 6.5 (13 skill بأسماء `shamel-*`) ↔ PROTOCOL §1/§9 + ARCHITECTURE §5 + BRAIN §5 (`/boot` `/gate` `/handoff` `/delegate` `/reflect` بلا سابقة) | تسميتا الـ skills متخالفتان بين القانون والأمثلة | `shamel-*` (FR-62 وقبول Phase 6) | توحيد أمثلة PROTOCOL/ARCHITECTURE/BRAIN على `/shamel-*` |
| L3 | 🟢 LOW | BRAIN §5.2 (`shamel doctor --install-cron`) ↔ PRD FR-31/ADR-006(د) (`shamel automation install`) | أمرا تثبيت مختلفان لنفس الجدولة | automation install (ADR-006-د) | BRAIN §5.2 → `shamel automation install` |
| L4 | 🟢 LOW | PROTOCOL D5/§8.2 (trailer `gate 4` بمسافة) ↔ PROJECT-STRUCTURE §2.1-5/§2.3 (`gate4` بلا مسافة) | صيغتا trailer متخالفتان — وregex فحص `git-check` سيقبل واحدة فقط | PROTOCOL (قانون git السلوكي) | أمثلة PS → `gate <N>` بمسافة |
| L5 | 🟢 LOW | PRD FR-02 (+08-المصفوفة بند 2): `nexus/agent-pins.json` ↔ ARCHITECTURE §2 + MASTER-PLAN 4.4: `nexus/pins.json` | اسمان لملف البصمات الواحد | pins.json (ARCHITECTURE) | PRD FR-02 → `pins.json` |
| L6 | 🟢 LOW | PRD FR-04 + MASTER-PLAN 4.3 (`nexus/personas.yaml` جدول الربط الوحيد) ↔ BRAIN §2.2 (`brain/org/PERSONAS.md` «+ جدول ربط ID↔persona») وشجرة ARCHITECTURE تغفل personas.yaml أصلاً | ازدواج مُعلن لجدول الربط + غيابه من الشجرة الحاكمة | personas.yaml وحده للربط الآلي | BRAIN: PERSONAS.md بشري صرف يشير للجدول؛ إضافة personas.yaml لشجرة ARCHITECTURE §2 |
| L7 | 🟢 LOW | 09-GAP-ANALYSIS GAP-16 (فجوات الخريطة العشرية تشمل architecture) ↔ 08-المصفوفة/PRD FR-04/MIGRATION §7 (fnt/qa/obs/brd فقط +GTW) | قائمتا الغرف الناقصة في خريطة العشر غير متطابقتين | 08 (التركيب المسنود للتقرير 05) | توحيد نص GAP-16 على fnt/qa/obs/brd(+GTW) أو إثبات architecture بمصدر |

---

## 2) ما أُصلح مباشرة (CRITICAL فقط — بأداة Edit، في الوثيقة الأدنى صحة)

1. **C1 · `PROJECT-STRUCTURE.md` §3.4** — قالب STATE.md حُوّل من frontmatter YAML إلى `key: value` صرفة مطابقة لـ BRAIN §2.3: أُزيلت أسيجة `---`، سُطّحت كتلة `facts:` إلى مفاتيح `facts_*`، أُضيف `counts_sha`، ودُمج الذيل (`blockers`/`next`) في القائمة الواحدة.
2. **C2 · `BRAIN.md` §6 المرحلة-0** — سكربت إنقاذ PRJ-SAKK: أُدرج تطهير الأسرار + `gitleaks --no-git` **قبل** أول `git add` وحارس `--staged` ثانٍ، `git init -b main` بدل الدفع إلى `master`، مع إحالة صريحة إلى التسلسل الملزم في PROJECT-STRUCTURE §2.3.

*(M1–M5 محسومة سلفاً بـ ADR-006 وتصحيح وثائقها commit مجدول في MASTER-PLAN 2.3 — لم تُلمس هنا كي يبقى ذلك الـ commit موحّداً كما خطط له.)*

---

## 3) عيّنات ما فُحص ووُجد متسقاً (نظافة صريحة)

- **الأعداد الجوهرية:** 105 وكيلاً · 15 غرفة · 9 بوابات (0–8) · سلّم routing رباعي (mechanical/workhorse/gatekeeper/deep بنفس الـ model aliases الأربعة) · 13 skill (spine 6 + power 7) · 114 سكربت (قبول ≥110 موحّد) · ≤15 أمراً مغربلاً · 12 مادة دستورية (00..11) · 47 جلسة legacy تُستورد — متطابقة عبر الوثائق العشر.
- **الثوابت السلوكية:** سقف حقن الإقلاع 1000 توكن · عتبة دين reflection = 5 · قاطع الدائرة عند 3 محاولات · سلسلة التصعيد (specialist→lead→conflict-resolver→arbiter→CEO + مسار CSO) · المساءلة CPO 0-2/CTO 3-4/CQO 5 · two-track (fast/deep، عند الشك deep) — بلا انحراف.
- **خرائط الإحالة:** كل GAP-01..20 مغطى بـ FR (خريطة PRD §9) وبمرحلة (MASTER-PLAN §12)؛ إحالات MIGRATION إلى Phases وADRs تحلّ كلها؛ إعادة تصنيف PRJ-SAKK gate 6→4/5 متسقة في 09/PRD/PS/MASTER-PLAN/MIGRATION.
- **قرارات Q1–Q7** (PRD §7.3) متطابقة مع ADR-001..004 ومع MIGRATION §1 (15 غرفة، GTW=Nexus، الكانون العربي، worktrees خارج `.claude/`، paths fail-loud).
