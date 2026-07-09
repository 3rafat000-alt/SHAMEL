# شامل / SHAMEL — المؤتمت: طبقة الأتمتة الحقيقية

**التاريخ:** 2026-07-10 · **الكاتب:** مصمّم طبقة الأتمتة (SHAMEL design) · **الحالة:** وثيقة تصميم ملزمة للـ PRD
**المصادر:** `08-COMPARISON-MATRIX.md` · `09-GAP-ANALYSIS.md` · `04-engines-tooling.md` + فحص حي للكود في WT (`.claude/hooks/` · `.claude/engine/tooling/` · `orchestrator/` · `main.py` · `company/os/sofi_tools/`)
**المبدأ الحاكم:** أتمتة حقيقية لا نظرية — **لا ادعاء أتمتة بلا إنفاذ آلي fail-closed قابل للفحص** (علاج GAP-04/11/12 بقاعدة واحدة). البنية داخل Claude Code مسطّحة (flat topology): **لا daemon داخلي أبداً** — الـ daemon الوحيد في المنظومة كلها هو `cron` نفسه.

---

## 1. الجرد الصادق — ما المؤتمت فعلاً اليوم vs المزعوم

### 1.1 مؤتمت فعلاً (بدليل تشغيلي، يُرحَّل إلى شامل)

| # | المكوّن | ما يفعله آلياً | الدليل |
|---|---------|----------------|--------|
| A1 | **hooks الخمسة v6.1** (WT) | `SessionStart` يحقن دماغ المشروع (STATE head + التذكرة التالية، سقف ~1000 توكن) · `UserPromptSubmit` لقاح الدروس (memdb.learn_match + lessons_cache.vaccine_for) + التقاط `[LEARN]` من التصحيحات · `PreToolUse` حارس أمني/git **يحجب فعلياً** (أوامر خطرة، `.env`، صيغة commit) · `PostToolUse` نطاقات checkpoint + التقاط observation · `Stop` breadcrumb إلى `sessions.jsonl` + `memdb.compress_session` + تذكير gate-proof متدرّج | فُحصت حيّة: `.claude/settings.json` يسلّك الخمسة بنمط `$CLAUDE_PROJECT_DIR`؛ التقارير (01، 07): «مثبتة تشغيلياً» |
| A2 | **substrate الست أدوات** | `taskq` (SQLite، آلة حالات صارمة) · `gateway` (جسر حتمي translator→queue) · `validate` (فحص schemas) · `check` (lint/test حقيقي مع exit مهيكل) · `gitflow` (يرفض force/reset مسبقاً) · `registry` (SSoT مخططات) | `sofi selftest --json` = **PASS 6/6** (04) |
| A3 | **`sofi doctor` (parity-check)** | تكافؤ 105↔105↔105 spawnable↔spec↔registry + 109 routes + مسارات skills — fail-closed | **PASS** حي (04، H1)؛ «أنجح آلية مكافحة تفكّك في المنظومة كلها» |
| A4 | **الفحص الميكانيكي للبوابات** | `validate_evidence()` fail-closed داخل gate-check: تذكرة done بلا evidence block = رفض آلي | (03): «قانون مُسلَّك كوداً لا وعظ» |
| A5 | **orchestrator الخارجي (G6)** | pipeline كامل خارج الجلسة يصل COMPLETED؛ `agent_invoker` يستدعي `claude -p` فعلياً (`agent_invoker.py:268-269`) مع وضع MOCK بديل؛ self-heal مُثبت (`MOCK_FAIL_THEN_PASS` ينجح في المحاولة 2) | (04، H1: WORKS·PARALLEL)؛ `--live` مُثبت |
| A6 | **`scheduler.py` (DAG walker)** | `sofi plan` يجمّد قائمة مهام إلى DAG، `sofi run` يمشيه ميكانيكياً — «what's ready» بصفر توكن | docstring مفحوص: «deterministic DAG scheduler … zero tokens on coordination» |

### 1.2 أتمتة ورقية (مزعومة، غير موجودة — كل بند يحمل بند إنفاذ في هذه الوثيقة)

| # | الادعاء | الواقع | GAP | يُغلق في |
|---|---------|--------|-----|----------|
| P1 | `/sofi-reflect` «scheduled dreaming» | **لا أتمتة SOFI مجدولة**: `crontab -l` (تحقق حي اليوم) يحوي سطرين نشطين كل دقيقة — Laravel scheduler لـ PRJ-SAKK الحي + سطر dangling لـ PRJ-SAAS-001 المعدوم — ولا سطر SOFI/reflection واحد؛ لا `LESSONS.md` لأي مشروع قط، `knw-reflector` spawn-on-demand فقط | GAP-11 | §2.3 + المرحلة 4 |
| P2 | memdb «ذاكرة مهيكلة» | `brain.db` بصفّ observations واحد — البنية موجودة والتغذية معدومة | GAP-11 | §2.2 (hooks تُغذّي) + المرحلة 2 |
| P3 | oracle desk «حلقة مؤتمتة» | يتطلب Chrome يدوياً على CDP :9222؛ `oracle status` يعيد **exit 0 حتى عند الفشل** | GAP-11 | §4 + المرحلة 7 |
| P4 | «GitHub Actions ينشر تلقائياً» (PRJ-SAKK gate 6) | `.github/workflows/` **فارغ تماماً**؛ runbook يستشهد بأربعة ملفات معدومة | GAP-04 | §5 + المرحلة 8 |
| P5 | حلقة `sync→checkpoint→handoff` | `paths.py` يفشل **صامتاً** من الـ worktree، `checkpoint` مكسور بنيوياً، `branch/head_sha` فارغان في STATE | GAP-09 | §2.4 + المرحلة 2 |
| P6 | «خرق SLO يعيد فتح Gate 1 آلياً» | لا instrumentation ولا alert rule واحدة قائمة | — | §5 (Gate 8) + المرحلة 8 |
| P7 | «fail-open آمن» | فشل الحُرّاس/الذاكرة صامت بلا عدّاد ولا إنذار — انهيار الانضباط قد يمرّ أسابيع | GAP-20 | §2.2 (hooks-health ledger) |

### 1.3 أتمتة مضادة (تعمل ضدنا — تُفكَّك قبل أي تفعيل)

| # | المكوّن | الضرر | الإجراء |
|---|---------|-------|---------|
| N1 | `session_start.py` في MAIN | يحقن آلياً في كل جلسة توجيهات الجيل الميت (`engine/tooling/` + «no slash-commands») — دستور معاكس حسب مجلد الإقلاع | يُسقط مع مصالحة GAP-02/08؛ نسخة WT هي الوحيدة الناجية |
| N2 | `dashboard/server.py` + `index.html` | مراقبة «آلية» تقرأ عالم 30 وكيلاً المنقرض — أتمتة تكذب | أرشفة؛ المراقبة تُبنى من جديد على `brain/db/` + nexus |
| N3 | fork الـ orchestrator المزدوج | نسختان تتباعدان في نفس اليوم؛ أي «تفعيل» قبل الدمج يرسّخ الانقسام | الدمج شرط مسبق (§3.1) |

**الخلاصة الصادقة:** المؤتمت الحقيقي اليوم = حلقة داخل-الجلسة (hooks) + أدوات حتمية تُستدعى عند الطلب + pipeline خارجي يعمل لكنه معزول عن الحوكمة. **لا أتمتة SOFI/شامل تجري اليوم بلا جلسة مفتوحة أو أمر يدوي** — لا أتمتة SOFI مجدولة (crontab المستخدم يحمل فقط مجدولَي Laravel لمشروعين، أحدهما dangling — §1.2 P1)، والـ CI صفر. شامل يبني على A1–A6 ويغلق P1–P7 بترتيب المراحل في §7.

---

## 2. الأتمتة داخل Claude Code — flat topology، لا daemon

### 2.1 المبدأ المعماري

ثلاث طبقات فقط داخل الجلسة، كلها سلبية (تُستدعى، لا تعمل في الخلفية):

1. **hooks** — أحداث الـ harness تشغّل سكربتات Python قصيرة (الحقن/الحجب/الالتقاط).
2. **skills** — انضباط يُستدعى بالاسم (`/shamel-boot`، `/shamel-gate`…)؛ «الجدولة» لأي skill تعيش **خارج** الجلسة في cron (§2.3).
3. **substrate** — أدوات حتمية exit-code-gated؛ «Python locates, model judges»؛ صفر توكن للعمل الميكانيكي.

قاعدة شامل: **كل ما يمكن أن يكون حتمياً لا يلمس نموذجاً** — الالتقاط والفحص والطوابير والتحقق الميكانيكي كود صرف؛ النموذج يُستدعى للحكم فقط.

### 2.2 خريطة hooks — 5 مرحّلة + 2 جديدة + إصلاح عرضي واحد

المصدر الوحيد للترحيل: نسخة **WT v6.1** (الأنضج — التقرير 07). نسخ MAIN تُدفن مع المصالحة.

| الحدث | السكربت | الأصل | الوظيفة | تعديل شامل |
|-------|---------|-------|---------|-------------|
| `SessionStart` | `session_start.py` | **مرحّل** من WT | حقن دماغ المشروع (STATE head + التذكرة التالية + digest ذاكرة) بسقف 1000 توكن | + سطر صحة واحد: نتيجة آخر `shamel doctor` الليلي (PASS/FAIL + عمره) — الجلسة تعرف أن الهيكل سليم قبل أن تعمل |
| `UserPromptSubmit` | `user_prompt_submit.py` | **مرحّل** | لقاح الدروس قبل العمل + التقاط `[LEARN]` من التصحيحات | كما هو (النصفان الحي والمستقبِل لحلقة reflection) |
| `PreToolUse` (Bash\|Read\|Edit\|Write) | `pre_tool_use.py` | **مرحّل** | الحارس الحاجب: git خطر · `.env` · صيغة commit | كما هو — الحاجب الوحيد المسموح |
| `PostToolUse` (Edit\|Write) | `post_tool_use.py` | **مرحّل** | نطاقات تذكير checkpoint + `memdb.capture` + telemetry | كما هو؛ يعتمد على إصلاح `paths.py` (§2.4) ليلتقط للمشروع الصحيح |
| `Stop` | `stop.py` | **مرحّل** | breadcrumb + `memdb.compress_session` + تذكير gate-proof متدرّج بسقف | كما هو |
| `PreCompact` | `pre_compact.py` | **جديد** | قبل ضغط السياق: يكتب لقطة توجيه (المشروع النشط، gate، uncommitted count، آخر 3 قرارات) إلى `brain/db/compact-snapshot.json` — فالجلسة بعد الضغط لا تفقد بوصلتها؛ `SessionStart` بعد compaction يعيد حقنها | جديد كلياً (~40 سطراً على نمط `_common.py`) |
| `SubagentStop` | `subagent_stop.py` | **جديد** | يلتقط خلاصة كل subagent (المهمة، الحكم، وجود evidence block) كصف memdb بنوع `delegation` — الوقود المفقود لحلقتي reflection (P1) وV5 (تدقيق الأحكام) | جديد (~35 سطراً) |

**الإصلاح العرضي (علاج GAP-20 — «رصد بلا حجب»):** تبقى كل الـ hooks fail-open (فشلها لا يعطّل الجلسة)، لكن `_common.py` يلفّ كل hook بعدّاد أعطال:

```python
# _common.py — يضاف لكل hook
def record_hook_failure(hook: str, err: str) -> None:
    row = {"ts": utcnow(), "hook": hook, "err": err[:200]}
    (SHAMEL_ROOT / ".shamel" / "hooks-health.jsonl").open("a").write(json.dumps(row) + "\n")
```

`shamel doctor` يقرأ الملف: **أي hook فشل ≥3 مرات في آخر 24 ساعة → doctor يطبع WARN ويُدرجه في حقن `SessionStart` التالي.** الانضباط لا ينهار بصمت بعد اليوم.

مقطع `settings.json` النهائي (7 أحداث):

```json
{
  "hooks": {
    "SessionStart":     [{ "hooks": [{ "type": "command", "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/session_start.py\"" }] }],
    "UserPromptSubmit": [{ "hooks": [{ "type": "command", "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/user_prompt_submit.py\"" }] }],
    "PreToolUse":  [{ "matcher": "Bash|Read|Edit|Write", "hooks": [{ "type": "command", "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/pre_tool_use.py\"" }] }],
    "PostToolUse": [{ "matcher": "Edit|Write",           "hooks": [{ "type": "command", "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/post_tool_use.py\"" }] }],
    "Stop":         [{ "hooks": [{ "type": "command", "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/stop.py\"" }] }],
    "PreCompact":   [{ "hooks": [{ "type": "command", "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/pre_compact.py\"" }] }],
    "SubagentStop": [{ "hooks": [{ "type": "command", "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/subagent_stop.py\"" }] }]
  }
}
```

### 2.3 الـ skills المجدولة — الجدولة في cron، التنفيذ في `claude -p`

داخل Claude Code لا يوجد مجدوِل — «scheduled skill» تعني: **سطر cron يستدعي `claude -p "/skill"` headless**. قاعدة اقتصاد التوكن تفصل نوعين:

| المهمة | النوع | الأمر (سطر cron) | التواتر | لماذا هذا النوع |
|--------|-------|-------------------|---------|------------------|
| فحص الهيكل | **حتمي** (لا نموذج) | `engine/bin/shamel doctor --json` | ليلي 03:15 | parity/paths/hooks-health — عدّ ومقارنة صرف |
| ضغط memdb | **حتمي** | `engine/bin/shamel memdb compact` | ليلي 03:30 | ضغط صفوف observations القديمة — ميكانيكي |
| تدقيق الميزانية | **حتمي** | `engine/bin/shamel budget report --json` | أسبوعي | تجميع أرقام runlog/telemetry |
| **reflection** (تقطير الدروس) | **نموذجي** | `claude -p "/shamel-reflect" --max-turns 15 --allowedTools …` | أسبوعي (الأحد 04:00) | الحكم «ما الدرس؟» يحتاج نموذجاً؛ يقرأ HANDOFFS + صفوف `delegation`/`[LEARN]` من memdb ويكتب `LESSONS.md` مُسنداً بالتذاكر |
| مراجعة oracle الدورية | **نموذجي** (اختياري، المرحلة 7) | `claude -p "/shamel-report weekly" ثم shamel oracle review` | أسبوعي | تأليف التقرير حكمٌ؛ الدفع والالتقاط حتميان |

ملف التفعيل الوحيد — `cron/shamel.crontab` (نسخة tracked في الريبو؛ التركيب **دمجاً غير مدمّر** — crontab المستخدم يحمل اليوم سطر Laravel scheduler الحي لـ PRJ-SAKK (§1.2 P1)، و`crontab <file>` الخام يستبدل crontab كاملاً ويمحوه بصمت؛ الإيقاف بحذف كتلة شامل. البديل المكافئ: ملف مستقل في `/etc/cron.d/shamel` لا يلمس crontab المستخدم أصلاً):

```cron
# >>> SHAMEL — المجدوِل الخارجي الوحيد
# تركيب غير مدمّر (idempotent، يحفظ الأسطر القائمة — لا تستخدم `crontab cron/shamel.crontab` الخام):
#   crontab -l | sed '/^# >>> SHAMEL/,/^# <<< SHAMEL/d' | cat - cron/shamel.crontab | crontab -
SHAMEL=/home/es3dlll/Desktop/SHAMEL
PATH=/home/es3dlll/.local/bin:/usr/bin:/bin
15 3 * * *  cd $SHAMEL && engine/bin/shamel doctor --json  >> brain/db/logs/doctor.jsonl  2>&1 || engine/bin/shamel notify "doctor FAIL"
30 3 * * *  cd $SHAMEL && engine/bin/shamel memdb compact  >> brain/db/logs/memdb.jsonl   2>&1
0  4 * * 0  cd $SHAMEL && claude -p "/shamel-reflect" --max-turns 15 --allowedTools "Read,Grep,Glob,Edit,Write" >> brain/db/logs/reflect.jsonl 2>&1
0  5 * * 0  cd $SHAMEL && engine/bin/shamel budget report --json >> brain/db/logs/budget.jsonl 2>&1
# <<< SHAMEL
```

قواعد ملزمة: كل سطر cron **مقيّد** (`--max-turns` للنموذجي، timeout داخلي للحتمي) · يكتب سجلّه في `brain/db/logs/` (gitignored) · فشله يستدعي `shamel notify` (سطح إنذار واحد: notify-send محلياً أو webhook لاحقاً) — **لا مهمة مجدولة صامتة الفشل** (عكس P3/P7) · **البيئة معلنة:** سطر `PATH=` في الملف إلزامي — cron يعمل بـ `/usr/bin:/bin` الافتراضي و`claude` يقيم في `~/.local/bin` (فُحص: `which claude`)، فبدونه سطر reflect يفشل command-not-found من أول ليلة · **أذونات headless معلنة:** `claude -p` non-interactive لا يستطيع منح أذونات أدوات تفاعلياً، فكل استدعاء يحمل `--allowedTools` بالقائمة الدنيا لمهمته (أو allowlist مكافئة في `settings.json`، أو `--permission-mode` مسجَّل) — بدونها reflect لا يستطيع كتابة `LESSONS.md` أصلاً؛ القاعدة نفسها تلزم invoker §3.2.

### 2.4 الـ substrate في الحلقة — آلة حالات واحدة تخلف الست

**tقرار شامل الحاسم (علاج GAP-06/15):** `taskq` هي **آلة حالات المهام الوحيدة** في المنظومة كلها. التطبيقات الستة المتوازية (tickets.py ×2، task-queue.sh، taskq.py، state_db.py ×2) تُخلَف بواحد:

```
pending → assigned → running → completed | failed
failed  → pending (إعادة محاولة) | cancelled
completed / cancelled = نهائيتان
```

- **`HANDOFFS.md` يبقى** واجهة القراءة البشرية/الوكيلية للتذاكر، لكنه **مرآة تُولَّد** من taskq (`shamel taskq sync-handoffs <PRJ>`) — لا مصدرَي حقيقة.
- **`state_db.py` يتقاعد**: جدول تاريخ الانتقالات (أفضل ما فيه، نسخة WT) يُدمج في taskq كجدول `history`؛ حالات الـ pipeline (BACKEND_PROCESSING…) تصبح **مهام taskq لكل غرفة** والـ pipeline مجرد view مشتق.
- **إعادة تسمية** (GAP-15): `registry.py` في substrate → **`schemas.py`** — كلمة registry تعود حصراً لسجلّ الوكلاء `nexus/registry.yaml`.

شجرة طبقة الأتمتة في شامل:

```
~/Desktop/SHAMEL/
├── nexus/                        # المصدر الوحيد: registry.yaml · routing.yaml · gates.yaml
├── engine/
│   ├── bin/shamel                # الموزّع الواحد (يخلف ثنائي sofi — bash رقيق → python)
│   ├── substrate/                # الست: taskq · gateway · validate · check · gitflow · schemas
│   │   ├── schemas/              # عقود JSON للـ gateway payloads وevidence blocks
│   │   └── selftest.sh           # PASS 6/6 أو لا شيء
│   └── lib/shamel_tools/         # brain · memdb · tickets(mirror) · routing · gates · doctor …
├── orchestrator/                 # الطبقة الخارجية الموحّدة (§3)
├── .claude/
│   ├── settings.json             # الأحداث السبعة (§2.2)
│   ├── hooks/                    # 7 سكربتات + _common.py
│   └── skills/                   # spine skills (/shamel-boot · /shamel-gate · /shamel-reflect …)
├── cron/shamel.crontab           # المجدوِل الخارجي الوحيد (§2.3)
├── brain/db/                      # حالة runtime (gitignored): tasks.db · brain.db · logs/ · hooks-health.jsonl
└── projects/                     # كل مشروع repo git خاص به — قانون يوم-صفر
```

### 2.5 الحلقة داخل-الجلسة كاملة (تسلسل حدث-بحدث)

```
فتح الجلسة
  └─ SessionStart ─────► حقن: STATE head + التذكرة + digest + صحة doctor        🤖
المستخدم/الـ CEO يكتب أمراً
  └─ UserPromptSubmit ─► لقاح: درس سابق مطابق يُحقن قبل العمل                   🤖
الوكيل يعمل (قد يفوّض subagents بأوامر RCCF)
  ├─ PreToolUse ───────► حجب الخطر (git/env/commit) قبل التنفيذ                 🤖 fail-closed
  ├─ أدوات substrate ──► taskq/check/gitflow — exit codes تسوق القرار           🤖 صفر توكن
  ├─ PostToolUse ──────► التقاط observation + تذكير checkpoint عند العتبة       🤖
  └─ SubagentStop ─────► التقاط حكم الـ subagent + evidence إلى memdb           🤖
إغلاق الشغل
  ├─ /shamel-gate ─────► validate_evidence (ميكانيكي) ثم gatekeeper بسياق نظيف  🤖 + ⚔️
  └─ Stop ─────────────► breadcrumb + compress_session + تذكير gate-proof      🤖
خارج الجلسة (cron)
  └─ doctor ليلي · memdb compact · reflect أسبوعي → LESSONS.md → لقاح الغد      🤖
```

هذه حلقة تعلّم مغلقة فعلياً: **العمل يُلتقط (hooks) → يُقطَّر (reflect المجدول) → يُحقن (اللقاح)** — البند المفقود الوحيد اليوم هو المجدوِل، وسطر cron واحد يغلقه.

---

## 3. الأتمتة الخارجية — orchestrator (`claude -p` + cron)

### 3.1 الدمج الملزم قبل أي تفعيل (fork G6)

نسخة شامل الموحّدة تُجمَّع من أفضل الفرعين (التقرير 04 §ما يُرحَّل، البند 4):

| المكوّن | المصدر المعتمد | لماذا |
|---------|----------------|-------|
| `translator_gateway.py` | نسخة **MAIN** (455 سطراً) | الأغنى |
| `agent_invoker.py` | الحالي (MOCK/live) | مُثبت؛ يُضاف `--model` من routing (أدناه) |
| `ceo_agent.py` | **إنقاذ من MAIN** (untracked، 14.8KB) | موجود في مكان واحد فقط — GAP-03 |
| تاريخ الانتقالات | جدول history من state_db نسخة **WT** (356 سطراً) → يُدمج في taskq | آلة حالات واحدة (§2.4) |
| `tools/` الـ 22 | توحيد الرموز على غرف v6 | إسقاط `bkd_05/uxr_02` |

### 3.2 الحلقة: translator → taskq → invoker → self-healing

```
cron أو يدوي: python3 orchestrator/main.py --cmd "أضف phone_number لجدول users واعرضه في شاشة الملف" --live
   │
   ▼
1) TRANSLATOR (استدعاء نموذج واحد — أو heuristics في MOCK)
   الأمر العامي → payload مهيكل {intent, rooms:[bck,mob], fields:[phone_number], risk:fast-track}
   │  يُفحص ضد os/substrate/schemas/gateway-payload.json (validate.py) — رفض = exit 1، لا تخمين
   ▼
2) TASKQ (حتمي)
   صف لكل غرفة: {id, room:bck, agent:bck-api-engineer, gate:4, state:pending, attempts:0}
   │
   ▼
3) INVOKER — لكل مهمة جاهزة (deps مكتملة):
   claude -p "<RCCF Work Order مولَّد من قالب الوكيل>" --model <من nexus/routing.yaml> \
            --max-turns <من effort class> --allowedTools <القائمة الدنيا من منح الوكيل في registry.yaml> \
            ; timeout مضبوط ; مسار binary مطلق/PATH صريح عند الإطلاق من cron (§2.3) ; الكتابة الذرّية للمخرجات
   (headless: لا منح أذونات تفاعلياً — --allowedTools المعلن شرط تشغيل، لا خيار)
   │
   ▼
4) CHECK (حتمي) — check.py يشغّل linters/tests الحقيقية لمسار المشروع
   exit 0 → taskq: running→completed + evidence block (cmd+exit+آخر أسطر output)
   exit 1 → SELF-HEAL: taskq: failed→pending، attempts+1، رسالة الخطأ تُحقن في prompt المحاولة التالية
             attempts == 3 → circuit breaker (§6.1): crash-dump JSON + تذكرة تصعيد، توقف
   │
   ▼
5) GITFLOW (حتمي، اختياري --commit) — فرع + commit تقليدي بتريلر شامل؛ يرفض force/reset
```

النمط مُثبت اليوم: `MOCK_FAIL_THEN_PASS` يفشل في المحاولة 1 وينجح في 2 — دليل تشغيلي على حلقة self-heal.

### 3.3 متى يُستخدم — وحدوده الملزمة

**يُستخدم لـ:** دفعات Gate-4 خلف عقد Gate-3 **مجمّد** (build conveyor ليلي) · مهام fast-track المصنّفة (نسخ، i18n، حقل غير مالي) · إعادة تشغيل مهام فشلت بأخطاء ميكانيكية · تشغيل regression طويل لا يبرر جلسة حية.

**حدوده (ملزمة، تُفحص كوداً لا وعظاً):**

1. **لا سلطة بوابات:** orchestrator يوصل المهمة إلى «completed + evidence» فقط؛ تقدّم البوابة حصراً عبر `gatekeeper` بسياق نظيف (V2) — المنفّذ لا يقيّم نفسه، والـ pipeline منفّذ. `nexus-binding.yaml` (أدناه) يحصر عمله في Gate 4.
2. **لا مسار deep-audit بلا إشراف:** مال/اعتمادات/auth/PII لا تدخل الـ conveyor الخارجي إلا كمهام مُفتتة من جلسة حية وقّعت التصنيف.
3. **قراءة الـ Nexus إلزامية** (إصلاح خرق «ONLY routing source»):

```yaml
# orchestrator/nexus-binding.yaml — قراءة فقط؛ shamel doctor يفحصه fail-closed
registry: nexus/registry.yaml      # الغرف/الوكلاء — رموز v6 حصراً؛ رمز غريب = رفض الإقلاع
routing:  nexus/routing.yaml       # يقرّر --model و effort لكل claude -p
gates:    nexus/gates.yaml         # نطاق العمل المسموح: gate 4 فقط
scope:    { gates: [4], tracks: [fast-track, gate4-behind-frozen-contract] }
budgets:  { max_tasks: 12, max_model_calls: 40, max_minutes: 90, max_attempts_per_task: 3 }
```

فحص doctor الجديد: `orchestrator rooms ⊆ registry rooms` و`invoker models ⊆ routing models` — أي انحراف يفشل الفحص الليلي.

### 3.4 MOCK vs live

| البعد | MOCK | live |
|-------|------|------|
| توليد الكود | stubs حتمية (`_generate_mock`) | `claude -p` حقيقي بموديل من routing |
| validators | توجيهات `MOCK_*` (نجاح فوري/فشل مقصود) | `check.py` على المشروع الفعلي |
| التكلفة | **صفر API** | مقيّد بـ budgets |
| الاستخدام | CI للأوركسترا نفسها (كل تعديل على orchestrator يمر بـ MOCK run كامل حتى COMPLETED قبل الدمج) · تدريب/عرض · اختبار self-heal | الإنتاج الفعلي للمهام |
| القاعدة | **MOCK هو الوضع الافتراضي**؛ `--live` قرار صريح ومسجَّل في run log | كل run يكتب `{run_id, budget_spent, tasks, verdicts}` إلى `brain/db/logs/orchestrator.jsonl` |

---

## 4. حلقة الـ oracle الخارجية (Gemini desk) — الدور والحدود

**الدور (Teaching VII):** مراجع خارجي استشاري بعقل مختلف — التقارير/المواصفات/نقاط القرار تُعرض عليه بدل مقاطعة البشر. الحلقة: **compose (inline) → sanitize (حذف مفاتيح/أسرار/.env) → condense → push → capture → parse → ingest** (خلاصة + action_items تصير تذاكر taskq).

**الإصلاحات الملزمة قبل اعتباره «مؤتمتاً» (P3):**

1. **سلّم نقل ثلاثي بدل CDP الحصري:** (1) Gemini API مباشرة (مفتاح في env، sanitized فقط) → (2) CDP :9222 كـ fallback يدوي → (3) فشل صريح. لا اعتماد على متصفح مفتوح يدوياً كمسار وحيد.
2. **صدق exit codes:** `shamel oracle status` يعيد **exit ≠ 0 عند تعذّر الاتصال** — نهاية «exit 0 عند الفشل».
3. **التقاط الرد idempotent:** timeout → `oracle capture` يستأنف الالتقاط ولا يعيد النشر (موجود، يُرحَّل كما هو).

**موقعه في الأتمتة وحدوده:**

| البند | القاعدة |
|-------|---------|
| متى يُستدعى آلياً | عند خروج كل بوابة (التقرير يُدفع بالتوازي — **لا يحجب** البوابة) · عند تصعيد عالق · مراجعة أسبوعية مجدولة (§2.3) |
| سلطته | **يستشير ولا يقرّر**: لا يعتمد بوابة (gatekeeper يقرّر)، لا يلمس git، ولا يخاطب المستخدم |
| مخرجاته | action_items → تذاكر taskq عادية تمر بنفس دورة التحقق — نصيحة الـ oracle لا تتجاوز الفحص |
| أمنه | sanitized حصراً — لا أسرار/PII/بيانات إنتاج تغادر الجهاز؛ الـ sanitizer نفسه ضمن selftest |
| الحلقة الملزمة | compose inline → اطلب توجيهاً مفصلاً → **حلّل ونفّذ الرد ذاتياً** — التوقف للبشر فقط عند فعل تدميري/غير قابل للعكس (ADR) |

---

## 5. خط الأنابيب الموحّد end-to-end

النقاط البشرية في الحياة الاعتيادية **ثلاث فقط**: (🧑1) الأمر الأول · (🧑2) ADR لأي فعل غير قابل للعكس · (🧑3) موافقة prod على مسار deep-audit (قابلة للضبط؛ fast-track بلا موافقة). كل ما عداها يجري بلا بشر.

```
🧑1 أمر بشري واحد («ابنِ X» / «أضف حقل Y»)
 │
 │ 🤖 hooks: لقاح الدروس يُحقن قبل أي عمل (UserPromptSubmit)
 ▼
TRANSLATOR ── نموذج واحد يحوّل العامية إلى payload مهيكل ──────────────── 🤖
 │ 🤖 validate.py: schema أو رفض (exit 1) — لا تخمين
 ▼
GATEWAY → TASKQ ── تفتيت إلى مهام بغرف/وكلاء/بوابات ─────────────────── 🤖 حتمي، صفر توكن
 │ 🤖 تصنيف المسار: fast-track ⇒ بوابات 1–3 تُطوى لفحص blueprint واحد
 │                 مال/auth/PII ⇒ deep-audit كامل (unsure ⇒ deep-audit)
 ▼
Gate 0–1  str + res ── مشكلة/متطلبات/Journey Map ──────────────────────── 🤖 وكلاء
 │ ⚔️ gatekeeper بسياق نظيف ضد معايير الدخول الأصلية + validate_evidence — 🤖 fail-closed
 ▼
Gate 2    dsn ── spec مجمّد + taste dials + WCAG ──────────────────────── 🤖 ثم ⚔️
 ▼
Gate 3    arc + dat + sec ── تجميد schema/API/threat-model ────────────── 🤖 ثم ⚔️
 │ 🔮 spec-review (7 steel rules) على طبقة gatekeeper — آلي، تقريره SEV-first
 │ 📤 oracle: التقرير يُدفع بالتوازي (لا يحجب) ─────────────────────────── 🤖
 ▼
Gate 4    BUILD متوازٍ خلف العقد المجمّد (bck · fnt · mob)
 │   المسار أ (جلسة حية): squads في worktrees + hooks ─────────────────── 🤖
 │   المسار ب (خارجي): cron → orchestrator → claude -p لكل غرفة
 │        → check.py → self-heal ×3 → completed+evidence ──────────────── 🤖 كامل بلا بشر
 │ 🤖 gitflow: فرع/commit تقليدي؛ force/reset مرفوضان مسبقاً
 ▼
Gate 5    qa ── تشغيل الحِزم آلياً: coverage ≥90% · perf budget · a11y ── 🤖
 │ ⚔️ حكم PASS/BLOCK واحد من غير المنفّذ + pass^k للمال/PII (V3) ──────── 🤖
 ▼
Gate 6    staging ── CI حقيقي: lint→test→build→scan→deploy→rollback rehearsal 🤖
 │            (workflow فعلي في .github/workflows/ — إغلاق GAP-04؛
 │             sofi gate-check يرفض Gate 6 ما لم يكن الـ workflow موجوداً وأخضر)
 ▼
🧑3 موافقة prod (deep-audit فقط — fast-track يعبر آلياً على أخضر)
 ▼
Gate 7    prod ── Blue/Green + rollback مُختبَر ─────────────────────────── 🤖
 ▼
Gate 8    observe ── SLI/SLO حية + alert⇄runbook 1:1 ───────────────────── 🤖
 │
 └─ 🤖 خرق SLO ⇒ تذكرة Gate-1 تُفتح آلياً ⇒ تعود للمسار من أوله (حلقة مغلقة)

خيوط عرضية دائمة: hooks تلتقط كل شيء 🤖 · doctor ليلي 🤖 · reflect أسبوعي يقطّر
LESSONS 🤖 · budget warden يعدّ الاستدعاءات 🤖 · oracle يستشار عند كل خروج بوابة 🤖
🧑2 يُستدعى فقط إذا صادف المسار فعلاً غير قابل للعكس (drop جدول، حذف بيانات، إنفاق).
```

**المفتاح:** 🤖 = بلا بشر · ⚔️ = تحقق عدائي آلي بسياق نظيف (لا self-grading) · 🔮 = طبقة gatekeeper النموذجية · 🧑 = نقطة بشرية.

---

## 6. Fail-safes — القواطع والميزانيات والتراجع

### 6.1 Circuit breakers

| القاطع | العتبة | الفعل الآلي |
|--------|--------|-------------|
| مهمة فاشلة | 3 محاولات (`attempts == 3` في taskq) | crash-dump JSON (`brain/db/crash/<task_id>.json`: المهمة، المحاولات، الأخطاء الثلاثة، آخر diff) + تذكرة تصعيد إلى سلسلة gtw→brd + **gateway يرفض إعادة enqueue لنفس البصمة** حتى يُحل التصعيد — آلة الحالات المُثبتة لا تُمس؛ القاطع طبقة فوقها |
| run خارجي | تجاوز أي حد في `budgets` (§3.3) | إيقاف نظيف: المهام الجارية تُكمل، لا مهمة جديدة، الحالة NEEDS_HUMAN في run log + notify |
| hooks | فشل ≥3 خلال 24h لنفس الـ hook | WARN في doctor + حقن SessionStart (رصد بلا حجب — GAP-20) |
| oracle | فشل النقل على السلّم الثلاثي | exit ≠ 0 + التذكرة تتقدم بلا استشارة (الـ oracle استشاري — غيابه لا يجمّد الخط) |
| جلسة عالقة | تذكير gate-proof في `Stop` بسقف تصعيد ثابت | لا يتصاعد للأبد (deadlock cap موجود في stop.py — يُرحَّل) |

### 6.2 Budgets (لا استدعاء بلا سقف)

- **داخل الجلسة:** كل Work Order يحمل effort class + call budget + fail-safe stop (المادة 01)؛ `routing.yaml` يقيّد النموذج لكل وكيل؛ `budget warden` يجمّع من runlog/telemetry ويرفع تقرير الهدر أسبوعياً (cron حتمي).
- **خارج الجلسة:** `budgets` في `nexus-binding.yaml` سقف صلب لكل run (مهام/استدعاءات/دقائق)؛ كل `claude -p` بـ `--max-turns` وtimeout؛ MOCK افتراضي.
- **cron:** كل سطر مقيّد ومسجّل؛ الوظيفة النموذجية الوحيدة الدورية (reflect) بسقف 15 turns أسبوعياً — التكلفة الدورية القصوى معروفة سلفاً.

### 6.3 Rollback (طريق العودة قبل طريق الذهاب)

| الطبقة | الآلية |
|--------|--------|
| git | gitflow يرفض force/reset مسبقاً (exit 2) + hook `pre_tool_use` يحجبها في الجلسة الحية · checkpoint «≤1 artifact uncommitted» · كل مشروع repo خاص (قانون يوم-صفر — GAP-01) فالانفجار محصور |
| مهام | `taskq cancel` من أي حالة غير نهائية · جدول history يعيد سرد أي مسار |
| migrations | «migration بلا rollback = مرفوضة» تُفحص ميكانيكياً في Gate 3/4؛ deploy-time migration فقط بعد بروفة rollback على staging data |
| نشر | Blue/Green + rollback مُختبَر (rehearsal شرط خروج Gate 6 يفحصه gate-check) |
| الأتمتة نفسها | **كل قدرة أتمتة لها kill-switch من سطر واحد**: حذف سطر cron · حذف مدخل hook من settings.json · `--live` غيابه = MOCK — إيقاف أي طبقة لا يتطلب فهم الطبقة |

### 6.4 المراقب الليلي (watchdog بلا daemon)

`shamel doctor` الليلي هو خط الدفاع الجامع — يفحص في نبضة واحدة: parity الوكلاء (105↔105↔سجل) · صحة hooks (العدّاد) · مسارات المشاريع (`paths` fail-loud: مسار معدوم = **FAIL** لا صمت — علاج GAP-09) · تطابق orchestrator↔nexus · وجود workflows حين تكون بوابة ≥6 معلنة (علاج GAP-04: **الادعاء يفشل الفحص إذا غاب إنفاذه**) · عمر آخر reflect. أي FAIL → notify + سطر في حقن SessionStart التالي.

---

## 7. خارطة التفعيل — مراحل، لا big bang

كل مرحلة: شرط دخول → تسليم → **برهان خروج قابل للفحص** → kill-switch. لا مرحلة تبدأ قبل برهان سابقتها.

| # | المرحلة | التسليم | برهان الخروج (exit bar) | kill-switch |
|---|---------|---------|--------------------------|-------------|
| 0 | **إنقاذ + مصالحة** (شرط مسبق، خارج هذه الوثيقة) | GAP-01/02/03: git init للمشاريع، توحيد السلالات، انتشال ceo_agent/الأدوات | كل أصل حي في git بسلالة واحدة | — |
| 1 | **النواة داخل-الجلسة** | ترحيل hooks الخمسة + substrate الست + doctor إلى شجرة شامل؛ إعادة تسمية schemas | `selftest` PASS 6/6 + `doctor` PASS + جلسة تجريبية تُظهر الحقن والحجب | حذف مدخلات hooks |
| 2 | **إصلاح حلقة الدماغ** | `paths.py` fail-loud + `checkpoint` يعمل من أي شجرة + hooks تُغذّي memdb فعلاً + hooks-health ledger + الـ hookان الجديدان | `checkpoint` يكتب `head_sha` حقيقياً في STATE لمشروع حي؛ memdb > 50 صفاً بعد أسبوع عمل | كما في 1 |
| 3 | **cron الحتمي** | doctor ليلي + memdb compact + budget أسبوعي + `shamel notify` | 7 ليالٍ متتالية بسجلات ناجحة + إنذار مُختبَر بفشل مصطنع | حذف أسطر cron |
| 4 | **cron النموذجي (reflection)** | `/shamel-reflect` أسبوعي عبر `claude -p` | أول `LESSONS.md` حقيقي مُسند بالتذاكر + درس منه يظهر لقاحاً في جلسة تالية (الحلقة مغلقة) | حذف سطر cron |
| 5 | **orchestrator MOCK موصول بالـ Nexus** | دمج الـ fork (§3.1) + `nexus-binding.yaml` + رموز v6 + فحص doctor الجديد + دمج state_db في taskq | MOCK run كامل حتى COMPLETED يقرأ registry/routing الرسميين؛ CI للأوركسترا = MOCK أخضر | `--live` غير ممنوح أصلاً |
| 6 | **orchestrator live على fast-track** | تفعيل `--live` لفئة fast-track فقط بميزانيات §3.3 | 3 مهام fast-track حقيقية تعبر live→check→evidence→⚔️ gate بلا تدخل؛ سجل الميزانية ضمن السقف | إزالة `--live` (يرتد MOCK) |
| 7 | **oracle مؤتمت** | سلّم النقل الثلاثي (API أولاً) + صدق exit codes + الدفع الآلي عند خروج البوابات + السطر الأسبوعي | استشارة كاملة push→capture→ingest بلا لمسة يد؛ فشل نقل مصطنع يعيد exit ≠ 0 | حذف الاستدعاء من skill البوابة |
| 8 | **CI/CD الحقيقي (البوابات 6–8)** | workflows فعلية lint→test→build→scan→deploy + Blue/Green + بروفة rollback + أول SLI/SLO + قاعدة «خرق SLO يفتح تذكرة Gate-1» ككود | gate-check يرفض Gate 6 بلا workflow أخضر (مُختبَر عمداً)؛ rollback rehearsal موثّق؛ إنذار SLO تجريبي يفتح تذكرة فعلاً | تعطيل الـ workflow |

**منطق الترتيب:** المراحل 1–2 تجعل الجلسة صادقة (تلتقط وتفحص فعلاً) · 3–4 تضيف الزمن (أول أتمتة تجري بلا جلسة مفتوحة — أرخصها أولاً) · 5–6 تضيف اليد الخارجية تحت الحوكمة · 7 تضيف العقل الخارجي · 8 تغلق الحلقة إلى production والمراقبة. كل مرحلة تُطفأ بسطر واحد دون فهم ما فوقها — **الأتمتة تُركَّب كطبقات قابلة للنزع، لا ككتلة**.

---

*نهاية الوثيقة — AUTOMATION.md · شامل / SHAMEL · 2026-07-10*
