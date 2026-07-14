# SHAMEL — تقرير 04: خريطة المحرّكات وطبقات الأدوات وقياس التكرار

**التاريخ:** 2026-07-10 · **المدقّق:** subagent (READ-ONLY) · **النطاق:** MAIN=`/home/es3dlll/Desktop/Lorka` · WT=`/home/es3dlll/Desktop/Lorka/.claude/worktrees/org-rooms-100`

---

## الجرد

### الأجيال الخمسة للمحرّكات (مرتّبة زمنياً)

| # | الطبقة | المسار | الجيل | الحجم | git |
|---|--------|--------|-------|-------|-----|
| G-A | **engine/** | `MAIN/engine/` | v5 «AUTOPILOT/DOCTRINE» — 30 وكيلاً، tiers لا rooms | 159 ملفاً فعلياً (+3105 vendored `cybersecurity-skills`) | tracked |
| G-B | **.opencode/** | `MAIN/.opencode/` | جيل OpenCode — 68 وكيلاً + `sofi-engine` bash suite | ضخم (node_modules) | **untracked بالكامل** (`git ls-files .opencode/` = 0) |
| G-C | **company/ + company/os** | `WT/company/` | v6 «Company of Rooms» — 15 غرفة/105 وكيلاً | `sofi_tools` = **24 موديول** Python + `bin/sofi` bash | tracked (10eb60a, e35ecbf) |
| G-D | **.claude/engine/tooling** | `WT/.claude/engine/tooling/` | substrate «الطبقة الداخلية» — 6 أدوات حتمية + موزّع `sofi` python | registry/taskq/validate/gateway/check/gitflow | tracked (10eb60a) |
| G-E | **orchestrator/ + tools/** | `WT/orchestrator` + `WT/tools` **و** فرع منفصل في `MAIN/orchestrator` + `MAIN/main.py` | «الطبقة الخارجية Option C» — pipeline حتمي خارج جلسة Claude | 4 موديولات + 10 غرف/**22 أداة** (عدّ `class X(Tool):` = 22) | نسخة WT committed (b6db3bb) · نسخة MAIN **untracked** |

### تفصيل G-A (الجيل القديم `MAIN/engine/`)
- الوثائق: `AUTOPILOT.md` (يصف «9 divisions, ~121 capabilities … 30-agent dev org» — `engine/AUTOPILOT.md:3`)، `DOCTRINE.md` (6 تعاليم — الجيل v6 لديه 7)، `PERSONAS.md`، `ROOMS-REFERENCE.md`، `ROSTER.md`، 21 بروتوكولاً في `protocols/`.
- التنظيم بالطبقات لا الغرف: `engine/agents/tier-0-strategy … tier-4-infrastructure + advisors`.
- **tooling حيّ وظيفياً**: `engine/tooling/bin/sofi` (bash → `python3 -m sofi_tools`، السطر 8) يعمل الآن — تشغيله بلا وسيطات يطبع usage بـ **24 أمراً فرعياً** (`projects…gemini…doctor`) ويخرج بسلام. `sofi_tools` القديمة = **13 موديولاً** فقط.
- الماسحات موجودة فعلاً: `engine/tooling/agents/ceo/sofi_scan.py` و`sofi_verify.py` و`feature_scan.py` و`squad_orchestrator_v2.py` (21 ملفاً في `agents/ceo/`).
- `engine/server-plane/` (Caddyfile + bootstrap) و`engine/ooda/engine/main.py` (OODA v2).
- **معلَن legacy رسمياً**: `engine/README.md:1-3` — «⛔ This directory is **legacy**. All content has moved to canonical homes» مع جدول هجرة (`engine/tooling/ → orchestrator/`، `engine/agents/ → .opencode/agents/`). ملاحظة: README هذا نفسه **untracked** (ظهر `??` في `git status`).
- **هل ما زال حيّاً؟** hooks الـ MAIN لا **تنفّذ** شيئاً منه (الـ 4 hooks في `.claude/settings.json` تستدعي `.claude/hooks/*.py` فقط)، لكن `session_start.py` في MAIN **يعلن** أوامره للنموذج في كل جلسة: `MAIN/.claude/hooks/session_start.py:83-84` يحقن نصاً يقول `engine/tooling/`: `sofi sync|checkpoint|…` + `python3 engine/tooling/agents/ceo/sofi_scan.py` — أي أنّ الجيل القديم ما زال «مُوصى به» للجلسات في MAIN. نسخة WT من نفس الـ hook مصحّحة وتشير إلى `company/os/bin/new-project.sh` (`WT/.claude/hooks/session_start.py:108`).

### تفصيل G-B (`.opencode/`)
- `sofi-engine/` = orchestration bash كامل موازٍ: `sofi-engine.sh` (CLI: run/next/advance/complete)، `task-queue/task-queue.sh` + `tasks.json` (state machine: pending→assigned→in_progress→completed|failed — السطور 2-3)، `orchestrator/brain-state-machine.sh` + `rccf-builder.sh`، `git-guard/`، `event-bus/`، `schema-registry/`، `translator/`، `workflow-engine/`.
- `.opencode/engine/tooling/bin` و`lib` **فارغان تماماً** (تمّ إفراغهما).
- 68 ملف وكيل في `.opencode/agents/`، و`.opencode/tools/` فيه 114 ملفاً (8 منها Python فقط — أغلبه توثيق غرف).
- كله خارج git → طبقة ميتة محلياً، رُحّلت فعلياً إلى `.claude/` الأصلية (راجع memory: «claude-team-installed»).

### تفصيل G-C (`WT/company/os`) — أمر التشغيل المطلوب
```
$ bash WT/company/os/bin/sofi doctor | tail
routing   : ✓ 109 routes (company/nexus/routing.yaml)
registry  : ✓ 15 rooms · 105 agents (company/nexus/registry.yaml)
agents    : ✓ 105 spawnables ↔ 105 room specs (105↔105)
skills    : ✓ registry skill paths exist
VERDICT   : PASS
```
- `bin/sofi` = نفس نمط bash→`python3 -m sofi_tools` كالجيل القديم حرفياً (`company/os/bin/sofi:8`) لكن المكتبة نمت 13→24 موديولاً (زيادة: memdb, lessons_cache, transitions, budget, telemetry, scheduler, acceptance, agentlint, event_server, resume, oracle-side…).
- **نقل بالجملة من v5**: `company/os/agents/` ما زال بنفس بنية الطبقات القديمة (`ceo/`, `tier-1-architecture/`, `tier-3-quality/` …) — `sofi_verify.py` **متطابق بايتاً** مع نسخة `engine/` (diff صامت)، بينما `sofi_scan.py` و`sofi_tools/tickets.py` تفرّعا.
- `company/os/ooda/engine/main.py` موجود — **نسخة ثانية** من OODA بجانب `engine/ooda/engine/main.py`.

### تفصيل G-D (substrate) — أمر التشغيل المطلوب
```
$ python3 WT/.claude/engine/tooling/sofi selftest --json
{"ok": true, "verdict": "PASS", "tools": {"registry": "PASS", "taskq": "PASS",
 "validate": "PASS", "gateway": "PASS", "check": "PASS", "gitflow": "PASS"}}
```
- موزّع Python (لا bash) بفلسفة معلَنة: «There is NO always-on daemon: the task queue is a ledger» (`sofi` docstring، السطور 4-6). `taskq.py` = SQLite بآلة حالات صارمة (pending→assigned→running→completed/failed — docstring السطور 6-12). `registry.py` هنا = SSoT لـ**مخطط DB وعقود API** (وليس سجلّ وكلاء — تصادم تسمية مع `nexus/registry.yaml`).

### تفصيل G-E (الإطار الخارجي) — المقارنة المطلوبة
- نسخة WT committed في `b6db3bb` (2026-07-09 22:25:34): `main.py` 423 سطراً + orchestrator (4 موديولات) + `tools/` أعلى الجذر (10 ملفات غرف مفردة + `tool_base.py`/`tool_runner.py`/`room_manager.py`). `ORCHESTRATOR.md:5-6` يعلنه «الطبقة الخارجية (Option C) — مكمّلة للطبقة الداخلية `.claude/engine/tooling/`».
- `agent_invoker.py` يستدعي وكلاء فعلياً عبر `subprocess.run(["claude","-p",prompt])` مع وضع MOCK بديل (`WT/orchestrator/agent_invoker.py:268-269`).
- **`diff -rq MAIN/orchestrator WT/orchestrator` ⇒ تفرّع حقيقي، لا نسخ**:
  - كل الملفات الأربعة المشتركة **تختلف** (state_db: 240 سطراً في MAIN مقابل **356** في WT؛ translator_gateway: **455** في MAIN مقابل 398 في WT).
  - فقط في MAIN: `ceo_agent.py` (CEO Agent بـ system prompt عربي، 14.8KB)، `orchestrator.db` (حالة SQLite حيّة)، و`tools/` **داخل** orchestrator كحِزَم (`tools/bkd_05/` مجلد) بدل ملفات مفردة.
  - نسخة MAIN كلها **untracked** (`?? main.py`, `?? orchestrator/` في `git status` على فرع `prj/PRJ-SAKK`).
  - أي: لا نسخة منهما superset — MAIN أضاف ceo_agent وكبّر الـ translator، وWT أعاد الهيكلة وكبّر state_db. **fork مزدوج لنفس الكود في نفس اليوم.**

### تفصيل البند 5 (`MAIN/main.py` + `dashboard/` + `index.html`)
- `MAIN/main.py` (`main.py:1-11`): «SOFI Engine — Multi-Agent Autonomous Orchestration Framework» — CLI الإطار الخارجي (rich console) لكن نسخة الـ fork: يستورد `orchestrator.ceo_agent.run_ceo` (السطر 31) غير الموجود في نسخة WT. جيل G-E، فرع MAIN، untracked.
- `dashboard/` = **جيل v5 صِرف** و**tracked**: `dashboard/server.py:3` «SOFI v5 — Live Observability Dashboard backend» ويقرأ `sofi_tools.tickets` + `engine/routing/routing.yaml` + «the 30-agent roster» (السطور 7-9) — مربوط عضوياً بالجيل القديم G-A.
- `MAIN/index.html` = صفحة هبوط ثابتة v5: `<title>SOFI — مؤسسة الوكلاء الذاتية · ثلاثون وكيلاً يبنون البرمجيات</title>` — «ثلاثون وكيلاً» يؤرّخها لجيل الـ 30.
- **تصحيح لخريطة السياق**: `MAIN/.claude/agents/` يحوي **105** ملف `.md` داخل 15 مجلد غرفة (`find … -name "*.md" | wc -l` = 105) وليس 15 — الـ 15 هي مجلدات الغرف فقط.

---

## الصحة

| الطبقة | الفحص | النتيجة |
|--------|-------|---------|
| G-A `engine/tooling` | تشغيل `bin/sofi` بلا وسيطات | يعمل — usage بـ 24 أمراً؛ **legacy معلَن لكنه وظيفي** وما زال يُعلَن في session_start الخاص بـ MAIN |
| G-B `.opencode` | git + محتوى | untracked كلياً، tooling/bin فارغ — **جثة محلية** |
| G-C `company/os` | `sofi doctor` | **PASS** — 109 routes، 105↔105، skills paths سليمة |
| G-D substrate | `sofi selftest --json` | **PASS** — الأدوات الست كلها |
| G-E orchestrator | git + diff | نسخة WT سليمة committed؛ نسخة MAIN fork untracked بقاعدة بيانات حيّة — **حالة انقسام** |
| dashboard/index | مصادر البيانات | يقرأ عالم v5 (30 وكيلاً، `engine/routing/routing.yaml`) — **منفصل عن واقع v6 (105)** |

---

## نقاط القوة

1. **الطبقتان الجديدتان مُختبَرتان ذاتياً وناجحتان**: substrate selftest = PASS شامل، وdoctor v6 = PASS بتكافؤ 105↔105 — انضباط تحقّق حقيقي (V1/V2) لا موجود في أي جيل سابق.
2. **فصل معماري واعٍ ومكتوب**: `ORCHESTRATOR.md` يعرّف الخارجي (terminal, state-DB, deterministic) مقابل الداخلي (in-session substrate) — أول جيل يرسم الحدود صراحة.
3. **آلات حالات صريحة في 3 طبقات** (taskq الصارم، state_db بـ frozenset transitions في `state_db.py:77-83`، task-queue.sh) — النمط نضج عبر الأجيال.
4. **agent_invoker بوضع MOCK/live** — قابلية اختبار حتمية بلا API.
5. **الجيل القديم موثّق خروجَه**: `engine/README.md` جدول هجرة كامل old→canonical — يسهّل الترحيل لشامل.
6. **`sofi doctor` كفكرة parity-check** (spawnables↔specs↔registry) هي أنجح آلية مكافحة تفكّك في المنظومة كلها.

---

## نقاط الضعف

### جدول التكرار الحاسم — 8 نقاط دخول تنفيذية، 5 منها اسمها «sofi»

| # | Entry point | النوع | الجيل | الحالة |
|---|-------------|-------|-------|--------|
| 1 | `MAIN/engine/tooling/bin/sofi` | bash→`python -m sofi_tools` (13 mod) | v5 | يعمل، legacy معلَن، ما زال يُحقَن في session_start بـ MAIN |
| 2 | `MAIN/.opencode/sofi-engine/sofi-engine.sh` | bash suite | OpenCode | untracked، ميت |
| 3 | `WT/company/os/bin/sofi` | bash→`python -m sofi_tools` (24 mod) | v6 | PASS — **الأنضج للحوكمة** |
| 4 | `WT/.claude/engine/tooling/sofi` | موزّع Python، 6 أدوات | substrate | PASS — **الأنضج للحتمية داخل الجلسة** |
| 5 | `WT/main.py` | CLI الإطار الخارجي | G-E/WT | committed |
| 6 | `MAIN/main.py` | نفسه + ceo_agent | G-E/fork | untracked، متفرّع |
| 7 | `tools/tool_runner.py` (WT) / `MAIN/orchestrator/tools/` | CLI الأدوات (22 tool) | G-E ×2 بنيتين | متفرّع |
| 8 | `MAIN/dashboard/server.py` | خادم مراقبة | v5 | tracked لكنه يقرأ عالماً منقرضاً |

### مصفوفة الـ concerns — التطبيقات المتوازية

| Concern | v5 (engine/) | OpenCode | v6 (company/os) | substrate | orchestrator خارجي | **الأنضج** |
|---------|--------------|----------|-----------------|-----------|--------------------|------------|
| **Task queue / State** | `tickets.py` (HANDOFFS.md) | `task-queue.sh` (tasks.json) | `tickets.py` (تفرّع، HANDOFFS.md) | `taskq.py` (SQLite صارم) | `state_db.py` ×2 forks (SQLite pipeline) | substrate `taskq` (selftest PASS) — **6 تطبيقات متوازية** |
| **Registry / SSoT** | `tooling/registry.yaml` + `ROSTER.md` | `agent-routing.json` + `schema-registry/` | `nexus/registry.yaml` (15×105، doctor PASS) | `registry.py` (**SSoT مخطط DB** — تصادم اسم) | `room_manager.py` (10 غرف برموز مختلفة!) | v6 `nexus/registry.yaml` |
| **Gate check** | `sofi_tools/gates.py` + `sofi_verify.py` | `lifecycle/gates.yaml` | `gates.py`+`transitions.py`+`nexus/gates.yaml` | `check.py` (lint/test runners) + `gateway.py` | انتقالات TaskState الضمنية | v6 gates + substrate check |
| **Git guard** | `sofi_tools/guard.py`+`gitops.py` | `sofi-engine/git-guard/` | `guard.py`+`gitops.py` (تفرّع) | `gitflow.py` (no force/reset) | — | substrate `gitflow` + hook `pre_tool_use.py` (منسوخ في MAIN وWT كليهما) |
| **Routing** | `routing.py` + `engine/routing/routing.yaml` | `agent-routing.json` | `routing.py` + `nexus/routing.yaml` (109) | — | `translator_gateway.py` ×2 forks (intent→room) | v6 `nexus/routing.yaml` |
| **Memory / Brain** | `brain.py` | `.opencode/memory/` | `brain.py`+`memdb.py`+`lessons_cache.py` | — | `orchestrator.db` history | v6 (memdb + brain-query) |
| **OODA** | `engine/ooda/engine/main.py` | — | `company/os/ooda/engine/main.py` | — | — | نسختان متعايشتان |
| **Oracle/Gemini** | 8 ملفات gemini في `agents/ceo/` | — | نفس الملفات منقولة + `oracle` cmd | — | — | v6 oracle desk |

### عيوب مركّزة
1. **انقسام G-E النشط أخطر عيب**: نفس الإطار الخارجي بنسختين متباعدتين في نفس اليوم — MAIN فيه `ceo_agent.py` + db حيّ لكنه untracked (قابل للضياع بأي checkout)، وWT فيه إعادة الهيكلة الأنظف. لا مالك واضح.
2. **تصادم تسمية «registry»**: 3 دلالات مختلفة (سجل وكلاء v5/v6، SSoT مخططات substrate، room_manager الخارجي) — فخ إدراكي للوكلاء.
3. **تضارب رموز الغرف**: الإطار الخارجي يستخدم `uxr_02/bkd_05/knb_10` (10 غرف) بينما v6 الرسمي `res/bck/knw` (15 غرفة، `nexus/registry.yaml`) — لا جسر بينهما.
4. **session_start في MAIN يوجّه الجلسات إلى الجيل الميت** (engine/tooling) بينما نسخة WT توجّه إلى v6 — سلوك الجلسة يعتمد على أي شجرة فُتحت.
5. **dashboard/index.html أثر v5 tracked** يعرض «30 وكيلاً» وقيماً من `engine/routing/routing.yaml` — واجهة مراقبة تكذب على واقع 105.
6. **ازدواج bash/python في نمط الموزّع نفسه**: `bin/sofi` bash (v5 وv6 متطابقا الأسلوب) مقابل `sofi` python (substrate) — نفس الاسم، سلوكان.

---

## التداخل مع الطبقات الأخرى

- **G-A→G-C نقلٌ لا قطيعة**: `company/os/agents/` ورث بنية tiers القديمة حرفياً داخل جيل الغرف؛ `sofi_verify.py` متطابق بايتاً بين الجيلين — أي إصلاح في أحدهما لن يصل الآخر.
- **G-A→dashboard**: الـ dashboard الحي (tracked) يستورد `sofi_tools` القديمة ويقرأ `engine/routing/routing.yaml` — حذف `engine/` يكسر الـ dashboard بصمت.
- **G-D↔G-E مكمّلان بالتصميم** (داخلي/خارجي) لكن **يتنافسان فعلياً** على task-state (taskq مقابل state_db) وعلى مفهوم gateway (semantic gateway مقابل translator_gateway) بلا عقد مشترك.
- **G-E↔G-C**: الإطار الخارجي لا يقرأ `nexus/registry.yaml` ولا `routing.yaml` — بنى عالمه الخاص (10 غرف/رموز خاصة)، فانقطعت وحدة المصدر التي ينص عليها CLAUDE.md («routing.yaml the ONLY routing source»).
- **hooks منسوخة**: `pre_tool_use.py` وبقية الأربعة موجودة في MAIN وWT بنسختي session_start مختلفتين — أي طبقة enforcement مزدوجة التعريف.
- **.opencode→.claude**: الترحيل تم (105 وكيلاً في `.claude/agents` بالجهتين) لكن الجثة (68 وكيلاً + sofi-engine + node_modules) ما زالت على القرص خارج git تلوّث البحث والسياق.

---

## ما يُرحَّل لنظام شامل

1. **substrate الست أدوات كاملاً** (`WT/.claude/engine/tooling/`) — أصغر نواة حتمية ناجحة selftest؛ فلسفة «ledger لا daemon» تصلح أساساً لشامل.
2. **نمط `sofi doctor` / parity-check** (`company/os/sofi_tools` doctor + registry 105↔105) — يعمَّم ليفحص تطابق كل الطبقات.
3. **`nexus/{registry,routing,gates}.yaml` كمصدر وحيد** — الأنضج تمثيلاً؛ يجب أن يستهلكه الإطار الخارجي بدل رموزه الخاصة.
4. **من G-E نسخة موحّدة بعد دمج الـ fork**: `state_db.py` (نسخة WT 356 سطراً) + `translator_gateway` (نسخة MAIN 455 سطراً الأغنى) + `ceo_agent.py` (فقط في MAIN — يُنقذ قبل الضياع) + `agent_invoker` بنمط MOCK/live + الـ 22 أداة موحَّدة الرموز مع v6.
5. **آلة حالات واحدة للمهام** تخلف الستّ: مواصفة taskq الصارمة + جداول تاريخ state_db.
6. **الماسحات الناضجة**: `feature_scan.py`، `sofi_scan.py` (نسخة v6 المتفرّعة الأحدث)، `sofi_verify.py` — بعد إزالة ازدواجها.
7. **oracle desk** (sanitize→condense→capture→ingest) من v6 — أكمل حلقة مراجعة خارجية.
8. **يُترك خلفنا**: `.opencode/` كلها، `engine/` (بعد نقل server-plane/Caddy إن لزم)، dashboard/index.html بصيغتهما v5 (يُعاد بناء المراقبة على معطيات v6)، وأحد نسختي OODA.

---

## الحكم

**DEGRADED** — الجيلان الجديدان (v6 company/os + substrate) سليمان ومُثبتان (doctor PASS + selftest PASS)، لكن المنظومة ككل تحمل 5 أجيال متعايشة، 8 نقاط دخول، حتى 6 تطبيقات متوازية للـ concern الواحد، وfork نشط غير مُلتزَم للإطار الخارجي في MAIN مع hooks لا تزال توجّه جلسات MAIN إلى الجيل الميت — تكرارٌ بنيوي يستنزف ويُهدّد بضياع كود حي (ceo_agent) وليس عطباً وظيفياً.
