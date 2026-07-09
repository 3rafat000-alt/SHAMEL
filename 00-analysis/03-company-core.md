# تدقيق شامل — نواة v6 «Company of Rooms» (`company/`)

**النطاق:** `/home/es3dlll/Desktop/Lorka/.claude/worktrees/org-rooms-100/company/` — الدستور، الـ Nexus، الغرف الـ 15، طبقة الـ OS، الـ Brain، والوثائق العليا.
**المنهج:** READ-ONLY؛ قراءة معمّقة للمواد 00/01/02/03/10 + عناوين البقية، parsing فعلي بـ Python لملفات YAML، عدّ فعلي على القرص، وتشغيل `sofi doctor`. كل ادعاء مسنود بـ file:line أو أمر+ناتج. التاريخ: 2026-07-10.

---

## الجرد

### 1. الدستور (CONSTITUTION + المواد 00–10)

| الملف | الأسطر | الحالة |
|---|---|---|
| `company/CONSTITUTION.md` | 152 | حيّ — 7 Teachings + Oath + CEO Covenant + Room Isolation Law + Precedence + Amendment |
| `constitution/00-operating-system.md` | 84 | العقد الكوني: 10 خطوات لكل turn + circuit breaker + two-track sizing |
| `constitution/01-work-order.md` | 157 | RCCF v3: الحقول الأربعة + canonical block + effort classes + self-check من 6 أسئلة |
| `constitution/02-grounding.md` | 30 | G1–G5 + نقاط الإنفاذ الميكانيكية |
| `constitution/03-verification.md` | 45 | V1–V5 + جدول wiring كامل |
| `constitution/04-reflection.md` | 26 | الأقصر — scheduled dreaming، ملكية `knw-reflector` |
| `constitution/05-token-economy.md` | 64 | سلّم الـ routing + budgets |
| `constitution/06-git-discipline.md` | 120 | branch model، checkpoints، worktrees |
| `constitution/07-security-law.md` | 54 | CSO veto، secrets، sanitized-external-only |
| `constitution/08-handoff-law.md` | 56 | tickets + room boundaries + sign-off |
| `constitution/09-research-law.md` | 48 | سلّم البحث brain→codebase→search→fetch→cite |
| `constitution/10-lifecycle-gates.md` | 38 | جدول البوابات التسع + gate discipline + parallelism |

11 مادة كما يعلن الدستور نفسه ("its eleven articles" — `CONSTITUTION.md:143`)، والجدول في `CONSTITUTION.md:114-128` يطابق الملفات على القرص واحد-لواحد `[verified: ls constitution/]`.

### 2. الـ Nexus (`company/nexus/`)

عدّ فعلي عبر `python3 + yaml.safe_load`:

- **`registry.yaml`** (1148 سطراً): `rooms_total: 15`، `agents_total: 105` — والعدّ الفعلي للوكلاء داخل الغرف = **105** (brd 7 · str 7 · res 7 · dsn 8 · arc 7 · bck 8 · fnt 8 · mob 6 · dat 7 · sec 8 · qa 7 · ops 7 · obs 6 · knw 6 · gtw 6). skills أعلى المستوى = **13**، tools = **4 مجموعات** (dict)، superpowers = **3** `[verified: parse output]`.
- **`gates.yaml`** (220 سطراً): **9 بوابات (id 0–8)**، كل بوابة تحمل `id·name·trigger·owner_room·agents·entry·artifacts·exit_bar·on_fail` بلا استثناء (البوابات 3–5 تضيف `squad_rooms`) `[verified: parse — طُبعت مفاتيح كل بوابة]`. يتصدّره block تعليقي يشرح الطبقتين (mechanical + adversarial) ويعلن سداد دين v5 رقم 5: "gates.GATE_ROLES is loaded from THIS file" (`gates.yaml:5-6`). فيه أيضاً `accountability` (brd-cpo 0–2 · brd-cto 3–4 · brd-cqo 5 · brd-ceo all · brd-cso veto) و`tracks` (fast_track/deep_audit) (`gates.yaml:20-29`).
- **`routing.yaml`** (214 سطراً): 4 نماذج (`mechanical=claude-haiku-4-5`، `workhorse=claude-sonnet-5`، `gatekeeper=claude-fable-5`، `deep=claude-opus-4-8`) · **109 routes** = 105 وكيلاً + 4 مسارات مهام (`code-review`، `commit-message`، `spec-review-gate`، `spec-review-scan`) — الفرق مُفسَّر بالكامل: `routes − agents = {4 task routes}` و`agents − routes = ∅` `[verified: set-diff]`. `effort_scaling` بخمس فئات (trivial-fix · single-role · cross-room · audit-sweep · arbitration) + `escalation` (raise_when/lower_when/priority_override) + `safety_overrides` + `budgeted_autonomy`.
- **`bus/`**: `ticket-schema.md` (126 سطراً — schema ملزم بحقول from/to/task/consumes/expected/route/status + header regex يطابق `tickets.py`) و`escalation.md` (83).
- **`NEXUS.md`** (125) + ملفان إضافيان: `agent-pins.json` (بصمات SHA-256 لكل spec وكيل — tamper-detection) و`gemini-audit-dispatch.yaml` (توجيه GitHub issues لوكلاء RCCF).

### 3. الغرف (`company/rooms/` — 15 غرفة)

عدّ فعلي لكل غرفة (loop على القرص): **كل غرفة بلا استثناء** تحمل `CHARTER.md` (83–101 سطراً) + `agents/` (المجموع 105 spec) + `skills/README.md` + `playbooks/` (ملفان حقيقيان لكل غرفة) + `tools/README.md`.

- **CHARTERs ليست stubs**: عيّنة `14-gateway/CHARTER.md` (97 سطراً) — mission، جدول أعضاء بالـ routes، gate ownership مُعلَّل ("owns no gate… correctly so" `:26`)، جداول consumes-from/produces-to، room bar من 7 بنود، escalation paths بحالات ملموسة. وعيّنة `10-quality/CHARTER.md` — يشرح squad الغرفتين (qa+sec) خلف نفس الـ merged build وقاعدة "ONE unambiguous PASS/BLOCK".
- **playbooks حقيقية**: مثل `05-backend/playbooks/gate-4-build-procedure.md` (99 سطراً) و`idempotent-job-design.md` (68).
- **skills/ و tools/ داخل الغرف = README-index فقط** (مثال `05-backend/skills/README.md` — جدول "متى تُشهر الغرفة كل skill"؛ يصرّح بنفسه أنه "not a duplicate of the skill files themselves"). أي أن المهارات والأدوات الفعلية تعيش خارج الغرفة (`.claude/skills/` و `company/os/`) — الغرف "self-contained" توثيقياً لا تنفيذياً.
- **specs الوكلاء غنية**: عيّنة `05-backend/agents/bck-blade-engineer.md` — frontmatter كامل (agent·persona_name·room·reports_to·gate·route·success_metric) + persona + Operating Prompt.

### 4. طبقة الـ OS (`company/os/`)

- **`sofi_tools/`**: **24 موديول Python، 5758 سطراً** `[verified: ls + wc]` — تغطي brain·tickets·routing·gates·gitops·guard·runlog·domain·tunnel + موديولات أحدث لم يذكرها CLAUDE.md: `acceptance`، `agentlint`، `budget`، `event_server`، `lessons_cache`، `memdb`، `paths`، `resume`، `scheduler`، `telemetry`، `transitions`.
- **`bin/sofi`**: bash dispatcher من 7 أسطر → `python3 -m sofi_tools`. الـ CLI يسجّل **32 subcommand** عبر `add_parser` + alias `gemini` بجوار `oracle` (الـ help يعرض 34 اسماً) `[verified: --help output]` — منها أوامر جديدة: `plan` (تجميد DAG)، `run`، `resume` (FRESH/DEGRADED/UNKNOWN)، `events` (telemetry)، `lint` (roster lint)، `recall` (memdb).
- **`GOVERNANCE.md`** (69 سطراً): قانون السكربتات، إنفاذه كود في `guard.py` (`GovernanceError` — `GOVERNANCE.md:3-5`).
- **`oracle/`**: 3 وثائق معمارية؛ السائق الفعلي في `agents/ceo/` (`gemini_review.py`، `gemini_bridge.py`، `sanitize_gemini_payload.py`) — مطابق لما يعلنه `14-gateway/CHARTER.md:79`.
- **`agents/`**: scanners (feature_scan، sofi_scan، sofi_verify، uiux_pipeline…) + **بقايا أجيال أقدم**: `tier-1-architecture/`، `tier-3-quality/`، `tier-4-infrastructure/` (تسمية v5 بالطبقات لا بالغرف)، و`autopilot/` (جيل AUTOPILOT) و`ooda/engine/main.py` (جيل OODA — موجود فعلاً على القرص).

### 5. الـ Brain (`company/brain/`)

- `BRAIN.md` (120 سطراً — معمارية الذاكرة org/project/session).
- `org/`: 6 ملفات حيّة، 753 سطراً إجمالاً — `HANDOFFS.md` 230، `DECISIONS.md` 111، `EVOLUTION.md` 119، `LESSONS.md` 82 (**فيه دروس فعلية** بصيغة sig — `LES-001 · sig: blind-start-amnesia · date: 2026-07-07`)، `PERSONAS.md` 53، `TEAM_STATUS.md` 38 + `archive-v5/`.
- `templates/`: 6 قوالب (STATE·CONTEXT·DECISIONS·HANDOFFS·LESSONS·FOUNDATIONS).
- **الحكم الفرعي: نظام ذاكرة مكتمل ومأهول، ليس هيكلاً فارغاً.**

### 6. الوثائق العليا

| الملف | الأسطر | الحالة |
|---|---|---|
| `ORG.md` | 254 | حيّ — mermaid chart + مرآة بشرية للـ registry |
| `RUNBOOK.md` | 135 | حيّ — حلقة تشغيل الـ CEO خطوة-خطوة |
| `BLUEPRINT.md` | 351 | حيّ — السجل التصميمي، خريطة v5→v6 ("75 new colleagues joined") |
| `research/PATTERNS.md` | 159 | حيّ — قاعدة الأدلة (13 research agents، أنماط منسوبة لمستودعات حقيقية) |

إضافة: `company/templates/` (7 قوالب تسليم: adr، journey-map، openapi، perf-budget…) و`superpowers/` (SUPERPOWERS.md + cybersecurity-skills vendored).

---

## الصحة

فحص ميكانيكي مباشر:

```
$ bash company/os/bin/sofi doctor
  routing   : ✓ 109 routes (company/nexus/routing.yaml)
  registry  : ✓ 15 rooms · 105 agents (company/nexus/registry.yaml)
  net-roles : 41 agents may reach the web
  agents    : ✓ 105 spawnables ↔ 105 room specs (105↔105)
  skills    : ✓ registry skill paths exist
  VERDICT   : PASS
```

- ملفات YAML الثلاثة تُحلَّل بلا أخطاء `[verified: yaml.safe_load]`.
- التطابق doctrine↔machine سليم: جدول البوابات في `10-lifecycle-gates.md:7-18` يطابق `gates.yaml` (نفس الـ owners والـ exit bars)، وجدول المواد في `CONSTITUTION.md` يطابق القرص.
- كل وكيل في الـ registry له route؛ لا وكيل بلا route ولا route يتيم (باستثناء 4 task-routes مقصودة).

---

## نقاط القوة

1. **مادتا 02 (Grounding) و03 (Verification) هما الأقوى** — ليستا وعظاً بل قانون مُسلَّك: G3 يُنفَّذ ميكانيكياً بـ `sofi_tools.gates.validate_evidence()` fail-closed (`02-grounding.md:22`، `03-verification.md:9`)، وV2 يفصل المنفّذ عن الحَكم بنيوياً (`gtw-gatekeeper` يرى الـ deliverable + الـ exit bar الأصلي فقط، وUNKNOWN حكم مشروع)، وV5 يدقّق الحَكم نفسه. كل قاعدة معلَّلة بحثياً (judge bias، pass^k، miscalibrated confidence).
2. **ازدواجية doctrine↔machine منضبطة**: كل قانون نصّي له توأم آلي (`10-lifecycle-gates.md` ↔ `gates.yaml`؛ Room Isolation ↔ `validate_room_boundary()`؛ routing ↔ `routes.<id>`) — والمصدر الواحد مُعلن صراحة ("Routes come from ONE source" `CONSTITUTION.md:138`).
3. **RCCF (المادة 01) brief-engineering ناضج**: كل حقل مربوط بنمط فشل محدد (`01-work-order.md:18-27`)، canonical block قابل للنسخ (`:70-103`)، frozen-brief/no-instruction-drip، effort classes بموازنات، و"clarify before commit".
4. **هرم Precedence + إجراء Amendment** (`CONSTITUTION.md:140-152`): تعارض الطبقات defect يُصعَّد لا يُفسَّر، والتعديل حصراً بقرار CEO مسجّل ADR — يمنع تحلّل العقيدة.
5. **صحة آلية قابلة للتشغيل**: `sofi doctor` PASS فعلياً، وأدوات أحدث مما يوثّقه CLAUDE.md (agentlint، agent-pins SHA-256، telemetry، resume) — الطبقة تتطور أسرع من توثيقها الأعلى.
6. **CHARTERs الغرف عالية الجودة وغير متكررة**: كل غرفة تعرّف interfaces (consumes/produces) وroom bar وescalation بحالات ملموسة لا قوالب منسوخة.

## نقاط الضعف

1. **"الاكتفاء الذاتي للغرف" اسمي جزئياً**: `skills/` و`tools/` داخل كل غرفة README-pointer واحد فقط؛ التنفيذ الفعلي مركزي في `.claude/skills/` و`company/os/` — نقل غرفة وحدها لا ينقل قدراتها.
2. **بقايا أجيال أقدم داخل نواة v6**: `os/autopilot/` (جيل AUTOPILOT)، `os/ooda/` (محرك OODA كامل)، `os/agents/tier-*` (تسمية v5 الطبقية) — تعيش بجوار بنية الغرف دون علامة deprecated، وتشوّش على مبدأ "المصدر الواحد".
3. **أسماء نماذج مثبّتة حرفياً في `routing.yaml`** (`claude-haiku-4-5`، `claude-sonnet-5`، `claude-opus-4-8`) — ستتعفن مع كل ترقية نماذج؛ المبدأ "nothing hardcodes a model" (`CONSTITUTION.md:138`) محفوظ خارج routing.yaml لكن الملف نفسه يحتاج صيانة يدوية دورية.
4. **المادة 04 (Reflection) الأضعف نسبياً**: 26 سطراً مقابل 157 للمادة 01 — الحلقة موصوفة لكن بلا تفاصيل إنفاذ آلي بمستوى شقيقاتها (ما الـ trigger الميكانيكي للجدولة؟).
5. **الإنفاذ يفترض الاستدعاء**: `sofi gate-check` وdoctor أدوات فحص لا حرّاس دائمون — لا شيء داخل `company/` يمنع تخطيها إن لم تُستدعَ (الـ hooks في `.claude/settings.json` خارج هذه النواة وfail-open بالتصميم).
6. **اعتماد مسار Oracle على خدمة خارجية** (Gemini pinned chat) — مسار التعطّل موثّق (`14-gateway/CHARTER.md:91`) لكنه dependency تشغيلي وحيد للـ Teaching VII.
7. **صياغة مزدوجة العدّ**: "105 specialists across 15 rooms (غرف) plus the boardroom" (`CONSTITUTION.md:4`) — الـ boardroom إحدى الغرف الـ 15 ووكلاؤها السبعة ضمن الـ 105؛ التباس لفظي لا رقمي.

## التداخل مع الطبقات الأخرى

- **`.claude/agents/` (WT)**: 105 spawnables مرآة لـ `rooms/*/agents/` — dual-file parity يفرضها doctor (PASS)، و`nexus/agent-pins.json` يبصمها SHA-256.
- **أجيال MAIN القديمة**: `engine/` (AUTOPILOT/DOCTRINE) في الجذر الرئيسي يتقاطع مفاهيمياً مع `company/os/autopilot/` و`os/ooda/` المدفونين هنا — نفس الأفكار بجيلين.
- **`orchestrator/` و`tools/` في جذر الـ WT**: أُطر خارجية (commit b6db3bb) تعمل بجوار `company/os/` — طبقة أدوات ثالثة موازية لـ sofi_tools.
- **جسر GitHub خارجي**: `nexus/gemini-audit-dispatch.yaml` يوجّه issues خارجية لوكلاء الغرف مباشرة — dispatch يمرّ خارج `gtw-dispatcher` النظري.
- **`brain/org/archive-v5/`**: تاريخ v5 محفوظ داخل النواة (مقصود — مرجعية personas/lessons).

## ما يُرحَّل لنظام شامل

1. **المادتان 02+03 حرفياً** (G1–G5، V1–V5) مع أدوات إنفاذهما (`validate_evidence`، fresh-context gatekeeper) — أنضج عقيدة grounding/verification في كل الأجيال.
2. **نموذج `gates.yaml` الآلي**: بوابة = owner+entry+artifacts+exit_bar+on_fail + مبدأ الطبقتين (mechanical ثم adversarial) + no-skip monotonic.
3. **نمط المصدر الواحد الثلاثي** registry/routing/gates + فاحص parity (`sofi doctor`) + بصمات `agent-pins.json`.
4. **RCCF Work Order** (المادة 01) كصيغة تفويض قياسية — الحقول الأربعة + effort classes + frozen brief.
5. **الـ bus كـ tickets في HANDOFFS.md** (`bus/ticket-schema.md`) — بلا middleware، git-native، قابل للتحقق regex.
6. **substrate `sofi_tools`** (24 موديولاً / 5758 سطراً) — خصوصاً الأحدث: agentlint، resume، telemetry، memdb.
7. **قوالب الـ brain + صيغة LESSONS بالـ sig** — ذاكرة إجرائية idempotent.
8. **صيغة CHARTER الغرفة** (mission/members/interfaces/room-bar/escalation) كقالب تعريف وحدات في شامل.
9. **ما لا يُرحَّل**: `os/autopilot/`، `os/ooda/`، `os/agents/tier-*` — تُترك كأرشيف أجيال؛ وتثبيت model IDs يُستبدل بطبقة alias.

## الحكم

**HEALTHY** — `sofi doctor` PASS فعلياً (105↔105، 109 routes، 15 غرفة)، البوابات التسع مكتملة الحقول، العقيدة والآلة متطابقتان، الـ brain مأهول؛ العيوب هيكلية-هجينية (بقايا أجيال داخل os/، اكتفاء ذاتي اسمي للغرف، model IDs مثبّتة) لا كسور تشغيلية.
