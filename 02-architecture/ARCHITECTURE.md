# شامل / SHAMEL — المعمارية الموحّدة (ARCHITECTURE)

**التاريخ:** 2026-07-10 · **الحالة:** Design Record v1.0 — يقود الـ PRD والتنفيذ
**المصادر الحاكمة:** `08-COMPARISON-MATRIX.md` (G3 يفوز في 8/10 أبعاد + المكوّنات الذهبية 1–21) · `09-GAP-ANALYSIS.md` (GAP-01…20 وخيط الترابط) · `03-company-core.md` (نواة v6 HEALTHY) · `04-engines-tooling.md` (5 أجيال محرّكات، 8 نقاط دخول، 6 تطبيقات للـ concern الواحد)
**الموقع الفيزيائي للنظام:** `~/Desktop/SHAMEL/` — ريبو git مستقل من اليوم صفر.

---

## 1. المبادئ المعمارية (ملزمة — تُقاس عليها كل مراجعة معمارية)

| # | المبدأ | المعنى التنفيذي | الفجوة التي يسدّها |
|---|--------|------------------|---------------------|
| P1 | **نسخة واحدة لكل concern** | لكل هَمّ (task-state، routing، registry، memory، gate-check، git-guard) تطبيقٌ واحد ومسارٌ واحد على القرص؛ أي نسخة ثانية = defect يُرصد آلياً بـ `shamel doctor` fail-closed | GAP-06 («محرّك الانجراف»)، GAP-14، GAP-15 |
| P2 | **الكود هو الحقيقة** | كل رقم في العقل (عدد models/tests/coverage) يولَّد بسكربت عدّ، لا يُكتب يدوياً؛ FOLDER-MAP عقد مولَّد من السكافولدر | GAP-12 (الدماغ يكذب) |
| P3 | **لا ادعاء بلا إنفاذ آلي fail-closed** | كل قاعدة دستورية لها توأم آلي يفشل بصوت عالٍ (`validate_evidence`, doctor, agentlint, gate-check)؛ «مؤتمت» بلا مشغّل فعلي = ادعاء مرفوض | GAP-04، GAP-11، GAP-20 |
| P4 | **git يوم-صفر** | لا مشروع ولا نظام يوجد دقيقة واحدة بلا `.git` + remote + أول commit؛ السكافولدر ينفّذها بنفسه؛ doctor يفشل عند أي مشروع بلا VCS | GAP-01 (سابقتا فقدان متحققتان) |
| P5 | **فصل المنفّذ عن الحَكم (التحقق العدائي)** | لا self-grading أبداً: فحص ميكانيكي fail-closed أولاً، ثم gatekeeper بسياق نظيف يرى الـ deliverable + الـ exit bar الأصلي فقط؛ UNKNOWN حكم مشروع | ميراث V1–V5 من G3 (المكوّن الذهبي 1) |
| P6 | **flat topology داخل Claude Code — لا daemon** | «ledger لا daemon» (فلسفة G5): الحالة في SQLite/ملفات، تُقرأ عند الاستدعاء؛ الأتمتة الطويلة خارج الجلسة عبر `claude -p` + cron حصراً | قيد بيئة التشغيل + ميراث G5/G6 |
| P7 | **اقتصاد التوكن: Python يحدّد، النموذج يحكم** | كل ما هو حتمي (عدّ، parsing، parity، lint، state) يجري بصفر توكن؛ النموذج يُستدعى للحكم والتصميم فقط؛ درع `.claudeignore` + سلّم routing اقتصادي بطبقة alias | البعد 10 في المصفوفة (G3+G5 الفائزان) |
| P8 | **مصدر توليد واحد، والباقي مشتقات** | ملف الوكيل القانوني واحد؛ spawnable الـ `.claude/agents/` **مولَّد** آلياً منه؛ تحريره اليدوي محظور ويكسر فحص البصمات | GAP-07 (تعريفان حيّان لنفس الـ ID)، GAP-16 |
| P9 | **بروتوكول واحد شامل: RCCF** | كل تفويض — بشري→CEO، غرفة→غرفة، جلسة→subagent، pipeline→invoker — هو Work Order رباعي (Role·Context·Command·Format) بنفس الـ schema والـ ticket header | «بروتوكول واحد شامل» + المكوّن الذهبي 6 |
| P10 | **فشل صاخب، تسمية غير ملتبسة** | `paths` لا يرجع مساراً معدوماً بصمت؛ اسم واحد لكل مفهوم (يموت ثنائي `sofi`، وتُفكّ دلالات registry الثلاث)؛ worktrees لا تُعشَّش تحت `.claude/` | GAP-05، GAP-09، GAP-15 |

---

## 2. شجرة المجلدات الكاملة

```
~/Desktop/SHAMEL/                        # ريبو git مستقل (origin على remote خارجي من commit #1)
│
├── SHAMEL.md                            # الوثيقة العليا: هوية النظام + خريطة الطبقات (تقرأ في دقيقتين)
├── CLAUDE.md                            # عقد سلوك الجلسة — pointers مضغوطة، لا محتوى (few token do trick)
├── MEMORY.md                            # خريطة التوجيه «أين أجد X؟» — pointers فقط، يملكها knw-lead
├── .claudeignore                        # الدرع: archive/ + vendor + كل ما لا يخص الجلسة (~80% خفض سياق)
├── .gitignore                           # يستثني projects/ (لكل مشروع repo خاص) و .worktrees/ و *.db
│
├── .claude/                             # طبقة تكامل Claude Code (القسم 5)
│   ├── settings.json                    # hooks الخمسة + صلاحيات + allow-rules نسبية المسار
│   ├── hooks/                           # 5 hooks بنمط $CLAUDE_PROJECT_DIR (guard/orientation/bands/vaccine/breadcrumbs)
│   │   ├── pre_tool_use.py              #   حارس أمني/git — النسخة الوحيدة في الوجود
│   │   ├── session_start.py             #   حقن brain head + gate + ticket (ميزانية 1000 توكن)
│   │   ├── user_prompt_submit.py        #   اللقاح (المكوّن الذهبي 4): مطابقة LESSONS قبل العمل + التقاط إشارات [LEARN]
│   │   ├── post_tool_use.py             #   نبض checkpoint عند انجراف الشجرة
│   │   ├── stop.py                      #   breadcrumb → brain/db/sessions.jsonl
│   │   └── hook_health.py              #   موديول مشترك تستدعيه الخمسة (ليس hook event): عدّاد أعطال fail-open + إنذار في doctor — GAP-20
│   ├── agents/                          # ⚙️ مولَّد آلياً — `shamel agents build` — تحريره اليدوي defect
│   │   └── <id>.md                      #   105 spawnable مشتقة من core/rooms/*/agents/*.md
│   ├── skills/                          # 13 مهارة: spine 6 (boot/gate/handoff/team/delegate/reflect)
│   │   └── ...                          #   + power 7 (audit/spec-review/feature/secure/fix/report/design-taste)
│   └── commands/                        # الأوامر المغربلة من الـ 54 (gate-check/deploy/parallel-build…)
│
├── core/                                # ❶ نواة الحوكمة — الدستور والغرف والـ Nexus
│   ├── CONSTITUTION.md                  # القانون الأعلى: 7 Teachings + Oath + Precedence + Amendment
│   ├── constitution/
│   │   ├── 00-operating-system.md       # العقد الكوني (10 خطوات لكل turn + circuit breaker)
│   │   ├── 01-work-order.md             # RCCF — البروتوكول الواحد الشامل
│   │   ├── 02-grounding.md              # G1–G5 (يرحَّل حرفياً من v6)
│   │   ├── 03-verification.md           # V1–V5 (يرحَّل حرفياً من v6)
│   │   ├── 04-reflection.md             # موسَّعة: + مشغّل فعلي (cron + claude -p) — سدّ GAP-11
│   │   ├── 05-token-economy.md          # سلّم routing بطبقة alias
│   │   ├── 06-git-discipline.md         # + قانون يوم-صفر (P4) + worktrees خارج .claude
│   │   ├── 07-security-law.md           # CSO veto · secrets · sanitized-external-only
│   │   ├── 08-handoff-law.md            # tickets + room boundaries + sign-off
│   │   ├── 09-research-law.md           # brain→codebase→search→fetch→cite
│   │   ├── 10-lifecycle-gates.md        # البوابات التسع + two-track
│   │   └── 11-intake-orchestration.md   # 🆕 جوهر G2 المنقذ: wear-the-hierarchy، leaf-spawn one hop —
│   │                                    #    محسوماً تناقضه مع الـ skills (المادة تشرّعهما معاً بأدوار مفصولة)
│   ├── nexus/                           # المصدر الواحد الثلاثي + طبقة النماذج
│   │   ├── registry.yaml                # rooms→agents→skills→tools (الاسم «registry» محجوز لهذا حصراً)
│   │   ├── routing.yaml                 # routes.<id> = tier·effort·caveman·budget·gate — **بأسماء aliases فقط**
│   │   ├── models.yaml                  # 🆕 طبقة alias: mechanical/workhorse/gatekeeper/deep → model-id
│   │   ├── gates.yaml                   # 9 بوابات كاملة الحقول (owner·entry·artifacts·exit_bar·on_fail)
│   │   ├── pins.json                    # بصمات SHA-256 لكل ملف وكيل قانوني + كل spawnable مولَّد
│   │   └── bus/
│   │       ├── ticket-schema.md         # schema الـ ticket الملزم (regex-verifiable)
│   │       └── escalation.md            # سلّم التصعيد + circuit breaker
│   ├── rooms/                           # 15 غرفة (ADR-004: خريطة الـ 15 رسمياً)
│   │   └── <NN-code>/                   # 00-boardroom … 14-gateway
│   │       ├── CHARTER.md               # mission/members/interfaces/room-bar/escalation
│   │       ├── agents/<id>.md           # 📌 الملف القانوني الواحد لكل وكيل (القسم 3.2)
│   │       ├── playbooks/               # إجراءات الغرفة الفعلية
│   │       └── tools/                   # 🆕 ممتلئة فعلاً: الـ 114 سكربت المنتشلة من G1 موزّعة على غرفها
│   │                                    #    (endpoint-scaffold, a11y-audit, sli-calc…) — يسدّ GAP-18
│   └── gates/
│       └── checklists/gate-0..8.md      # الـ checklists التفصيلية المنتشلة من G1 (مكمّل gates.yaml)
│
├── engine/                              # ❷ الطبقة الحتمية الموحّدة (القسم 3.3)
│   ├── bin/shamel                       # الموزّع الواحد — Python خالص (يموت نمط bash→python)
│   ├── shamel_tools/                    # المكتبة الواحدة (اندماج sofi_tools×24 + substrate×6 + orchestrator)
│   │   ├── core/    paths.py taskq.py gitflow.py check.py validate.py schemas.py selftest.py
│   │   ├── nexus/   registry.py routing.py gates.py tickets.py doctor.py agentlint.py pins.py agents_build.py
│   │   ├── brain/   brain.py memdb.py lessons.py telemetry.py resume.py counts.py
│   │   ├── net/     domain.py tunnel.py oracle.py
│   │   └── pipeline/ state.py translator.py invoker.py ceo.py runner.py
│   ├── scanners/                        # feature_scan.py · code_scan.py · verify.py (نسخة واحدة — يموت التطابق البايتي)
│   └── selftest/                        # `shamel selftest --json` — PASS إلزامي في CI
│
├── brain/                               # ❸ طبقة العقل — مستوى المنظمة (القسم 3.4)
│   ├── BRAIN.md                         # معمارية الذاكرة الثلاثية: org / project / session
│   ├── org/                             # DECISIONS · LESSONS (صيغة sig) · EVOLUTION · PERSONAS · TEAM_STATUS · HANDOFFS
│   ├── db/
│   │   ├── brain.db                     # memdb SQLite+FTS5 — يُغذَّى آلياً من hooks (سدّ «صفّ واحد»)
│   │   ├── taskq.db                     # آلة الحالات الواحدة للمهام + جداول تاريخ الانتقالات (دمج state_db)
│   │   └── sessions.jsonl               # breadcrumbs الجلسات
│   └── templates/                       # STATE · CONTEXT · DECISIONS · HANDOFFS · LESSONS · FOUNDATIONS
│
├── projects/                            # ❹ طبقة المشاريع (القسم 3.5) — مستثناة من git الإطار
│   ├── README.md                        # قانون المشروع (يوم-صفر، بوابات، دماغ داخلي)
│   └── PRJ-XXXX/                        # 🔒 ريبو git مستقل بـ remote خاص — يولد بـ `shamel new`
│       ├── .git/                        #    قبل أي ملف آخر (P4)
│       ├── _context/                    #    دماغ المشروع — داخل repo المشروع، يُلتزم مع كوده
│       │   ├── STATE.md CONTEXT.md DECISIONS.md HANDOFFS.md LESSONS.md FOUNDATIONS.md
│       │   └── features/<F>/GATE0..GATE8/   # artifacts البوابات لكل feature
│       ├── _scratch/                    #    مؤقت — يُطهَّر عند خروج البوابة، لا يدخل التاريخ
│       └── <code…>                      #    المنتج نفسه
│
├── archive/                             # ❺ مقبرة الأجيال — شواهد قبور، ليست أحياء-أموات (ADR-001)
│   ├── README.md                        # ⛔ فهرس: ما دُفن، متى، أين الـ snapshot/tag، وماذا انتُشل منه
│   ├── g1-opencode/  g2-engine-v5/  g4-org-rooms/  g6-orchestrator-fork/
│   └── (كل مجلد: MANIFEST.md + tag إشاري إلى snapshot — لا node_modules ولا db حية)
│
└── .worktrees/                          # worktrees الإطار — خارج .claude/ نهائياً (سدّ GAP-05)
```

**أدوار المسارات الحاكمة بسطر:** `core/` = ماذا يجوز (قانون) · `engine/` = كيف يُنفَّذ حتمياً (صفر توكن) · `brain/` = ماذا نعرف (ذاكرة) · `projects/` = ماذا نبني (منتجات معزولة) · `.claude/` = كيف تتصل الجلسة (تكامل) · `archive/` = ماذا كنا (تاريخ مبصوم).

---

## 3. الطبقات الخمس

### 3.1 نواة الحوكمة (core/)

تُرحَّل من G3 شبه كاملة — الفائز في 8/10 أبعاد والوحيد HEALTHY (المصفوفة §2) — بأربعة تعديلات جراحية:

1. **مادة 11 جديدة (intake-orchestration):** جوهر G2 الوحيد المستحق (wear-the-hierarchy، leaf-spawn one hop) يدخل الدستور بصياغة تحسم تناقضه التاريخي مع الـ skills: *المهارات واجهة الانضباط داخل الجلسة؛ التقمّص الهرمي بروتوكول التفويض بين الوكلاء — لا يتزاحمان.*
2. **طبقة alias للنماذج (`models.yaml`):** `routing.yaml` لا يذكر model-id حرفياً بعد اليوم (سدّ GAP-17):

```yaml
# core/nexus/models.yaml — الملف الوحيد الذي يُلمس عند ترقية نماذج
aliases:
  mechanical: claude-haiku-4-5      # 🟢 80% من العمليات الروتينية
  workhorse:  claude-sonnet-5       # 🔵 الكود الواضح
  gatekeeper: inherit               # 🔮 نموذج الجلسة الحدودي — الفحص العدائي
  deep:       claude-opus-4-8       # 🟣 الملاذ الأخير حصراً
policy:
  routing_yaml_may_reference: [mechanical, workhorse, gatekeeper, deep]  # agentlint يفشل عند أي id حرفي
```

3. **البوابات بطبقتين، بلا استثناء:** ميكانيكية (`shamel gate-check` → `validate_evidence()` fail-closed: cmd+exit code | file:line | diff/SHA) ثم عدائية (`gtw-gatekeeper` بسياق نظيف ضد الـ exit bar الأصلي). درس GAP-04 يُسلَّك كوداً: بوابات 6–7 تتطلب artifacts قابلة للتشغيل (workflow موجود + rollback مُختبَر) — إعلان «CI ينشر تلقائياً» بلا workflow يفشل الفحص آلياً.
4. **الغرف مكتفية فعلاً:** `rooms/*/tools/` تمتلئ بالـ 114 سكربت المنتشلة من G1 (التسمية أصلاً على مخطط v6 — المصفوفة بند 10)، فيتحول «الاكتفاء الذاتي الاسمي» (GAP-18) إلى حقيقي. `skills/` تبقى مركزية في `.claude/skills/` **بتوثيق صريح** أن هذا تصميم لا نقص.

### 3.2 طبقة الوكلاء — توحيد الجرود الخمسة في جرد واحد

**الوضع الموروث:** 5 جرود متوازية (105 RCCF spawnable · 105 spec · 100 persona عربية · 105 stub نحيف · 68 opencode) ونفس `@agent` = سلوك مختلف حسب الفرع (GAP-07).

**القرار (ADR-003): ملفان مرتبطان — قانوني واحد مكتوب باليد + spawnable مولَّد آلياً.** الملف القانوني يدمج الجرود الثلاثة المستحقة (spec الآلي + RCCF التشغيلي + persona/حوكمة G4 البشرية) في وثيقة واحدة؛ والـ spawnable مشتق حتمي لا يُحرَّر يدوياً.

**بنية الملف القانوني** `core/rooms/<NN>/agents/<id>.md`:

```markdown
---
# ——— القسم الآلي (يقرؤه engine + registry + agents_build) ———
id: bck-api-engineer
room: 05-backend
reports_to: bck-lead
gate: 4
route: workhorse            # alias فقط — agentlint يرفض model-id حرفياً
effort: single-role
tools: [Read, Edit, Write, Bash, Grep]        # least-privilege صريح — ملف بلا tools: يفشل agentlint
web: false                                     # منح الويب الصريحة فقط (كانت 21/105 في v6)
success_metric: "كل endpoint يطابق العقد المجمّد؛ 422-JSON لا 302"
# ——— قسم الحوكمة البشرية (ميراث G4 — كان كوناً موازياً، صار frontmatter) ———
persona_name: "كريم فاروق"                     # جدول الربط ID↔persona يُنهي ازدواج الكوانين (GAP-15)
authority: {operational: implement-within-contract, financial: none, veto: none}
escalation: bck-lead
dependencies: [arc-api-architect, dat-db-engineer]
---
# Persona
(الشخصية العربية الغنية من كانون G4 — مرجع بشري، لا يُحقن في الـ spawnable)

# Operating Contract
gate · consume · produce · gate-bar · handoff · escalate

# Operating Prompt (RCCF)
🎭 Role · 📂 Context · 🎯 Command · 📐 Format
```

**التوليد والتحقق (حتمي، صفر توكن):**

```
$ shamel agents build      # يولّد .claude/agents/<id>.md من frontmatter+RCCF لكل ملف قانوني
$ shamel doctor            # parity ثلاثي: قانوني ↔ spawnable ↔ registry.yaml (105↔105↔105)
                           # + مطابقة SHA-256 مع pins.json — spawnable مُحرَّر يدوياً = FAIL
```

- الجرد D (stubs النحيفة، `model: inherit` ×105 بلا `tools:`) **يُلغى نهائياً** — يسدّ GAP-07 وGAP-10 معاً.
- كانون G1 الـ 68 (14 ملوثة CJK، موديل ميت) **يُؤرشف** بعد انتشال فكرتَي translator وper-agent permissions (المصفوفة بند 13).
- فجوات تغطية G4 (لا fnt/qa/obs) تصبح غير ذات موضوع: خريطة الغرف الرسمية 15، والـ personas تُطعَّم في الملفات القانونية الموجودة عبر جدول الربط.

### 3.3 الطبقة الحتمية — موزّع واحد يخلف نقاط الدخول الثماني

**الوضع الموروث:** 8 نقاط دخول (5 باسم `sofi`)، 6 تطبيقات متوازية لإدارة المهام وحدها، `sofi_verify.py` متطابق بايتاً بين جيلين (تقرير 04).

**القرار (ADR-002): `engine/bin/shamel` — موزّع Python واحد.** خريطة الدمج — ماذا يبقى من كل جيل:

| المصدر | ما يُرحَّل | ما يموت |
|--------|------------|----------|
| **bash `sofi` v6 (G-C)** — 24 موديول / 32 أمراً | **المكتبة كاملة** تصبح نواة `shamel_tools/` (brain·tickets·routing·gates·guard·gitops·domain·tunnel·oracle·memdb·agentlint·telemetry·resume·budget·doctor) + سطح الـ CLI | غلاف bash (`bin/sofi` bash→python)، بقايا tiers/autopilot/ooda داخل `os/agents/`، الازدواج البايتي مع G2 |
| **substrate Python (G-D)** — 6 أدوات PASS | **`taskq.py` يصبح آلة الحالات الواحدة** (pending→assigned→running→completed/failed) خالفةً التطبيقات الستة · `gitflow.py` (منع force/reset) · `check.py` (lint/test runners) · `validate.py` · فلسفة «ledger لا daemon» · نمط `selftest --json` | `registry.py` يُعاد تسميته `schemas.py` (فكّ تصادم الدلالات الثلاث — GAP-15) · `gateway.py` يندمج في `pipeline/translator.py` (كان ينافسه بلا عقد مشترك) |
| **orchestrator خارجي (G-E)** — بعد دمج الـ fork | يصبح `shamel_tools/pipeline/`: `translator.py` (نسخة MAIN الأغنى 455 سطراً) · `invoker.py` (`claude -p` بوضع MOCK/live) · `ceo.py` (`ceo_agent.py` المنقذ من MAIN) · `state.py` (نسخة WT 356 سطراً — جداول التاريخ تندمج **داخل `taskq.db`** كجدول transitions، لا db ثانية) · الأدوات الـ 22 موحَّدة الرموز | رموز الغرف العشرية الخاصة (`bkd_05/uxr_02`) — **الـ pipeline يقرأ `core/nexus/*.yaml` حصراً**، `main.py`×2 والـ fork يُطويان |
| **G-A engine/ v5 + G-B .opencode** | الماسحات (نسخة v6 المتفرّعة الأحدث) → `engine/scanners/` · الـ 114 سكربت → `core/rooms/*/tools/` · browser-eyes (بعد نزع الاعتمادات المضمّنة — GAP-13) | كل الباقي → `archive/` |

**سطح الأوامر الموحّد:**

```
shamel <domain> <verb>
  doctor | selftest              # صحة النظام (fail-closed في CI — يفشل عند أي concern مزدوج)
  agents build|lint|pins         # توليد spawnables + least-privilege lint + بصمات
  new PRJ-XXXX "title"           # سكافولدر: git init + remote + commit#1 + _context/ + domain register
  sync|checkpoint|claim|release  # حلقة git الدستورية (داخل repo المشروع — paths فشل صاخب)
  brain query|recall|counts      # العقل: FTS5 + الأرقام المولَّدة (P2)
  route|dispatch|escalate        # الاقتصاد + الـ bus
  gate check|advance|tag         # الطبقتان: ميكانيكي fail-closed ثم gatekeeper عدائي
  pipeline plan|run|resume       # المحرك الخارجي (يعمل بـ claude -p خارج الجلسة، MOCK/live)
  oracle review|capture|status   # مكتب المراجعة الخارجية (+ fallback API، exit≠0 عند الفشل — GAP-11)
  domain|tunnel up|down          # التعريض المحلي/المؤقت
  reflect run                    # حلقة الأحلام — يستدعيها cron (القسم 5)
```

### 3.4 طبقة العقل (brain/)

ثلاث طبقات ذاكرة بمسؤول واحد لكل طبقة، وقاعدة «routing ≠ behavior» محفوظة:

| الطبقة | الموطن | الكاتب | آلية الإنفاذ |
|--------|--------|--------|---------------|
| **Org** | `brain/org/` (DECISIONS·LESSONS·EVOLUTION·PERSONAS·TEAM_STATUS) | `knw-*` + ADRs بقرار CEO | LESSONS بصيغة sig (`LES-001 · sig: blind-start-amnesia`) — idempotent، تُحقن كلقاح عبر hook الـ UserPromptSubmit |
| **Project** | `projects/<PRJ>/_context/` — **داخل repo المشروع** | الوكلاء عبر العقد الكوني | `shamel checkpoint` يلتزم الدماغ مع الكود في نفس الـ repo (سدّ العيب القاتل لـ G3 — GAP-01/09) |
| **Session** | `brain/db/` (brain.db FTS5 · sessions.jsonl) | hooks آلياً | PostToolUse/Stop يكتبان observations — memdb لا يعود «بصفّ واحد» (GAP-11) |

قواعد ملزمة: **MEMORY.md pointers فقط** · **«تذكّر» هي trigger الكتابة العقائدية الوحيد** · **كل أرقام العقل مولَّدة** (`shamel brain counts` يعدّ models/controllers/tests من الكود — P2) · حلقة reflection **مجدولة فعلياً** لا ورقياً (القسم 5) · تعارض STATE↔CONTEXT↔code يرفعه doctor كـ defect (خرق G5 يُرصد آلياً).

### 3.5 طبقة المشاريع (projects/)

- **قانون يوم-صفر (P4):** `shamel new PRJ-XXXX` ينفّذ بالترتيب الذرّي: `git init` → إنشاء remote → scaffold `_context/` من `brain/templates/` → commit#1 → `shamel domain register` — لا مشروع بلا VCS ولو لدقيقة (سابقتا xo-game وheart-clinic).
- **العزل:** كل `PRJ-XXXX/` ريبو مستقل؛ إطار SHAMEL يتجاهله في git لكنه يفحصه في doctor: مشروع بلا `.git` أو بلا remote أو بـ `_context/` غير ملتزم = **FAIL** لا تحذير.
- **البوابات مجسَّدة:** `_context/features/<F>/GATE0..GATE8/` — كل بوابة artifacts فعلية يفحصها `gate check` (نمط PRJ-SAKK الناجح: 19 artifact حياً).
- **حلّ المسارات:** `shamel_tools/core/paths.py` يحلّ `projects_dir()` بترتيب صريح (env `SHAMEL_PROJECTS_DIR` → `~/Desktop/SHAMEL/projects/`) ويرمي استثناء صاخباً عند الغياب — لا مسار معدوم بصمت، ولا عمى worktrees (GAP-09).
- `_scratch/` داخل المشروع للمؤقتات؛ يُطهَّر عند خروج البوابة ولا يدخل التاريخ.

---

## 4. تدفّق البيانات end-to-end

```
 أمر بشري (جلسة Claude Code في ~/Desktop/SHAMEL أو داخل PRJ)
   │
   ▼
[SessionStart hook] حقن الاتجاه: STATE head + gate + الـ ticket التالي   (≤1000 توكن)
[UserPromptSubmit hook] اللقاح لكل prompt: مطابقة LESSONS ذات الصلة + التقاط إشارات [LEARN]
   │
   ▼
❶ Gateway/Intake  — `pipeline/translator.py` (دلالي) + `gtw-dispatcher` (حوكمي)
   • النية → غرفة/وكيل عبر core/nexus/registry.yaml (رموز v6 الموحّدة — لا كون موازٍ)
   • gtw-router يبصم المسار من routing.yaml + models.yaml (aliases)
   ▼
❷ Work Order RCCF (المادة 01 — البروتوكول الواحد)
   • frozen brief: Role·Context·Command·Format + effort class + call budget + fail-safe stop
   • لا يكتمل الرباعي بمحدّدات؟ → clarify، لا spawn غامض
   ▼
❸ Ticket  — `shamel dispatch` يسجّل في taskq.db — **المرجع الأوحد لحالة المهام (P1)**؛ سطر الـ ticket في
   HANDOFFS.md **إسقاط مولَّد** منه يكتبه dispatch نفسه (git-native، regex-verifiable — لا يُحرَّر يدوياً)؛
   تباعُد الاثنين يرصده فحص parity «taskq↔HANDOFFS» fail-closed مسمّى داخل `shamel doctor` (P3)
   ▼
❹ Agents  — spawn subagent(s) من .claude/agents/ المولَّدة (least-privilege فعلي)
   • عزل الغرف: specialist → Lead → Lead الغرفة الهدف → specialist (نقل حرفي)
   • incomplete upstream → reject upward · فوق الصلاحية → escalate (لا تخمين)
   • أدوات الغرفة (rooms/*/tools) والماسحات تعمل بصفر توكن — النموذج يحكم فقط (P7)
   ▼
❺ Evidence block  — done بلا دليل = غير موجود: cmd+exit code | file:line | diff/SHA
   ▼
❻ Gates (طبقتان، بلا تخطٍّ)
   a. `shamel gate check` — validate_evidence() fail-closed + artifacts قابلة للتشغيل
   b. gtw-gatekeeper — سياق نظيف، exit bar الأصلي، pass^k للمال/auth/PII، UNKNOWN مشروع
   • فشل ×3 → circuit breaker: crash-dump JSON + تصعيد (specialist→lead→conflict-resolver→arbiter→CEO)
   ▼
❼ Checkpoint  — `shamel checkpoint` داخل repo المشروع (كود + _context معاً) + trailer SHAMEL: PRJ·TKT·gate·agent
   ▼
❽ Memory  — STATE (head_sha مولَّد) → CONTEXT append → DECISIONS إن لا-رجعة → ticket التالي عبر `shamel dispatch` (❸: taskq.db أولاً، سطر HANDOFFS إسقاطه)
   • [PostToolUse/Stop hooks] → observations إلى brain.db + breadcrumb
   ▼
❾ الحلقات الراجعة (خارج الجلسة — flat topology)
   • cron → `claude -p "/reflect"` → LESSONS جديدة بصيغة sig → لقاح الجلسة التالية (❶)
   • `shamel oracle review` → Gemini desk (sanitize→condense→capture→ingest) → ينصح ولا يقرّر البوابات
   • Gate 8: SLO breach → إعادة فتح Gate 1 رسمياً — الدورة تلتف
```

كل سهم في المخطط له إنفاذ آلي (P3): الحقن hook، الـ ticket regex + parity «taskq↔HANDOFFS» في doctor، الدليل `validate_evidence`، البوابة gate-check، الالتزام gitflow، الذاكرة memdb — لا خطوة تعتمد على «حسن النية».

---

## 5. نقاط التكامل مع Claude Code

القيد الحاكم: **flat topology داخل الجلسة — لا daemon داخلي؛ الأتمتة الخارجية عبر `claude -p` + cron حصراً (P6).**

| نقطة التكامل | الآلية | الدور في شامل |
|---------------|--------|----------------|
| **Hooks** (`.claude/settings.json` → `.claude/hooks/`) | 5 أحداث: PreToolUse / SessionStart / UserPromptSubmit / PostToolUse / Stop | الحارس (يحجب force/reset/.env/صيغ commit فاسدة) · حقن الاتجاه · اللقاح (مطابقة LESSONS + التقاط [LEARN] لكل prompt) · نبض checkpoint · breadcrumbs. **نسخة واحدة في الوجود** (نهاية ازدواج MAIN/WT — GAP-08)؛ fail-open يبقى لكن مع موديول `hook_health.py` (ليس حدثاً سادساً) عدّاد أعطال يظهر في doctor (GAP-20) |
| **Skills** (`.claude/skills/` — 13) | spine 6: boot/gate/handoff/team/delegate/reflect · power 7: audit/spec-review/feature/secure/fix/report/design-taste | واجهة الانضباط داخل الجلسة؛ المادة 11 تحسم شرعيتها دستورياً؛ palette واحدة لأن worktrees لم تعد تحت `.claude/` (GAP-05) |
| **Subagents** (`.claude/agents/` — 105) | مولَّدة بـ `shamel agents build`، مبصومة في pins.json | التفويض بالـ RCCF؛ least-privilege في `tools:` frontmatter؛ doctor يكسر أي تحرير يدوي (P8) |
| **Commands** (`.claude/commands/`) | المغربل من الـ 54 (gate-check/deploy/parallel-build…) | اختصارات تشغيلية فوق `shamel` — لا منطق فيها، توجيه فقط |
| **الأتمتة الخارجية** | `cron` → `claude -p` | ① reflection ليلي: `claude -p "/reflect" --cwd ~/Desktop/SHAMEL` (أول مشغّل فعلي للمادة 04 — GAP-11) ② `shamel pipeline run` للدورات الطويلة (invoker بـ `claude -p`، MOCK للاختبار بلا API) ③ `shamel doctor --ci` أسبوعياً |
| **CI (GitHub Actions)** | على repo الإطار وكل repo مشروع | `shamel doctor` + `selftest` + `agents lint` fail-closed — أي ازدواج concern أو spawnable منحرف أو مشروع بلا VCS يفشل البناء |

مثال تسجيل الجدولة (خارج الجلسة، بلا daemon):

```cron
# reflection ليلي + صحة أسبوعية
15 3 * * *  cd ~/Desktop/SHAMEL && claude -p "/reflect" >> brain/db/reflect.log 2>&1
0  6 * * 1  cd ~/Desktop/SHAMEL && engine/bin/shamel doctor --ci || notify "SHAMEL doctor FAIL"
```

---

## 6. القرارات المعمارية (ADRs)

### ADR-001 — مصير الأجيال الستة: انتشال → دفن مبصوم → شامل
- **الحالة:** مقبول · **السياق:** 6 أجيال متعايشة، 8 نقاط دخول، أصول ذهبية untracked مهددة بالضياع الفوري (GAP-01/03)، وطبقات ميتة تلوّث كل grep (GAP-14).
- **القرار:** الترتيب ملزم — *الإنقاذ لا ينتظر أحداً*: (أ) **انتشال فوري قبل أي تنظيف:** الـ 114 سكربت + browser-eyes + gate checklists من G1؛ `ceo_agent.py` + `translator_gateway` (455) + `orchestrator.db` من fork MAIN؛ الـ stash يبقى حتى اكتمال المصالحة. (ب) **مصير كل جيل:** G1 OpenCode → `archive/g1-opencode/` بعد الانتشال (حذف node_modules 63M + memory الفارغة) · G2 engine/ v5 → `archive/g2-engine-v5/` بعد التقاط intake-orchestration (→ المادة 11) والماسحات · G3 v6 → **يُرحَّل شبه كامل** — هو العمود الفقري (core/ + معظم shamel_tools) · G4 org-rooms → حوكمته السداسية + الكانون العربي يُدمجان في frontmatter الملفات القانونية عبر جدول ربط، والأصل → `archive/g4-org-rooms/` · G5 substrate → **يُرحَّل كاملاً** نواةً لـ `shamel_tools/core/` · G6 orchestrator → نسخة موحّدة من الـ fork-ين → `shamel_tools/pipeline/` والـ fork يُطوى. (ج) كل دفن = MANIFEST + git tag إشاري — شاهد قبر، لا أحياء-أموات؛ dashboard/index.html v5 تُدفن ويُعاد بناء المراقبة على معطيات شامل.
- **العواقب:** لا كود فريد خارج git؛ grep نظيف؛ ثمن لمرة واحدة: جدول ربط ID↔persona ودمج fork يدويان.

### ADR-002 — موزّع حتمي واحد: `shamel` (Python) يخلف نقاط الدخول الثماني
- **الحالة:** مقبول · **السياق:** 5 تنفيذيات باسم `sofi` («PATH order silently decides»)، 6 تطبيقات لإدارة المهام، ازدواج بايتي بين أجيال (GAP-06/15).
- **القرار:** نقطة دخول واحدة `engine/bin/shamel` (Python خالص — يموت نمط bash→python المزدوج)؛ مكتبة واحدة `shamel_tools/` بأربعة أحياء (core/nexus/brain/net) + `pipeline/`؛ **`taskq.py` آلة الحالات الوحيدة** وجداول تاريخ G6 تندمج فيها؛ `registry.py` substrate يُسمّى `schemas.py`؛ الـ pipeline الخارجي يقرأ `core/nexus/*.yaml` حصراً (نهاية رموز الغرف الموازية). `shamel doctor` يفشل عند أي concern بتطبيقين.
- **العواقب:** إصلاح واحد يصل الجميع؛ اسم واحد لكل مفهوم؛ ثمن: إعادة كتابة imports وترحيل بيانات db القديمة مرة واحدة.

### ADR-003 — جرد وكلاء واحد: ملف قانوني مكتوب + spawnable مولَّد (لا تحرير يدوي)
- **الحالة:** مقبول · **السياق:** 5 جرود، تعريفان حيّان لنفس الـ 105 IDs بسلوك وصلاحيات مختلفة حسب الفرع (GAP-07)، وجيل بلا least-privilege إطلاقاً (GAP-10).
- **القرار:** المصدر الوحيد `core/rooms/<NN>/agents/<id>.md` (frontmatter آلي + حوكمة G4 البشرية + persona + RCCF)؛ `.claude/agents/` **مشتق حتمي** بـ `shamel agents build`؛ `agentlint` fail-closed يرفض: ملفاً بلا `tools:` صريحة، model-id حرفياً، spawnable لا يطابق بصمته في pins.json. جرد D يُلغى؛ كانونا G1/G4 يُؤرشفان بعد الدمج.
- **العواقب:** `@agent` واحد = سلوك واحد أينما استُدعي؛ persona غنية بلا تكلفة حقن (لا تدخل الـ spawnable)؛ ثمن: خطوة build إلزامية بعد أي تعديل وكيل (يفرضها hook + CI).

### ADR-004 — شامل ريبو مستقل على سطح المكتب؛ 15 غرفة؛ worktrees خارج `.claude/`؛ دماغ المشروع داخل repo المشروع
- **الحالة:** مقبول · **السياق:** ثلاث سلالات git متباعدة وشجرة جذر منزوعة (GAP-02)؛ نزيف palette بسبب تعشيش worktrees تحت `.claude/` (GAP-05)؛ المشروع الحي ودماغه خارج أي VCS (GAP-01/09)؛ تردد 10-vs-15 غرفة (GAP-16).
- **القرار:** `~/Desktop/SHAMEL/` ريبو جديد نظيف — **قطيعة سلالية**: يُبنى بالانتشال المبصوم من الأجيال (ADR-001) لا بوراثة تاريخ Lorka المتشظي (Lorka يبقى أرشيفاً مرجعياً)؛ خريطة الغرف الرسمية **15** (الأكمل تغطية)؛ worktrees في `.worktrees/` بجذر الريبو؛ كل مشروع ريبو مستقل بقانون يوم-صفر و`_context/` يُلتزم مع كوده؛ `paths.py` فشل صاخب.
- **العواقب:** جلسة واحدة = دستور واحد = palette واحدة (نهاية «الانفصام بحسب مجلد الإقلاع» — GAP-08)؛ حلقة sync→checkpoint→handoff قابلة للتنفيذ فعلاً؛ ثمن: هجرة PRJ-SAKK إلى repo خاص (وهي أصلاً البند الإسعافي الأول).

### ADR-005 — عقيدة الإنفاذ: لا ادعاء بلا آلية fail-closed، والحُرّاس يبلّغون عن أنفسهم
- **الحالة:** مقبول · **السياق:** Gate 6 معلنة فوق نشر معدوم (GAP-04)؛ «scheduled reflection» بلا مجدول وoracle يرجع exit 0 عند الفشل (GAP-11)؛ دماغ يناقض الكود (GAP-12)؛ hooks fail-open صامتة (GAP-20).
- **القرار:** كل ادعاء نظامي يحمل بند إنفاذ مسمّى: تقدّم البوابة = `validate_evidence()` fail-closed + gatekeeper عدائي + artifacts قابلة للتشغيل · reflection = cron فعلي بـ `claude -p` · oracle = fallback API + `exit≠0` عند الفشل · أرقام العقل = مولَّدة بـ `shamel brain counts` (الكود هو الحقيقة) · hooks تبقى fail-open (لا تعطّل الجلسة) لكن بعدّاد أعطال يظهر في doctor — *رصد بلا حجب* · doctor+selftest+agentlint بوابة CI على كل repo.
- **العواقب:** «الأتمتة الورقية» مستحيلة بنيوياً؛ الثقة بالبوابات تعود لأنها تقيس واقعاً قابلاً للتشغيل؛ ثمن: صرامة تُبطئ الإعلانات المتفائلة — وهذا مقصود.

---

*هذه الوثيقة هي الـ Design Record الأعلى لشامل؛ تعديلها حصراً بـ ADR جديد يُلحق بالقسم 6 — لا تحرير صامت (Amendment ميراث G3).*
