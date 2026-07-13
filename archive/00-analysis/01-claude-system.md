# تقرير شامل 01 — نظام `.claude` الأصلي (native Claude Code config) عبر الجيلين

**المدقّق:** وكيل SHAMEL (read-only) · **التاريخ:** 2026-07-10
**النطاق:** `WT=/home/es3dlll/Desktop/Lorka/.claude/worktrees/org-rooms-100/.claude` (جيل v6 «Company of Rooms») مقابل `MAIN=/home/es3dlll/Desktop/Lorka/.claude` (جيل OpenCode-port)

---

## الجرد

### 1) WT — `.claude` جيل v6 (الأحدث)

| المكوّن | العدد/الحالة | الدليل |
|---|---|---|
| `agents/` | **105 ملفاً flat** بنمط `<roomcode>-<role>.md` | `ls agents/*.md \| wc -l` → 105 |
| توزيع الغرف | arc 7 · bck 8 · brd 7 · dat 7 · dsn 8 · fnt 8 · gtw 6 · knw 6 · mob 6 · obs 6 · ops 7 · qa 7 · res 7 · sec 8 · str 7 = **105 عبر 15 غرفة** | `sed 's/-.*//' \| uniq -c` |
| `skills/` | **13 مهارة** كل واحدة `SKILL.md` (41–124 سطراً) | `ls skills/` |
| `hooks/` | 5 hooks بايثون + `_common.py` (كلها fail-open) | `ls hooks/` |
| `settings.json` | 5 أحداث hook مسلّكة + permissions + skillOverrides | `settings.json:41-94` |
| `commands/` | **غير موجود** — لا command palette في هذا الجيل | `ls: cannot access .../commands` |
| `engine/tooling/` | 6 أدوات substrate: `registry.py · taskq.py · validate.py · gateway.py · check.py · gitflow.py` + schemas + tests | `ls engine/tooling/` |
| `memory/` | `brain.db` (SQLite + wal) · `events.jsonl` · `sessions.jsonl` | `ls memory/` |
| `sofi.json` | workspace manifest يشير إلى `company/nexus/registry.yaml` و`company/CONSTITUTION.md` (v6.0) | `sofi.json:22-30` |

**بنية agent (عينات من 3 غرف مختلفة):**
- `agents/sec-pentester.md` — frontmatter كامل: `name` + `description` (متى يُستدعى) + **`tools:` بمنح صريحة** (Read/Grep/Glob/Write/Edit/Bash/WebSearch/WebFetch, أسطر 4-12) + `model: sonnet` (سطر 13). ثم RCCF كامل: `## 🎭 Role` (سطر 21) · `## 📂 Context` (24) · `## 🎯 Command` (30) · `## 📐 Format` (35) · `## ↪ Handoff & escalation` (41)، مع سطر Route يطابق `routing.yaml` وسطر Spec يشير إلى `company/rooms/09-security/agents/sec-pentester.md` (سطر 18).
- `agents/dsn-ui-designer.md` — نفس الهيكل، `model: sonnet`، منح أضيق (بلا Bash، سطر 4-11)، success metric صريح (سطر 32).
- `agents/gtw-gatekeeper.md` — `model: inherit` (سطر 9)، أدوات read-only + Bash فقط (أسطر 4-8) — least-privilege للقاضي.

**تغطية RCCF محقّقة آلياً على الـ105 كلها:** الأقسام الخمسة `🎭/📂/🎯/📐/↪` = **105/105 لكل قسم**، و`name:` frontmatter = 105/105، وسطر `Spec: company/rooms/...` = 105/105 (grep counts).

**توزيع الـmodel (الـ economic grid حيّ في الملفات):** `haiku ×15` (knw-doc-writer, gtw-router, sec-secrets-warden…) · `sonnet ×72` · `inherit ×18` (الـboardroom السبعة + leads حسّاسة + gtw-gatekeeper + arc-review-architect…). منح الويب: **WebSearch=21 وWebFetch=21 لنفس الأسماء** — تطابق تام مع `registry.yaml` (تحقق ببايثون: نفس القائمة الـ21 حرفياً).

**تصنيف الـ13 skill:**
- **Discipline spine (6):** `sofi-boot · sofi-gate · sofi-handoff · sofi-team · sofi-delegate · sofi-reflect`
- **Power tools (7):** `sofi-audit · sofi-spec-review · sofi-feature · sofi-secure · sofi-fix · sofi-report · sofi-design-taste`
- **Vendored:** صفر داخل `.claude/skills/` — المهارات السيبرانية الـ817 تعيش في `company/superpowers/cybersecurity-skills/` ومستبعدة من الـauto-context عبر `.claudeignore` (السطران الأخيران).

### 2) MAIN — `.claude` جيل OpenCode-port

**تصحيح جوهري لخريطة الأجيال:** الادعاء «agents=15 فقط» غير دقيق — `agents/` تحوي **15 مجلد غرفة** (`arc/ bck/ brd/ …`) وبداخلها **105 ملف .md** (`find -name "*.md" | wc -l` → 105). الجيل موثّق ذاتياً: `MAIN/.claude/README.md:1` = «*SOFI AI, ported from `.opencode`*» و«*105 agents · 15 rooms*»، والـcommit `4b4d9ed feat(team): port full .opencode enterprise into native .claude config` على فرع `prj/PRJ-SAKK`.

| المكوّن | العدد | ملاحظة |
|---|---|---|
| `agents/<room>/*.md` | 105 | **نحيفة**: ~5 أسطر، `name+description+model: inherit` فقط — `bck/bck-api-engineer.md` = 5 أسطر مقابل 42 سطراً لنظيره في WT |
| `model:` | `inherit` ×105 (الكل) | **لا cost-routing ولا tools frontmatter إطلاقاً** — كل وكيل يرث كامل toolset الجلسة |
| `skills/` | 107 | = 105 مرآة skill-لكل-agent + `sofi-v6-org` + `sofi-v6-gate-flow` (كل SKILL.md ~36 سطراً) |
| `commands/` | 54 | palette كاملة: `new/fix/rm` لكل غرفة + `gate-check · deploy · parallel-build · run-lifecycle · security-sweep…` |
| `tools/<room>/<role>/` | سكربتات لكل دور | طبقة ثالثة مكرّرة لكل persona |
| `engine/` | نظام تشغيل خاص به (identity/governance/agents) | مستقل عن `company/` في WT |
| `settings.json` | `allow: []` + **4 hooks فقط** (بلا `UserPromptSubmit`) | diff مع WT |
| `hooks/` | نفس الأسماء الخمسة لكن **جيل أقدم**: `grep memdb\|telemetry\|lessons_cache` → **صفر نتيجة**؛ `stop.py` يختلف بـ93 سطراً و`user_prompt_submit.py` بـ90 (غير مسلّك أصلاً في settings) | diff line counts |

### 3) `.claudeignore` في الجذرين
متطابقان في الأساس (14 سطراً: vendor/ node_modules/ *.log *.min.* dist/ build/ tests/fixtures/ docs/legacy/ storage caches .bundle *.tar.gz *.zip). **WT يضيف «درع v6 للتوكن»:** `company/superpowers/cybersecurity-skills/` + `company/brain/org/archive-v5/` — غائبان عن MAIN.

### 4) settings — تفصيل WT
- **Hooks (أسطر 41-94):** `PreToolUse` على `Bash|Read|Edit|Write` → `pre_tool_use.py` · `SessionStart` · `UserPromptSubmit` · `PostToolUse` على `Edit|Write` · `Stop` — كلها عبر `$CLAUDE_PROJECT_DIR` (portable).
- **Permissions (أسطر 3-6):** `allow: Edit(/.claude/skills/sofi-reflect/**), Edit(/.claude/skills/sofi-secure/**)` — سماح ذاتي لحلقة reflect/secure بتحديث مهاراتها دون prompt.
- **skillOverrides (أسطر 8-40):** إطفاء 31 مهارة `seo-*` (plugin residue).
- `settings.local.json` موجود في WT فقط (سماحات جلسة محلية غير حساسة).

---

## الصحة

**فحوص آلية (نواتج فعلية):**
- `bash company/os/bin/sofi doctor` → **VERDICT: PASS**: `routing ✓ 109 routes` · `registry ✓ 15 rooms · 105 agents` · `agents ✓ 105 spawnables ↔ 105 room specs (105↔105)` · `skills ✓ registry skill paths exist` · `net-roles: 41`.
  - الـ41 مقابل 21 منحة ويب **ليست تناقضاً**: `sofi_tools/registry.py:185-198` يضمّ من لديه `tools: inherit` في الـregistry (boardroom + leads يرثون toolset الجلسة) إلى الـ21 الصريحين — تعريف مقصود.
- **Dual-parity (المطلوب عينة 10 — نُفّذ كاملاً):** عينة 10 عبر الغرف (brd-ceo, mob-perf-profiler, dat-privacy-officer, bck-blade-engineer, dsn-motion-designer, str-lead…) كلها `OK` مع spec مقابل في `company/rooms/<NN>/agents/`، **ثم فحص `comm` الشامل: صفر فروقات أسماء بين الـ105 spawnable والـ105 spec**. الوجه الـspec أغنى (persona + `route:` + `success_metric` في frontmatter — `company/rooms/09-security/agents/sec-pentester.md:1-11`, 56 سطراً) والوجه الـspawnable هو الـoperating prompt — تكامل لا تكرار.
- **Hooks تعمل حياً:** `memory/sessions.jsonl` آخر سطر بتاريخ 2026-07-09 head=b6db3bb — hook الـStop يكتب فعلاً.

**ماذا يفعل كل hook فعلياً (قراءة كود):**
1. **`pre_tool_use.py` (الحارس، الوحيد الذي يحجب):** قائمة DANGEROUS regex (أسطر 21-40): rm -rf على الجذور، sudo، mkfs/dd، fork bomb، git push --force / reset --hard / clean -f / filter-branch / حذف فروع محمية. حماية `.env` قراءةً وكتابةً مع استثناء `.env.example` (أسطر 128-133، exit 2). **انضباط git عند الالتزام:** إلزام Conventional-Commit (regex سطر 48-51) وحجب staging لمسارات محرّمة `_scratch/ .env* *.pem audit.jsonl` (أسطر 53-57، 81-82). تحذير (لا حجب) على secrets ملصوقة في الكود (أسطر 151-155). كل حجب يُدوَّن في `.claude/memory/audit.jsonl` (أسطر 98-114). fail-open موثّق (سطر 11).
2. **`session_start.py`:** يحقن orientation تلقائياً: branch+HEAD + المشروع النشط (STATE head + next ticket من HANDOFFS) + palette + **memdb digest بميزانية 1000 توكن** (سطر 35) — تفعيل «no blind start».
3. **`post_tool_use.py`:** عدّاد بنطاقات THRESHOLD=12 تغييراً غير ملتزم (سطر 27) → تذكير `sofi checkpoint` مرة لكل band (لا spam، أسطر 97-105)، + `memdb.capture` و`telemetry.send_event` لكل Edit/Write (أسطر 39-46).
4. **`stop.py`:** breadcrumb لكل جلسة في `sessions.jsonl` (project/head/uncommitted/gate) + `memdb.compress_session` + **تذكير gate-evidence متدرّج بسقف 5** (`_REMINDER_CAP` سطر 33) لا يحجب أبداً (لا `decision` field).
5. **`user_prompt_submit.py` (WT فقط):** «اللقاح» — `memdb.learn_match` + `lessons_cache.vaccine_for` يعرضان درساً مطابقاً قبل العمل، والتقاط `[LEARN]` عند prompt تصحيحي (regex أسطر 29-40).

**صحة MAIN:** الطبقة تعمل (كانت LIVE على PRJ-SAKK) لكنها **جيل مجمّد**: hooks بلا ذاكرة v6.1، وuser_prompt_submit موجود لكنه غير مسلّك في settings، وكل وكلائها بلا منح أدوات وبلا routing.

---

## نقاط القوة

1. **تناظر آلي مثالي 105↔105** بين spawnable وspec، محروس بـ`sofi doctor` (PASS محقّق) وبمصدر واحد `registry.yaml` — لا drift يدوي.
2. **بنية RCCF متجانسة 100%** عبر الـ105 (5/5 أقسام في كل ملف، محقّق بـgrep) مع description «Use when…» يجعل الـauto-delegation دقيقاً.
3. **least-privilege حقيقي في الجيل v6:** منح `tools:` صريحة لكل وكيل (21 فقط يصلون للويب — يطابق registry حرفياً؛ الحارس gtw-gatekeeper read-only+Bash)، مقابل صفر تقييد في جيل MAIN.
4. **الـeconomic grid منزَّل في الملفات لا في الوثائق فقط:** haiku 15 / sonnet 72 / inherit 18 يطابق فلسفة «cheapest route that clears the bar».
5. **طبقة hooks ناضجة هندسياً:** fail-open مدروس، audit trail، تذكيرات bands غير مزعجة، سقف anti-deadlock، وحلقة ذاكرة كاملة (capture → digest → vaccine → compress) — أفضل قطعة كود في النظام.
6. **انضباط git على مستوى الـharness** لا الاتفاق فقط: حجب force-push/reset --hard وفرض Conventional Commits وحماية المسارات المحرّمة قبل وقوعها.
7. **درع التوكن:** `.claudeignore` في WT يستبعد 817 مهارة سيبرانية والأرشيف v5 من الـauto-context.

## نقاط الضعف

1. **جيلان متعايشان بنفس المسارات المنطقية:** MAIN فيه `.claude` كامل (105 agents نحيفة + 107 skills + 54 commands + tools/ + engine/ خاص) يوازي WT ويناقضه بنية وروحاً — أي دمج أعمى سيفسد الاثنين.
2. **نزيف تهيئة عبر التعشيش (config bleed) — محقّق حياً:** الجلسة الحالية تعمل داخل WT ومع ذلك المهارات المحمّلة فيها هي palette جيل MAIN (107 skills + 54 commands ظاهرة في قائمة الجلسة، بينما `sofi-boot` الـ13 في WT **غير محمّلة**) `[verified: قائمة مهارات هذه الجلسة]` — لأن الـworktree يقبع تحت `MAIN/.claude/worktrees/` `[inferred]`. النتيجة: v6 يعمل بواجهة أوامر الجيل القديم.
3. **hooks متشعّبة بين الجذرين:** نفس الأسماء، أجيال مختلفة (`stop.py` يختلف بـ93 سطراً؛ MAIN بلا memdb إطلاقاً) — مصدران للحقيقة لسلوك الجلسة حسب مكان فتحها.
4. **جيل MAIN بلا أي عزل صلاحيات:** `model: inherit` ×105 وبلا `tools:` — كل persona يحمل Bash والويب فعلياً؛ يناقض `07-security-law`.
5. **تضخّم ثلاثي في MAIN:** لكل دور agent + skill مرآة + مجلد tools (105×3 قطعة) — كلفة صيانة بلا قيمة بعد ظهور نمط الـ13 skill.
6. **WT بلا `commands/`:** الـ54 workflow (new/fix/rm/gate-check/deploy…) موجودة فقط في الجيل القديم — فجوة وظيفية إن أُطفئ MAIN.
7. ثغرات صغرى موثّقة: فحص صيغة الالتزام fail-open على الرسائل الديناميكية (`pre_tool_use.py:87-90`)؛ `lessons_cache` مستهلَك من دالة واحدة فقط (observation 7718)؛ `doctor` يعرض `projects: 0` داخل WT لأن المشاريع في جذر MAIN.

## التداخل مع الطبقات الأخرى

- **مع `company/` (v6):** التداخل صحّي ومقصود — كل spawnable يشير إلى spec في `company/rooms/` وroute في `company/nexus/routing.yaml`، والـhooks تستورد `sofi_tools` من `company/os/` (`session_start.py:32-35`). `.claude` في WT هو «واجهة الـharness» للـcompany لا نظاماً موازياً.
- **مع جيل OpenCode:** MAIN/.claude هو حرفياً «`.opencode` منقولاً» (README:1) — فالتداخل هنا وراثة كاملة: engine/ خاص به يوازي `company/` ويكرّر الدستور والregistry بصيغته.
- **مع جيل AUTOPILOT (`MAIN/engine/`):** لا استيراد مباشر وجدته من `.claude` إلى `engine/` القديم في أي من الجيلين — عزل جيد.
- **مع `orchestrator/` و`tools/` (WT):** `engine/tooling` الـ6 أدوات تعيش داخل `.claude/engine/` في WT — موقع غير معتاد (substrate تنفيذي داخل مجلد تهيئة الـharness) ويستحق نقلاً في شامل.
- **مع plugins (claude-mem/caveman):** الـhooks مصمّمة «تكاملاً لا تصادماً» (`stop.py:7-8` يصرّح أنه يكمّل claude-mem)؛ skillOverrides تدير ضجيج seo-*.

## ما يُرحَّل لنظام شامل

1. **صيغة الـspawnable RCCF كاملة** (frontmatter: name/description-with-triggers/**tools least-privilege**/model) + قاعدة «الأقسام الخمسة» — الأصل الأثمن، يُرحَّل كما هو.
2. **حزمة الـhooks الخمسة بجيل WT** (v6.1 مع memdb/vaccine/audit.jsonl/bands/caps) + نمط تسليكها في settings عبر `$CLAUDE_PROJECT_DIR` — تُرحَّل حرفياً وتصبح المصدر الوحيد (تُسقط نسخ MAIN).
3. **مبدأ dual-parity المفحوص آلياً** (spawnable ↔ spec ↔ registry.yaml واحد) مع فحص `doctor` fail-closed في CI.
4. **الـeconomic grid المنزّل في frontmatter** (توزيع haiku/sonnet/inherit) بدل inherit الشامل.
5. **نمط «13 مهارة» (spine 6 + power 7)** بدل انفجار 105-مرآة؛ مع **إنقاذ الـ54 commands من MAIN** بعد غربلة (gate-check/deploy/parallel-build قيّمة) — الشيء الوحيد الذي يستحق الترحيل من الجيل القديم.
6. **درع `.claudeignore`** بسطور v6 + `sofi.json` كmanifest يشير للمصادر لا يكرّرها.
7. **قرار معماري لشامل:** فك تعشيش الـworktrees من تحت `.claude/` (سبب النزيف رقم 2) ونقل `engine/tooling` خارج مجلد التهيئة.
8. **لا يُرحَّل:** وكلاء MAIN النحاف الـ105، الـ107 skills المرآة، `tools/<room>/<role>`، وengine/ الخاص بالـport — كلها superseded.

## الحكم

**HEALTHY** — طبقة `.claude` جيل v6 في WT سليمة ومتناظرة آلياً (doctor PASS، 105↔105، RCCF 105/105، hooks حيّة بأثر مسجّل) وهي أنضج طبقة في المنظومة؛ التحفّظ الوحيد أن جيل MAIN بجانبها LEGACY كامل (opencode-port) يسبّب نزيف palette عبر تعشيش الـworktrees ويجب إطفاؤه لا دمجه في شامل.
