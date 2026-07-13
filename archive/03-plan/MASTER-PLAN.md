# شامل / SHAMEL — الخطة الكبرى (MASTER-PLAN)

**الإصدار:** 1.0 · **التاريخ:** 2026-07-10 · **الحالة:** خطة تنفيذ ملزمة — تقود البناء والترحيل من أول أمر إلى التشغيل الكامل
**المصادر الحاكمة:** `PRD.md` (FR/NFR/G/RSK) · `ARCHITECTURE.md` (P1–P10 · ADR-001..005) · `BRAIN.md` · `PROTOCOL.md` · `AUTOMATION.md` (§7) · `PROJECT-STRUCTURE.md` · `08-COMPARISON-MATRIX.md` · `09-GAP-ANALYSIS.md` (GAP-01..20)
**الوثيقة الشقيقة:** `MIGRATION.md` — مصير كل طبقة قائمة، خطوة بخطوة، مع rollback لكل خطوة.
**الجذر المستهدف:** `~/Desktop/SHAMEL/` — ريبو git مستقل جديد (ADR-004: قطيعة سلالية عن Lorka؛ Lorka يبقى أرشيفاً مرجعياً قراءة-فقط).

---

## 0) كيف تُقرأ هذه الخطة

1. **12 مرحلة مرقّمة (Phase 0 → Phase 11)** بترتيب ملزم مستمد من خيط الترابط في تحليل الفجوات: *إنقاذ → مصالحة → تأسيس → توحيد (محرّكات/وكلاء/عقل) → طبقة الجلسة → مصنع → أول مشروع → أتمتة خارجية → دفن → قبول وتشغيل*. لا مرحلة تبدأ قبل استيفاء بوابة خروج سابقتها المعلنة في اعتمادياتها.
2. **كل بند يحمل إسناده** بين قوسين: `FR-xx` من الـ PRD، `GAP-xx` من تحليل الفجوات، `ADR-00x` من المعمارية، أو `<وثيقة>§`.
3. **الجهد نسبي** — S (جلسة عمل واحدة تقريباً) · M (عدة جلسات) · L (عمل ممتد متعدد الجلسات) — لا تواريخ.
4. **قاعدة إغلاق المرحلة (V2):** المرحلة لا تُعلن منتهية إلا باجتياز معايير قبولها الميكانيكية (أوامر بexit code) **ثم** حكم عدائي fresh-context من فاحص غير منفّذها؛ UNKNOWN حكم مشروع → تصعيد (`PROTOCOL.md` §4.2).
5. **قواعد أمان عرضية (تسري على كل المراحل):**
   - tag إشاري قبل لمس أي طبقة: `pre-shamel/<layer>` (تفصيلها في `MIGRATION.md` §0).
   - محظور مطلقاً: `git reset --hard` · `git push --force` · `git stash drop` قبل ADR · أي حذف قبل snapshot مبصوم (RSK-01/02، `PROTOCOL.md` D8).
   - كل قرار لا-رجعة = سطر ADR في `brain/org/DECISIONS.md` (NFR-03).
   - أي ازدواج جديد يظهر أثناء التنفيذ = defect يُسجَّل ويُغلق قبل تقدم المرحلة (P1، FR-34).

### 0.1 جدول المراحل

| # | المرحلة | الهدف بسطر | الجهد | تعتمد على | الفجوات التي تُغلق |
|---|---------|------------|-------|-----------|---------------------|
| 0 | الإنقاذ | صفر أصول فريدة خارج VCS — اليوم، قبل أي شيء | M | — | GAP-01 · GAP-03 · جزء GAP-13 |
| 1 | المصالحة | سلالة git واحدة في Lorka + قتل الدستور المزدوج | M | 0 | GAP-02 · جزء GAP-08 · GAP-19 |
| 2 | التأسيس | ريبو `~/Desktop/SHAMEL/` بالهيكل القانوني + الدستور + الـ Nexus | M | 1 | GAP-17 · جزء GAP-15/08 |
| 3 | توحيد المحرّكات | `shamel` واحد + `shamel_tools` واحدة + آلة حالات واحدة | L | 0، 2 | GAP-06 · GAP-09 · GAP-15 |
| 4 | توحيد الوكلاء | جرد قانوني واحد، spawnables مولَّدة، كانون personas واحد | L | 2، 3 | GAP-07 · GAP-10 · GAP-16 · GAP-18 |
| 5 | توحيد العقل | دماغ ثلاثي الطبقات بموطن واحد لكل طبقة + memdb مغذّى | M | 2، 3 | GAP-12 · جزء GAP-08/11 |
| 6 | الأتمتة داخل الجلسة | hooks الـ 7 + skills الـ 13 + الأوامر المغربلة | M | 3، 5 | GAP-05 · GAP-20 |
| 7 | مصنع المشاريع | `shamel new` بقانون يوم-صفر + folder-map/facts + بروتوكول الاستيراد | M | 3، 5، 6 | GAP-01 (بنيوياً) · جزء GAP-09 |
| 8 | ترحيل PRJ-SAKK | أول مشروع شرعي في المصنع — مُعاد التصنيف، دماغه صادق | M | 0، 7 | GAP-04 · GAP-12 · GAP-13 |
| 9 | الأتمتة الخارجية | cron حقيقي + reflection + orchestrator (MOCK→live) + oracle | L | 3–6، 8 | GAP-11 |
| 10 | التقاعد والدفن | كل جيل ميت في `archive/` بشاهد قبر مبصوم | M | 0، 3–9 | GAP-14 |
| 11 | التشغيل الكامل والقبول | G-01..G-12 كلها خضراء + CI/CD حقيقي + الإعلان التشغيلي | M | الكل | إغلاق خريطة التغطية كاملة |

---

## Phase 0 — الإنقاذ (Rescue): الأصول الفريدة إلى git اليوم

**الهدف:** لا يبقى بايت فريد ذو قيمة خارج نظام تحكم بالإصدارات — «الإنقاذ لا ينتظر أحداً» (`09-GAP-ANALYSIS.md` §خيط الترابط، PRD §7.1). تُنفَّذ في مواقع الأصول الحالية (Lorka)، لا في SHAMEL — البناء يأتي لاحقاً.

### Workstreams

| # | العمل | التفصيل | الإسناد |
|---|-------|---------|---------|
| 0.1 | **R1 — PRJ-SAKK إلى git** | التسلسل الملزم حرفياً من `PROJECT-STRUCTURE.md` §2.3: snapshot tar خارج الشجرة (بلا vendor/node_modules) → **تطهير الأسرار قبل أول `git add`** (اعتمادات `browser-eyes.sh:13-14` → env؛ `gitleaks detect --no-git` نظيف) → `.gitignore` القياسي → `git init -b main` → مراجعة `--cached --stat` → commit إنقاذ بترايلر → remote خارجي أو mirror محلي bare على وسيط ثانٍ | GAP-01 · FR-40 (سابقة) · GAP-13 |
| 0.2 | **R2 — إنقاذ fork الـ orchestrator في MAIN** | فرع إنقاذ `rescue/g6-main` في ريبو Lorka يلتزم: `ceo_agent.py` (14.8KB — موجود حصراً هناك untracked) + `translator_gateway.py` (455 سطراً) + `orchestrator.db` الحي | GAP-03 · ADR-001-أ |
| 0.3 | **R3 — كنوز G1 إلى git** | إدخال `MAIN/.opencode/tools/` الـ 114 سكربت + `skills/qa/browser-eyes` (بعد نزع الاعتمادات — شرط FR-70) + gate checklists 0–8 إلى فرع إنقاذ `rescue/g1-assets` | GAP-03 · مصفوفة §3 بنود 10–12 |
| 0.4 | **تثبيت الـ stash فرعاً** | `git branch rescue/stash-teardown stash@{0}` — يحفظ teardown-backup (3368 ملفاً) كفرع عادي **دون** المساس بالـ stash نفسه؛ لا `stash drop` قبل ADR في Phase 1 | GAP-03 · RSK-02 |
| 0.5 | **بصمات ما-قبل** | tags إشارية: `pre-shamel/main-head` و`pre-shamel/wt-head` + ملف جرد `rescue/INVENTORY.md` (ما أُنقذ، أين، sha256 للـ tar) | MIGRATION §0 |

### التسليمات
ريبو PRJ-SAKK حي بremote/mirror · فرعا إنقاذ `rescue/g6-main` و`rescue/g1-assets` · فرع `rescue/stash-teardown` · `rescue/INVENTORY.md` · نسخة tar مبصومة على وسيط ثانٍ.

### معايير القبول (ميكانيكية)
```bash
git -C ~/Desktop/Lorka/projects/PRJ-SAKK log --oneline | wc -l          # ≥ 1
git -C ~/Desktop/Lorka/projects/PRJ-SAKK remote -v | wc -l              # ≥ 1 (أو mirror مسجَّل في STATE)
gitleaks detect --source ~/Desktop/Lorka/projects/PRJ-SAKK --no-git     # exit 0
git -C ~/Desktop/Lorka cat-file -e rescue/g6-main:main-orchestrator/ceo_agent.py   # exit 0 (المسار حسب لقطة الإنقاذ)
git -C ~/Desktop/Lorka ls-tree -r rescue/g1-assets --name-only | grep -c 'tools/'  # ≥ 110
git -C ~/Desktop/Lorka branch --list 'rescue/stash-teardown' | wc -l    # = 1
git -C ~/Desktop/Lorka stash list | wc -l                                # لم ينقص (الـ stash لم يُمس)
sha256sum -c rescue/INVENTORY.sha256                                     # exit 0 (الـ tar سليم على الوسيط الثاني)
```

**الاعتماديات:** لا شيء — هذه نقطة الصفر المطلقة.
**المخاطر:** RSK-01 (ضياع قبل الاكتمال — التخفيف: تنفيذ فوري، ممنوع أي `checkout/clean` قبل إتمامها) · تسرّب سر إلى تاريخ SAKK (التخفيف: gitleaks حارسان — قبل الـ staging وعليه — 0.1).
**الجهد:** M.

---

## Phase 1 — المصالحة (Reconciliation): سلالة واحدة، دستور واحد

**الهدف:** إنهاء «ثلاث حقائق git» و«انفصام الدستور بحسب مجلد الإقلاع» في Lorka قبل أن يُبنى شيء فوقها (GAP-02، Q1 في PRD §7.3).

### Workstreams

| # | العمل | التفصيل | الإسناد |
|---|-------|---------|---------|
| 1.1 | فرع مصالحة | اعتماد `origin/main` مرجعاً؛ فرع `reconcile/unify` يعيد زرع الحمولة الفريدة من `prj/PRJ-SAKK` (23 أمام) و`main` المحلي (9 أمام) عليه بـ merge/cherry-pick — **لا rebase مدمّر للتاريخ المنشور** | GAP-02 · R4 |
| 1.2 | حسم تصادمات العقيدة | CLAUDE.md وMEMORY.md وhooks: نسخة WT (الأنضج) تفوز؛ كل حسم يدوي = سطر ADR | GAP-08 · FR-14 |
| 1.3 | تفكيك الأتمتة المضادة | `MAIN/.claude/hooks/session_start.py` (يحقن الجيل الميت) يُعطَّل بإزالة إدخاله من `settings.json` في فرع المصالحة — الملف يبقى للأرشيف | AUTOMATION §1.3 N1 |
| 1.4 | حزمة hygiene | allow-rules الخاملة · hook غير المسجّل `user_prompt_submit.py` في MAIN · مراجع `opencode.json` الميتة · `projects/README.md` المشير لمسار v5 — commit واحد | GAP-19 |
| 1.5 | مصير الـ stash | بعد اكتمال 1.1–1.2: مقارنة فرع `rescue/stash-teardown` بالنتيجة؛ الفريد يُلتقط، ثم ADR يوثّق جواز `stash drop` (التنفيذ الفعلي في Phase 10) | GAP-03 · RSK-02 |

### التسليمات
فرع `reconcile/unify` مدموج في `main` ومدفوع لـ origin · ADRs الحسم · Lorka بنسخة CLAUDE/MEMORY/hooks واحدة.

### معايير القبول
```bash
git -C ~/Desktop/Lorka rev-list --left-right --count origin/main...main | awk '{print $1+$2}'   # = 0 بعد الدمج والدفع
find ~/Desktop/Lorka -maxdepth 2 -name MEMORY.md | wc -l                                        # = 1
grep -rn 'engine/tooling' ~/Desktop/Lorka/.claude/settings.json                                 # لا نتيجة (N1 مفكّك)
grep -c '^## ADR-' ~/Desktop/Lorka/company/brain/org/DECISIONS.md                               # زاد بعدد قرارات الحسم
```

**الاعتماديات:** Phase 0 (لا مصالحة فوق أصول غير منقذة).
**المخاطر:** RSK-02 (حسم خاطئ يضيع حمولة — التخفيف: فرع معزول + الفروع الإنقاذية باقية + ADR لكل حسم).
**الجهد:** M.

---

## Phase 2 — التأسيس: ريبو شامل والهيكل القانوني

**الهدف:** `~/Desktop/SHAMEL/` موجود كريبو git بremote من commit#1 (P4 مطبَّق على الإطار نفسه)، بالشجرة القانونية والدستور الكامل والمصدر الآلي الرباعي.

### Workstreams

| # | العمل | التفصيل | الإسناد |
|---|-------|---------|---------|
| 2.1 | ولادة الريبو | `git init -b main` + `.gitignore` (يستثني `projects/` و`.worktrees/` و`*.db`) + `.claudeignore` (درع السياق) + remote خارجي + commit#1 | ADR-004 · P4 · FR-62 |
| 2.2 | الشجرة القانونية | إنشاء الهيكل حرفياً من `ARCHITECTURE.md` §2: `core/` (CONSTITUTION + constitution/ + nexus/ + rooms/ + gates/checklists/) · `engine/` (bin/ + shamel_tools/ + scanners/ + selftest/) · `brain/` (BRAIN.md + org/ + db/ + templates/) · `.claude/` · `archive/` · `projects/` · `.worktrees/` | ARCHITECTURE §2 |
| 2.3 | **ADR-006 — حسم تعارضات المسارات بين وثائق التصميم الست** | قبل أي نسخ: قرار واحد يحسم الاختلافات المرصودة — (أ) موقع الموزّع: `engine/bin/shamel` (ARCHITECTURE/PROTOCOL) لا `os/bin/` (PRD/BRAIN/AUTOMATION)؛ (ب) موطن الـ runtime: `brain/db/` gitignored (ARCHITECTURE) يوحّد `.claude/memory/` (BRAIN) و`.shamel/` (AUTOMATION)، والسجلات في `brain/db/logs/`؛ (ج) اسم موديول مخططات substrate: `schemas.py` (ARCHITECTURE) لا `schemadb.py`؛ (د) ملف الجدولة الوحيد: `cron/shamel.crontab` (PROTOCOL §9.4/AUTOMATION §2.3) و`shamel automation install/status` (FR-31) يعملان عليه لا على `cron.d/` منفصل؛ (هـ) عدد أحداث hooks الرسمي = 7 (الخمسة المرحّلة + PreCompact + SubagentStop). الوثائق المخالفة تُصحَّح بcommit واحد | PROTOCOL §التحكيم · AUTOMATION §2.2/2.3 · GAP-15 (منع فخ دلالي جديد) |
| 2.4 | الدستور 00–11 | ترحيل المواد 00–10 من v6 (المادتان 02/03 حرفياً — FR-22/23) + **كتابة المادة 11** (intake-orchestration: wear-the-hierarchy، leaf-spawn one hop، شرعية الـ skills محسومة نصاً) | FR-20 · مصفوفة §3 بند 14 |
| 2.5 | الـ Nexus الرباعي | `registry.yaml` + `routing.yaml` (aliases فقط) + `gates.yaml` (9 بوابات كاملة الحقول + tracks) + **`models.yaml` الجديد** (طبقة alias الوحيدة) + `pins.json` فارغ مهيأ + `bus/` (ticket-schema + escalation) | FR-50/52/60 · GAP-17 |
| 2.6 | ملفات القمة | `SHAMEL.md` (هوية النظام بدقيقتين) · `CLAUDE.md` (pointers مضغوطة) · `MEMORY.md` (وريث نسخة WT، <200 سطر، مسارات محدَّثة) · `archive/README.md` (بروتوكول الدفن) | FR-14 · BRAIN §2.4 · ADR-001-ج |
| 2.7 | تسجيل ADR-001..006 | القرارات المعمارية الخمسة من ARCHITECTURE + ADR-006 أعلاه، في `brain/org/DECISIONS.md` من اليوم الأول | NFR-03 |

### التسليمات
ريبو SHAMEL حي بremote · دستور 12 مادة · nexus رباعي + models.yaml · MEMORY/CLAUDE/SHAMEL.md · سجل ADR مؤسَّس.

### معايير القبول
```bash
git -C ~/Desktop/SHAMEL remote -v | wc -l                                    # ≥ 1
ls ~/Desktop/SHAMEL/core/constitution/*.md | wc -l                           # = 12
grep -rn 'claude-[a-z]*-[0-9]' ~/Desktop/SHAMEL/core/nexus/ --include='*.yaml' | grep -v models.yaml | wc -l   # = 0  (FR-60)
python3 - <<'EOF'                                                            # الرباعي يُحلَّل
import yaml,sys
for f in ['registry','routing','gates','models']:
    yaml.safe_load(open(f'/home/es3dlll/Desktop/SHAMEL/core/nexus/{f}.yaml'))
EOF
wc -l < ~/Desktop/SHAMEL/MEMORY.md                                           # < 200 (FR-14)
grep -l 'wear-the-hierarchy' ~/Desktop/SHAMEL/core/constitution/11-*.md      # موجود (FR-20)
grep -rn 'os/bin/shamel\|\.shamel/\|schemadb' ~/Desktop/Lorka/.claude/worktrees/org-rooms-100/_scratch/shamel/*.md | wc -l   # = 0 بعد commit تصحيح الوثائق (2.3)
```

**الاعتماديات:** Phase 1 (مصادر المحتوى موحّدة).
**المخاطر:** نسخ محتوى قبل حسم ADR-006 يزرع ازدواج مسارات جديداً (التخفيف: 2.3 يسبق 2.4–2.6 إلزامياً).
**الجهد:** M.

---

## Phase 3 — توحيد المحرّكات: نقطة دخول واحدة، مكتبة واحدة، آلة حالات واحدة

**الهدف:** `engine/bin/shamel` يخلف نقاط الدخول الثماني (5 منها باسم `sofi`)، و`taskq` يخلف التطبيقات الستة المتوازية لإدارة المهام (ADR-002، GAP-06).

### Workstreams

| # | العمل | التفصيل | الإسناد |
|---|-------|---------|---------|
| 3.1 | `shamel_tools/` الموحّدة | دمج ثلاثي المصادر بخريطة ARCHITECTURE §3.3: `sofi_tools` الـ 24 موديلاً (نواة الأحياء core/nexus/brain/net) + substrate الست (`taskq·gitflow·check·validate·gateway·registry`) + pipeline G6 الموحّد؛ الغلاف bash→python يموت — الموزّع Python خالص | ADR-002 · مصفوفة §3 بنود 15/17/18 |
| 3.2 | حزمة إعادة التسمية | `registry.py` (substrate) → `schemas.py` · الماسحات `sofi_scan/sofi_verify` → `shamel_scan/shamel_verify` نسخة واحدة في `engine/scanners/` (يموت التطابق البايتي مع G2) · لا ملف باسم `sofi*` داخل الجذر | FR-05 · FR-81 · GAP-15 |
| 3.3 | `taskq` آلة الحالات الوحيدة | `pending→assigned→running→completed|failed` + جدول `history` مدموج من `state_db.py` (نسخة WT 356 سطراً)؛ `HANDOFFS.md` مرآة تولَّد بـ `shamel taskq sync-handoffs` — parity «taskq↔HANDOFFS» فحص مسمّى في doctor | AUTOMATION §2.4 · ARCHITECTURE §4-❸ |
| 3.4 | `paths.py` fail-loud | سلّم حل صريح (`SHAMEL_HOME`/`SHAMEL_PROJECTS_DIR` → `~/Desktop/SHAMEL/...`) + استثناء صاخب عند الغياب + وعي worktrees (`git rev-parse --git-common-dir`) | FR-42 · GAP-09 · PROJECT-STRUCTURE §0 |
| 3.5 | `checkpoint` fail-closed | commit في ريبو المشروع + كتابة `head_sha/branch` في STATE آلياً؛ «no brain to checkpoint» = فشل exit≠0 لا تحذير | FR-11/43 · BRAIN §3.2 |
| 3.6 | `gate-check` بطبقتيه | `validate_evidence()` fail-closed + فحص artifacts قابلة للتشغيل (بوابة 6: workflow موجود وله run أخضر + rollback مُتدرَّب) + `validate_no_skip()` + `validate_room_boundary()` | FR-23/51 · PROTOCOL §3/§5 |
| 3.7 | `doctor` المعمَّم + `selftest` | يرث فحوص v6 (parity/YAML/مسارات) ويضيف: كشف الازدواج لأي concern · rescue-scan · مطابقة الأتمتة · بصمات التوليد · عدّاد أعطال hooks · parity route/gate المولَّدة · `--brain` (فحوص BRAIN §7.6)؛ `selftest --json` للطبقة الحتمية | FR-34 · NFR-04 |
| 3.8 | pipeline G6 الموحّد | `shamel_tools/pipeline/`: `translator.py` (نسخة MAIN 455) + `invoker.py` (MOCK/live، `--allowedTools` إلزامي) + `ceo.py` (المنقَذ) + `state.py` (تاريخه في taskq)؛ رموز غرف v6 حصراً؛ **يقرأ `core/nexus/*.yaml` فقط** — أي جدول غرف مضمّن محذوف | FR-32 · GAP-03 · AUTOMATION §3.1 |
| 3.9 | oracle/domain/tunnel | ترحيل الموديولات الثلاثة؛ oracle بسلّم النقل الثلاثي (API → CDP → فشل صريح) + exit≠0 عند الفشل (التفعيل الآلي في Phase 9) | FR-33/45 |

### التسليمات
`engine/bin/shamel` يعمل بسطح الأوامر الموحّد (ARCHITECTURE §3.3) · `selftest` PASS · `doctor` PASS على الهيكل · pipeline موحّد بوضع MOCK جاهز.

### معايير القبول
```bash
~/Desktop/SHAMEL/engine/bin/shamel selftest --json | python3 -c "import json,sys; d=json.load(sys.stdin); sys.exit(0 if d['pass'] else 1)"
find ~/Desktop/SHAMEL -path '*/archive' -prune -o -name 'sofi*' -type f -print | wc -l    # = 0 (FR-05/G-03)
grep -rn 'rooms *=\|ROOM_CODES\|bkd_05\|uxr_02' ~/Desktop/SHAMEL/engine/shamel_tools/pipeline/ | wc -l   # = 0 (FR-32)
# اختبار سلبي fail-loud (FR-42):
python3 -c "import os; os.environ.pop('SHAMEL_HOME',None); from shamel_tools.core import paths; paths.projects_dir()" ; echo $?   # ≠ 0 برسالة صريحة عند غياب الجذر
# اختبار سلبي checkpoint (FR-11):
~/Desktop/SHAMEL/engine/bin/shamel checkpoint PRJ-GHOST "test: probe" ; echo $?          # ≠ 0 «project repo missing»
# اختبار سلبي الازدواج (FR-34): زرع تنفيذي ثانٍ مؤقت ثم:
~/Desktop/SHAMEL/engine/bin/shamel doctor ; echo $?                                       # ≠ 0 ويسمّي الازدواج
md5sum ~/Desktop/SHAMEL/engine/scanners/*.py | awk '{print $1}' | sort | uniq -d | wc -l  # = 0 (لا توائم بايتية)
```

**الاعتماديات:** Phase 2 (الشجرة والـ Nexus) · Phase 0 (كود G6 المنقَذ).
**المخاطر:** إعادة كتابة imports تكسر أوامر موروثة بصمت (التخفيف: selftest + سطح CLI يُختبر أمراً-أمراً في جلسة قبول) · دمج fork يرسّخ النسخة الأفقر (التخفيف: خريطة المصادر المعتمدة في AUTOMATION §3.1 ملزمة).
**الجهد:** L.

---

## Phase 4 — توحيد الوكلاء: جرد واحد، توليد حتمي، كانون واحد

**الهدف:** إنهاء الجرود الخمسة: ملف قانوني واحد لكل وكيل في `core/rooms/`، spawnable مولَّد مبصوم، personas مربوطة بجدول (ADR-003).

### Workstreams

| # | العمل | التفصيل | الإسناد |
|---|-------|---------|---------|
| 4.1 | 15 غرفة بـ CHARTERs | `core/rooms/00-boardroom … 14-gateway` بالقالب الخماسي (mission/members/interfaces/room-bar/escalation) — خريطة الـ 15 رسمية (Q3) | FR-01 · GAP-16 |
| 4.2 | الملفات القانونية الـ 105 | دمج ثلاثي لكل وكيل: frontmatter آلي (id/room/route-alias/tools/web/success_metric) + حوكمة G4 السداسية (`authority:`) + persona + Operating Contract + RCCF — بالبنية الحرفية في ARCHITECTURE §3.2 | FR-02/53 · GAP-07 |
| 4.3 | `personas.yaml` | جدول الربط الوحيد agent-id ↔ persona-id ↔ الاسم الكانوني العربي-السوري (Q4) + aliases الكوانين المتقاعدة؛ استكمال فجوات fnt/qa/obs/brd بpersonas جديدة بنفس القالب السداسي | FR-04 · GAP-15/16 |
| 4.4 | `agents build` + `pins.json` | مولّد حتمي spec→spawnable (`.claude/agents/<id>.md`) + بصمات SHA-256؛ تحرير spawnable يدوياً يكسر doctor؛ جرد D (stubs) لا يُنسخ إطلاقاً | FR-02 · ADR-003 |
| 4.5 | `agents lint` fail-closed | يرفض: ملفاً بلا `tools:` صريحة · `model:` حرفياً (aliases فقط) · محارف دخيلة CJK (درس 14/68) · اسماً بشرياً حراً خارج personas.yaml؛ منح الويب من registry حصراً (21 منحة نمطاً) | FR-03 · GAP-10 · NFR-10 |
| 4.6 | ملء `rooms/*/tools/` | توزيع الـ 114 سكربت المنقَذة (R3) على غرفها (التسمية أصلاً على مخطط v6) — نهاية README-placeholder؛ `bash -n` نظيفة كلها | FR-81 · GAP-18 |
| 4.7 | حسم GTW | GTW = مشغّلو الـ Nexus حصراً؛ محتوى org-rooms GTW-06 (API Gateway الخارجي) يُعاد توزيعه على `arc-integration-architect`/`bck-integration-engineer`/`sec-authn-engineer` | FR-05-ج · GAP-15 |
| 4.8 | checklists البوابات | `core/gates/checklists/gate-0..8.md` المنقَذة من G1 مربوطة بمداخل gates.yaml | FR-50 · مصفوفة §3 بند 12 |

### التسليمات
105 ملفاً قانونياً · 105 spawnable مولَّدة · personas.yaml كامل · rooms/tools ممتلئة · pins.json مبصوم · agentlint في doctor.

### معايير القبول
```bash
ls ~/Desktop/SHAMEL/core/rooms/ | wc -l                                          # = 15 (FR-01)
~/Desktop/SHAMEL/engine/bin/shamel agents build && git -C ~/Desktop/SHAMEL diff --exit-code .claude/agents/   # التوليد حتمي (FR-02)
# اختبار سلبي: تعديل يدوي لأي spawnable ثم doctor → exit ≠ 0 (بصمة مخالفة)
~/Desktop/SHAMEL/engine/bin/shamel agents lint ; echo $?                          # = 0 (FR-03)
grep -rL '^tools:' ~/Desktop/SHAMEL/core/rooms/*/agents/*.md | wc -l              # = 0
grep -L 'authority:' ~/Desktop/SHAMEL/core/rooms/*/agents/*.md | wc -l            # = 0 (FR-53)
python3 -c "import yaml; yaml.safe_load(open('/home/es3dlll/Desktop/SHAMEL/core/nexus/personas.yaml'))"       # (FR-04)
find ~/Desktop/SHAMEL/core/rooms/*/tools -type f -name '*.sh' | wc -l             # ≥ 110 (FR-81)
find ~/Desktop/SHAMEL/core/rooms/*/tools -name '*.sh' -exec bash -n {} +          # exit 0
grep -c 'WebSearch' ~/Desktop/SHAMEL/.claude/agents/*.md | grep -v ':0' | wc -l   # يطابق منح registry بالضبط
```

**الاعتماديات:** Phase 2 (registry/routing) · Phase 3 (أدوات build/lint/doctor) · Phase 0 (الأدوات المنقَذة).
**المخاطر:** RSK-03 (تحرير spawnables يدوياً يعيد GAP-07 — التخفيف: pins + doctor في CI) · دمج personas يخلط الكوانين (التخفيف: personas.yaml مصدر الربط الوحيد + مراجعة عدائية لعينات).
**الجهد:** L.

---

## Phase 5 — توحيد العقل: ثلاث طبقات، مالك لكل ملف، أرقام مولَّدة

**الهدف:** خلافة أنظمة الذاكرة الثمانية بثلاثة مواطن (org/project/session)، بملكية مُسلَّكة وأرقام لا تُكتب يدوياً (BRAIN.md كاملة).

### Workstreams

| # | العمل | التفصيل | الإسناد |
|---|-------|---------|---------|
| 5.1 | قانون العقل | `brain/BRAIN.md` (تنزيل وثيقة التصميم قانوناً) + القوالب الثمانية في `brain/templates/` (+FOLDER-MAP +LOCKS على قوالب v6 الستة) | FR-10 · BRAIN §2 |
| 5.2 | ترحيل org brain | `company/brain/org/` الستة → `brain/org/` بحفظ التاريخ + إضافة frontmatter §2.3 لكل ملف + `TEAM_STATUS.md` يتحول مولَّداً (`@generated`) | BRAIN §6 صفوف 3a–3c |
| 5.3 | `OWNERS.yaml` | مصفوفة الملكية كاملة (BRAIN §7.2) بتغطية واحد-لواحد لشجرة الذاكرة؛ doctor يطابق frontmatter↔المصفوفة fail-closed | BRAIN §7.2 · GAP-08 |
| 5.4 | memdb موحّد | `brain/db/brain.db` (مخطط FTS5 يُرحَّل كما هو) + استيراد `sessions.jsonl` MAIN الـ 47 كـ observations بمصدر `legacy-sessions`؛ نسخة WT الاختبارية تُحذف بسطر ADR | FR-13 · BRAIN §6 صفوف 4a/4b/5 |
| 5.5 | «الكود هو الحقيقة» | `shamel brain facts <PRJ>` (سكربت عدّ يكتب بلوك مولَّداً + `counts_sha`) + `shamel brain-audit` يقارن ويفشّل الانحراف | FR-12 · GAP-12 |
| 5.6 | LESSONS بصيغة sig | صيغة `LES-NNN·sig·situation·what_failed·rule·source` + `doctor --lessons` (كل source يشير TKT/SHA موجوداً، sig فريدة) — التغذية المجدولة في Phase 9 | FR-15 · BRAIN §5.3 |
| 5.7 | فحوص `doctor --brain` | جدول BRAIN §7.6 كاملاً (المواطن الثلاثة، frontmatter، STATE كامل الحقول، توصيل hooks، ازدواج sha256، نمو brain.db، counts_sha) | BRAIN §7.6 |

### التسليمات
`brain/` كامل (قانون + org مرحَّل + قوالب 8 + OWNERS) · brain.db بـ 47 observation موروثة · brain facts/brain-audit يعملان · doctor --brain مسلَّك.

### معايير القبول
```bash
sqlite3 ~/Desktop/SHAMEL/brain/db/brain.db "SELECT COUNT(*) FROM observations WHERE source='legacy-sessions'"   # = 47 (BRAIN §6-4a)
ls ~/Desktop/SHAMEL/brain/templates/ | wc -l                                    # = 8
~/Desktop/SHAMEL/engine/bin/shamel doctor --brain ; echo $?                     # = 0
find ~/Desktop/SHAMEL -name MEMORY.md | wc -l                                   # = 1 (FR-14)
# اختبار سلبي (FR-12): تحرير رقم يدوياً في STATE مشروع تجريبي ثم:
~/Desktop/SHAMEL/engine/bin/shamel brain-audit PRJ-TEST ; echo $?               # ≠ 0 ويسمّي الحقل
python3 -c "import yaml; y=yaml.safe_load(open('/home/es3dlll/Desktop/SHAMEL/brain/OWNERS.yaml')); assert y['version']==1"
```

**الاعتماديات:** Phase 2 (الشجرة) · Phase 3 (memdb/doctor tooling).
**المخاطر:** ترحيل org brain يفقد تاريخ git (التخفيف: نقل ضمن فرع بحفظ التاريخ + md5 قبل/بعد للنص الحر — BRAIN §6-3b) · frontmatter جديد يكسر ملفات قديمة (التخفيف: schema JSON في doctor يُختبر على الملفات المرحَّلة قبل الاعتماد).
**الجهد:** M.

---

## Phase 6 — الأتمتة داخل الجلسة: الحُرّاس السبعة والمهارات الـ 13

**الهدف:** نسخة hooks واحدة في الوجود (7 أحداث) بعدّاد أعطال مرئي، وpalette واحدة (GAP-05/20).

### Workstreams

| # | العمل | التفصيل | الإسناد |
|---|-------|---------|---------|
| 6.1 | ترحيل الخمسة | hooks WT v6.1 (guard/orientation/vaccine/bands/breadcrumbs) بنمط `$CLAUDE_PROJECT_DIR` — النسخة الوحيدة؛ session_start يضاف له سطر صحة doctor الليلي | FR-30 · AUTOMATION §2.2 |
| 6.2 | الجديدان | `pre_compact.py` (لقطة توجيه قبل ضغط السياق) + `subagent_stop.py` (التقاط أحكام subagents كصفوف `delegation` — وقود reflection وV5) | AUTOMATION §2.2 |
| 6.3 | `_common.py` + عدّاد الأعطال | fail-open يبقى، وكل استثناء يُسجَّل (`record_hook_failure`)؛ ≥3 أعطال/24h = WARN في doctor + حقن SessionStart | GAP-20 · FR-30 |
| 6.4 | settings.json السبعة | المقطع الحرفي من AUTOMATION §2.2 (7 أحداث) | AUTOMATION §2.2 |
| 6.5 | skills الـ 13 | spine 6 + power 7 بأسماء `shamel-*`؛ لا مرايا 107 | FR-62/82 |
| 6.6 | الأوامر المغربلة | ≤15 أمراً قيّماً من الـ 54 (gate-check/deploy/parallel-build/security-sweep…) بفحص مراجع آلي (درس dangling الـ 100% في G1) | FR-82 · GAP-05 |
| 6.7 | قياس ميزانية الحقن | عدّاد توكن في hook الـ orientation ≤1000 + تسجيل القياس | G-09 · FR-30 |

### التسليمات
`.claude/hooks/` (7+_common) · settings.json · 13 skill · ≤15 أمراً · قياس حقن موثّق.

### معايير القبول
```bash
python3 -c "import json; h=json.load(open('/home/es3dlll/Desktop/SHAMEL/.claude/settings.json'))['hooks']; assert len(h)==7"
ls ~/Desktop/SHAMEL/.claude/skills | wc -l                                      # = 13، وكلها shamel-*
ls ~/Desktop/SHAMEL/.claude/commands | wc -l                                    # ≤ 15 (FR-82)
# اختبار حي (FR-30): أمر خطر (git reset --hard) داخل جلسة تجريبية → يُحجب فعلياً ويُسجَّل في audit
# اختبار سلبي (GAP-20): إفشال hook متعمد (خطأ syntax مؤقت) → يظهر في عدّاد doctor خلال الفحص التالي
test "$(wc -c < ~/Desktop/SHAMEL/brain/db/orientation-budget.log)" -gt 0        # قياس ≤1000 مسجَّل
```

**الاعتماديات:** Phase 3 (doctor/memdb) · Phase 5 (الدماغ الذي تحقنه الـ hooks).
**المخاطر:** RSK-09 (fail-open يخفي الانهيار — التخفيف: 6.3) · hooks لا تُحمَّل في جلسات المشاريع (التخفيف: توصيل ريبو المشروع في Phase 7 — BRAIN §2.2).
**الجهد:** M.

---

## Phase 7 — مصنع المشاريع: يوم-صفر قانوناً

**الهدف:** `shamel new` ذرّي fail-closed ينتج مشروعاً مولوداً مُصدَّراً، وشكل قانوني يفحصه CI مستقل داخل كل مشروع (PROJECT-STRUCTURE كاملة).

### Workstreams

| # | العمل | التفصيل | الإسناد |
|---|-------|---------|---------|
| 7.1 | `shamel new` | الخطوات الـ 13 (PROJECT-STRUCTURE §3.2): حل الجذر fail-loud → الشجرة القانونية (بلا `src/`؛ `frontend/` بـ ADR-000 فقط) → `.gitignore/.gitattributes` → دماغ 7 ملفات (+LESSONS فارغاً) → `_context/features/` → docs الثمانية + FOLDER-MAP مولَّد → deploy/tests skeletons → CI + سكربتا الفحص standalone → **git init + pre-commit (gitleaks+conventional) + commit#1** → remote أو `(pending)` → domain register؛ فشل أي خطوة = تراجع كامل (trap) | FR-40/41/44 · GAP-01 |
| 7.2 | folder-map + facts | `shamel folder-map [--check]` (عقد مولَّد، تحريره يفشل CI) + `shamel facts` (كتلة `facts:` في STATE) + النسختان standalone `.github/shamel/{folder_map,facts}.py` بختم `SHAMEL_CHECKS_VERSION` وdoctor يكشف انحراف النسخ | FR-12/41 · PROJECT-STRUCTURE §7.1 |
| 7.3 | `projects --verify` | لكل مشروع: `.git` + remote (أو mirror مسجَّل) + `_context/` ملتزَم + توصيل hooks — fail-closed في doctor | G-05 · FR-40 · BRAIN §2.2 |
| 7.4 | توصيل hooks للمشاريع | السكافولدر يكتب `<PRJ>/.claude/settings.json` مشيراً عبر `$SHAMEL_HOME` للنسخ الكانونية — توصيل لا نسخ | BRAIN §2.2 (البند الملزم) |
| 7.5 | بروتوكول الاستيراد | `shamel import scan` (كشف stack من الـ locks + عدّ + secret-scan → تقرير JSON هو مصدر الدماغ الوحيد) + مراحل الاستيراد الست | PROJECT-STRUCTURE §6 |
| 7.6 | domain/tunnel | ترحيل التكامل المُثبت (`<slug>.local` + tunnel seed-only) | FR-45 |

### التسليمات
`shamel new/import scan/folder-map/facts/projects --verify` تعمل · قوالب ci.yml/deploy · مشروع تجريبي PRJ-TEST مولود كاملاً.

### معايير القبول
```bash
~/Desktop/SHAMEL/engine/bin/shamel new PRJ-TEST "probe" HIGH --remote <url>
git -C ~/Desktop/SHAMEL/projects/PRJ-TEST log --oneline | wc -l                 # ≥ 1 وremote غير فارغ (FR-40)
diff <(~/Desktop/SHAMEL/engine/bin/shamel folder-map PRJ-TEST --print) ~/Desktop/SHAMEL/projects/PRJ-TEST/docs/FOLDER-MAP.md   # = 0 (FR-41)
test -f ~/Desktop/SHAMEL/projects/PRJ-TEST/_context/LESSONS.md                  # موجود يوم-صفر (سد GAP-11)
test -f ~/Desktop/SHAMEL/projects/PRJ-TEST/.claude/settings.json                # توصيل hooks (BRAIN §2.2)
grep -c 'SHAMEL_CHECKS_VERSION' ~/Desktop/SHAMEL/projects/PRJ-TEST/.github/shamel/*.py   # = 2
# اختبار سلبي الذرّية: قطع خطوة git (remote وهمي فاشل) → لا يبقى نصف سكافولد على القرص
# اختبار سلبي Pattern B: shamel new PRJ-B --web B بلا --adr-source → رفض قبل إنشاء أي شيء
~/Desktop/SHAMEL/engine/bin/shamel projects --verify ; echo $?                  # = 0
```

**الاعتماديات:** Phase 3 (المكتبة) · Phase 5 (القوالب) · Phase 6 (hooks الكانونية للتوصيل).
**المخاطر:** سكافولد نصفي عند فشل خطوة متأخرة (التخفيف: `set -euo pipefail` + trap تراجع، والاختبار السلبي أعلاه شرط قبول).
**الجهد:** M.

---

## Phase 8 — ترحيل PRJ-SAKK: أول مشروع شرعي في المصنع

**الهدف:** SAKK (المُنقَذ في Phase 0) يصبح مشروعاً قانونياً كاملاً: شكل مطابق، دماغ صادق مولَّد، بوابة مُعادة التصنيف بالإثبات، CI حقيقي (GAP-04/12/13).

### Workstreams

| # | العمل | التفصيل | الإسناد |
|---|-------|---------|---------|
| 8.1 | الجرد الآلي | `shamel import scan` على ريبو SAKK — تقرير JSON (stack فعلي: Blade+Tailwind وRiverpod؛ العدّ: 25 model·38 controller·10 migrations) | PROJECT-STRUCTURE §6 م1 · GAP-12 |
| 8.2 | التبنّي تحت المصنع | نقل/ربط الريبو تحت جذر المشاريع (`projects/PRJ-SAKK/` أو `SHAMEL_PROJECTS_DIR`) — نقل مجلد لريبو مستقل، لا عملية git عابرة للسلالات | FR-42 · MIGRATION §7 |
| 8.3 | مواءمة الشكل | تصحيح الانحرافات عن الشكل القانوني (لا `src/`؛ tests الجذرية للعابر فقط — الفارغتان `integration/`/`load/` تُملآن بعقد README أو تسقطان من الخريطة) + `.github/shamel/` standalone | FR-41 · PROJECT-STRUCTURE §1.1 |
| 8.4 | الدماغ الصادق | `shamel facts` يولّد الأرقام · روايات الـ stack تُصحَّح بADR (Riverpod-vs-Bloc: توحيد أو قبول موثَّق) · إضافة LESSONS/FOUNDATIONS/LOCKS الغائبة · ملء branch/head_sha بأول checkpoint | GAP-12 · BRAIN §6 صف 2 |
| 8.5 | إعادة التصنيف | STATE: gate 6 → **4/5** رسمياً؛ ما لا دليل تاريخي عليه يُعلَّم `UNVERIFIED-LEGACY` — يُمنع اختراع artifacts بأثر رجعي | FR-51 · GAP-04 · PROJECT-STRUCTURE §6 م5 |
| 8.6 | أمان الاستيراد | browser-eyes معمَّم باعتمادات env حصراً · Flutter API base بـ `--dart-define` بلا افتراضي إنتاجي · Dockerfile بلا `|| true` + locks منسوخة | FR-70/73 · GAP-13 |
| 8.7 | CI من أول push | `ci.yml` القياسي (coverage ≥90 عتبة آلية + gitleaks + contract job) + تسجيل `IMPORTED.md` | PROJECT-STRUCTURE §7.1 |

### التسليمات
PRJ-SAKK: ريبو خاص تحت المصنع · STATE بgate ≤5 وfacts مولَّدة · CI أخضر · ADRs الانحرافات · سطر IMPORTED.md.

### معايير القبول
```bash
~/Desktop/SHAMEL/engine/bin/shamel projects --verify | grep PRJ-SAKK            # PASS
grep '^gate:' <SAKK>/_context/STATE.md                                          # ≤ 5 (FR-51)
grep 'generated_at:' <SAKK>/_context/STATE.md | grep -v null                    # facts مولَّدة (FR-12)
gitleaks detect --source <SAKK>                                                 # exit 0 (FR-70)
grep -rn '|| true' <SAKK>/deploy/Dockerfile | wc -l                             # = 0 (FR-73)
# اختبار سلبي (GAP-04): shamel gate-check PRJ-SAKK 6 قبل وجود deploy workflow أخضر → FAIL يسمّي الغائب
gh run list -R <sakk-remote> --workflow ci --limit 1 --json conclusion         # success
```

**الاعتماديات:** Phase 0 (R1) · Phase 7 (المصنع والاستيراد).
**المخاطر:** RSK-10 (مقاومة إعادة التصنيف — التخفيف: gate-check يجعل الإعلان بلا tag ناجح خرقاً آلياً) · نقل الريبو يكسر مسارات جلسات قديمة (التخفيف: paths fail-loud يصرخ بدل الصمت).
**الجهد:** M.

---

## Phase 9 — الأتمتة الخارجية: الزمن واليد والعقل الخارجي

**الهدف:** إغلاق «الأتمتة الورقية» P1–P7: كل ادعاء دوري له مشغّل cron مسجَّل بسجل، والمحرك الخارجي يعمل تحت الحوكمة (AUTOMATION §7 مراحل 3–7).

### Workstreams

| # | العمل | التفصيل | الإسناد |
|---|-------|---------|---------|
| 9.1 | cron الحتمي | `cron/shamel.crontab` (tracked) بتركيب **غير مدمّر** (sed-merge أو `/etc/cron.d/shamel` — لا `crontab <file>` خام: crontab المستخدم يحمل Laravel scheduler حياً) + `PATH=` معلن + `shamel notify`؛ الوظائف: doctor ليلي · memdb compact · budget أسبوعي | FR-31 · AUTOMATION §2.3 |
| 9.2 | `automation install/status` | يعمل على ملف crontab الواحد (ADR-006-د): مطابقة الثلاثية ادعاء↔سطر cron↔سجل jsonl — أي ادعاء بلا ثلاثية = فشل doctor | FR-31 · G-07 |
| 9.3 | reflection مجدولة | `reflect-cron.sh` (عتبة دين ≥5 + flock + `claude -p "/shamel-reflect" --max-turns --allowedTools`) + `doctor --lessons` تحققاً فورياً + بند exit bar «reflection debt ≤ 5» في gate-check | FR-15 · GAP-11 · BRAIN §5.2 |
| 9.4 | orchestrator MOCK موصول | `nexus-binding.yaml` (scope: gate 4، budgets صلبة) + فحص doctor `rooms ⊆ registry` و`models ⊆ routing` + MOCK run كامل حتى COMPLETED = CI الأوركسترا | FR-32 · AUTOMATION §3.3/§7-5 |
| 9.5 | orchestrator live على fast-track | `--live` لفئة fast-track فقط؛ 3 مهام حقيقية تعبر live→check→self-heal→evidence→حكم gatekeeper بلا تدخل؛ run log بميزانية ضمن السقف | AUTOMATION §7-6 · V2 |
| 9.6 | oracle مؤتمت | السلّم الثلاثي (API → CDP → فشل صريح exit≠0) + الدفع الآلي عند خروج كل بوابة (لا يحجبها) + action_items → تذاكر taskq | FR-33 · AUTOMATION §4 |

### التسليمات
crontab شامل حي بسجلات · أول `LESSONS.md` حقيقي مُسند · orchestrator موحّد MOCK+live مقيّد · oracle بمصداقية exit codes.

### معايير القبول
```bash
crontab -l | sed -n '/>>> SHAMEL/,/<<< SHAMEL/p' | grep -c shamel               # ≥ 3 أسطر (FR-31)
~/Desktop/SHAMEL/engine/bin/shamel automation status ; echo $?                  # = 0 فقط عند اكتمال الثلاثيات
wc -l < ~/Desktop/SHAMEL/brain/db/logs/doctor.jsonl                             # ≥ 7 (سبع ليالٍ ناجحة — AUTOMATION §7-3)
grep -c '^## LES-' <PRJ>/_context/LESSONS.md                                    # ≥ 1 بsig+source (FR-15)
# الحلقة مغلقة: درس مقطَّر يظهر لقاحاً في جلسة تالية (فحص حقن UserPromptSubmit موثَّق)
grep -rn 'ROOM_CODES\|rooms *= *\[' ~/Desktop/SHAMEL/engine/shamel_tools/pipeline/ | wc -l   # = 0 (FR-32)
pgrep -f 'shamel.*pipeline' | wc -l                                             # = 0 بعد انتهاء أي run (NFR-05)
# اختبار سلبي oracle (FR-33): فصل CDP وحجب API → shamel oracle status يرجع ≠ 0
# اختبار سلبي إنذار: إفشال وظيفة cron مصطنع → shamel notify يطلق فعلاً
```

**الاعتماديات:** Phases 3–6 (الأدوات والحلقة الداخلية) · Phase 8 (مشروع حي يولّد ديناً انعكاسياً ومهام fast-track).
**المخاطر:** RSK-04 (بيئة cron ناقصة PATH/أذونات headless — التخفيف: `PATH=` في الملف + `--allowedTools` إلزامية) · RSK-05 (تعطل oracle — استشاري لا يجمّد) · live يتجاوز نطاقه (التخفيف: nexus-binding scope وbudgets يفحصها doctor).
**الجهد:** L.

---

## Phase 10 — التقاعد والدفن: مقبرة مبصومة، لا أحياء-أموات

**الهدف:** كل جيل مُتقاعد في `archive/` بشاهد قبر (MANIFEST + tag)، والمسارات الميتة لا تلوّث grep بعد اليوم (GAP-14، G-12، ADR-001-ج). **التفصيل التنفيذي طبقة-بطبقة في `MIGRATION.md` — هذه المرحلة تنفّذ قراراته.**

### Workstreams

| # | العمل | التفصيل | الإسناد |
|---|-------|---------|---------|
| 10.1 | دفن G1 `.opencode` | بعد التحقق أن المنتشَل (114+browser-eyes+checklists) داخل SHAMEL: snapshot tar بلا node_modules → حذف node_modules (63M) و`.sofi-run/` وmemory الصفرية (المرحلة الحذفية الوحيدة — استرداد بـ tar أو `npm ci`) → أرشفة الباقي بشاهد قبر | مصفوفة §4 · GAP-14 · MIGRATION §5 |
| 10.2 | دفن G2 `engine/` | بعد التقاط المادة 11 والماسحات: `git mv` إلى الأرشيف + tag `archive/g2-engine-v5` | مصفوفة §4 · MIGRATION §4 |
| 10.3 | دفن dashboard v5 | `dashboard/` + `index.html` («30 وكيلاً») يُؤرشفان — المراقبة البديلة مشروع لاحق خارج النطاق (PRD §4.2-3) | GAP-14 |
| 10.4 | طي fork G6 | بعد MOCK أخضر على النسخة الموحّدة (9.4): fork MAIN يُطوى — الاسترداد الدائم عبر `rescue/g6-main` | MIGRATION §3 |
| 10.5 | دفن جيل الـ port | `MAIN/.claude` (105 stubs + 107 skills مرآة + engine الخاص) بعد غربلة الأوامر (6.6) | GAP-07 · FR-82 |
| 10.6 | دفن أرومة v6 داخل Lorka | `company/` وأخواتها تبقى في Lorka كأرشيف مرجعي read-only (ADR-004) مع شاهد `⛔ superseded by ~/Desktop/SHAMEL` في رأس CLAUDE.md هناك | ADR-004 |
| 10.7 | تصفية الذاكرات والـ stash | ملفات engine الجذرية (بعد برهان التطابق البايتي) · MEMORY نسخة MAIN · `stash drop` أخيراً بموجب ADR الموثَّق في 1.5 — الفرع `rescue/stash-teardown` يبقى | BRAIN §6 صفوف 1b/6/7 |
| 10.8 | فهرس المقبرة | `archive/INDEX.md` في SHAMEL: لكل جيل — ماذا كان، لماذا دُفن، ماذا انتُشل منه، tag الـ snapshot، ADR المرجع | ADR-001-ج · G-12 |

### معايير القبول
```bash
git -C ~/Desktop/Lorka tag -l 'archive/*' | wc -l                               # ≥ 4 (g1/g2/port/dashboard)
grep -c '^| ' ~/Desktop/SHAMEL/archive/INDEX.md                                 # صف لكل جيل متقاعد
du -sh ~/Desktop/Lorka/MAIN/.opencode 2>/dev/null                               # بلا node_modules (< 6M)
~/Desktop/SHAMEL/engine/bin/shamel doctor --dupes ; echo $?                     # = 0 — لا ملف حي في مسار متقاعد (BRAIN §7.1)
~/Desktop/SHAMEL/engine/bin/shamel doctor --rescue-scan ; echo $?               # = 0 — لا untracked ذهبي (G-01)
head -3 ~/Desktop/Lorka/CLAUDE.md | grep '⛔'                                    # شاهد القبر في الأرومة
```

**الاعتماديات:** Phase 0 (الانتشال اكتمل) · Phases 3–9 (كل مستهلك انتقل — لا دفن قبل انتقال المستهلكين).
**المخاطر:** RSK-07 (دفن ما لم يُنتشل — التخفيف: rescue-scan شرط دخول المرحلة، وقاعدة snapshot-first حرفية من توصية H2).
**الجهد:** M.

---

## Phase 11 — التشغيل الكامل والقبول: G-01..G-12 خضراء

**الهدف:** النظام يعمل نظاماً واحداً: CI fail-closed على ريبو شامل، SAKK يتقدم نحو 6–7 بواقع قابل للتشغيل، حلقة Gate-8 مسلَّكة، وجدول أهداف الـ PRD كله أخضر — ثم الإعلان التشغيلي.

### Workstreams

| # | العمل | التفصيل | الإسناد |
|---|-------|---------|---------|
| 11.1 | CI ريبو شامل | GitHub Actions: `doctor --strict` + `selftest` + `agents lint` fail-closed على كل push — أي ازدواج/انحراف توليد/مشروع بلا VCS يفشل البناء | FR-34 · NFR-04 · ARCHITECTURE §5 |
| 11.2 | بوابتا 6–7 حقيقيتان لـ SAKK | `deploy.yml` فعلي + بروفة rollback موثَّقة على بيانات staging + Blue/Green — gate-check يقبل 6 فقط بها | FR-51/73 · AUTOMATION §7-8 |
| 11.3 | حلقة Gate 8 | أول SLI/SLO + خريطة alert↔runbook 1:1 + اختبار مصطنع: خرق SLO يفتح تذكرة Gate-1 فعلاً | AUTOMATION §1.2-P6/§7-8 · PROTOCOL L8 |
| 11.4 | `BOUNDARIES.md` | إعلان الحدود داخلي/خارجي (flat topology، لا daemon، مصدر Nexus المشترك، claude -p/cron) | FR-83 |
| 11.5 | جولة القبول الكبرى | تنفيذ جدول G-01..G-12 كاملاً (أدناه) + خريطة تغطية GAP-01..20 (PRD §9 DoD) — بيد فاحص fresh-context غير المنفّذين | V2 · PRD §3/§9 |
| 11.6 | الإعلان التشغيلي | ADR ختامي: SHAMEL هو جذر العمل الوحيد؛ الجلسات تُفتح عليه حصراً؛ Lorka أرشيف مرجعي؛ alias انتقالي `sofi→shamel` خارج الجذر لمدة محددة ثم يسقط | ADR-004 · FR-80 |

### جدول القبول الختامي (G-01..G-12 → الفحص)

| الهدف | الفحص الميكانيكي | المرحلة المصدر |
|-------|-------------------|-----------------|
| G-01 صفر أصول خارج VCS | `shamel doctor --rescue-scan` = 0 | 0، 10 |
| G-02 سلالة واحدة | `git branch -a` في SHAMEL: main + prj/* قصيرة فقط | 1، 2 |
| G-03 نقطة دخول واحدة | `find` sofi* (خارج archive) = 0 | 3 |
| G-04 جرد وكلاء واحد | doctor parity + بصمات = PASS | 4 |
| G-05 كل مشروع repo خاص | `shamel projects --verify` = 0 | 7، 8 |
| G-06 بوابة = واقع | gate-check fail-closed مُختبَر سلبياً | 3، 8، 11 |
| G-07 أتمتة مثبتة | `shamel automation status` = 0 | 9 |
| G-08 دماغ صادق | `shamel brain-audit` = 0 على كل المشاريع | 5، 8 |
| G-09 اقتصاد سياق | قياس حقن ≤1000 توكن مسجَّل | 6 |
| G-10 تعلم فعلي | سجل reflect ≥ 1 تشغيل/أسبوع + LES موجودة | 9 |
| G-11 صفر انحراف صامت | عدّاد أعطال hooks في doctor = مرئي ومُختبَر | 6 |
| G-12 تقاعد نظيف | archive/INDEX كامل + doctor --dupes = 0 | 10 |

**الاعتماديات:** كل المراحل.
**المخاطر:** إعلان تشغيلي قبل اكتمال الجدول يعيد إنتاج «بوابة فوق واقع معدوم» (التخفيف: 11.6 مشروط بـ 11.5 كاملاً — نفس منطق FR-51 على شامل نفسه).
**الجهد:** M.

---

## 12) خريطة تغطية الفجوات (GAP → مراحل الإغلاق)

GAP-01→0/7/8 · GAP-02→1 · GAP-03→0/10 · GAP-04→8/11 · GAP-05→1/6 (+worktrees خارج `.claude/` بنيوياً في 2) · GAP-06→3 (+doctor دائم) · GAP-07→4 · GAP-08→1/2/5 · GAP-09→3/7 · GAP-10→4 · GAP-11→5/9 · GAP-12→5/8 · GAP-13→0/8 · GAP-14→10 · GAP-15→2/3/4 · GAP-16→4 · GAP-17→2 · GAP-18→4 · GAP-19→1 · GAP-20→6.

**قاعدة الختام:** لا يُغلق هذا الملف إلا بعد أن يمر جدول Phase 11 كاملاً بفحص عدائي fresh-context — الخطة نفسها تخضع لقانونها: **لا ادعاء بلا إنفاذ آلي fail-closed** (P3).
