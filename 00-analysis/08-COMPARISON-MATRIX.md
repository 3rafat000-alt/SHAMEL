# شامل / SHAMEL — تقرير 08: مصفوفة المقارنة الكبرى بين أجيال النظام

**التاريخ:** 2026-07-10 · **المحلّل:** وكيل التركيب (SHAMEL synthesis) · **الوضع:** تركيب فوق تقارير خام، لا فحص جديد
**المصادر:** التقارير 01–07 في `_scratch/shamel/` + تقريرا الصحة المنشوران `sofi-health.html` (H1) و`sofi-opencode-health.html` (H2). كل خلية تُسند بمصدرها بين قوسين: (01)…(07)، (H1)، (H2).

---

## 0) تعريف الأجيال الستة + تصحيحات على خريطة المهمة

| # | الجيل | المسار الفعلي | الهوية | تصحيح مسنود |
|---|-------|----------------|--------|--------------|
| G1 | **OpenCode** | `MAIN/.opencode/` | 68 وكيلاً في 10 غرف مرقّمة + translator، مشغّل OpenCode مهجور | untracked كلياً — `git ls-files .opencode` = 0 (02) |
| G2 | **Engine القديم (v5 AUTOPILOT)** | `MAIN/engine/` | **تصحيح: 30 وكيلاً في 5 tiers، لا «15 agents»** — `engine/AUTOPILOT.md:3` «30-agent dev org» (04) | legacy معلَن ذاتياً (`engine/README.md:1-3`) (04) |
| G3 | **v6 Company of Rooms** | `WT/company/` + `WT/.claude/` | 105 وكيلاً / 15 غرفة / Nexus / دستور 11 مادة | `sofi doctor` = PASS (03، H1) |
| G4 | **org-rooms** | `WT/org-rooms/` | 100 persona عربية-سورية في 10 ملفات غرف (2217 سطراً) | توثيق HR صرف — لا ذراع تنفيذية (05) |
| G5 | **الطبقة الحتمية (substrate)** | `WT/.claude/engine/tooling/` | 6 أدوات Python حتمية + موزّع `sofi` بفلسفة «ledger لا daemon» | `selftest --json` = PASS 6/6 (04) |
| G6 | **الإطار الخارجي (Option C)** | `WT/orchestrator/ + tools/` (+fork في MAIN) | pipeline حتمي خارج الجلسة، يستدعي `claude -p` فعلياً | fork مزدوج نشط MAIN↔WT في نفس اليوم (04) |

**تصحيح إضافي موروث:** الادعاء «MAIN/.claude/agents = 15» خاطئ — هي 105 ملفات داخل 15 مجلد غرفة (stubs من 6 أسطر، جيل port منفصل عن G3) (01، 05، 07).

---

## 1) المصفوفة الكبرى — 10 أبعاد × 6 أجيال

### البعد 1: الوكلاء والتنظيم

| الجيل | التقييم | الدليل |
|---|---|---|
| G1 OpenCode | ضعيف/مهجور — 68 وكيلاً بـ10 غرف مرقّمة، موديل ميت واحد `opencode/big-pickle` للجميع، 14/68 ملوّثة بمحارف CJK؛ personas عربية غنية أسلوبياً | (02) (05) (H2: «roster clean but incomplete، تنقصه 5 غرف») |
| G2 Engine v5 | متجاوَز — 30 وكيلاً بتنظيم طبقات (tier-0…4) لا غرف؛ بنية tiers تسرّبت حتى إلى `company/os/agents/` | (04) |
| G3 v6 | **الأنضج** — 105↔105↔105 (spawnable↔spec↔registry) مثبتة آلياً بـ`sofi doctor`، RCCF 105/105، least-privilege فعلي (21 وكيلاً فقط بالويب)، اقتصاد نماذج منزَّل بالملفات (haiku15/sonnet72/inherit18) | (01) (03) (05) (H1: Slice A HEALTHY) |
| G4 org-rooms | غني بشرياً، مقطوع آلياً — 100 persona بقالب سداسي + حوكمة صلاحيات per-person لا نظير لها؛ لكن صفر ربط ID↔spawnable، وفجوات fnt/qa/obs/boardroom + تصادم GTW الدلالي | (05) |
| G5 substrate | لا وكلاء — `registry.py` هنا SSoT مخططات DB (تصادم تسمية مع سجلّ الوكلاء) | (04) |
| G6 orchestrator | يستدعي وكلاء فعلياً (`agent_invoker` عبر `claude -p` بوضع MOCK/live) لكن برموز غرف قديمة (10 غرف `uxr_02/bkd_05`) تخالف v6 الرسمي | (04) |

### البعد 2: الذاكرة / الدماغ

| الجيل | التقييم | الدليل |
|---|---|---|
| G1 | ميتة — `memory/` أربعة ملفات jsonl كلها 0 بايت («bash engine never ran») | (02) (07) (H2) |
| G2 | مجمّدة — ملفات HANDOFFS/PERSONAS في `engine/` نُسخت بايت-بايت إلى `company/brain/org` ثم تجمّد الأصل | (07) |
| G3 | **الأفضل تصميماً** — BRAIN.md بثلاث طبقات (org/project/session)، org brain مأهول (LESSONS فعلية بصيغة sig)، memdb/brain.db بـFTS5 (وليد: صف واحد)، قوالب 6؛ **العيب القاتل خارجه:** دماغ المشروع الحي PRJ-SAKK خارج أي git | (03) (07) (06) |
| G4 | لا ذاكرة — وثائق ثابتة | (05) |
| G5 | ذاكرة حالة لا معرفة — `taskq.py` SQLite بآلة حالات صارمة (ledger) | (04) |
| G6 | ذاكرة pipeline — `state_db.py` SQLite (تاريخ انتقالات)؛ متشظية بين fork-ين (240 مقابل 356 سطراً) و`orchestrator.db` حي untracked في MAIN | (04) |

### البعد 3: الأوركسترا والتوجيه

| الجيل | التقييم | الدليل |
|---|---|---|
| G1 | bash suite كامل (`sofi-engine`: task-queue/brain-state-machine/rccf-builder/translator) معلَن legacy ذاتياً؛ فكرة translator الدلالية قيّمة | (02) (04) |
| G2 | `bin/sofi` bash→sofi_tools (13 موديلاً) يعمل حتى الآن؛ dashboard v5 يقرأ عالماً منقرضاً (30 وكيلاً) | (04) |
| G3 | **الأنضج** — Nexus ثلاثي المصدر الواحد: `routing.yaml` (109 routes، 4 نماذج، effort_scaling)، `registry.yaml` (15×105)، escalation chain + Room Isolation؛ CLI بـ32 subcommand | (03) |
| G4 | لا شيء آلي — اعتماديات بينية موصوفة نصياً فقط (قسم الاعتماديات في كل persona) | (05) |
| G5 | `gateway.py` (semantic gateway) — جزء من الست، PASS؛ لكن يتنافس مفهومياً مع translator_gateway الخارجي بلا عقد مشترك | (04) |
| G6 | pipeline حتمي كامل خارج الجلسة يصل COMPLETED و`--live` مُثبت؛ **لا يقرأ nexus إطلاقاً** — بنى عالمه الخاص فخرق «routing.yaml the ONLY source» | (04) (H1: Slice D WORKS·PARALLEL) |

### البعد 4: الأدوات الحتمية

| الجيل | التقييم | الدليل |
|---|---|---|
| G1 | **الكنز المحتوائي** — 114 سكربت bash تنفيذي per-agent بالتسمية الجديدة أصلاً (endpoint-scaffold، a11y-audit، sli-calc…)، 104/105 pass syntax؛ **موجودة فقط خارج git** | (02) (H2: tools HEALTHY) |
| G2 | scanners ناضجة (`feature_scan.py`, `sofi_scan.py`, `sofi_verify.py`) — لكنها الآن مزدوجة (نسخة متطابقة بايتاً داخل company/os) | (04) |
| G3 | `sofi_tools` 24 موديلاً / 5758 سطراً (memdb, agentlint, telemetry, resume, budget…) — الأغنى وظيفياً؛ doctor PASS | (03) (04) |
| G4 | صفر أدوات | (05) |
| G5 | **الأنقى حتمياً** — 6 أدوات (registry/taskq/validate/gateway/check/gitflow) selftest PASS 6/6، فلسفة معلنة «NO always-on daemon» | (04) (H1: 28/28 green) |
| G6 | 22 أداة (`class Tool`) 22/22 خضراء + tool_runner/room_manager؛ لكن بنيتان متفرعتان (ملفات مفردة في WT، حِزم في MAIN) | (04) (H1) |

### البعد 5: البوابات / دورة الحياة

| الجيل | التقييم | الدليل |
|---|---|---|
| G1 | 9 gate checklists تفصيلية (`gate-0..8.md`) + `lifecycle/gates.yaml` — مادة مكمّلة قيّمة | (02) |
| G2 | `sofi_tools/gates.py` + `sofi_verify.py` — بذرة الفكرة | (04) |
| G3 | **الأكمل** — `gates.yaml` 9 بوابات كاملة الحقول (owner/entry/artifacts/exit_bar/on_fail) + accountability + two-track + طبقتا فحص (ميكانيكي `validate_evidence` fail-closed + adversarial عبر gtw-gatekeeper)؛ التجسيد العملي: 19 artifact بوابات GATE0→GATE8 في PRJ-SAKK | (03) (06) |
| G4 | لا بوابات | (05) |
| G5 | `check.py` (lint/test runners) — عضلة إنفاذ ميكانيكية للبوابات، لا نموذج بوابات ذاته | (04) |
| G6 | انتقالات TaskState ضمنية فقط — لا مفهوم بوابات صريح | (04) |

### البعد 6: الأتمتة

| الجيل | التقييم | الدليل |
|---|---|---|
| G1 | hooks bash (84 سطراً) لم تعمل قط — telemetry sinks كلها 0 بايت | (02) (H2) |
| G2 | hooks MAIN القديمة (4 أحداث، بلا memdb)؛ `session_start` في MAIN لا يزال يوجّه الجلسات لهذا الجيل الميت | (01) (04) (07) |
| G3 | **الأنضج** — 5 hooks v6.1 (حارس أمني/git يحجب فعلياً، حقن orientation بميزانية 1000 توكن، bands، لقاح الدروس، breadcrumbs مثبتة تشغيلياً)؛ الثغرة: reflection «scheduled» بلا مجدوِل — crontab فارغ، لا LESSONS.md لأي مشروع | (01) (07) |
| G4 | لا أتمتة | (05) |
| G5 | لا hooks — يُستدعى عند الحاجة (بالتصميم: ledger لا daemon) | (04) |
| G6 | أتمتة خارج الجلسة كاملة — pipeline يجري حتى COMPLETED بوضع live حقيقي | (04) (H1) |

### البعد 7: الحوكمة / الدستور

| الجيل | التقييم | الدليل |
|---|---|---|
| G1 | ثلاثة سجلات تنظيمية متناقضة داخل الطبقة نفسها (105/15 مقابل 70/10 مقابل 67 فعلي) | (02) |
| G2 | DOCTRINE 6 تعاليم + 21 بروتوكولاً؛ **تناقض عقائدي مباشر مع v6**: يشرّع «no slash-commands» بينما v6 يبني الانضباط على 13 skill؛ فيه جوهر فريد (intake-orchestration: wear-the-hierarchy) | (07) |
| G3 | **الأقوى في كل الأجيال** — دستور 11 مادة، المادتان 02 (G1–G5) و03 (V1–V5) قانون مُسلَّك كوداً لا وعظ (`validate_evidence` fail-closed، فصل المنفّذ عن الحَكم)، هرم Precedence + Amendment بقرار ADR | (03) |
| G4 | فريد في بعده — حوكمة صلاحيات **بشرية** per-person (سلطة تشغيلية/مالية/فيتو/تصعيد/اعتماديات) لا نظير لها في أي جيل آخر | (05) |
| G5 | حوكمة ضمنية بالكود (gitflow يمنع force/reset)؛ غير موثّق في عقيدة v6 — «parallel, undocumented substrate» | (04) (H1: MEDIUM) |
| G6 | خارج الحوكمة — لا يستهلك registry/routing/gates الرسمية؛ رموز غرف خاصة | (04) |

### البعد 8: التوثيق

| الجيل | التقييم | الدليل |
|---|---|---|
| G1 | README-ات ⛔ legacy صادقة (توثيق خروج نموذجي) لكن السجلات الداخلية متضاربة | (02) |
| G2 | AUTOPILOT/ROSTER/ROOMS-REFERENCE — جدول هجرة old→canonical كامل يسهّل الترحيل؛ README الـlegacy نفسه untracked | (04) |
| G3 | **الأشمل** — ORG (254) / RUNBOOK (135) / BLUEPRINT (351) / PATTERNS (159) حيّة + CHARTERs غنية غير مستنسخة (interfaces/room-bar/escalation)؛ عيب: يتطور أسرع من توثيقه (أدوات غير مذكورة في CLAUDE.md) | (03) |
| G4 | 2217 سطراً من أغنى توثيق بشري؛ تفاوت قالب (3 غرف مفصّلة ~350 سطراً، 7 مضغوطة ~164) | (05) |
| G5 | docstrings فلسفية جيدة داخل الكود؛ لا توثيق خارجي — طبقة موازية غير معلنة في v6 | (04) (H1) |
| G6 | `ORCHESTRATOR.md` يعلن الحدود صراحة (خارجي/داخلي Option C) — أول جيل يرسمها كتابةً | (04) |

### البعد 9: النضج التشغيلي (يعمل الآن؟)

| الجيل | التقييم | الدليل |
|---|---|---|
| G1 | **لا يعمل** — 100% dangling refs (61/61 عيّنة) بين 54 أمراً والوكلاء؛ untracked؛ PIDs ميتة | (02) (H2: DEGRADED·half-migrated) |
| G2 | يعمل تقنياً (usage بـ24 أمراً) لكنه legacy معلَن؛ dashboard الحي يعرض عالم 30 وكيلاً المنقرض | (04) |
| G3 | **HEALTHY — يعمل الآن**: doctor PASS (109 routes، 105↔105)، hooks حية بأثر مسجّل، 0 ملف تهيئة غير صالح؛ التحفّظ: عمى `paths.py` عن `projects/` من الـworktree | (01) (03) (H1: HEALTHY) (06) |
| G4 | لا «يعمل» أصلاً — طبقة توثيق معلّقة بلا ذراع | (05) |
| G5 | **يعمل — PASS 6/6** selftest | (04) (H1) |
| G6 | يعمل (COMPLETED + --live مثبت) لكنه **منقسم**: fork MAIN untracked بقاعدة بيانات حية و`ceo_agent.py` مهدد بالضياع | (04) (H1: WORKS·PARALLEL) |

### البعد 10: تكلفة التوكن

| الجيل | التقييم | الدليل |
|---|---|---|
| G1 | عبء صِرف — 69M (منها 63M node_modules) تلوّث أي grep/تدقيق؛ لا يُحمَّل في السياق لكنه ضجيج قرصي | (02) |
| G2 | خطِر سياقياً — `session_start` في MAIN يحقن توجيهات الجيل الميت في كل جلسة تُفتح هناك | (04) (07) |
| G3 | **الأكفأ** — `.claudeignore` درع (يستبعد 817 مهارة سيبرانية + archive-v5 ≈ 80% خفض سياق)، grid اقتصادي منزَّل بالملفات (15 haiku/72 sonnet)، نمط 13 skill بدل 107 مرآة، caveman متدرج | (01) (03) |
| G4 | محايد — لا يُحمَّل تلقائياً؛ إن حُقن فهو 2217 سطراً بلا مردود آلي | (05) |
| G5 | **صفر توكن للعمل الحتمي** — Python locates, model judges؛ العمليات الآلية خارج LLM كلياً | (04) |
| G6 | صفر توكن جلسة (خارجها) + وضع MOCK يختبر بلا API إطلاقاً | (04) |

---

## 2) صف الفائز لكل بُعد

| البُعد | الفائز | لماذا (مسند) | مكمّل إلزامي من جيل آخر |
|---|---|---|---|
| الوكلاء والتنظيم | **G3 v6** | 105↔105↔105 آلي + RCCF + least-privilege (01، 03، H1) | طبقة حوكمة الصلاحيات البشرية من G4 + جدول ربط ID↔persona (05) |
| الذاكرة/الدماغ | **G3 v6** | BRAIN 3 طبقات + memdb FTS5 + org brain مأهول (03، 07) | إنفاذ «project brain في repo المشروع» — البند المكسور (06، 07) |
| الأوركسترا والتوجيه | **G3 v6 (Nexus)** | المصدر الواحد الثلاثي registry/routing/gates (03) | محرك التنفيذ خارج الجلسة من G6 بعد ربطه بالـNexus (04) |
| الأدوات الحتمية | **G5 substrate** (نواة) | selftest PASS، ledger-no-daemon، آلة حالات صارمة (04، H1) | محتوى G1: الـ114 سكربت per-agent تملأ `rooms/*/tools/` الفارغة (02) |
| البوابات/دورة الحياة | **G3 v6** | gates.yaml كامل الحقول + طبقتا فحص + 19 artifact حي (03، 06) | checklists gate-0..8 التفصيلية من G1 (02) |
| الأتمتة | **G3 v6 (hooks WT)** | 5 hooks v6.1 بحلقة ذاكرة كاملة، مثبتة تشغيلياً (01، 07) | مجدوِل حقيقي لحلقة reflection (الفجوة الوحيدة) + pipeline G6 للأتمتة الطويلة (04) |
| الحوكمة/الدستور | **G3 v6** | 11 مادة، G1–G5/V1–V5 مسلّكة fail-closed (03) | مادة intake-orchestration من G2 (wear-the-hierarchy) + حوكمة G4 البشرية (07، 05) |
| التوثيق | **G3 v6** | ORG/RUNBOOK/BLUEPRINT/CHARTERs حية متطابقة مع الآلة (03) | العمق البشري السداسي من G4 كمرجع personas (05) |
| النضج التشغيلي | **G3 + G5 معاً** | الوحيدان بفحص ذاتي ناجح الآن: doctor PASS + selftest PASS (03، 04، H1) | — |
| تكلفة التوكن | **G3 (داخل الجلسة) + G5/G6 (خارجها)** | درع .claudeignore + grid اقتصادي؛ والحتمي صفر-توكن (01، 04) | — |

**الحصيلة: G3 يفوز في 8/10 أبعاد؛ G5 في الأدوات الحتمية؛ ولا بُعد يفوز به G1/G2/G4 منفرداً — لكن كلاً منها يحمل مكوّناً ذهبياً واحداً لا بديل عنه.**

---

## 3) ما يُرحَّل إلى شامل — المكوّنات الذهبية عبر كل الأجيال

### من G3 v6 (العمود الفقري — يُرحَّل شبه كامل)
1. **المادتان 02+03** (G1–G5, V1–V5) مع أدوات إنفاذهما (`validate_evidence` fail-closed، gatekeeper fresh-context) — أنضج عقيدة grounding/verification (03).
2. **الثلاثي nexus** `registry/routing/gates.yaml` كمصدر وحيد + فاحص parity `sofi doctor` fail-closed في CI + بصمات `agent-pins.json` (03، 04).
3. **صيغة الوكيل المزدوجة**: spec غني آلياً (frontmatter `route/success_metric/gate/reports_to`) + spawnable RCCF بمنح tools least-privilege — مع **توليد** الـstub الخفيف آلياً من الـspec (درس جيل D) (05، 01).
4. **hooks الخمسة v6.1** (guard/orientation/bands/vaccine/breadcrumbs) بنمط `$CLAUDE_PROJECT_DIR` — المصدر الوحيد، تُسقط نسخ MAIN (01، 07).
5. **BRAIN ثلاثي الطبقات + memdb FTS5 + MEMORY.md نسخة WT + قوالب brain + صيغة LESSONS بالـsig** (03، 07).
6. **RCCF Work Order** (المادة 01: frozen brief + effort classes + evidence block) + bus كـtickets في HANDOFFS (03).
7. **oracle desk** (sanitize→condense→capture→ingest) **بشرط** إضافة API fallback بدل الاعتماد الحصري على CDP اليدوي (03، 07).
8. **نمط 13 skill (spine 6 + power 7)** + درع `.claudeignore` + نمط archive-v5 كإجراء تقاعد معياري (01، 07).
9. صيغة CHARTER الغرفة (mission/members/interfaces/room-bar/escalation) كقالب وحدات شامل (03).

### من G1 OpenCode (انتشال قبل الحذف — أصول خارج git، أولوية قصوى)
10. **`tools/` الـ114 سكربت bash** — تسدّ فجوة `company/rooms/*/tools/` الفارغة، والتسمية أصلاً على مخطط v6؛ **تُدخل git فوراً** (02).
11. **`skills/qa/browser-eyes`** + سكربته الحي (فحص بصري بمتصفح حقيقي — لا مقابل في v6)، بعد تعميمه لأي PRJ ونزع الاعتمادات المضمّنة (02، 06).
12. **gate checklists 0–8** كمكمّل تفصيلي لـ`gates.yaml` (02).
13. فكرتا **translator** (بوابة دلالية قبل CEO) و`permission: {edit, bash}` per-agent في frontmatter (05).

### من G2 Engine v5 (التقاط الجوهر ثم الدفن)
14. **منطق intake-orchestration** (wear-the-hierarchy، leaf-spawn one hop) — يستحق مادة دستورية تحسم تناقضه مع الـskills (07).
15. **الماسحات** feature_scan/sofi_scan/sofi_verify — نسخة v6 المتفرّعة الأحدث، بعد إزالة الازدواج البايتي (04).

### من G4 org-rooms
16. **طبقة حوكمة الصلاحيات السداسية** (سلطة/مال/فيتو/تصعيد/اعتماديات per-person) + الكانون العربي-السوري — **بشرط** جدول ربط ID↔persona يُنهي ازدواج الكانونين (Priya Nair/عمّار خضّور/كريم فاروق لدور واحد) (05).

### من G5 substrate
17. **الأدوات الست كاملة** + فلسفة «ledger لا daemon» + **مواصفة taskq** كآلة الحالات الواحدة التي تخلف التطبيقات الستة المتوازية للـconcern نفسه (04).

### من G6 الإطار الخارجي (بعد دمج الـfork — قبل الضياع)
18. **نسخة موحّدة**: `state_db` (WT 356 سطراً) + `translator_gateway` (MAIN 455 الأغنى) + **إنقاذ `ceo_agent.py`** (موجود فقط في MAIN، untracked) + `agent_invoker` بنمط MOCK/live + الـ22 أداة موحَّدة الرموز مع v6 وموصولة بالـNexus (04).

### من طبقة المشاريع (تقرير 06 — دروس مدفوعة الثمن)
19. **قانون يوم-صفر**: `git init` + remote + أول commit داخل السكافولدر نفسه — لا مشروع بلا VCS ولو لدقيقة (مشروعان ضاعا فعلاً) (06).
20. **نمط `_context/features/GATE0..GATE8`** + FOLDER-MAP كعقد مولَّد لا وثيقة يدوية + قاعدة «الكود هو الحقيقة» (أرقام الـbrain تولَّد بسكربت) + حُرّاس `gitops.checkpoint()` (06).
21. **الـ54 commands** من MAIN/.claude بعد غربلة (gate-check/deploy/parallel-build قيّمة) — الشيء الوحيد المستحق من جيل الـport (01).

---

## 4) ما يُتقاعد (بنمط archive-v5 — شاهد قبر، لا ترك أحياء-أموات)

| المكوّن | الإجراء | السند |
|---|---|---|
| `.opencode/` كلها بعد انتشال البنود 10–13 | حذف node_modules (63M) + `.sofi-run/` + memory الفارغة؛ أرشفة agents الـ68 (14 ملوثة CJK، موديل ميت) | (02) (05) (H2: «keep as archive… do not delete blindly — snapshot first») |
| `MAIN/engine/` (v5) بعد البندين 14–15 | أرشفة؛ ومعه تصحيح `session_start` في MAIN الذي لا يزال يوجّه للجيل الميت | (04) (07) |
| جيل الـport في `MAIN/.claude` | 105 stubs + 107 skills مرآة + `tools/<room>/<role>` + engine الخاص — superseded كلياً (يُنقذ منه الـ54 commands فقط) | (01) (05) |
| `dashboard/` + `index.html` | v5 صِرف (يعرض «30 وكيلاً» ويقرأ `engine/routing`) — يُعاد بناء المراقبة على معطيات v6 | (04) |
| `company/os/{autopilot, ooda, agents/tier-*}` + نسختا OODA | بقايا أجيال داخل نواة v6 بلا علامة deprecated — أرشفة | (03) (04) |
| fork MAIN للإطار الخارجي | بعد إنقاذ `ceo_agent.py` ودمج الـtranslator — يُطوى الـfork | (04) |
| `MEMORY.md` نسخة MAIN + سلالات git الثلاث | تُقتل نسخة MAIN؛ توحيد على فرع مرجعي فوق origin/main (شرط مسبق لأي «شامل») | (07) |
| `sofi-engine/` bash suite + hooks G1 | legacy معلَن ذاتياً، لم تعمل قط | (02) |
| model IDs المثبّتة حرفياً في routing.yaml | تُستبدل بطبقة alias | (03) |

---

## 5) قرارات حاسمة يجب حسمها قبل الترحيل (من التقارير، لا اجتهاد)

1. **توحيد git**: ثلاث سلالات عقيدة (prj/PRJ-SAKK × origin/main × main محلي) — اعتماد origin/main مرجعاً وإعادة زرع الحمولة الفريدة فوقه (07).
2. **حسم تصادم GTW**: نفس الكود، وظيفتان (Nexus حوكمي في v6 مقابل API Gateway خارجي في org-rooms) — إعادة تسمية أحدهما (05).
3. **خريطة الغرف**: 15 (الأكمل تغطية) أم 10 — وإن اعتُمدت العشر تُسدّ فجوات fnt/qa/obs (05).
4. **فك تعشيش الـworktrees** من تحت `.claude/` (سبب نزيف palette المُثبت حياً) + نقل substrate خارج مجلد التهيئة + إعادة تسمية أحد ثنائيي `sofi` و`registry.yaml` (01، H1).
5. **إصلاح `paths.py`**: فشل صاخب بدل الصمت + حلّ صريح للـworktrees — أدوات v6 حالياً عمياء عن المشروع الوحيد الحي (06).

---

## 6) الحكم الختامي

**G3 (v6 Company of Rooms) هو الهيكل العظمي لشامل بلا منازع** — الفائز في 8/10 أبعاد والوحيد HEALTHY بفحص ذاتي ناجح (doctor PASS — 03، H1). **G5 substrate** ينضم إليه نواةً حتمية (selftest PASS — 04). البقية مناجم لا هياكل: **G1** يسلّم 114 أداة + browser-eyes + checklists قبل دفنه (02)، **G2** يسلّم intake-orchestration والماسحات (07، 04)، **G4** يسلّم الحوكمة البشرية والكانون العربي (05)، **G6** يسلّم محرك التنفيذ الخارجي بعد دمج fork-يه وربطه بالـNexus (04). الخطران الوجوديان قبل أي بناء: كود المنتج والدماغ الحي خارج أي git (06)، والأصول الذهبية لـG1 خارج git أيضاً (02) — **الانتشال أولاً، ثم التقاعد، ثم شامل.**
