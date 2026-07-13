# شامل / SHAMEL — وثيقة متطلبات المنتج (PRD)

**الإصدار:** 1.0 · **التاريخ:** 2026-07-10 · **الحالة:** مرجع أم (Master Reference)
**المصادر الملزمة:** `08-COMPARISON-MATRIX.md` (المصفوفة) · `09-GAP-ANALYSIS.md` (GAP-01…GAP-20) · تقارير التدقيق 03/05/06 في `_scratch/shamel/`
**الجذر المستهدف:** `~/Desktop/SHAMEL/` — repo git مستقل جديد يخلف كل أجيال SOFI الستة (G1–G6).

**المبادئ الحاكمة (غير قابلة للتفاوض):**
1. **مصدر حقيقة واحد لكل concern** — لا تكرار طبقات (علاج GAP-06).
2. **عقل/دماغ مهيكل ومؤتمت** — الذاكرة تتغذى آلياً لا يدوياً (علاج GAP-11/12).
3. **بروتوكول واحد شامل** — دستور واحد يحقنه كل مسار إقلاع (علاج GAP-08).
4. **أتمتة حقيقية لا نظرية** — كل ادعاء أتمتة له مشغّل فعلي قابل للإثبات (علاج GAP-04/11).
5. **مصنع مشاريع موحّد** — كل مشروع repo git خاص من الدقيقة صفر (علاج GAP-01/09).
6. **اقتصاد توكن** — few token do trick (وراثة درع G3).
7. **التحقق العدائي** — لا self-grading؛ المنفّذ لا يحكم على نفسه أبداً (وراثة V2).
8. **يعمل داخل Claude Code** — flat topology، لا daemon داخلي؛ الأتمتة الخارجية عبر `claude -p` + cron (وراثة فلسفة G5 «ledger لا daemon»).

---

## 1. الرؤية والمشكلة

### 1.1 الرؤية

**شامل** هو النظام الموحّد الواحد لتشغيل مؤسسة برمجيات ذاتية القيادة بوكلاء AI داخل Claude Code: مشغّل بشري واحد + شركة وكلاء منظّمة في غرف، تحكمها بوابات دورة حياة عدائية التحقق، وتخدمها طبقة أدوات حتمية صفرية-التوكن، ودماغ مهيكل يتعلم آلياً — كل ذلك في **جذر واحد، سلالة git واحدة، دستور واحد، نقطة دخول تنفيذية واحدة**.

### 1.2 المشكلة — لماذا نظام جديد وليس ترقية سادسة؟

التدقيق الشامل (تقارير 01–07 + تقريرا الصحة) أثبت أن المنظومة الحالية ليست نظاماً واحداً بل **ستة أجيال متعايشة** تتقاسم قرصاً واحداً وتتناقض:

| العرَض | الدليل | الجذر |
|---|---|---|
| أصل الشركة الأساسي (منصّة fintech كاملة: 25 model · 38 controller · 136 ملف dart + دماغه) خارج أي VCS، مع **سابقتَي فقدان متحققتين** (xo-game، heart-clinic) وwipe موثّق | GAP-01 | لا قانون «يوم-صفر git» في المصنع |
| ثلاث سلالات git متباعدة في مستودع واحد؛ الجلسة تعيش تحت دستور مختلف حسب مجلد الإقلاع («no slash-commands» في MAIN مقابل «13 skill مقدّسة» في WT) | GAP-02, GAP-08 | لا مصدر عقيدة واحد |
| كود حي فريد untracked مهدد بالضياع الفوري: fork الـ orchestrator + `ceo_agent.py` + 114 سكربت أدوات + browser-eyes | GAP-03 | الابتكار يسبق الالتزام (commit) |
| 5 أجيال محرّكات · 8 نقاط دخول (5 باسم `sofi`) · 8 أنظمة ذاكرة · 5 جرود وكلاء · حتى 6 تطبيقات متوازية للـ concern الواحد | GAP-06 | كل جيل بُني بجوار سلفه لا فوقه |
| نفس `@agent-id` = وكيل مختلف السلوك والموديل والصلاحيات حسب الفرع (stub بـ `model: inherit` بلا tools مقابل RCCF كامل least-privilege) | GAP-07, GAP-10 | جردان حيّان لنفس الـ 105 IDs |
| Gate 6 «مجتازة» فوق CI معدوم وrunbook يستشهد بأربعة ملفات غير موجودة — في منتج أموال/KYC | GAP-04 | البوابات تقبل ادعاءً بلا artifact قابل للتشغيل |
| «scheduled reflection» بلا مجدوِل (crontab فارغ)، memdb بصفّ واحد، oracle يرجع exit 0 عند الفشل | GAP-11 | أتمتة ورقية: العقيدة تعلن ما لا يعمل |
| الدماغ يكذب: STATE ≠ CONTEXT ≠ الكود (أرقام وstack — ثلاث روايات للويب كلها خاطئة) | GAP-12 | أرقام تُكتب يدوياً بدل أن تُولَّد |

**الخلاصة:** المشكلة ليست نقص القدرات — G3 (v6) فاز في 8/10 أبعاد بالمصفوفة وG5 يعمل PASS 6/6 — بل **غياب الوحدة**: لا شيء يمنع نشوء نسخة موازية جديدة، ولا شيء يجبر الادعاء على مطابقة الواقع. شامل يُبنى ليكون النسخة الأخيرة: يرحّل الفائزين، يدفن الباقي بشواهد قبور، ويحوّل مبادئ «المصدر الواحد» و«لا ادعاء بلا إنفاذ» من وعظ إلى فحوصات fail-closed.

### 1.3 لماذا الآن

خيط الترابط في تحليل الفجوات صريح: **الإنقاذ لا ينتظر** (GAP-01/03 قابلة للفناء بأمر `rm -rf` واحد أو `git checkout` عرَضي)، والمصالحة (GAP-02) بوابة كل توحيد لاحق. كل يوم تأخير يوسّع التباعد بين السلالات الثلاث ويرفع كلفة الدمج.

---

## 2. المستخدم

### 2.1 المشغّل الواحد (The Single Operator)

- **من هو:** مهندس/مؤسس واحد يدير المؤسسة كلها من جلسات Claude Code على سطح مكتب Linux محلي. لا فريق بشري ثانٍ، لا مستخدم متزامن.
- **ما يحتاجه:**
  - إقلاع بلا التباس: أي جلسة تُفتح من أي مسار داخل شامل تحقن **نفس** الدستور ونفس الخريطة (عكس واقع GAP-08).
  - تفويض بثقة: `@agent-id` يعني وكيلاً واحداً معرّف السلوك والموديل والصلاحيات (عكس GAP-07).
  - رؤية حقيقية: `shamel doctor` وتقارير الدماغ تعكس القرص لا الأمنيات (عكس GAP-12).
  - استرداد مضمون: لا عمل يضيع — كل شيء في git بremote (عكس GAP-01/03).
  - كلفة محتملة: حقن السياق مضبوط، والعمل الحتمي صفري-التوكن (وراثة G3+G5).
- **ما لا يحتاجه:** واجهات ويب إدارية، تعدد مستخدمين، صلاحيات RBAC بشرية — هذه خارج النطاق (§4).

### 2.2 وكلاء AI (المستخدمون الآليون)

| الصنف | الدور | ما يستهلكه من شامل |
|---|---|---|
| **جلسة الأوركسترا (CEO)** | القيادة داخل الجلسة: تفويض RCCF، قرارات بوابات، تحكيم | CLAUDE.md + hooks orientation + `shamel` CLI + registry/routing/gates |
| **الوكلاء المتخصصون (subagents)** | تنفيذ التذاكر داخل الجلسة عبر spawn | spawnable مولّد + spec الغرفة + دماغ المشروع + أدوات الغرفة |
| **المحرك الخارجي (pipeline)** | أتمتة طويلة خارج الجلسة عبر `claude -p` | نفس الـ Nexus (لا عالم موازٍ — عكس واقع G6) + state ledger |
| **العرّاب الخارجي (oracle)** | مراجعة خارجية sanitized (Teaching VII) | مكتب oracle: sanitize→condense→push→capture→ingest |
| **المهام المجدولة (cron)** | reflection، hygiene، تقارير دورية | manifests في `automation/cron.d/` تستدعي `claude -p /skill` |

**قاعدة معمارية:** كل هؤلاء يقرؤون **نفس** الملفات الثلاثة (`registry.yaml` · `routing.yaml` · `gates.yaml`). لا يحق لأي مستهلك بناء نسخته الخاصة من الحقيقة (درس G6 الذي «لا يقرأ nexus إطلاقاً»).

---

## 3. الأهداف ومقاييس النجاح

كل هدف يقاس ميكانيكياً — لا مقياس يعتمد على تقييم ذاتي (اتساقاً مع V4).

| ID | الهدف | المقياس | الهدف الرقمي | طريقة القياس |
|----|-------|---------|---------------|----------------|
| G-01 | صفر أصول خارج VCS | ملفات فريدة untracked ذات قيمة | **0** | `shamel doctor --rescue-scan` يفحص المسارات الذهبية؛ exit 0 |
| G-02 | سلالة git واحدة | فروع عقيدة متباعدة | **1** (main + فروع prj/ قصيرة العمر) | `git branch -a` + فحص ahead/behind في doctor |
| G-03 | نقطة دخول تنفيذية واحدة | تنفيذيات باسم النظام على PATH وداخل الشجرة | **1** (`shamel`) | `find ~/Desktop/SHAMEL -path '*/archive' -prune -o -name 'sofi*' -type f -executable -print` = 0 |
| G-04 | جرد وكلاء واحد | مصادر تعريف يدوية لكل agent-id | **1** (spec) + مشتق مولّد واحد | `shamel doctor` parity + فحص «مولّد لا محرَّر» بالبصمات |
| G-05 | كل مشروع repo خاص | مشاريع بلا `.git` أو بلا remote | **0** | `shamel projects --verify` fail-closed |
| G-06 | بوابة = واقع | بوابات معلنة فوق artifacts معدومة | **0** | `shamel gate-check` fail-closed على artifacts قابلة للتشغيل |
| G-07 | أتمتة مثبتة | ادعاءات أتمتة بلا مشغّل مسجّل | **0** | `shamel automation status`: كل ادعاء ↔ سطر cron/hook فعلي |
| G-08 | دماغ صادق | تناقض أرقام/stack بين الدماغ والكود | **0** | أرقام الدماغ مولّدة بسكربت؛ `shamel brain-audit` يقارن |
| G-09 | اقتصاد سياق | حجم الحقن التلقائي عند الإقلاع | **≤ 1000 توكن** | عدّاد hook الـ orientation (وراثة ميزانية v6) |
| G-10 | تعلم فعلي | دروس LESSONS مولّدة بحلقة مجدولة | **≥ 1 تشغيل/أسبوع** مسجّل | سجل تشغيل `automation/logs/reflect.jsonl` + crontab |
| G-11 | صفر انحراف صامت للحُرّاس | أعطال hooks غير مرئية | **0** (تُعدّ وتُرفع) | عدّاد أعطال في تقرير doctor (علاج GAP-20) |
| G-12 | تقاعد نظيف | طبقات ميتة بلا شاهد قبر داخل شامل | **0** | لا مسار legacy يُنسخ إلى SHAMEL إلا تحت `archive/` بوسم ⛔ |

---

## 4. النطاق / خارج النطاق

### 4.1 داخل النطاق

1. إنشاء `~/Desktop/SHAMEL/` كـ repo git جديد بالبنية القانونية (§5.0) وربطه بـ remote.
2. **عمليات الإنقاذ R1–R4** (§7.1) — شرط مسبق يسبق أي بناء.
3. ترحيل المكوّنات الفائزة من الأجيال الستة حسب قرارات §7 (دستور v6، Nexus، hooks، brain، substrate، أدوات G1، محرك G6 الموحّد، حوكمة G4…).
4. طبقة أدوات حتمية واحدة (`shamel_tools`) + CLI واحد (`shamel`).
5. مصنع مشاريع موحّد بقانون يوم-صفر git، وترحيل PRJ-SAKK كأول مشروع (بعد إعادة تصنيفه Gate 4/5 — GAP-04).
6. أتمتة خارجية حقيقية: cron manifests + pipeline خارجي عبر `claude -p` + مكتب oracle بـ API fallback.
7. تقاعد معياري لكل الأجيال القديمة بنمط archive-v5 (شاهد قبر ⛔ + tag/snapshot) في مواقعها الأصلية، مع فهرس مركزي في شامل.

### 4.2 خارج النطاق (صراحةً)

1. **إعادة كتابة كود منتج PRJ-SAKK** — يُرحَّل كما هو؛ إصلاحات أمانه (GAP-13) تذاكر ضمن دورة حياته لا ضمن بناء شامل.
2. **أي daemon داخلي / خدمة مقيمة** — محظور بالمبدأ 8؛ لا watchers، لا servers دائمة (event_server الموروث يُقيَّد كأداة تُستدعى عند الطلب أو يُتقاعد).
3. **واجهة مراقبة ويب (dashboard)** — dashboard v5 يُتقاعد؛ بناء بديل على معطيات شامل مشروع لاحق مستقل.
4. **تعدد المشغّلين البشريين / مزامنة سحابية للفرق.**
5. **دعم منصّات تشغيل غير Claude Code** (OpenCode مات مع G1).
6. **ترحيل شامل لمحتوى الأجيال المتقاعدة** — يُرحَّل المذكور في §7 حصراً؛ الباقي أرشيف يُقرأ عند الحاجة ولا يُنسخ.
7. تغيير stack defaults للمنتجات (Laravel/Blade/Flutter تبقى؛ تصحيح توثيق Riverpod-vs-Bloc بند دماغ لا بند بناء).

### 4.3 البنية القانونية للجذر (مرجع للأقسام التالية)

```
~/Desktop/SHAMEL/                      # repo git واحد + remote
├── CLAUDE.md                          # العقد السلوكي الوحيد (يُحقن في كل جلسة)
├── MEMORY.md                          # خريطة التوجيه الوحيدة — pointers فقط
├── constitution/                      # البروتوكول الواحد: 12 مادة (00..11)
├── nexus/
│   ├── registry.yaml                  # الغرف→الوكلاء→المهارات→الأدوات (SSoT)
│   ├── routing.yaml                   # الشبكة الاقتصادية (tiers لا model IDs)
│   ├── models.yaml                    # طبقة alias الوحيدة: tier → model id
│   ├── gates.yaml                     # البوابات التسع machine-readable
│   ├── personas.yaml                  # جدول ربط ID ↔ persona (كانون واحد)
│   └── bus/                           # ticket-schema.md · escalation.md
├── rooms/<NN-code>/                   # 15 غرفة: CHARTER + agents/ + tools/ + playbooks/
│   └── 05-backend/
│       ├── CHARTER.md
│       ├── agents/bck-api-engineer.md # الـ spec = مصدر الحقيقة الوحيد للوكيل
│       ├── tools/                     # سكربتات per-agent (منتشلة من G1 — 114)
│       └── playbooks/
├── brain/
│   ├── BRAIN.md                       # معمارية الذاكرة (org/project/session)
│   ├── org/                           # DECISIONS · LESSONS · EVOLUTION · …
│   ├── templates/                     # قوالب STATE/CONTEXT/… (7)
│   └── memdb/brain.db                 # SQLite FTS5 — يتغذى آلياً من hooks
├── os/
│   ├── bin/shamel                     # نقطة الدخول التنفيذية الوحيدة
│   ├── shamel_tools/                  # المكتبة الحتمية الموحّدة (Python)
│   └── scanners/                      # feature_scan · shamel_scan · shamel_verify (نسخة واحدة)
├── automation/
│   ├── cron.d/                        # manifests مُعلَنة → crontab عبر shamel automation install
│   ├── pipeline/                      # المحرك الخارجي الموحّد (state_db · agent_invoker · translator_gateway · ceo_agent)
│   ├── oracle/                        # مكتب المراجعة الخارجية (CDP + API fallback)
│   └── logs/                          # سجلات تشغيل الأتمتة (jsonl)
├── .claude/
│   ├── agents/<id>.md                 # spawnables — مولّدة 100% من rooms/*/agents (لا تُحرَّر يدوياً)
│   ├── skills/                        # العمود الفقري: 13 skill (spine 6 + power 7)
│   ├── commands/                      # الأوامر المُغربَلة القيّمة من الـ 54
│   ├── hooks/                         # الحُرّاس الخمسة + عدّاد أعطال
│   └── settings.json
├── archive/INDEX.md                   # فهرس شواهد القبور (أين دُفن كل جيل + tag)
├── projects/                          # حاوية المشاريع — كل PRJ-XXXX repo git مستقل
│   └── PRJ-SAKK/ (.git + remote خاص)
└── .claudeignore                      # درع السياق
```

---

## 5. المتطلبات الوظيفية (FR)

كل متطلب يحمل: الوصف الملزم، والإسناد (GAP يعالجه أو مكوّن فائز يرحّله من المصفوفة §2/§3). معايير القبول التفصيلية في §9.

### 5.0 اصطلاح

- **fail-closed** = الفحص يمنع التقدم عند الفشل (exit ≠ 0 يوقف السلسلة).
- **مولَّد (generated)** = ملف يُنتجه أمر من مصدر أعلى؛ تحريره اليدوي خرق يكتشفه doctor.
- **المصفوفة §N** = بند الترحيل رقم N في `08-COMPARISON-MATRIX.md` §3.

### 5.1 تنظيم الوكلاء والغرف

**FR-01 — خريطة الغرف الرسمية: 15 غرفة.**
شامل يعتمد خريطة v6 الخمس عشرة (`brd str res dsn arc bck fnt mob dat sec qa ops obs knw gtw`) — الأكمل تغطيةً (مصفوفة §5 قرار 3؛ فجوات fnt/qa/obs في خريطة العشر مثبتة بمصفوفة 15×10 في تقرير 05). كل غرفة مجلد `rooms/<NN-code>/` يحوي `CHARTER.md` بالقالب القياسي (mission · members+routes · interfaces consumes/produces · room-bar · escalation — مصفوفة §9)، و`agents/` و`tools/` و`playbooks/` **فعلية لا README-pointers** (علاج GAP-18: تُملأ `tools/` من منتشَل G1 — FR-81).
*الإسناد: مصفوفة بُعد 1 (الفائز G3) + §3 بند 9 · GAP-16 · GAP-18.*

**FR-02 — جرد وكلاء واحد: الـ spec مصدر، والـ spawnable مولَّد.**
لكل وكيل ملف spec واحد في `rooms/<room>/agents/<id>.md` بـ frontmatter آلي كامل:

```yaml
---
agent: bck-api-engineer
persona: PER-042            # مفتاح في nexus/personas.yaml — لا اسم حرّ
room: 05-backend
reports_to: bck-lead
gate: 4
route: {tier: workhorse, effort: medium, caveman: lite, budget: 12}
tools: [Read, Edit, Write, Bash]        # least-privilege صريح — لا وراثة
success_metric: "contract parity: 0 endpoint drift vs frozen OpenAPI"
authority:                  # حوكمة G4 السداسية (FR-53)
  operational: "ينفّذ ضمن العقد المجمّد فقط"
  financial: none
  veto: "رفض دمج محدود بنطاق مهمته + تصعيد"
  escalation: bck-lead
---
```

الـ spawnable في `.claude/agents/<id>.md` **يولَّد حصراً** بأمر `shamel agents build` من هذا الـ frontmatter (RCCF: 🎭📂🎯📐 + Operating Contract). تحرير spawnable يدوياً = خرق يكتشفه doctor عبر بصمات SHA-256 (`nexus/agent-pins.json`). هذا يلغي نهائياً جرد D (stubs الـ 6 أسطر) وينهي «تعريفين حيّين لنفس الـ ID».
*الإسناد: GAP-07 (العلاج الحرفي: «توليد أي stub آلياً من frontmatter الـ spec») · مصفوفة §3 بند 3 · تقرير 05 §ما يُرحَّل بنود 1/2/4.*

**FR-03 — least-privilege إلزامي ومفحوص.**
لا يوجد على القرص أي تعريف وكيل بلا `tools:` صريحة ولا بـ `model: inherit` معمَّم (استثناء وحيد: tier `gatekeeper` يُحل إلى inherit عبر `models.yaml`). منح الويب (`WebSearch/WebFetch`) تُمنح في الـ registry حصراً وتُسقَط على الـ spawnables عند التوليد (v6: 21 منحة صريحة — النمط يُرحَّل). فاحص `shamel lint agents` (وراثة agentlint) **fail-closed** في doctor وفي CI.
*الإسناد: GAP-10 (العلاج الحرفي) · مصفوفة §3 بند 3.*

**FR-04 — كانون personas واحد بجدول ربط.**
`nexus/personas.yaml` هو جدول الربط الوحيد `agent-id ↔ persona-id ↔ الاسم البشري ↔ ملف الـ HR الموسّع`:

```yaml
personas:
  - id: PER-042
    agent: bck-api-engineer
    name_canonical: "عمّار خضّور"        # قرار الكانون: العربي-السوري (G4)
    aliases: ["Priya Nair", "كريم فاروق"] # الكوانين المتقاعدة — للأرشيف والبحث
    hr_profile: rooms/05-backend/agents/hr/BKD-05-04.md
```

يُعتمد كانون واحد للأسماء (قرار §7.3-Q4)، وتُرحَّل ملفات org-rooms الـ 100 كطبقة HR موسّعة مربوطة بالجدول — لا كون موازٍ بعد اليوم. الأدوار التي لا نظير لها (فجوات fnt/qa/obs/brd في خريطة العشر) تُستكمل personas جديدة بنفس القالب السداسي.
*الإسناد: GAP-15 (جدول الربط) · GAP-16 · مصفوفة §3 بند 16.*

**FR-05 — حزمة إعادة التسمية الواحدة (فخاخ الدلالة).**
تُحسم في commit تأسيسي واحد: (أ) نقطة الدخول اسمها `shamel` — لا يبقى ملف باسم `sofi*` داخل الجذر الجديد (استثناء وحيد: المدفون تحت `archive/` — نمط FR-20)، والماسحات المنتشلة تدخل بأسمائها الجديدة `shamel_scan`/`shamel_verify` (FR-81)؛ (ب) كلمة **registry** تعني حصراً سجل الوكلاء `nexus/registry.yaml` — موديول مخططات substrate يُعاد تسميته `schemas.py`؛ (ج) **GTW** يعني حصراً مشغّلي الـ Nexus (حوكمة داخلية) — محتوى org-rooms GTW-06 (API Gateway الخارجي: Kong/OAuth2/rate-limit) يُعاد توزيعه على `arc-integration-architect` + `bck-integration-engineer` + `sec-authn-engineer` كما حدد تقرير 05؛ (د) رموز الغرف في المحرك الخارجي تُوحَّد على رموز v6 (`bck` لا `bkd_05`).
*الإسناد: GAP-15 (العلاج الحرفي: «حزمة إعادة تسمية واحدة») · تقرير 05 §التداخل 2.*

**FR-06 — البوابة الدلالية (translator) أمام الـ CEO.**
مدخل خام من المشغّل → وكيل translator (أو خطوة `translator_gateway` في المحرك الخارجي) يحوّله إلى JSON مهيكل (intent · scope · priority · effort-class) قبل وصوله لجلسة الأوركسترا. داخل الجلسة يؤدي `gtw-dispatcher` الدور نفسه. النسخة المعتمدة من الكود: `translator_gateway` الأغنى (455 سطراً — MAIN) بعد إنقاذه ودمجه.
*الإسناد: مصفوفة §3 بند 13 (فكرة G1) + بند 18 (كود G6) · GAP-03.*

### 5.2 العقل / الدماغ

**FR-10 — دماغ ثلاثي الطبقات.**
ثلاث طبقات معرّفة في `brain/BRAIN.md`: **org** (قرارات/دروس/تطور المؤسسة — في repo شامل)، **project** (STATE·CONTEXT·DECISIONS·HANDOFFS·LESSONS·FOUNDATIONS·LOCKS — داخل repo المشروع نفسه)، **session** (breadcrumbs عبر hooks). القوالب السبعة تُرحَّل من `brain/templates/` مع frontmatter `memory-type` قابل للاستعلام.
*الإسناد: مصفوفة بُعد 2 (الفائز G3) + §3 بند 5.*

**FR-11 — دماغ المشروع يعيش ويُلتزم في repo المشروع.**
`_context/` جزء من شجرة المشروع، و`shamel checkpoint <PRJ>` يعمل commit **في repo المشروع** (لا repo الإطار). غياب `.git` في المشروع = **فشل صريح** لا تحذير. هذا يسدّ «البند المكسور» الذي جعل `branch/head_sha` فارغين في STATE رغم gate 6.
*الإسناد: GAP-01 · GAP-09 (العلاج: «تحويل no brain to checkpoint من تحذير إلى فشل») · مصفوفة §2 (مكمّل بُعد الذاكرة).*

**FR-12 — «الكود هو الحقيقة»: أرقام الدماغ تولَّد لا تُكتب.**
كل رقم قابل للعدّ في الدماغ (models/controllers/tests/migrations/features) يولَّده `shamel brain-audit --stamp` بسكربت عدّ ويختمه بتاريخ + أمر التوليد. `FOLDER-MAP.md` **عقد مولَّد** من السكافولدر (`shamel scaffold map`) لا وثيقة يدوية. أي stack معلن في STATE يُطابَق ضد manifests فعلية (`composer.json`/`pubspec.yaml`/`package.json`) — التناقض يفشّل brain-audit.
*الإسناد: GAP-12 (العلاج الحرفي) · تقرير 06 §ما يُرحَّل بندا 3/6.*

**FR-13 — memdb مؤتمت التغذية + استرجاع موحّد.**
`brain/memdb/brain.db` (SQLite FTS5) يتغذى آلياً: hook الـ Stop يكتب observation لكل جلسة، و`shamel checkpoint` يفهرس رؤوس CONTEXT، و`/shamel-reflect` يكتب الدروس. `shamel recall "<query>"` هو الاسترجاع الموحّد (brain-query الموروث). القبول: memdb لا يبقى «بصفّ واحد» — كل جلسة تترك أثراً.
*الإسناد: GAP-11 (memdb بصفّ واحد — العلاج: «ملء memdb من observations») · مصفوفة §3 بند 5.*

**FR-14 — MEMORY.md واحدة: خريطة توجيه، لا محتوى.**
ملف واحد في الجذر، pointers فقط («أين أجد X؟»)، يملكه `knw-lead`. نسخ MEMORY المتوازية (MAIN/WT/stash) تُصفّى إلى هذه الواحدة أثناء المصالحة (§7.1-R4) ثم تُدفن. الكتابة الدائمة للعقيدة تبقى محكومة بمشغّل «تذكّر/remember» حصراً.
*الإسناد: GAP-08 (خريطتا MEMORY متعارضتان) · تقرير 07 عبر المصفوفة §3 بند 5.*

**FR-15 — LESSONS بصيغة sig + حلقة تعلم مغلقة.**
الدروس بصيغة `LES-NNN · sig: <signature> · date · situation · what-failed · rule · ticket` (idempotent — الـ sig يمنع التكرار). حلقة `/shamel-reflect` تقطّر HANDOFFS → LESSONS على مستويي org والمشروع، ويحقن hook الـ orientation («لقاح الدروس») الدروس ذات الصلة عند الإقلاع. الجدولة الفعلية في FR-31.
*الإسناد: مصفوفة §3 بند 5 (صيغة sig) · GAP-11 (لا LESSONS لأي مشروع قط).*

### 5.3 البروتوكول الواحد

**FR-20 — دستور واحد من 12 مادة يخدمه كل مسار إقلاع.**
`constitution/00..11`: المواد 00–10 تُرحَّل من v6 (العقد الكوني، Work Order، Grounding، Verification، Reflection، Token Economy، Git، Security، Handoff، Research، Gates) + **مادة 11 جديدة: Intake & Orchestration** تلتقط جوهر G2 (wear-the-hierarchy، leaf-spawn one hop) **وتحسم صراحةً** تناقض العقيدة القديم: الـ skills الـ 13 هي واجهة الانضباط الرسمية (لا تحريم slash-commands). هرم Precedence + Amendment بقرار ADR يُرحَّلان كما هما. **لا يوجد في شامل كله إلا نسخة hooks واحدة تحقن هذا الدستور** — انفصام «دستور بحسب مجلد الإقلاع» يستحيل بنيوياً لأن الجذر واحد والسلالة واحدة.
*الإسناد: GAP-08 (العلاج) · مصفوفة §3 بندا 1/14 · تقرير 03 §قوة 4.*

**FR-21 — RCCF Work Order صيغة التفويض الوحيدة.**
كل spawn = أمر عمل رباعي (Role·Context·Command·Format) بموجب المادة 01: frozen brief (لا instruction drip)، effort class + call budget + fail-safe stop، evidence block متوقَّع. `/shamel-delegate <agent> <task>` يولّد الكتلة القانونية. غير قادر على ملء الأجزاء الأربعة بمحدّدات → «وضّح قبل أن تفوّض».
*الإسناد: مصفوفة §3 بند 6 · تقرير 03 §قوة 3.*

**FR-22 — Grounding G1–G5 قانوناً مُسلَّكاً.**
تُرحَّل المادة 02 حرفياً مع نقاط إنفاذها: مصدر أو صمت (`[unverified]` + توقف)، الامتناع مكافأ، حقيقة التنفيذ (أمر+ناتج+exit code منسوخ، self-report ≠ دليل)، فصل `[verified]`/`[inferred]`، إظهار التعارض لا حله بصمت.
*الإسناد: مصفوفة §3 بند 1 («أنضج عقيدة grounding») · تقرير 03 §قوة 1.*

**FR-23 — Verification V1–V5: التحقق العدائي بنيوياً.**
تُرحَّل المادة 03 مع أدواتها: `validate_evidence()` **fail-closed** داخل gate-check (تذكرة done بلا evidence block = مرفوضة آلياً)؛ التقدم بين البوابات حصراً عبر فحص عدائي fresh-context بواسطة `gtw-gatekeeper` ضد المعايير الأصلية — **المنفّذ لا يحكم على نفسه أبداً**، وUNKNOWN حكم مشروع؛ pass^k للأموال/auth/PII؛ لا فعل غير قابل للعكس يُبنى على ثقة لفظية؛ الحَكم نفسه يُدقَّق (spot-check خلف PASS و0-findings).
*الإسناد: مصفوفة §3 بند 1 · المبدأ الحاكم 7 · GAP-04 (البوابات فقدت معناها لغياب هذا الإنفاذ على artifacts).*

**FR-24 — الـ bus: تذاكر git-native بschema ملزم.**
التذاكر تعيش في `HANDOFFS.md` بصيغة `bus/ticket-schema.md` (from/to/task/consumes/expected/route/status + header regex يطابق `tickets.py`) — بلا أي middleware. سلسلة التصعيد: specialist → room lead → `gtw-conflict-resolver` → `brd-arbiter` → CEO؛ circuit breaker عند 3 محاولات فاشلة (crash-dump JSON + تذكرة تصعيد).
*الإسناد: مصفوفة §3 بند 6 · تقرير 03 §ما يُرحَّل بند 5.*

### 5.4 الأتمتة (حقيقية، قابلة للإثبات)

**FR-30 — الحُرّاس الخمسة + عدّاد أعطال مرئي.**
تُرحَّل hooks v6.1 الخمسة كنسخة وحيدة في `.claude/hooks/` بنمط `$CLAUDE_PROJECT_DIR`: **PreToolUse** (حجب أوامر خطرة/`.env`/صيغة commit سيئة — يحجب فعلياً)، **SessionStart** (orientation بميزانية ≤1000 توكن: STATE head + التذكرة التالية + لقاح الدروس)، **PostToolUse** (نُدَف checkpoint عند انجراف الشجرة)، **Stop** (breadcrumb → memdb). تبقى fail-open بالتصميم **لكن** كل فشل hook يزيد عدّاداً في `automation/logs/hooks-failures.jsonl` يُرفع في `shamel doctor` — «رصد بلا حجب».
*الإسناد: مصفوفة §3 بند 4 · GAP-20 (العلاج الحرفي).*

**FR-31 — مجدوِل خارجي فعلي: قاعدة «لا ادعاء أتمتة بلا مشغّل».**
كل سلوك دوري يُعلَن في manifest تحت `automation/cron.d/` ويُثبَّت بأمر واحد:

```yaml
# automation/cron.d/reflect.yaml
job: shamel-reflect
schedule: "0 6 * * 1"                 # أسبوعياً — الاثنين 06:00
command: claude -p "/shamel-reflect" --cwd ~/Desktop/SHAMEL
log: automation/logs/reflect.jsonl
on_error: append-alert                 # يظهر في doctor
```

`shamel automation install` يزرع الأسطر في crontab، و`shamel automation status` يطابق: **كل ادعاء «scheduled» في العقيدة ↔ سطر crontab حي ↔ سجل تشغيل**. أي ادعاء بلا الثلاثية = فشل doctor. الحد الأدنى المُثبَّت يوم-واحد: reflect (أسبوعي) + brain-audit (يومي) + doctor (يومي).
*الإسناد: GAP-11 (العلاج الحرفي: «لكل ادعاء أتمتة بند إنفاذ… cron/hook دوري») · المبدأ الحاكم 4 و8 (أتمتة خارجية عبر claude -p/cron).*

**FR-32 — المحرك الخارجي الموحّد، موصول بالـ Nexus.**
pipeline واحد في `automation/pipeline/` يدمج fork-ي G6: `state_db.py` (نسخة WT الأحدث 356 سطراً) + `translator_gateway.py` (نسخة MAIN الأغنى 455) + `ceo_agent.py` (المنقذ من MAIN) + `agent_invoker` بوضعي MOCK/live عبر `claude -p`. **قيد ملزم:** يقرأ `nexus/registry.yaml + routing.yaml + gates.yaml` حصراً — يُحذف أي جدول غرف/routes مضمّن (خرق G6 التاريخي لـ «routing.yaml the ONLY source» يُمنع بفحص استيراد في CI). flat topology: يُستدعى ويخرج، لا يبقى مقيماً.
*الإسناد: مصفوفة §3 بند 18 (بنوده الخمسة حرفياً) · GAP-03 · GAP-15 (توحيد الرموز) · المبدأ 8.*

**FR-33 — مكتب الـ oracle بـ fallback ومصداقية exit code.**
الحلقة تُرحَّل (sanitize→condense→push→capture→parse→ingest إلى HANDOFFS) مع إصلاحين ملزمين: (أ) **API fallback** عند غياب متصفح CDP — لا اعتماد حصري على Chrome يدوي على :9222؛ (ب) `shamel oracle status` يرجع **exit ≠ 0 عند الفشل** (الحالي يرجع 0 زوراً). يبقى المكتب استشارياً: لا يعتمد بوابات — `gtw-gatekeeper` يقرر. sanitized-only: لا أسرار/PII/بيانات إنتاج للخدمة الخارجية.
*الإسناد: مصفوفة §3 بند 7 (الشرط الحرفي) · GAP-11 (oracle exit 0 عند الفشل).*

**FR-34 — doctor معمَّم: فاحص الوحدة الدائم.**
`shamel doctor` يرث فحوص v6 (parity 105↔105↔registry، صحة YAML، مسارات skills) **ويضيف فحوص شامل**: (أ) كشف الازدواج — أي تطبيقين لنفس الـ concern (نقطتا دخول، سجلان، نظاما ذاكرة) = FAIL؛ (ب) `projects --verify` (FR-40)؛ (ج) مطابقة الأتمتة (FR-31)؛ (د) بصمات التوليد (FR-02)؛ (هـ) عدّاد أعطال hooks (FR-30)؛ (و) rescue-scan للأصول untracked داخل الجذر؛ (ز) parity الحقول المولَّدة: `route` (frontmatter الـ spec ↔ `routes.<id>` في routing.yaml — FR-60) و`gate` (frontmatter ↔ قوائم `agents:` في gates.yaml). doctor **fail-closed في CI** لمستودع شامل نفسه.
*الإسناد: GAP-06 (العلاج الحرفي: «فاحص doctor معمَّم يفشل عند أي ازدواج جديد») · مصفوفة §3 بند 2.*

### 5.5 مصنع المشاريع

**FR-40 — قانون يوم-صفر: لا مشروع بلا VCS ولو لدقيقة.**
`shamel new PRJ-XXXX "title"` ينفّذ **داخل السكافولدر نفسه وبترتيب ذري**:

```bash
mkdir -p projects/PRJ-XXXX && cd projects/PRJ-XXXX
git init && git branch -M main
# زرع الشكل القانوني (FR-41) + الدماغ من القوالب
git add -A && git commit -m "chore(scaffold): PRJ-XXXX day-zero"
git remote add origin <remote-url>   # إلزامي — يطلب الـ URL أو ينشئه عبر gh
git push -u origin main
shamel domain register PRJ-XXXX      # <slug>.local
```

`shamel projects --verify` يفحص كل مشروع: `.git` موجود + remote مضبوط + آخر push ≤ 7 أيام — أي خرق = FAIL في doctor. حاوية `projects/` تبقى متجاهَلة في repo شامل **لأن** كل مشروع repo مستقل — التجاهل لم يعد خطراً بعد أن صار الـ init قانوناً.
*الإسناد: GAP-01 (العلاج الحرفي) · مصفوفة §3 بند 19 («الدرس المدفوع الثمن: مشروعان ضاعا فعلاً») · تقرير 06 §ضعف 1/2.*

**FR-41 — شكل قانوني واحد + FOLDER-MAP مولَّد.**
اصطلاح سداسي واحد يولّده السكافولدر ويطابقه الواقع: `_context/ · docs/ · backend/ · frontend/ · mobile/ · deploy/ · tests/` (تُزرع الحاويات المطلوبة فعلاً حسب نوع المشروع، والخريطة تولَّد مما زُرع). `docs/FOLDER-MAP.md` يولَّد بـ `shamel scaffold map` من الشجرة الحقيقية — يقتل انحراف «scaffold ≠ واقع ≠ خريطة» الثلاثي المثبت في PRJ-SAKK.
*الإسناد: GAP-12 · تقرير 06 §ضعف 3/4 و§ما يُرحَّل بند 3 · مصفوفة §3 بند 20.*

**FR-42 — حلّ مسارات fail-loud وواعٍ بالـ worktrees.**
`shamel_tools/paths.py`: جذر المشاريع يُحل بترتيب صريح (`SHAMEL_PROJECTS_DIR` → `~/Desktop/SHAMEL/projects`)، وأي مسار محلول غير موجود = **استثناء صاخب** لا مسار معدوم صامت. حلّ صريح للـ worktrees (الصعود إلى جذر الـ repo الرئيس عبر `git rev-parse --git-common-dir`). كذلك قرار معماري: **worktrees شامل لا تُعشَّش تحت `.claude/`** (سبب نزيف palette المثبت) — تعيش في `~/Desktop/SHAMEL-worktrees/` أو `.worktrees/` بالجذر.
*الإسناد: GAP-09 (العلاج الحرفي) · GAP-05 (فك التعشيش) · مصفوفة §5 قرارا 4/5.*

**FR-43 — حُرّاس checkpoint تُرحَّل وتُشدَّد.**
`gitops.checkpoint()` كما هو (conventional-commit إجباري، فحص مسارات محظورة secrets/`_scratch` مع unstage بلا `--hard`، trailer `SHAMEL:` بحقول PRJ·TKT·gate·agent-id، ختم `head_sha` في STATE) فوق repos مشاريع حقيقية، مع تحويل «no brain to checkpoint» من تحذير إلى **فشل**.
*الإسناد: تقرير 06 §ما يُرحَّل بند 4 (الحرفي) · مصفوفة §3 بند 20 · GAP-09.*

**FR-44 — سجل artifacts البوابات القياسي.**
`_context/features/GATE0-… → GATE8-…` بأسماء قياسية (INCEPTION، OPENAPI.yaml، THREAT-MODEL، A11Y-MATRIX، OBSERVE-CONFIG…) — «أنجح فكرة في PRJ-SAKK» تصبح جزءاً من القالب، و`gate-check` يقرأ منها.
*الإسناد: مصفوفة §3 بند 20 · تقرير 06 §قوة 2.*

**FR-45 — الدومين المحلي والنفق العام.**
يُرحَّلان من v6: `shamel domain register/up` (كل مشروع `<slug>.local` — لا `127.0.0.1:PORT` خام)، و`shamel tunnel up/down` (مؤقت، seed-data فقط، ليس staging/prod). المالك: `ops-domain-warden`.
*الإسناد: مصفوفة بُعد 3/4 (وراثة G3 عاملة — تكامل `/etc/hosts` المثبت حياً في تقرير 06).*

### 5.6 الحوكمة والبوابات

**FR-50 — البوابات التسع machine-readable + checklists تفصيلية.**
`nexus/gates.yaml` يُرحَّل كاملاً (لكل بوابة: `id·name·trigger·owner_room·agents·entry·artifacts·exit_bar·on_fail` + `accountability` + `tracks`)، ويُكمَّل بـ gate checklists 0–8 المنتشلة من G1 كمرفقات تفصيلية لكل بوابة (`rooms/…/playbooks/` أو `constitution/checklists/`).
*الإسناد: مصفوفة بُعد 5 (الفائز G3 + المكمّل الإلزامي من G1) + §3 بندا 2(03)/12.*

**FR-51 — بوابة معلنة = artifacts قابلة للتشغيل (fail-closed).**
`shamel gate-check <PRJ> <N>` يتحقق ميكانيكياً من **وجود وقابلية تشغيل** artifacts البوابة قبل السماح بالإعلان: Gate 6 مثلاً تتطلب workflow CI موجوداً وقابلاً للتفعيل + rollback مُختبَراً — لا «GitHub Actions ينشر تلقائياً» فوق `workflows/` فارغ. الإعلان في STATE عن gate أعلى من آخر `gate-tag` ناجح = خرق يكتشفه brain-audit. **إجراء تصحيحي فوري:** PRJ-SAKK يُعاد تصنيفه رسمياً Gate 4/5 عند الترحيل.
*الإسناد: GAP-04 (العلاج الحرفي) · FR-23 (V1/V4).*

**FR-52 — التصنيف ثنائي المسار (two-track sizing).**
Fast-Track (منخفض الخطر: نصوص، i18n، حقل، validation غير مالي) يطوي البوابات 1–3 في فحص blueprint واحد؛ الأموال/الاعتمادات/auth/PII = Deep-Audit كامل البوابات التسع بلا استثناء؛ عند الشك → Deep-Audit. مُسلَّك في `gates.yaml: tracks`.
*الإسناد: مصفوفة بُعد 5 · تقرير 03 (gates.yaml:20-29).*

**FR-53 — طبقة الحوكمة البشرية السداسية.**
حوكمة الصلاحيات per-agent من G4 (سلطة تشغيلية · مالية · فيتو · تصعيد · اعتماديات) تُرحَّل إلى frontmatter الـ spec (`authority:` — انظر FR-02) فتصبح queryable آلياً بدل نص HR معلّق. الثوابت المؤسسية تُسلَّك في `gates.yaml`/الدستور: فيتو `brd-cso` الأمني مطلق دون الـ CEO؛ المساءلة CPO 0–2 · CTO 3–4 · CQO 5.
*الإسناد: مصفوفة §3 بند 16 + بُعد 7 (المكمّل الإلزامي) · GAP-16 (العلاج: «ترحيل طبقة الحوكمة السداسية إلى frontmatter جرد B»).*

### 5.7 الاقتصاد (routing)

**FR-60 — مصدر توجيه واحد + طبقة aliases للنماذج.**
`nexus/routing.yaml` هو مصدر التوجيه الوحيد (سلّم 🟢mechanical → 🔵workhorse → 🔮gatekeeper → 🟣deep، route لكل وكيل + مسارات مهام). **حدّ القانونية (منعاً لازدواج المصدر):** الشبكة نفسها (السلّم · effort classes · priority_override · مسارات المهام) قانونية هنا؛ أما `route:` لكل وكيل فمصدره القانوني frontmatter الـ spec (FR-02)، وكتلة `routes.<id>` في هذا الملف **تولَّد** منه بأمر `shamel agents build` — doctor يفحص التطابق (FR-34)، أسوة بحل منح الويب (FR-03). **لا model ID حرفي فيه** — الأسماء الحرفية تعيش حصراً في `nexus/models.yaml`:

```yaml
# nexus/models.yaml — الملف الوحيد الذي يذكر model IDs
aliases:
  mechanical: claude-haiku-4-5
  workhorse:  claude-sonnet-5
  gatekeeper: inherit          # نموذج الجلسة الحدودي
  deep:       claude-opus-4-8
```

ترقية نموذج = تعديل سطر واحد + `shamel agents build` لإعادة توليد الـ spawnables. doctor يفشل إن وجد model ID حرفياً خارج هذا الملف.
*الإسناد: GAP-17 (العلاج الحرفي: «طبقة alias… في ملف واحد قابل للتبديل») · مصفوفة §4 (بند التقاعد الأخير).*

**FR-61 — ميزانية autonomy + تصعيد بالدليل.**
effort classes الخمس (trivial-fix · single-role · cross-room · audit-sweep · arbitration) مع call budget + fail-safe stop لكل Work Order؛ التصعيد على السلّم بالدليل فقط (فشل validation مرتين، تعارض متطلبات، أمن/PII/مال، migration غير قابل للعكس، تحكيم)؛ `priority_override` (CRITICAL +1/+1، LOW سقفه workhorse)؛ `gtw-budget-warden` يملك عدّادات الصرف وcircuit breakers. 🟣deep محظور لكتابة كود روتيني.
*الإسناد: مصفوفة بُعد 3 (Nexus الفائز) · تقرير 03 (effort_scaling/escalation/budgeted_autonomy المثبتة).*

**FR-62 — درع السياق.**
(أ) `.claudeignore` يستبعد vendor/node_modules/أرشيفات المهارات الضخمة (نمط خفض ~80%)؛ (ب) palette مهارات واحدة: **13 skill** (spine 6: boot/gate/handoff/team/delegate/reflect + power 7: audit/spec-review/feature/secure/fix/report/design-taste) بأسماء `shamel-*` — لا 107 مرآة؛ (ج) حقن الإقلاع ≤1000 توكن (FR-30)؛ (د) caveman متدرج `lite|full|ultra` للثرثرة — **الكود والcommits وتحذيرات الأمان نثر كامل أبداً لا يُضغط**.
*الإسناد: مصفوفة بُعد 10 (الفائز G3) + §3 بند 8 · GAP-05 (توحيد الـ palette) · GAP-14 (تكلفة الطبقات الميتة).*

### 5.8 الأمان

**FR-70 — صفر أسرار hardcoded + ماسح إلزامي.**
لا اعتمادات مضمّنة في أي سكربت/كود يدخل شامل — شرط مسبق حرفي على انتشال browser-eyes (نزع اعتمادات admin في `browser-eyes.sh:13-14` إلى env/secret store قبل الإدخال). `sec-secrets-warden` يشغّل مسح أسرار آلي (hook PreToolUse يحجب `.env` + مسح دوري عبر cron manifest)، والاكتشاف = تدوير فوري.
*الإسناد: GAP-13 (العلاج الحرفي) · GAP-03 (شرط الانتشال) · مصفوفة §3 بند 11.*

**FR-71 — sanitized-external-only.**
كل ما يخرج لخدمة خارجية (oracle/بحث) يمر بـ sanitizer (redact مفاتيح/أسرار/.env) — لا أسرار/PII/بيانات إنتاج خارج الجهاز أبداً. النفق العام (FR-45) seed-data فقط ويُقتل بعد الاستعمال.
*الإسناد: مصفوفة §3 بند 7 · وراثة `07-security-law` (تقرير 03).*

**FR-72 — الفيتو الأمني ومسار Deep-Audit.**
فيتو `brd-cso` مطلق تحت الـ CEO في كل الغرف والبوابات؛ الأموال/KYC/auth/PII تدخل Deep-Audit إلزامياً (FR-52) مع pass^k عند البوابتين 5–6 (V3). بيئات الاختبار تُفصل افتراضياً عن الإنتاج (درس Flutter المشير افتراضياً لـ API إنتاجي).
*الإسناد: مصفوفة بُعد 7 · GAP-13 (فصل بيئة API).*

**FR-73 — بناء قابل لإعادة الإنتاج fail-closed.**
قوالب النشر في المصنع: `composer install` بلا `|| true` (الفشل يفشّل البناء)، `composer.lock`/`package-lock` ملزمان ويُنسخان، وimage builds حتمية. `gate-check` للبوابة 6 يرفض Dockerfile يبتلع الفشل.
*الإسناد: GAP-13 (العلاج الحرفي: «composer install fail-closed مع lock ملزم»).*

### 5.9 الواجهات (CLI · hooks · oracle · أدوات)

**FR-80 — CLI واحد: `shamel`.**
نقطة دخول تنفيذية واحدة `engine/bin/shamel` → `python3 -m shamel_tools`، ترث subcommands v6 الـ 32 (projects·brain·brain-query/recall·route·gate-check·dispatch·squad·handoff·escalate·sync·checkpoint·claim·release·worktree·gate-merge·gate-tag·git-check·domain·tunnel·doctor·rooms·registry·budget·oracle·plan·run·resume·events·lint·…) وتضيف: `agents build` (FR-02) · `automation install/status` (FR-31) · `brain-audit` (FR-12) · `scaffold map` (FR-41) · `new` (FR-40). alias انتقالي `sofi → shamel` مسموح **خارج** الجذر فقط ولمدة محددة.
*الإسناد: GAP-15 (ثنائي sofi) · GAP-06 (8 نقاط دخول → 1) · مصفوفة §3 بند 2.*

**FR-81 — أدوات الغرف: الاكتفاء الذاتي فعلي.**
الـ 114 سكربت bash المنتشلة من G1 (التسمية أصلاً على مخطط v6: endpoint-scaffold، a11y-audit، sli-calc…) تدخل git وتوزَّع على `rooms/<room>/tools/` — تنتهي حقبة الـ README-placeholder. الماسحات (feature_scan · shamel_scan · shamel_verify — النسخة الأحدث بعد إزالة الازدواج البايتي، مُعادة التسمية من `sofi_*` ضمن حزمة FR-05) تعيش نسخة واحدة في `os/scanners/`. مهارة **browser-eyes** (فحص بصري بمتصفح حقيقي) تُعمَّم لأي PRJ بعد تنظيفها (FR-70). قاعدة governance موروثة: السكربتات تكتب داخل مشروعها فقط؛ exit code يحكم الـ pipeline؛ one-off → `_scratch/` يُطهَّر عند خروج البوابة.
*الإسناد: GAP-03 (الانتشال) · GAP-18 (العلاج: «ملء tools/ الغرف من المنتشَل — لا وضع وسط») · مصفوفة §3 بنود 10/11/15.*

**FR-82 — المهارات والأوامر: غربلة لا استنساخ.**
الـ skills الـ 13 تُرحَّل بأسماء `shamel-*`. من أوامر جيل الـ port الـ 54 تُغربَل القيّمة فقط (gate-check · deploy · parallel-build · security-sweep وأمثالها) إلى `.claude/commands/` — الباقي يسقط مع جيله. dual-form (spec↔spawnable) يبقى لكن **الطرف الثاني مولَّد** (FR-02).
*الإسناد: مصفوفة §3 بندا 8/21 · GAP-05 (غربلة الـ 54).*

**FR-83 — إعلان الحدود: داخلي مقابل خارجي.**
وثيقة `automation/BOUNDARIES.md` (وراثة نمط `ORCHESTRATOR.md` — أول جيل رسم الحدود كتابةً) تعلن: ما يعمل داخل الجلسة (hooks، skills، subagents — flat topology)، وما يعمل خارجها (cron، pipeline، oracle capture)، وكيف يتقاسمان **نفس** الـ Nexus وقاعدة الحالة، ولماذا لا daemon داخلي.
*الإسناد: مصفوفة بُعد 8 (G6: «أول جيل يرسمها كتابةً») · المبدأ 8.*

---

## 6. المتطلبات غير الوظيفية (NFR)

| ID | المتطلب | التحديد الملزم | الإسناد |
|----|---------|-----------------|---------|
| NFR-01 | **اقتصاد التوكن** | حقن الإقلاع ≤1000 توكن؛ العمليات الحتمية (عدّ، parity، evidence validation، scaffold) صفر استدعاء LLM («Python locates, model judges»)؛ 80% من العمليات الروتينية على tier mechanical | مصفوفة بُعد 10 (G3+G5) |
| NFR-02 | **الموثوقية — fail-loud** | لا فشل صامت في المكتبة: مسار معدوم/دماغ غائب/oracle فاشل = exit ≠ 0 واستثناء صريح؛ hooks وحدها fail-open وبعدّاد مرئي | GAP-09/11/20 |
| NFR-03 | **قابلية التدقيق** | كل قرار غير قابل للعكس = ADR؛ كل تذكرة done = evidence block (cmd+exit \| file:line \| diff/SHA)؛ كل gate advance = سجل فحص عدائي؛ كل تشغيل أتمتة = سطر jsonl | FR-23/31، مصفوفة §3 بند 1 |
| NFR-04 | **الفحص الذاتي المستمر** | `shamel doctor` يعمل يومياً (cron) وفي CI fail-closed؛ substrate بـ selftest يمر 100% قبل أي إصدار | مصفوفة بُعد 9 (G3+G5) |
| NFR-05 | **flat topology** | صفر عمليات مقيمة يملكها شامل؛ كل التنفيذ إما داخل جلسة Claude Code أو عمليات قصيرة العمر يطلقها cron/المشغّل | المبدأ 8، فلسفة G5 |
| NFR-06 | **قابلية النقل** | لا مسار مطلق hardcoded خارج `paths.py`/`settings`؛ env overrides (`SHAMEL_PROJECTS_DIR`…)؛ يعمل من أي clone للجذر | GAP-09/19 |
| NFR-07 | **قابلية الصيانة** | نسخة واحدة لكل concern (يفحصها doctor)؛ ترقية نموذج = سطر واحد (FR-60)؛ إضافة وكيل = ملف spec واحد + توليد | GAP-06/17 |
| NFR-08 | **سلامة git** | لا `reset --hard`/`--force` (حجب hook)؛ لا أسرار/`_scratch` في التاريخ؛ commit مبكر ومتكرر؛ handoff بلا commit = غير موجود | وراثة `06-git-discipline` |
| NFR-09 | **حياد اللغة** | العقيدة والpersonas عربية تقنية؛ الكود والcommits والتحذيرات الأمنية إنجليزية نثرية كاملة غير مضغوطة | FR-62 |
| NFR-10 | **صفر تلوث نصي** | فحص محارف دخيلة (CJK وغيرها) على كل ملف persona/spec عند الاستيراد والتوليد — درس تلوث 14/68 في G1 | تقرير 05 §صحة 4 |

---

## 7. قرارات الترحيل

### 7.1 عمليات الإنقاذ — تسبق كل شيء (اليوم صفر، قبل بناء الجذر)

مصدرها خيط الترابط في تحليل الفجوات: «الإنقاذ لا ينتظر أحداً».

| # | العملية | التفصيل | الإسناد |
|---|---------|---------|---------|
| R1 | **PRJ-SAKK إلى git** | `git init` داخل المشروع + commit أولي (كود + `_context/`) + remote خارجي — قبل أي بند آخر | GAP-01 |
| R2 | **إنقاذ fork الـ orchestrator** | commit لـ `ceo_agent.py` (14.8KB — موجود فقط في MAIN untracked) + `translator_gateway` (455 سطراً) + `orchestrator.db` على فرع إنقاذ | GAP-03 |
| R3 | **إنقاذ كنوز G1** | إدخال `tools/` الـ 114 + `browser-eyes` (بعد نزع الاعتمادات — FR-70) + gate checklists 0–8 إلى git | GAP-03, GAP-13 |
| R4 | **المصالحة** | اعتماد `origin/main` مرجعاً؛ إعادة زرع الحمولة الفريدة من `prj/PRJ-SAKK` وmain المحلي فوقه على فرع مصالحة؛ حسم تصادمات CLAUDE.md/MEMORY.md يدوياً + ADR؛ الـ stash يبقى حتى اكتمال المصالحة ثم يوثَّق التخلص | GAP-02 |

### 7.2 ماذا يُرحَّل من كل جيل (قرارات ملزمة — من المصفوفة §2/§3)

| الجيل | القرار | ما يُرحَّل إلى شامل | ما يُدفن (archive ⛔ + tag) |
|-------|--------|----------------------|------------------------------|
| **G3 v6** (الفائز 8/10) | **العمود الفقري — يُرحَّل شبه كامل** | الدستور (11 مادة + إنفاذ 02/03) · ثلاثي الـ Nexus + doctor + agent-pins · صيغة الوكيل المزدوجة (بتوليد الطرف الثاني) · hooks الخمسة · BRAIN + memdb + قوالب + LESSONS-sig · RCCF + bus · oracle (بشرط FR-33) · 13 skill + `.claudeignore` · قالب CHARTER · `sofi_tools` (24 موديلاً — يُعاد تجذيرها كـ `shamel_tools`) | `os/autopilot/` · `os/ooda/` ×2 · `os/agents/tier-*` · model IDs الحرفية (تستبدلها FR-60) |
| **G5 substrate** | **النواة الحتمية — يُرحَّل كاملاً** | الأدوات الست (registry→`schemas.py` · taskq · validate · gateway · check · gitflow) · فلسفة «ledger لا daemon» · **مواصفة taskq كآلة الحالات الواحدة** التي تخلف التطبيقات الستة المتوازية لإدارة المهام | لا شيء — يندمج في `shamel_tools` (يخرج من تحت `.claude/`) |
| **G6 orchestrator** | **يُرحَّل بعد توحيد الـ fork** | `state_db` (WT) + `translator_gateway` (MAIN) + `ceo_agent.py` (منقذ R2) + `agent_invoker` MOCK/live + الـ 22 أداة موحَّدة الرموز — **موصولاً بالـ Nexus إلزامياً** (FR-32) + نمط `ORCHESTRATOR.md` للحدود (FR-83) | fork MAIN بعد الدمج · جداول الغرف/الرموز المضمّنة المخالفة للـ Nexus |
| **G1 OpenCode** | **انتشال ثم دفن** (R3) | 114 سكربت أدوات → `rooms/*/tools/` · browser-eyes (منظّفاً) · gate checklists 0–8 · فكرتا translator وpermission-per-agent | كل `.opencode/` (68 وكيلاً — 14 ملوثة CJK، موديل ميت) · node_modules 63M يُحذف · `.sofi-run/` · memory الصفرية · hooks bash التي لم تعمل قط |
| **G2 Engine v5** | **التقاط الجوهر ثم الدفن** | منطق intake-orchestration (wear-the-hierarchy، leaf-spawn) → **المادة 11** (FR-20) · الماسحات الثلاث (النسخة الأحدث، نسخة واحدة) | `engine/` كاملاً · dashboard v5 + `index.html` («30 وكيلاً») · `session_start` القديم في MAIN (يُصحَّح ضمن R4) · DOCTRINE الـ 21 بروتوكولاً (تعارضها حُسم في المادة 11) |
| **G4 org-rooms** | **يُرحَّل كطبقة، لا ككون** | حوكمة الصلاحيات السداسية → frontmatter `authority:` (FR-53) · الكانون العربي-السوري + الملفات الـ 100 كـ HR profiles مربوطة بـ `personas.yaml` (FR-04) | الخريطة العشرية (تخسر أمام الـ 15) · دلالة GTW-06 الخارجية (يعاد توزيعها — FR-05) |
| **جيل الـ port (MAIN/.claude)** | **يُلغى** | الأوامر القيّمة فقط من الـ 54 بعد الغربلة (FR-82) | 105 stubs · 107 skills مرآة · engine الخاص به |
| **طبقة المشاريع** | **الدروس تُقنَّن** | قانون يوم-صفر (FR-40) · GATE0..8 artifacts (FR-44) · FOLDER-MAP مولَّد (FR-41) · حُرّاس checkpoint (FR-43) · «الكود هو الحقيقة» (FR-12) · نمط Cloudflare→Caddy→حاوية · PRJ-SAKK نفسه يُرحَّل repo مستقلاً **بإعادة تصنيف Gate 4/5** (FR-51) | `projects/README.md` المشير لمسارات v5 · روايات الـ stack الكاذبة (تُصحَّح بـ brain-audit) |

### 7.3 قرارات معمارية محسومة (كانت معلّقة في المصفوفة §5)

| # | السؤال | القرار في شامل | الإسناد |
|---|--------|-----------------|---------|
| Q1 | توحيد git؟ | origin/main مرجعاً + فرع مصالحة (R4)؛ شامل يبدأ repo جديداً نظيفاً بعد المصالحة | GAP-02 |
| Q2 | تصادم GTW؟ | GTW = Nexus حصراً؛ محتوى API-Gateway يُعاد توزيعه على arc/bck/sec | GAP-15، تقرير 05 |
| Q3 | 15 غرفة أم 10؟ | **15** — الأكمل تغطية | FR-01، تقرير 05 |
| Q4 | كانون الأسماء؟ | العربي-السوري canonical (هوية شامل) والدولي alias محفوظ في personas.yaml | FR-04 |
| Q5 | تعشيش worktrees؟ | يُفك — خارج `.claude/` نهائياً | FR-42، GAP-05 |
| Q6 | ثنائيا sofi/registry؟ | `shamel` الوحيد؛ registry = وكلاء فقط | FR-05/80 |
| Q7 | paths الصامت؟ | fail-loud + worktree-aware | FR-42، GAP-09 |

---

## 8. المخاطر والافتراضات

### 8.1 المخاطر

| ID | الخطر | الاحتمال | الأثر | التخفيف |
|----|-------|----------|-------|---------|
| RSK-01 | ضياع أصول untracked (PRJ-SAKK، ceo_agent، أدوات G1) قبل اكتمال الإنقاذ | متوسط | كارثي — غير قابل للاسترداد | R1–R3 تنفَّذ أولاً وقبل أي تنظيف/بناء؛ ممنوع أي `checkout/clean/stash drop` قبل إتمامها |
| RSK-02 | تصادمات مصالحة git (ثلاث سلالات + stash 3368 ملفاً) تُحسم خطأً فتضيع حمولة فريدة | متوسط | عالٍ | فرع مصالحة معزول، حسم CLAUDE/MEMORY يدوي مع ADR لكل قرار، الـ stash لا يُمس حتى النهاية (R4) |
| RSK-03 | انحراف التوليد: تحرير spawnables يدوياً يعيد إنتاج GAP-07 | متوسط | متوسط | بصمات agent-pins + doctor fail-closed في CI (FR-02/34) |
| RSK-04 | الأتمتة الورقية تعود: manifest بلا crontab أو cron بيئته ناقصة (PATH/auth لـ `claude -p`) | متوسط | متوسط | `automation status` يطابق الثلاثية ادعاء↔crontab↔سجل؛ سجل jsonl لكل تشغيل مع exit code (FR-31) |
| RSK-05 | اعتماد oracle على خدمة خارجية (Gemini) يتعطل | متوسط | منخفض | FR-33: fallback API + exit≠0 + المكتب استشاري لا يملك بوابة — تعطله لا يجمّد دورة الحياة |
| RSK-06 | ترقية/تقاعد نماذج Anthropic يكسر التوجيه | مرتفع زمنياً | منخفض | طبقة aliases بملف واحد (FR-60) + إعادة توليد بأمر واحد |
| RSK-07 | نطاق الترحيل يتضخم (نقل محتوى الأجيال بدل المذكور حصراً) فيعيد التكرار | متوسط | عالٍ | §4.2 بند 6 + doctor يكشف الازدواج (FR-34) + archive/INDEX.md يوثّق ما دُفن أين |
| RSK-08 | bus factor = 1 (مشغّل واحد وجهاز واحد) | دائم | عالٍ | remotes خارجية إلزامية لكل repo (شامل + كل مشروع — FR-40، G-05) |
| RSK-09 | hooks fail-open تُخفي انهيار طبقة الانضباط أسابيع | منخفض بعد العلاج | متوسط | عدّاد الأعطال المرئي في doctor اليومي (FR-30، G-11) |
| RSK-10 | إعادة تصنيف PRJ-SAKK (من 6 إلى 4/5) تُقاوَم فتبقى بوابة كاذبة كسابقة معيارية | منخفض | عالٍ | FR-51 يجعل الإعلان بلا gate-tag ناجح خرقاً آلياً — لا مجال للمجاملة |

### 8.2 الافتراضات

1. **بيئة التشغيل:** سطح مكتب Linux محلي، Claude Code هو الـ runtime الوحيد للوكلاء، و`claude -p` متاح لـ cron بجلسة مصادَقة صالحة.
2. **مشغّل واحد** يملك قرار الدمج النهائي في المصالحة (R4) — لا حاجة لآلية تصويت.
3. **الوصول للأجيال القديمة قراءةً** يبقى متاحاً حتى اكتمال الانتشال والأرشفة (لا حذف قبل snapshot — توصية H2 الحرفية).
4. **remote خارجي متاح** (GitHub عبر `gh`) لشامل ولكل مشروع.
5. **حسابا الخدمات الخارجية** (Gemini للـ oracle) متاحان؛ غيابهما لا يعطّل النظام (RSK-05).
6. **stack defaults** تبقى كما هي (Laravel/Blade/Flutter)؛ أي تغيير قرار منتَج لاحق لا قرار شامل.
7. أعداد الجرد المرجعية (105 وكيلاً · 15 غرفة · 9 بوابات · 13 skill · 114 أداة) صحيحة كما أثبتتها التقارير بالعدّ الفعلي — أي فرق يُكتشف عند الترحيل يعالج بتذكرة لا باجتهاد صامت.

---

## 9. معايير القبول (لكل FR — فحص ميكانيكي، لا تقييم ذاتي)

كل معيار يُصاغ كأمر/فحص بشرط نجاح صريح؛ التحقق النهائي يجريه فاحص عدائي fresh-context (اتساقاً مع V2) لا منفّذ البند.

| FR | معيار القبول الميكانيكي |
|----|--------------------------|
| FR-01 | `ls rooms/ \| wc -l` = 15؛ لكل غرفة: CHARTER بالأقسام الخمسة + `tools/` يحوي ملفات تنفيذية (لا README وحيد)؛ `shamel doctor` يفحص البنية = PASS |
| FR-02 | `shamel agents build && git diff --exit-code .claude/agents/` = 0 (التوليد حتمي)؛ تعديل يدوي لأي spawnable ثم `shamel doctor` = FAIL (بصمة مخالفة)؛ عدد specs = عدد spawnables = عدد registry entries |
| FR-03 | `shamel lint agents` = exit 0؛ `grep -rL '^tools:' rooms/*/agents/*.md` = فارغ؛ `grep -c 'WebSearch' .claude/agents/*.md` يطابق منح الـ registry بالضبط |
| FR-04 | `python3 -c "yaml.safe_load(open('nexus/personas.yaml'))"` بلا خطأ؛ كل `persona:` في specs موجود في الجدول (فحص doctor)؛ صفر أسماء بشرية حرّة في frontmatter |
| FR-05 | `find ~/Desktop/SHAMEL -path '*/archive' -prune -o -name 'sofi*' -type f -print` = 0؛ ملف واحد فقط باسم `registry.yaml`؛ `grep -r 'bkd_05\|uxr_02' automation/` = 0 |
| FR-06 | إدخال خام عبر `shamel dispatch --raw "<نص>"` ينتج JSON مهيكلاً بحقول intent/scope/priority/effort-class قبل أي spawn |
| FR-10 | القوالب السبعة موجودة في `brain/templates/`؛ كل قالب بـ frontmatter `memory-type`؛ `shamel brain-query` يعمل على الطبقات الثلاث |
| FR-11 | `shamel checkpoint PRJ-X "test: probe"` داخل مشروع بلا `.git` = exit ≠ 0 برسالة صريحة؛ داخل مشروع سليم = commit في repo المشروع (يتحقق بـ `git -C projects/PRJ-X log -1`) وحقلا branch/head_sha في STATE غير فارغين |
| FR-12 | تحرير رقم يدوياً في STATE ثم `shamel brain-audit` = FAIL يذكر الحقل؛ `shamel scaffold map` يولّد FOLDER-MAP يطابق `find` الفعلي؛ إعلان stack بلا manifest مطابق = FAIL |
| FR-13 | بعد 3 جلسات: `sqlite3 brain/memdb/brain.db 'select count(*) from observations'` ≥ 3؛ `shamel recall "<كلمة من جلسة سابقة>"` يرجع نتيجة |
| FR-14 | ملف MEMORY.md واحد في الشجرة (`find -name MEMORY.md \| wc -l` = 1)؛ لا يحوي محتوى معرفي (pointers فقط — مراجعة knw-lead) |
| FR-15 | بعد أول تشغيل reflect: `grep -c '^LES-' brain/org/LESSONS.md` ≥ 1 وكل درس يحمل sig+ticket؛ تشغيل ثانٍ بنفس المدخلات لا يضاعف الدروس (idempotency بالـ sig) |
| FR-20 | `ls constitution/*.md \| wc -l` = 12؛ المادة 11 موجودة وتنص صراحةً على شرعية الـ skills؛ `find -path ./archive -prune -o -name 'session_start*' -print` = ملف واحد |
| FR-21 | `/shamel-delegate bck-api-engineer "مهمة"` ينتج كتلة رباعية كاملة بحقول effort-class/budget/evidence؛ الكتلة الناقصة تُرفض بالنص القانوني «clarify before commit» |
| FR-22 | عيّنة تسليم بادعاء بلا مصدر تُرفض في المراجعة العدائية؛ نص المادة 02 المرحَّل يطابق الأصل (diff دلالي موثّق إن عُدّل) |
| FR-23 | تذكرة done بلا evidence block → `shamel gate-check` = FAIL (اختبار سلبي مسجّل)؛ سجل gate advance يظهر هوية فاحص ≠ هوية منفّذ؛ حكم UNKNOWN مقبول في الـ schema |
| FR-24 | تذكرة مخالفة للـ regex في HANDOFFS يكشفها `shamel lint tickets`؛ سيناريو 3 محاولات فاشلة ينتج crash-dump JSON + تذكرة تصعيد (اختبار محاكاة) |
| FR-30 | الـ hooks الخمسة مسجّلة في `settings.json` وتعمل (أمر خطر يُحجب فعلياً — اختبار حي)؛ حقن الإقلاع مقيس ≤1000 توكن؛ إفشال hook متعمد يظهر في عدّاد doctor |
| FR-31 | `shamel automation install && crontab -l \| grep shamel` ≥ 3 أسطر؛ `shamel automation status` = exit 0 فقط عند اكتمال ثلاثية ادعاء↔cron↔سجل؛ سجل reflect.jsonl يحوي تشغيلاً حقيقياً |
| FR-32 | `grep -rn 'rooms *=\|ROOM_CODES' automation/pipeline/` = 0 (لا جداول مضمّنة)؛ تشغيل MOCK يصل COMPLETED بقراءة الـ Nexus فقط؛ `pgrep -f pipeline` بعد الانتهاء = 0 (لا مقيم) |
| FR-33 | فصل CDP ثم `shamel oracle review …` ينجح عبر fallback أو يرجع exit ≠ 0 (لا نجاح زائف)؛ payload مرسل مفحوص خالٍ من أسرار (اختبار حقن سر وهمي → يُredact) |
| FR-34 | زرع ازدواج متعمد (تنفيذي ثانٍ/سجل ثانٍ) → `shamel doctor` = FAIL يسمّيه؛ doctor في CI يمنع الدمج عند الفشل؛ rescue-scan يكشف ملفاً ذهبياً untracked مزروعاً؛ تحرير `routes.<id>` يدوياً في routing.yaml بما يخالف frontmatter الـ spec → doctor = FAIL (parity الـ route) |
| FR-40 | `shamel new PRJ-TEST "t"` ينتج repo بـ `git -C projects/PRJ-TEST log --oneline \| wc -l` ≥ 1 و`git remote -v` غير فارغ؛ فشل إضافة remote يفشّل السكافولدر كله (ذرّية)؛ `shamel projects --verify` = PASS |
| FR-41 | شجرة المشروع المولَّد تطابق الشكل القانوني؛ `diff <(shamel scaffold map --print) docs/FOLDER-MAP.md` = 0 |
| FR-42 | من worktree: `python3 -c "from shamel_tools.paths import projects_dir; print(projects_dir())"` يرجع الجذر الصحيح أو يرمي استثناء صريحاً — لا مسار معدوم صامت؛ لا worktree تحت `.claude/` |
| FR-43 | commit بصيغة غير conventional يُرفض؛ ملف داخل `_scratch/` يُunstage تلقائياً؛ الـ trailer `SHAMEL:` موجود في كل checkpoint (فحص `git log --format=%B`) |
| FR-44 | مشروع مولَّد يحوي `_context/features/`؛ `shamel gate-check` يرفض بوابة بلا artifact قياسي مسمّى |
| FR-45 | `shamel domain register PRJ-TEST` يضيف سطر `/etc/hosts` بوسم النظام؛ `shamel tunnel down` يقتل النفق فعلاً (probe بعد الإغلاق يفشل) |
| FR-50 | `gates.yaml` يُحلَّل و9 بوابات كاملة الحقول (فحص parse يطبع مفاتيح كل بوابة)؛ كل بوابة تشير لـ checklist موجود على القرص |
| FR-51 | إعلان gate 6 على مشروع بلا workflow → `shamel gate-check PRJ 6` = FAIL يسمّي الـ artifact الغائب؛ STATE الخاص بـ PRJ-SAKK المرحَّل يقول gate ≤ 5 |
| FR-52 | تذكرة موسومة money/PII تُوجَّه Deep-Audit آلياً (فحص التصنيف في dispatch)؛ Fast-Track موثّق بحدوده في gates.yaml |
| FR-53 | `grep -L 'authority:' rooms/*/agents/*.md` = فارغ؛ استعلام `shamel registry --authority veto` يرجع حاملي الفيتو ومنهم brd-cso |
| FR-60 | `grep -rn 'claude-[a-z]*-[0-9]' nexus/ --include='*.yaml' \| grep -v models.yaml` = 0؛ تغيير alias واحد + `shamel agents build` يحدّث كل الـ spawnables المتأثرة |
| FR-61 | كل Work Order مولَّد يحمل effort-class + budget؛ محاكاة تجاوز budget تفعّل circuit breaker (سجل + توقف)؛ route بـ deep لمهمة روتينية يرفضها الـ router |
| FR-62 | `.claudeignore` موجود ويغطي vendor/node_modules/archive؛ `ls .claude/skills \| wc -l` = 13 بأسماء shamel-*؛ قياس حقن الإقلاع ≤1000 |
| FR-70 | ماسح الأسرار على الشجرة كاملة = 0 نتيجة (بعد زرع سر وهمي = 1 نتيجة — يعمل)؛ browser-eyes المرحَّل يقرأ الاعتمادات من env حصراً |
| FR-71 | اختبار حقن نص فيه مفتاح وهمي عبر oracle → الـ payload الصادر (المسجّل) لا يحويه |
| FR-72 | تذكرة أمنية بفيتو cso تجمّد المسار (لا يتقدم gate-check)؛ مهمة auth مصنّفة Deep-Audit آلياً |
| FR-73 | `grep -rn '\|\| true' projects/*/deploy/Dockerfile` = 0 في القوالب؛ build بلا lockfile يفشل في gate-check للبوابة 6 |
| FR-80 | `which shamel` واحد؛ `shamel --help` يسرد المجموعات الموروثة والجديدة؛ `shamel doctor` = PASS على الجذر المكتمل |
| FR-81 | `find rooms/*/tools -type f -name '*.sh' \| wc -l` ≥ 110 وكلها `bash -n` نظيفة؛ `git ls-files rooms/*/tools \| wc -l` = العدد نفسه (كلها tracked)؛ نسخة واحدة من كل ماسح (`md5sum` لا يجد توائم) |
| FR-82 | `ls .claude/commands \| wc -l` ≤ 15 (المغربَل فقط)؛ كل أمر منها يُنفَّذ بلا مرجع dangling (فحص مراجع آلي — درس G1 الـ 100%) |
| FR-83 | `automation/BOUNDARIES.md` موجود ويذكر صراحة: flat topology، لا daemon، مصدر Nexus المشترك، وحدود claude -p/cron |

**بوابة قبول الوثيقة ككل (Definition of Done للـ PRD):** كل FR أعلاه يحمل إسناداً (GAP-xx أو بند مصفوفة) — مفحوص؛ كل GAP من العشرين يعالجه FR واحد على الأقل — خريطة التغطية: GAP-01→FR-11/40 · GAP-02→R4/Q1 · GAP-03→R2/R3/FR-81 · GAP-04→FR-51/23 · GAP-05→FR-42/62/82 · GAP-06→FR-34/80 + NFR-07 · GAP-07→FR-02 · GAP-08→FR-14/20 · GAP-09→FR-11/42/43 · GAP-10→FR-03 · GAP-11→FR-13/15/31/33 · GAP-12→FR-12/41 · GAP-13→FR-70/72/73 · GAP-14→§7.2 (الدفن المعياري) + G-12 · GAP-15→FR-04/05/80 · GAP-16→FR-01/04/53 · GAP-17→FR-60 · GAP-18→FR-01/81 · GAP-19→حزمة hygiene ضمن R4 وdoctor (FR-34) · GAP-20→FR-30.

---

*نهاية الوثيقة — شامل PRD v1.0. أي تعديل لاحق يمر بإجراء Amendment (ADR بقرار المشغّل) ويُحدَّث فيه رقم الإصدار.*
