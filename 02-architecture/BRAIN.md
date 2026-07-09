# شامل / SHAMEL — العقل والدماغ: معمارية الذاكرة الموحّدة

**الوثيقة:** BRAIN — التصميم الملزم لطبقة الذاكرة في نظام شامل · **التاريخ:** 2026-07-10
**المصادر:** 07-memory-brain-protocols.md · 08-COMPARISON-MATRIX.md (البعد 2) · 09-GAP-ANALYSIS.md (GAP-01/06/08/09/11/12/20) · `company/brain/BRAIN.md` (G3) · `WT/MEMORY.md` · `sofi_tools/memdb.py`
**المبدأ الحاكم:** مصدر حقيقة واحد لكل مستوى · الالتقاط مؤتمت والتقطير مؤتمت (لا «scheduled» بلا مجدوِل) · الكود هو الحقيقة · لا كتابة بلا مالك · flat topology داخل Claude Code — لا daemon داخلي، الأتمتة الخارجية عبر `claude -p` + cron.

---

## 1) المشكلة — ثمانية أنظمة ذاكرة متوازية بلا مصدر حقيقة واحد

التقرير 07 عدّ **8 أنظمة ذاكرة متوازية** تعيش الآن في نفس المساحة، ثلاثة منها جثث بلا شاهد قبر:

| # | النظام | الحالة | العطب الجوهري |
|---|--------|--------|----------------|
| 1 | `MEMORY.md` ×2 (MAIN vs WT) | حيّان متعارضان | md5 مختلف؛ كل خريطة توجّه لجيل آخر — «مصدر الحقيقة» نفسه مزدوج |
| 2 | Project brain الحي (`PRJ-SAKK/_context/`) | حيّ | **خارج أي git** — صفر نسخ احتياطي، وسابقتا فقدان متحققتان (GAP-01) |
| 3 | `company/brain/` (v6) | حيّ نظرياً | org brain مستنسَخ بايت-بايت من `engine/` ثم تباعد صامت |
| 4 | `sessions.jsonl` ×2 | MAIN حيّ (47 جلسة)، WT اختباري | جيلان لنفس الـ breadcrumbs |
| 5 | `brain.db` (memdb FTS5) | مبنيّ، وليد | **صف observations واحد** — بنية ممتازة لم تُملأ قط |
| 6 | ملفات `engine/` الجذرية | ميتة | HANDOFFS/PERSONAS متطابقة بايتياً مع نسخة v6 — أصل مشترك تجمّد |
| 7 | `.opencode/memory/` | ميتة | 4 ملفات jsonl كلها 0 بايت — «bash engine never ran» |
| 8 | Harness memory + claude-mem | حيّ خارجياً | 20 مجلد مشروع لنفس الشجرة؛ تكامل بالصدفة لا بالتصميم |

يُضاف إليها العطبان المنهجيان:
- **جيلا بروتوكولات** (engine 21 ملفاً vs constitution 11 مادة، 8 أزواج diff≠0) بتناقض عقائدي مباشر: hook كل شجرة يحقن دستوراً معاكساً للأخرى (GAP-08) — «انفصام دماغي بحسب مجلد الإقلاع».
- **حلقة reflection نظرية بالكامل** (GAP-11): `/sofi-reflect` بلا مجدوِل، `crontab -l` فارغ، لا `LESSONS.md` لأي مشروع قط، والخلاصة الموثقة: *«الالتقاط مؤتمت جيداً؛ التقطير والتوحيد يدويان بالكامل — الذاكرة تتراكم ولا تتعلّم»*.
- **الدماغ يكذب** (GAP-12): STATE ≠ CONTEXT ≠ الكود (أرقام models/controllers وثلاث روايات للـ stack) — خرق G5، لأن الأرقام تُكتب يدوياً.
- **أدوات عمياء** (GAP-09): `projects_dir()` يفشل صامتاً، `checkpoint` مكسور بنيوياً، `branch`/`head_sha` فارغان في STATE رغم gate 6.

**الحكم الموروث:** تصميم الطبقات الثلاث في `BRAIN.md` (v6) هو «أفضل توصيف ذاكرة في كل الأجيال» (07) — البنية سليمة التصميم، مهترئة التوحيد. شامل لا يعيد اختراع النموذج؛ **يوحّد تجسيده ويؤتمت حلقته المكسورة**.

---

## 2) التصميم — ثلاثة مستويات، مصدر حقيقة واحد لكل مستوى

### 2.1 قانون الطبقات

| المستوى | الموطن الفيزيائي الوحيد | النطاق | العمر | git |
|---|---|---|---|---|
| **Org brain** | `~/Desktop/SHAMEL/brain/org/` | الشركة نفسها: عقيدة، ADRs، دروس معمَّمة | دائم | نعم — ريبو شامل، فرع `main` |
| **Project brain** | `<PRJ-repo>/_context/` | مشروع واحد: state، وقائع، قرارات، تذاكر، دروس | عمر المشروع | نعم — **داخل ريبو المشروع الخاص** (قانون يوم-صفر) |
| **Session memory** | `~/Desktop/SHAMEL/.claude/memory/` | جلسة/تشغيل: breadcrumbs، observations، audit | runtime فقط | **أبداً** (gitignored) |

قواعد صلبة:
- **لا ملف ذاكرة خارج هذه المواطن الثلاثة.** أي ملف حالة/معرفة في مكان آخر = عيب يرصده `shamel doctor`.
- **عزل جذري بين المشاريع** — الـ org brain هو الذاكرة المشتركة الوحيدة، ويحمل عقيدة ودروساً، لا محتوى مشاريع.
- **الحقيقة تتدرج صعوداً فقط:** session → (تخرّج بموجب العقد) → project → (تقطير reflection + قرار ترقية) → org. لا كتابة هابطة.

### 2.2 شجرة الملفات الكاملة

```
~/Desktop/SHAMEL/                          # ريبو git — الإطار نفسه
├── CLAUDE.md                              # عقد السلوك (behavior) — ليس ذاكرة
├── MEMORY.md                              # الفهرس الموجِّه الوحيد — pointers فقط، <200 سطر
├── brain/
│   ├── BRAIN.md                           # هذه المعمارية كقانون منزَّل
│   ├── OWNERS.yaml                        # مصفوفة الملكية: ملف → كاتب وحيد (§7.2)
│   ├── org/
│   │   ├── DECISIONS.md                   # ADR-NNN مؤسسية (معمارية الشركة نفسها)
│   │   ├── EVOLUTION.md                   # خارطة تحسين الإطار
│   │   ├── LESSONS.md                     # LES-NNN معمَّمة، sig-keyed
│   │   ├── PERSONAS.md                    # البشر خلف الـ ids (+ جدول ربط ID↔persona)
│   │   ├── TEAM_STATUS.md                 # ⚙ مولَّد آلياً — لا يُحرَّر يدوياً (§7.4)
│   │   └── HANDOFFS.md                    # تذاكر عمل الإطار (لا المشاريع)
│   ├── templates/                         # قوالب دماغ المشروع — يستنسخها السكافولدر
│   │   ├── STATE.md · CONTEXT.md · DECISIONS.md · HANDOFFS.md
│   │   ├── LESSONS.md · FOUNDATIONS.md · LOCKS.md · FOLDER-MAP.md
│   └── archive/                           # المقبرة المعيارية — كل جيل متقاعد بشاهد قبر
│       ├── README.md                      # بروتوكول الدفن (⛔ + tag + ADR)
│       ├── v5-engine/ · v6-company-brain/ · opencode-memory/ ...
├── .claude/
│   ├── memory/                            # طبقة الجلسة — gitignored بالكامل
│   │   ├── brain.db                       # SQLite FTS5 (observations + sections) — §4.3
│   │   ├── sessions.jsonl                 # سطر لكل جلسة (Stop hook)
│   │   ├── audit.jsonl                    # حجب أمني (PreToolUse guard)
│   │   └── health.json                    # عدّاد أعطال hooks (§7.5)
│   └── hooks/                             # خمسة hooks + _common.py (fail-open + عدّاد)
├── os/
│   ├── bin/shamel                         # الموزّع الوحيد (اسم واحد — يحسم ثنائي sofi، GAP-15)
│   └── shamel_tools/                      # paths · brain · memdb · tickets · reflect · doctor
└── projects/                              # أو خارج الشجرة عبر SHAMEL_PROJECTS_DIR
    └── PRJ-0001/                          # ريبو git مستقل — .git يوم-صفر إلزامي
        ├── .git · .github/ · src/ ...
        └── _context/                      # دماغ المشروع — داخل ريبو المشروع نفسه
            ├── STATE.md                   # working — أين نحن (يُكتب فوقه)
            ├── CONTEXT.md                 # semantic — وقائع append-only
            ├── DECISIONS.md               # procedural — ADRs مع rollback
            ├── HANDOFFS.md                # episodic — التذاكر (الـ bus)
            ├── LESSONS.md                 # procedural — reflection فقط
            ├── FOUNDATIONS.md             # semantic — العقيدة منزَّلة على المشروع
            ├── LOCKS.md                   # working — path claims للفرق المتوازية
            └── _runlog.md                 # working — سطر لكل فعل أداة
```

**حسم مسارات GAP-09:** `shamel_tools.paths` يحلّ الجذر بهذا الترتيب: env `SHAMEL_HOME` → `~/Desktop/SHAMEL` — وإن غاب الاثنان **يفشل صاخباً** (`raise PathsError`, exit≠0)، لا يرجع مساراً معدوماً بصمت أبداً. worktrees تُحَلّ صراحة (`git rev-parse --git-common-dir`) — لا عمى worktree بعد اليوم.

**توصيل الـ hooks في ريبوهات المشاريع (ملزم — طبقة الجلسة لا تعمل بدونه):** الـ harness يحمّل الـ hooks من إعدادات **مجلد الجلسة**، لا من شجرة شامل — وجلسة تُفتح داخل `<PRJ-repo>` (حالة العمل الأساسية، إذ كل مشروع ريبو مستقل بقانون يوم-صفر) لا ترى `SHAMEL/.claude/hooks/` تلقائياً. لذلك السكافولدر (`shamel project init`) **يثبّت التوصيل في كل ريبو مشروع**: يكتب `<PRJ-repo>/.claude/settings.json` بإدخالات الـ hooks الخمسة مشيرة عبر `$SHAMEL_HOME` إلى النسخ الكانونية في `SHAMEL/.claude/hooks/` — **توصيل لا نسخ** (مصدر كود واحد، لا bytes تتباعد — §7.1)؛ البديل المكافئ المقبول: تثبيت user-level في `~/.claude/settings.json` يغطي كل الجلسات. `shamel doctor --brain` يفحص وجود التوصيل في كل مشروع نشط — مشروع بلا توصيل = **FAIL** (§7.6)، وإلا صارت طبقة الجلسة صفر التقاط لجلسات المشاريع وقاعدة §7.5 «قاعدة لا تنمو = hook ميت» ترسّب النظام ببنائه — إعادة إنتاج حرفية لنمط `.opencode/memory` صفر-بايت المدفون في §1.

### 2.3 Frontmatter schema الموحّد

كل ملف دماغ (عدا `STATE.md` — انظر أدناه) يبدأ بـ frontmatter واحد قياسي، تتحقق منه `shamel doctor` بمخطط JSON Schema:

```yaml
---
type: brain            # brain | ticket | lesson | adr        (إلزامي)
mem: semantic          # semantic | episodic | procedural | working  (إلزامي)
prj: PRJ-0001          # أو "org" لملفات brain/org/            (إلزامي)
owner: knw-reflector   # الكاتب الشرعي الوحيد — يطابق OWNERS.yaml    (إلزامي)
updated: 2026-07-10    # يمرَّر من المستدعي — الوكلاء لا يملكون الساعة (إلزامي)
---
```

```json
{ "$id": "shamel://schemas/brain-frontmatter.json",
  "type": "object",
  "required": ["type", "mem", "prj", "owner", "updated"],
  "properties": {
    "type":    {"enum": ["brain", "ticket", "lesson", "adr"]},
    "mem":     {"enum": ["semantic", "episodic", "procedural", "working"]},
    "prj":     {"pattern": "^(PRJ-[0-9A-Z]{4,}|org)$"},
    "owner":   {"pattern": "^([a-z]{3}-[a-z0-9-]+|@(generated|checkpoint|acting-agent|hooks))$"},
    "updated": {"pattern": "^\\d{4}-\\d{2}-\\d{2}$"},
    "last_reflected_tkt": {"pattern": "^TKT-[0-9]{3,}$"}
  },
  "additionalProperties": false }
```

ملاحظتا إحكام (تمنعان رسوب ملفات التصميم ذاته في doctor):
- `owner` يقبل معرّف وكيل **أو** صنف سكربت `@…` — الأصناف الأربعة `@generated`/`@checkpoint`/`@acting-agent`/`@hooks` هي حرفياً أصناف OWNERS.yaml (§7.2)؛ المطابقة frontmatter↔مصفوفة تبقى fail-closed.
- `last_reflected_tkt` **اختياري** (خارج `required`) ومشروع فقط في frontmatter `LESSONS.md` — هو marker حلقة reflection (§5.1)؛ doctor يرفض وجوده في أي ملف آخر.

**`STATE.md` استثناء مقصود:** صيغة `key: value` صرفة بلا frontmatter (تُقرأ بـ parser حتمي، لا YAML lib) — لأنها الملف الذي يُقرأ أولاً في كل turn ويجب أن يبقى أرخص قراءة ممكنة:

```
# STATE — PRJ-0001
title: sakk fintech platform
gate: 4
status: building
priority: HIGH
blockers: none
branch: prj/PRJ-0001
head_sha: 483d355            # ⚙ يكتبه shamel checkpoint — يدوي = خرق
last_route: workhorse
local_domain: sakk.local
local_port: 8801
public_url: none
counts_sha: a1b2c3d          # ⚙ بصمة آخر توليد أرقام (§7.4)
created: 2026-07-01
updated_by: bck-lead
```

**صيغة التذكرة** (بلوكات `## TKT-NNN · gate N` داخل `HANDOFFS.md`) و**صيغة الدرس** (`## LES-NNN` بحقول `sig/mem/situation/what_failed/rule/source`) تُرحَّلان من v6 كما هما — كلتاهما مثبتتان تشغيلياً (19 artifact بوابات حية في PRJ-SAKK) — مع إبقاء الحقول `type:`/`mem:`/`status:`/`sig:` لأنها أساس الاستعلام المهيكل (§4).

### 2.4 `MEMORY.md` — الفهرس الموجِّه: خريطة لا مخزن

**نسخة واحدة** في جذر شامل (وريث نسخة WT — الأحدث والأشمل؛ نسخة MAIN تُقتل — §6). عقدها:
- يجيب سؤالاً واحداً: **«أين أجد X؟»** — pointers فقط، صفر محتوى. السلوك في `CLAUDE.md`، والمحتوى في الملف الهدف (routing ≠ behavior ≠ content).
- ميزانية صلبة: **<200 سطر** — يفحصها doctor. المدخلة التي تنمو تدفع تفاصيلها للملف الهدف.
- سلّم البحث مصرَّح في رأسه: الخريطة → دماغ المشروع النشط → الكود (grep) → `shamel brain query` → الويب (للأدوار الحاملة Web tools، مع cite).
- مالكه الوحيد: أمين المكتبة (`knw-lead` أو وريثه في شامل). مدخلة جديدة = سطر pointer واحد، تُكتب فقط عند نشوء موطن دائم جديد.

### 2.5 خريطة أنواع الذاكرة (أربعة أنواع، أربعة بيوت)

| النوع | السؤال | الملفات | سياسة الضغط |
|---|---|---|---|
| **semantic** | ما الصحيح؟ | `CONTEXT.md` · `FOUNDATIONS.md` · org `PERSONAS.md` | قابل للضغط (caveman) عند >300 سطر |
| **episodic** | ماذا حدث؟ | `HANDOFFS.md` · `_runlog.md` · `sessions.jsonl` | task prose قابل للضغط؛ evidence blocks **أبداً** |
| **procedural** | كيف نتصرف؟ | `DECISIONS.md` · `LESSONS.md` · `EVOLUTION.md` | القواعد وrollback plans **لا تُضغط أبداً** |
| **working** | ما في اليد الآن؟ | `STATE.md` · `LOCKS.md` · `_scratch/` | رخيص، يُكتب فوقه، يُطهَّر عند إغلاق البوابة |

التوحيد يجري باتجاه واحد: **episodic → (reflection) → procedural** — وهذا هو موضوع §5.

---

## 3) دورة الكتابة — متى يُكتب ماذا وأين

### 3.1 القاعدة الفاصلة: contract-driven vs trigger

| المسار | ما يُكتب | المشغّل | الكاتب |
|---|---|---|---|
| **Contract-driven** (كل turn فاعل — لا ينتظر كلمة) | دماغ المشروع: artifact → checkpoint → CONTEXT → STATE → التذكرة التالية | العقد الكوني، خطوة "بعد الفعل" | الوكيل المنفِّذ (ضمن ملكية الملف) |
| **Trigger «تذكّر» / "remember"** | ذاكرة العقيدة/التفضيلات الدائمة: `CLAUDE.md`، `MEMORY.md` (سطر pointer)، harness memory | كلمة «تذكّر» من المستخدم — **المشغّل الوحيد** | أمين المكتبة / الجلسة الرئيسية |
| **Reflection فقط** | `LESSONS.md` (مشروع + org) | مجدوِل §5 — أبداً per-turn، أبداً من المنفِّذ | reflector |
| **Hooks فقط** | طبقة الجلسة كلها (`brain.db`، `sessions.jsonl`، `audit.jsonl`) | أحداث الـ harness — الوكلاء لا يكتبون هنا إطلاقاً | الكود الحتمي |
| **Generated فقط** | `TEAM_STATUS.md`، أرقام العدّ في الدماغ، `FOLDER-MAP.md`، `head_sha` | `shamel doctor --emit` / `shamel checkpoint` / السكافولدر | السكربت (⚙) |

قاعدة مرافقة: **تغيير سياسة يلمس ملفه المالك الواحد، لا يُنثَر عبر الملفات.**

### 3.2 نصف العقد الكوني — القراءة قبل الفعل والكتابة بعده

```
# قبل الفعل (لا بداية عمياء):
shamel sync PRJ-0001                    # git orient: fetch + الفرع + يرفض شجرة قذرة
1. STATE.md      → gate · branch · head_sha · blockers
2. HANDOFFS.md   → تذكرتي (consumes · expected · route)
3. CONTEXT.md    → الوقائع     4. DECISIONS.md → القرارات الملزمة
5. LESSONS.md    → لا تكرار لفشل معروف (+ org LESSONS مرة كل جلسة)
6. الـ artifact المجمّد المستهلَك — غير مجمّد؟ ارفض صعوداً وتوقف

# بعد الفعل (غير الملتزَم = غير مرئي):
1. الـ artifact في مساره الدقيق
2. shamel checkpoint PRJ-0001 "feat: ..."     # commit في ريبو المشروع + تحديث head_sha آلياً
3. append CONTEXT.md "- [gate N] fact [src]"  # (+ DECISIONS.md إن كان لا-رجعة، مع rollback)
4. تذكرة التالي في HANDOFFS.md                # route + expected + متطلب evidence
```

فرقان جوهريان عن v6:
1. **`head_sha` لم يعد كتابة يدوية:** `shamel checkpoint` يلتزم في ريبو المشروع **ثم يكتب `head_sha`/`branch` في STATE.md بنفسه** — الحقل الفارغ الذي فضحه التقرير 07 يستحيل بنيوياً، لأن الكاتب هو السكربت.
2. **`checkpoint` بلا `.git` محلي = فشل fail-closed** (exit≠0 + رسالة «project repo missing — run shamel project init»)، لا تسلّق صامت لريبو الإطار (علاج GAP-09 الحرفي).

### 3.3 حقيقة التنفيذ (G3) والدليل (V1) — شرطا دخول الذاكرة

- واقعة بلا إسناد (`file:line` / SHA / URL / brain-ref) لا تدخل `CONTEXT.md` — تُكتب `[unverified]` وتقف.
- تذكرة `done` بلا **evidence block** (أمر+ناتج+exit code | file:line | diff/SHA) يرفضها `shamel gate-check` fail-closed — الترحيل الحرفي لـ `validate_evidence()`.
- **الأرقام لا تُكتب يدوياً:** كل عدّ في الدماغ (models، controllers، اختبارات) يولَّد بـ `shamel brain facts <PRJ>` ويُختم بـ `counts_sha` في STATE — قاعدة «الكود هو الحقيقة» التي تقتل GAP-12.

---

## 4) الاسترجاع — مهيكل، grep-first، سياق مقسوم

### 4.1 السلّم (قف عند أول إصابة — كل درجة أغلى من سابقتها)

```
0. MEMORY.md (الخريطة)          → أين يعيش X؟                    ~صفر توكن
1. shamel brain query            → استعلام frontmatter مهيكل        صفر توكن نموذج
2. rg/grep على الدماغ والكود     → Python locates, model judges     شبه صفر
3. shamel mem search (FTS5)      → observations + sections           ~400 توكن/إصابة
4. قراءة section مستهدف          → byte-offset لا الملف كاملاً
5. الويب                         → أدوار Web tools فقط + verify + cite
```

**لا vector DB — قرار متعمد يُرحَّل:** الدماغ صغير، مهيكل، grep-able؛ frontmatter + ripgrep يتفوق على الـ embeddings دقةً وكلفةً وقابلية تدقيق على هذا الحجم (ADR-009 في org DECISIONS — يُعاد تثبيته في ADR شامل).

### 4.2 `shamel brain query` — الاستعلام المهيكل

```bash
shamel brain query PRJ-0001 --status open --gate 4 --to bck-lead     # تذاكر مفتوحة
shamel brain query PRJ-0001 --type lesson --grep "migration"          # دروس بموضوع
shamel brain query org --type adr --since 2026-06-01                  # ADRs مؤسسية
```

المنفّذ حتمي (`shamel_tools.tickets.query` — substring case-insensitive على حقول الـ frontmatter/التذاكر)؛ الناتج جدول `file:line` مضغوط. النموذج يستدعي، لا يمسح.

### 4.3 طبقة `brain.db` — الـ FTS5 (يُرحَّل مخطط memdb.py كما هو)

```sql
CREATE TABLE observations (            -- الالتقاط الخام: PostToolUse/Stop hooks
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT NOT NULL, source TEXT, kind TEXT,
  summary TEXT, body TEXT, project TEXT);
CREATE VIRTUAL TABLE observations_fts USING fts5(summary, body);

CREATE TABLE sections (                -- فهرس عناوين ملفات الدماغ
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  file TEXT NOT NULL, heading TEXT,
  byte_start INTEGER, byte_end INTEGER,   -- استرجاع مقطع لا ملف: ~12k → ~400 توكن
  sha256 TEXT, summary TEXT, project TEXT);
CREATE VIRTUAL TABLE sections_fts USING fts5(heading, summary);
```

قاعدة واحدة في `SHAMEL/.claude/memory/brain.db` معمودة `project` — الجلسات المفتوحة داخل ريبو مشروع تحلّها hooks عبر `SHAMEL_HOME` **بشرط توصيل الـ hooks المثبّت في ريبو المشروع** (الفقرة الملزمة في §2.2 — الحلّ عبر `SHAMEL_HOME` يجيب عن المسار فقط؛ التحميل نفسه يضمنه التوصيل، ويفحصه doctor). **LLM لا يلمس مسار الكتابة** — كل دوال memdb تخزين/فهرسة/تجميع نص حتمي.

### 4.4 تقسيم السياق — الحقن المدرّج (لا dump)

| اللحظة | ما يُحقن | السقف |
|---|---|---|
| SessionStart | رأس STATE (gate/branch/head_sha/blockers) + التذكرة المفتوحة + digest من brain.db | **1000 توكن** (سقف صلب في الـ hook) |
| UserPromptSubmit | مطابقة FTS topical: دروس/observations ذات صلة بنص الطلب («لقاح الدروس») | ~300 توكن |
| عند الطلب | مقطع section عبر byte-offset، لا الملف | حسب المقطع |
| أبداً | حقن `CONTEXT.md`/`HANDOFFS.md` كاملة تلقائياً | — |

`.claudeignore` يبقى الدرع: vendor/node_modules/أرشيف المقبرة مستبعدة من أي auto-context — نمط الـ ~80% خفض المثبت في v6.

---

## 5) حلقة التعلّم — reflection مجدولة ومؤتمتة فعلاً

**التشخيص الموروث:** الالتقاط مؤتمت، التقطير يدوي — «الذاكرة تتراكم ولا تتعلّم» (GAP-11). شامل يغلق الحلقة بثلاثة مشغّلات، كلها متوافقة مع flat topology (لا daemon داخلي):

### 5.1 الدين الانعكاسي (reflection debt) — العدّاد الحتمي

```bash
shamel reflect debt PRJ-0001
# → debt: 12 done-tickets منذ آخر reflection (marker: last_reflected_tkt في frontmatter LESSONS.md)
```

يُحسب بعدّ تذاكر `status: done` في `HANDOFFS.md` بعد آخر `TKT` مقطَّر (مسجَّل في frontmatter `LESSONS.md` كـ `last_reflected_tkt: TKT-041`). صفر LLM.

### 5.2 المشغّلات الثلاثة — بالضبط كيف

**المشغّل 1 — cron خارجي (المجدوِل الحقيقي، أسبوعي):** سطر crontab يثبّته `shamel doctor --install-cron` (ويفحص وجوده دورياً):

```cron
# SHAMEL reflection — أحد كل أسبوع 22:00 + doctor يومي 08:00
0 22 * * 0  flock -n /tmp/shamel-reflect.lock  $HOME/Desktop/SHAMEL/os/bin/reflect-cron.sh  >> $HOME/Desktop/SHAMEL/brain/db/logs/cron.log 2>&1
0 8  * * *  $HOME/Desktop/SHAMEL/engine/bin/shamel doctor --brain --quiet || notify-send "SHAMEL doctor FAIL"
```

`reflect-cron.sh` (حتمي، ~30 سطراً):

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$HOME/Desktop/SHAMEL"
for prj in $(engine/bin/shamel projects --active --ids); do
  debt=$(engine/bin/shamel reflect debt "$prj" --number)
  [ "$debt" -lt 5 ] && continue                      # عتبة: 5 تذاكر done
  claude -p "/reflect $prj" \
      --permission-mode acceptEdits --max-turns 20 \
      --allowedTools "Read,Grep,Glob,Edit,Write,Bash(engine/bin/shamel *)"
  engine/bin/shamel doctor --lessons "$prj"              # تحقق فوري fail-closed (§5.3)
done
```

هذا هو نمط شامل المعياري للأتمتة: **الخارج يجدول، `claude -p` ينفّذ جلسة headless، الحتمي يتحقق.**

**المشغّل 2 — إغلاق البوابة (contract-driven):** exit bar لكل بوابة يتضمن بنداً: `reflection debt ≤ 5` — يفحصه `shamel gate-check` ميكانيكياً. دين أعلى = البوابة لا تتقدم حتى يجري `/reflect`. بهذا يستحيل مشروع يصل gate 6 بلا `LESSONS.md` (الحالة الموثقة في PRJ-SAKK).

**المشغّل 3 — التذكير داخل الجلسة (fail-open):** الـ Stop hook يحسب الدين؛ عند ≥ العتبة يسجّل نداءً يُحقن في SessionStart التالي: `«reflection debt: 12 — شغّل /reflect PRJ-0001»`. تذكير متصاعد مسقوف (نمط `_REMINDER_CAP=5` المثبت في stop.py v6) — لا يحجب أبداً.

### 5.3 عقد الدرس — مقتبس لتذكرة، idempotent، بلا self-grading

مهارة `/reflect <PRJ>` (وريثة `/sofi-reflect`) تقرأ HANDOFFS منذ الـ marker وتقطّر:

```md
## LES-007
- **sig:** migration-rollback-untested-g4     # مفتاح idempotency — sig معروف = تخطٍّ
- **mem:** procedural
- **date:** 2026-07-12
- **situation:** TKT-038 — migration للحقل X وصلت review بلا rollback مجرَّب.
- **what_failed:** الـ rollback كُتب ولم يُشغَّل؛ فشل على staging.
- **rule:** لا تُقبل migration قبل تشغيل rollback فعلياً وإرفاق ناتجه exit 0.
- **source:** TKT-038 · commit 9f3ab21
```

ضمانات الحلقة:
- **الكاتب الوحيد** لـ LESSONS هو الـ reflector — أي كتابة أخرى يرصدها doctor (ملكية §7.2).
- **التحقق العدائي لا الذاتي:** `shamel doctor --lessons` (حتمي، fail-closed) يتحقق أن كل `source:` يشير إلى TKT/commit **موجود فعلاً**، وأن كل `sig` فريد، وأن الـ frontmatter صالح — الـ reflector لا يصحّح نفسه؛ فشل الفحص يفتح تذكرة escalation.
- **الترقية للعقيدة قرار لا أتمتة:** درس متكرر عبر ≥2 مشروع يُقترح للترقية إلى `brain/org/LESSONS.md` أو الدستور — reflection **تقترح** (تذكرة إلى الـ boardroom)، لا تعيد كتابة العقيدة ذاتياً أبداً.
- الدروس تُقرأ في كل boot (خطوة 5 من عقد القراءة) + تُحقن topically عبر FTS — فتُغلق الدائرة: تعلّمنا → لا نكرر.

---

## 6) الهجرة — خريطة نقل كل ذاكرة قائمة إلى شامل

**الترتيب ملزم** (خيط الترابط في 09): إنقاذ ← مصالحة ← نقل ← دفن ← تحقق. لا دفن قبل الانتشال.

### المرحلة 0 — الإنقاذ (اليوم، قبل أي بند آخر — GAP-01/03)

```bash
cd ~/Desktop/Lorka/projects/PRJ-SAKK
# الأسرار قبل التاريخ (MIGRATION §0-8): تطهير اعتمادات browser-eyes.sh → env أولاً، ثم فحص نظيف
gitleaks detect --source . --no-git          # يجب exit 0 قبل أي add — ما يدخل التاريخ يبقى فيه
git init -b main
git add -A ':!_scratch'
gitleaks detect --source . --staged          # حارس ثانٍ fail-closed
git commit -m "rescue: full snapshot incl. _context brain"
git remote add origin <remote> && git push -u origin main
```

*(التسلسل الملزم الكامل — snapshot tar، `.gitignore` القياسي، مراجعة staged — في `PROJECT-STRUCTURE.md` §2.3؛ هذه الفقرة مرآة مختصرة له.)*

الدماغ الحي `_context/` يدخل أول commit مع الكود. (إنقاذ ceo_agent/translator/stash يجري بموازاته — خارج نطاق هذه الوثيقة.)

### المرحلة 1 — جدول النقل (نظام-بنظام، بأمر تحقق لكل صف)

| # | المصدر القائم | الوجهة في شامل | الإجراء | التحقق |
|---|----------------|------------------|---------|---------|
| 1a | `WT/MEMORY.md` (6339B — الأشمل، بأقسام write-triggers) | `SHAMEL/MEMORY.md` | **الأساس المعتمد** — نقل + تحديث المسارات إلى شجرة شامل | `wc -l < MEMORY.md` < 200 + كل pointer يحلّ (`doctor --map`) |
| 1b | `MAIN/MEMORY.md` (3322B — يوجّه لجيل engine الميت) | `brain/archive/main-memory-md/` | **يُقتل** — أرشفة بشاهد قبر، لا دمج (خرائطه تشير لموتى) | `test ! -f ~/Desktop/Lorka/MEMORY.md` بعد المصالحة |
| 2 | `PRJ-SAKK/_context/` (الدماغ الحي) | `<PRJ-SAKK repo>/_context/` — يبقى في مكانه، لكن **داخل ريبو المشروع** (مرحلة 0) | إصلاح المحتوى: ملء `branch`/`head_sha` عبر أول `shamel checkpoint`؛ توليد الأرقام بـ `brain facts`؛ إضافة `LESSONS.md`/`FOUNDATIONS.md`/`LOCKS.md` الغائبة من القوالب؛ **إعادة تصنيف gate 6 → 4/5** (GAP-04) | `shamel doctor --brain PRJ-SAKK` أخضر: STATE كامل الحقول + frontmatter صالح + repo فيه remote |
| 3a | `company/brain/BRAIN.md` + `templates/` (6) | `brain/BRAIN.md` (هذه الوثيقة تخلفه) + `brain/templates/` (8 — يضاف FOLDER-MAP + LOCKS) | نقل مع إعادة كتابة المسارات وقواعد §3/§5 الجديدة | doctor يتحقق أن السكافولدر ينسخ 8/8 |
| 3b | `company/brain/org/` (6 ملفات حية) | `brain/org/` | نقل git-history-preserving (`git mv` ضمن فرع المصالحة)؛ إضافة frontmatter §2.3 لكل ملف؛ `TEAM_STATUS.md` يتحول لمولَّد | md5 قبل/بعد للنص الحر + `doctor --frontmatter` أخضر |
| 3c | `company/brain/org/archive-v5/` | `brain/archive/v5-law/` | ينتقل كما هو — مجمّد read-only | عدد الملفات متطابق |
| 4a | `MAIN/.claude/memory/sessions.jsonl` (47 جلسة حقيقية) | `brain.db.observations` (source=`legacy-sessions`) ثم الملف إلى `brain/archive/` | **استيراد لا نسخ**: `shamel mem import-jsonl --kind session <file>` | `sqlite3 brain.db "SELECT COUNT(*) FROM observations WHERE source='legacy-sessions'"` = 47 |
| 4b | `WT/.claude/memory/sessions.jsonl` (7 أسطر test) | — | حذف (بيانات اختبار معلنة) | شاهد قبر في ADR الهجرة |
| 5 | `WT/.claude/memory/brain.db` (صف واحد) | `SHAMEL/.claude/memory/brain.db` | يُنقل كنواة القاعدة الوحيدة؛ الـ hooks الخمسة تبدأ ملأه فعلياً | عدّاد أسبوعي في doctor: rows يجب أن تنمو (قاعدة «قاعدة لا تنمو = hook ميت») |
| 6 | `MAIN/engine/{HANDOFFS,PERSONAS,DECISIONS,EVOLUTION,TEAM_STATUS}.md` | `brain/archive/v5-engine-brain/` | **دفن بعد برهان التطابق**: HANDOFFS/PERSONAS متطابقان بايتياً مع نسخة org (07) — نسخة org هي الوريث؛ EVOLUTION تباعد (60 سطراً) → diff يُراجَع يدوياً وتُلتقط الأسطر الفريدة قبل الدفن | `diff engine/HANDOFFS.md brain/org/HANDOFFS.md` (على الأصول قبل الأرشفة) + ADR دفن |
| 7 | `MAIN/.opencode/memory/` (4 ملفات × 0 بايت) | — | حذف مباشر — لا شيء يُنقل من العدم؛ سطر في شاهد قبر `.opencode` | `find .opencode/memory -size +0c` فارغ (برهان ما-قبل-الحذف) |
| 8 | Harness memory + claude-mem (خارجي) | يبقى خارجياً — **حدود تكامل معلنة** | سطران في `MEMORY.md`: (أ) `mem-search` للاستعلام عن جلسات ماضية؛ (ب) قاعدة: harness memory لا يُستشهد به كـ ground truth للدماغ — التخرج عبر §3 فقط | pointer rows موجودة + doctor لا يعدّه نظام ذاكرة داخلياً |
| 9 | `engine/protocols/` (21) vs `constitution/` (11) | دستور شامل (وثيقة البروتوكول المرافقة) | constitution 00–10 هي الصياغة الوحيدة؛ يُلتقط **intake-orchestration** (wear-the-hierarchy) كمادة جديدة قبل دفن engine — يحسم التناقض العقائدي (GAP-08) | مادة مرقمة موجودة + `engine/` كله في archive |

### المرحلة 2 — الدفن المعياري (نمط archive-v5 معمَّماً)

كل جيل متقاعد: (1) snapshot/tag git (`archive/<name>-final`)، (2) نقل إلى `brain/archive/<name>/` مع `README.md` شاهد قبر (ماذا كان، لماذا دُفن، ماذا انتُشل منه، ADR المرجع)، (3) سطر في `brain/org/DECISIONS.md`. **لا ترك أحياء-أموات** — المجلد الذي لا شاهد له إما حي مُدار أو عيب doctor.

### المرحلة 3 — التحقق الختامي

```bash
shamel doctor --brain --strict
# يفشل إن: وُجد ملف ذاكرة خارج المواطن الثلاثة · بقي md5 مكرر بين شجرتين
# · pointer ميت في MEMORY.md · مشروع بلا .git/remote · frontmatter غير صالح
```

---

## 7) الضمانات — لا ازدواج، لا كتابة بلا مالك، هيلث تشيك دوري

### 7.1 لا ازدواج — «نسخة واحدة لكل concern» مُسلَّكة

- **فاحص الازدواج:** `doctor --dupes` يحسب sha256 لكل ملفات الذاكرة المعروفة + يمسح المسارات القديمة (engine/، .opencode/، company/brain خارج شامل) — أي تطابق بايتي بين ملفين حيين، أو أي ملف ذاكرة حي في مسار متقاعد = **FAIL** (يحاكي فحص parity الذي أثبت نفسه في `sofi doctor` 105↔105).
- **خريطة توجيه واحدة، قاعدة FTS واحدة، دماغ مشروع واحد داخل ريبو المشروع** — التعدد نفسه صار عيباً قابلاً للرصد، لا حالة مقبولة.
- الترقية عبر الطبقات نسخ-بالتقطير لا نسخ-بالاستنساخ: الدرس يصعد للـ org **معاد صياغته معمَّماً** مع `source:` يشير للأصل — لا bytes مكررة تتباعد لاحقاً (قاتل نمط engine↔org).

### 7.2 لا كتابة بلا مالك — `brain/OWNERS.yaml`

```yaml
# ملف → كاتبه الشرعي الوحيد + مشغّله. doctor يطابقه مع frontmatter `owner:` لكل ملف.
version: 1
org:
  brain/BRAIN.md:           {owner: brd-ceo,           trigger: adr}        # العقيدة — تغييرها قرار ADR، لا أتمتة
  brain/org/DECISIONS.md:   {owner: knw-historian,     trigger: adr}
  brain/org/LESSONS.md:     {owner: knw-reflector,     trigger: reflection}
  brain/org/EVOLUTION.md:   {owner: brd-chief-of-staff, trigger: contract}
  brain/org/PERSONAS.md:    {owner: knw-lead,          trigger: contract}
  brain/org/HANDOFFS.md:    {owner: "@acting-agent",   trigger: contract, schema: ticket}
  brain/org/TEAM_STATUS.md: {owner: "@generated",      trigger: "shamel doctor --emit"}
  brain/templates/*:        {owner: knw-lead,          trigger: contract}   # تعديل قالب = تعديل عقد الدماغ
  MEMORY.md:                {owner: knw-lead,          trigger: "تذكّر | new-durable-location"}
project:   # ينطبق على كل PRJ
  _context/STATE.md:        {owner: "@checkpoint",     trigger: contract}   # head_sha/branch سكربت فقط
  _context/CONTEXT.md:      {owner: "@acting-agent",   trigger: contract, mode: append-only}
  _context/DECISIONS.md:    {owner: "@acting-agent",   trigger: irreversible, requires: rollback}
  _context/HANDOFFS.md:     {owner: "@acting-agent",   trigger: contract, schema: ticket}
  _context/LESSONS.md:      {owner: knw-reflector,     trigger: reflection}
  _context/FOUNDATIONS.md:  {owner: "@generated",      trigger: "scaffold (shamel project init)"}
  _context/LOCKS.md:        {owner: "@acting-agent",   trigger: "claim/release"}
  _context/FOLDER-MAP.md:   {owner: "@generated",      trigger: "scaffold + re-emit"}   # §7.4
  _context/_runlog.md:      {owner: "@hooks",          trigger: harness-events}
session:
  .claude/memory/*:         {owner: "@hooks",          trigger: harness-events}   # الوكلاء ممنوعون
```

**قاعدة الاكتمال (ملزمة):** المصفوفة تغطي كل ملف في شجرة §2.2 واحداً-لواحد — ملف ذاكرة بلا صف مطابق = FAIL (§7.6 صف 2)، ولا مالك افتراضي ضمني؛ إضافة ملف ذاكرة جديد للشجرة تستلزم صفّه هنا في نفس الـ commit (يفحصه `doctor --brain`: شجرة §2.2 ↔ OWNERS.yaml تطابق تام، على نمط parity 105↔105).

الإنفاذ ثلاثي: (أ) frontmatter `owner:` يطابق المصفوفة (doctor، fail-closed في gate-check)؛ (ب) الـ PreToolUse guard يحذّر عند Write/Edit على ملف ذاكرة من غير مالكه ويعدّ المخالفة في `health.json` (رصد لا حجب — الجلسة لا تُكسر)؛ (ج) `mode: append-only` لـ CONTEXT يُفحص بـ diff حتمي عند checkpoint (إعادة كتابة سطر قديم = تحذير + عدّاد).

### 7.3 التحقق العدائي — الذاكرة لا تصحّح نفسها

- كاتب الدرس ≠ فاحصه (`doctor --lessons` حتمي fail-closed) — §5.3.
- تذكرة done بلا evidence block لا تعبر gate-check (`validate_evidence` fail-closed) — §3.3.
- **spot-check دوري (V5):** الـ gatekeeper يسحب عيّنة من التذاكر خلف كل PASS ويقارن الادعاء بالدليل — انحراف = تذكرة escalation.

### 7.4 «الكود هو الحقيقة» — الأرقام المولَّدة

`shamel brain facts <PRJ>` يعدّ (models/controllers/tests/migrations/coverage) من القرص ويكتب بلوك `<!-- generated:counts -->` في CONTEXT + `counts_sha` في STATE. doctor يعيد العدّ ويقارن — انحراف = **الدماغ يكذب** = FAIL. `FOLDER-MAP.md` عقد مولَّد من السكافولدر، لا وثيقة يدوية.

### 7.5 fail-open مرصود — عدّاد أعطال الـ hooks (علاج GAP-20)

الـ hooks تبقى fail-open (فشل الذاكرة لا يكسر الجلسة) **لكن ما عاد صامتاً**: كل استثناء داخل hook يُلتقط في `_common.py` ويزيد عدّاداً في `.claude/memory/health.json` (`{hook, count, last_error, last_ts}`). doctor اليومي يرفعه؛ عدّاد >0 لأسبوع = تذكرة إلزامية. **قاعدة النمو:** brain.db التي لا تكبر أسبوعاً والجلسات تجري = hook ميت = FAIL (يقتل نمط «بنية ممتازة بصف واحد»).

### 7.6 `shamel doctor --brain` — الهيلث تشيك الدوري (cron يومي §5.2)

| الفحص | الوضع |
|---|---|
| كل ملف ذاكرة في المواطن الثلاثة فقط؛ لا ملف حي في مسار متقاعد | FAIL |
| frontmatter صالح schema §2.3 + `owner:` يطابق OWNERS.yaml | FAIL |
| STATE.md: كل المفاتيح موجودة و`head_sha`/`branch` **غير فارغين** | FAIL |
| كل `_context/` داخل ريبو git له remote + آخر commit ≤ آخر تعديل ملف | FAIL |
| توصيل hooks شامل مثبّت لكل مشروع نشط (`.claude/settings.json` في ريبو المشروع أو user-level — §2.2) | FAIL |
| LESSONS: sig فريدة، `source:` TKT/SHA موجود فعلاً | FAIL |
| MEMORY.md <200 سطر، pointers تحلّ كلها، لا بلوكات محتوى | FAIL |
| لا ازدواج sha256 بين ملفات ذاكرة حية (§7.1) | FAIL |
| reflection debt لكل مشروع نشط ≤ 5 + سطر cron مثبّت | WARN→FAIL عند البوابة |
| brain.db: integrity_check + نمو أسبوعي + health.json عدّادات = 0 | WARN (أسبوع = FAIL) |
| `counts_sha` يطابق إعادة العدّ (§7.4) | FAIL |

`--strict` يرفع كل WARN إلى FAIL — وهو الوضع الإلزامي في CI وفي أي `gate-check`.

---

## خلاصة التصميم في سطر

**ثلاث طبقات بموطن فيزيائي واحد لكل طبقة، خريطة توجيه واحدة، كتابة بمالك وعقد، استرجاع مهيكل grep-first بلا vector، والتقطير مؤتمت بثلاثة مشغّلات (cron خارجي + بوابة + تذكير) — والصحة كلها تحت `shamel doctor` الذي يجعل الازدواج والصمت والكذب عيوباً قابلة للفشل، لا عادات قابلة للتراكم.**
