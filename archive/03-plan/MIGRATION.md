# شامل / SHAMEL — خطة الترحيل (MIGRATION)

**الإصدار:** 1.0 · **التاريخ:** 2026-07-10 · **الحالة:** خطة ملزمة — تُنفَّذ ضمن مراحل `MASTER-PLAN.md` (الإحالات أدناه بـ Phase N)
**المصادر:** `08-COMPARISON-MATRIX.md` (§3 المكوّنات الذهبية · §4 التقاعد) · `09-GAP-ANALYSIS.md` · `PRD.md` §7 · `ARCHITECTURE.md` (ADR-001..004) · `BRAIN.md` §6 · `AUTOMATION.md` §3.1 · `PROJECT-STRUCTURE.md` §2.3/§6
**مفردات القرار (أربعة لا خامس لها):** **يُرحَّل كما هو** (نسخ بأدنى تعديل مسارات/أسماء) · **يُدمج** (توحيد نسخ متعددة في واحدة) · **يُعاد بناؤه** (الفكرة تبقى، التجسيد يُكتب من جديد) · **يُتقاعد+يُؤرشف** (شاهد قبر ⛔ + tag + MANIFEST — بعد انتشال الذهب).

---

## 0) قواعد السلامة العشر (تسري على كل طبقة، بلا استثناء)

1. **tag قبل اللمس:** كل طبقة تأخذ tag إشارياً `pre-shamel/<layer>` على حالتها الراهنة قبل أول خطوة — نقطة الاسترجاع الدنيا لأي rollback.
2. **snapshot-first للحذف:** لا يُحذف بايت إلا وله snapshot مبصوم (tar + sha256 على وسيط ثانٍ) أو تاريخ git يحويه — توصية H2 الحرفية: «snapshot first، do not delete blindly».
3. **لا أوامر مدمّرة:** محظور في كل الخطوات: `git reset --hard` · `git push --force` · `git stash drop` (قبل ADR وبعد تحويل الـ stash فرعاً) · `rm -rf` على مسار بلا snapshot · إعادة كتابة تاريخ منشور.
4. **نسخ لا نقل في البداية:** الترحيل إلى SHAMEL يجري **نسخاً** (الأصل يبقى قراءة-فقط) — النقل/الأرشفة الفعلية لا تقع إلا بعد أن يثبت doctor أن النسخة الجديدة مكتملة (نافذة dual-run).
5. **نافذة dual-run:** بين «النسخة الجديدة تعمل» و«الأصل يُدفن» نافذة تشغيل متوازٍ يقاس فيها التكافؤ (parity/selftest/md5 حسب الطبقة)؛ الدفن مشروط بخضرتها.
6. **نقطة اللاعودة معرَّفة سلفاً:** لكل طبقة حدث واحد مسمّى بعده يتحول الـ rollback من «تجاهل بسيط» إلى «استرجاع من tag/snapshot» — لا نقطة لاعودة غير معلنة.
7. **كل دفن = ثلاثية:** MANIFEST.md (ماذا كان، لماذا، ماذا انتُشل) + git tag `archive/<name>` + سطر في `brain/org/DECISIONS.md` — «لا أحياء-أموات» (ADR-001-ج).
8. **الأسرار قبل التاريخ:** أي محتوى يدخل git لأول مرة يمر بـ secret-scan (gitleaks) **قبل** أول `git add` — ما دخل التاريخ يبقى فيه (GAP-13).
9. **ازدواج مؤقت مُعلَن:** خلال النافذة يُسجَّل الازدواج المتعمد في `archive/INDEX.md` كحالة انتقالية بأجل — كي لا يعدّه doctor لاحقاً defect مجهولاً.
10. **قرار فوق السلطة → تصعيد:** أي تعارض حسم أثناء الترحيل (أي نسخة أصح؟ أي سطر يُلتقط؟) يُحسم بـ ADR لا باجتهاد صامت (G5).

---

## 1) جدول القرارات — الملخص التنفيذي

| # | الطبقة | الموقع الحالي | القرار | الوجهة | Phase | نقطة اللاعودة | مرساة الـ rollback |
|---|--------|----------------|--------|---------|-------|----------------|---------------------|
| 1 | **v6 Company (G3)** | `WT/company/` + `WT/.claude/` | **يُرحَّل كما هو** (شبه كامل، بتعديلات جراحية) | `SHAMEL/core/` + `engine/shamel_tools/` + `.claude/` + `brain/` | 2–6 | تحوّل الجلسات إلى SHAMEL (Phase 11) | الأصل في Lorka يبقى سليماً + `pre-shamel/wt-head` |
| 2 | **substrate (G5)** | `WT/.claude/engine/tooling/` | **يُرحَّل كما هو** (كاملاً، بإعادة تسمية وإخراج من `.claude/`) | `SHAMEL/engine/shamel_tools/core/` | 3 | أرشفة النسخة الأصل بعد dual-run أخضر | tag + النسخة الأصل حتى نهاية النافذة |
| 3 | **orchestrator (G6)** | `WT/orchestrator/+tools/` + fork MAIN (untracked) | **يُدمج** (توحيد الفرعين) ثم يُعاد تجذيره | `SHAMEL/engine/shamel_tools/pipeline/` | 0، 3، 9 | طي fork MAIN بعد MOCK أخضر | فرع `rescue/g6-main` (دائم) |
| 4 | **engine القديم (G2 v5)** | `MAIN/engine/` | **يُتقاعد+يُؤرشف** بعد التقاط الجوهر (المادة 11 + الماسحات) | `archive/g2-engine-v5` (tag) — الجوهر إلى `core/constitution/11` و`engine/scanners/` | 2، 3، 10 | `git mv` إلى الأرشيف | `git revert` لِـ commit الأرشفة |
| 5 | **.opencode (G1)** | `MAIN/.opencode/` (untracked كلياً، 69M) | **انتشال ثم يُتقاعد+يُؤرشف** | الذهب → `core/rooms/*/tools/` + `core/gates/checklists/`؛ الجثة → `archive/g1-opencode` | 0، 4، 10 | حذف node_modules بعد الـ snapshot | tar مبصوم + `npm ci` من lockfile + فرع `rescue/g1-assets` |
| 6 | **org-rooms (G4)** | `WT/org-rooms/` (2217 سطراً) | **يُدمج** كطبقة (حوكمة + كانون) والأصل يُؤرشف | `authority:` في frontmatter + `nexus/personas.yaml` + HR profiles | 4، 10 | أرشفة الأصل بعد برهان تغطية personas.yaml | الأصل tracked — `git revert` |
| 7 | **projects (PRJ-SAKK + الحاوية)** | `MAIN/projects/` (خارج أي VCS) | **يُعاد بناؤه** كنمط (المصنع) + المحتوى **يُرحَّل كما هو** إلى ريبو خاص | ريبو PRJ-SAKK مستقل تحت `SHAMEL/projects/` | 0، 7، 8 | أول `git push` لتاريخ SAKK (الأسرار قبله إلزاماً) | tar خارج الشجرة + كل خطوة لاحقة commit قابل revert |
| 8 | **جيل الـ port** (ملحق) | `MAIN/.claude/` (105 stubs + 107 skills + 54 أمراً) | **يُتقاعد+يُؤرشف** بعد غربلة الأوامر (≤15) | القيّم → `SHAMEL/.claude/commands/`؛ الباقي → أرشيف | 6، 10 | أرشفة ما بعد الغربلة | tag `pre-shamel/main-head` |
| 9 | **dashboard v5** (ملحق) | `MAIN/dashboard/` + `index.html` (tracked) | **يُتقاعد+يُؤرشف** — بديله مشروع لاحق خارج النطاق | `archive/` | 10 | commit الأرشفة | `git revert` |
| 10 | **الذاكرات المتوازية** (ملحق) | MEMORY ×2 · sessions ×2 · brain.db · ملفات engine الجذرية · stash | **يُدمج** وفق جدول BRAIN §6 (استيراد لا استنساخ) | `SHAMEL/MEMORY.md` + `brain/db/brain.db` + `brain/org/` | 1، 5، 10 | `stash drop` (بعد فرع الإنقاذ + ADR) | فرع `rescue/stash-teardown` + أرشيفات الجثث |

---

## 2) الطبقة 1 — v6 Company of Rooms (G3): العمود الفقري

**القرار: يُرحَّل كما هو (شبه كامل).** الفائز في 8/10 أبعاد، الوحيد HEALTHY بفحص ذاتي ناجح (مصفوفة §2/§6). التعديلات الجراحية الأربعة فقط: المادة 11 الجديدة، طبقة `models.yaml`، ملء `rooms/*/tools/`، وتوليد الـ spawnables بدل صيانتها (ARCHITECTURE §3.1).

**ما يُرحَّل:** الدستور 00–10 (المادتان 02/03 حرفياً) · ثلاثي الـ Nexus + doctor + pins · صيغة الوكيل المزدوجة (الطرف الثاني مولَّداً) · hooks الخمسة (WT) · BRAIN + templates + memdb + LESSONS-sig · RCCF + bus · oracle (بشرط FR-33) · 13 skill + `.claudeignore` + قالب CHARTER · `sofi_tools` الـ 24 موديلاً (تُعاد تجذيرها `shamel_tools`).
**ما لا يُرحَّل (يُدفن مع Phase 10):** `os/autopilot/` · `os/ooda/` ×2 · `os/agents/tier-*` · model IDs الحرفية في routing.yaml.

**خطوات الترحيل الآمنة:**
1. tag `pre-shamel/wt-head` (تم في Phase 0.5).
2. النسخ إلى SHAMEL بترتيب المراحل: constitution+nexus (Phase 2) → sofi_tools→shamel_tools (Phase 3) → rooms/agents (Phase 4) → brain (Phase 5) → hooks/skills (Phase 6) — **نسخ مع تحويل مسارات وأسماء** (`sofi`→`shamel`، `company/`→`core/`)، الأصل لا يُمس.
3. برهان التكافؤ قبل اعتماد كل قطعة: `shamel doctor` يعيد إنتاج نتائج `sofi doctor` (105↔105↔105، 109 routes) + diff دلالي موثَّق للمواد المعدَّلة (FR-22).
4. نافذة dual-run: Lorka يبقى صالحاً للجلسات حتى الإعلان التشغيلي (Phase 11.6).
5. بعد الإعلان: شاهد `⛔ superseded by ~/Desktop/SHAMEL` في رأس CLAUDE.md في Lorka — Lorka كله أرشيف مرجعي (ADR-004)، لا يُحذف.

**نقطة اللاعودة:** الإعلان التشغيلي (Phase 11.6) — قبله SHAMEL نسخة عديمة الأثر يمكن هجرها بلا كلفة.
**Rollback:** العودة للعمل من Lorka WT كما كان — لم يتغير فيه شيء سوى شاهد قبر قابل للـ revert؛ SHAMEL يُهجر أو يُصحَّح.
**التحقق:** `shamel doctor --strict` PASS + جدول Phase 11 (G-01..G-12).

---

## 3) الطبقة 2 — substrate (G5): النواة الحتمية

**القرار: يُرحَّل كما هو (كاملاً).** selftest PASS 6/6، «الأنقى حتمياً» (مصفوفة بُعد 4). ثلاثة تعديلات: يخرج من تحت `.claude/` (كان «طبقة موازية غير معلنة»)، `registry.py`→`schemas.py` (فك تصادم الدلالات الثلاث — GAP-15، والاسم النهائي محسوم بـ ADR-006)، و`gateway.py` يندمج في `pipeline/translator.py` (كانا متنافسين بلا عقد مشترك).

**خطوات الترحيل الآمنة:**
1. tag `pre-shamel/substrate` (مشمول بـ `pre-shamel/wt-head`).
2. نسخ الست إلى `SHAMEL/engine/shamel_tools/core/` مع إعادة التسمية وإصلاح الـ imports — commit واحد لكل أداة (تتبع أنظف).
3. `shamel selftest --json` في الموطن الجديد = PASS 6/6 **قبل** أي خطوة لاحقة — بار القبول الموروث نفسه.
4. ترحيل بيانات `taskq.db` القائمة (إن وُجدت صفوف حية) بسكربت استيراد idempotent + دمج جدول history من state_db (انظر §4 الطبقة 3).
5. dual-run أسبوعاً: الأصل في `.claude/engine/tooling/` يبقى، ويُعلَن ازدواجاً انتقالياً بأجل (قاعدة §0-9).
6. بعد النافذة: وسم الأصل deprecated وأرشفته مع دفعة Phase 10.

**نقطة اللاعودة:** أرشفة النسخة الأصل بعد نافذة dual-run الخضراء — قبلها التراجع = مجرد استئناف استعمال الأصل.
**Rollback:** النسخة الأصل موجودة حتى نهاية النافذة؛ بعدها `git revert` لـ commit الأرشفة (الأصل tracked في WT).
**التحقق:** `selftest` PASS + `doctor` لا يرى ازدواجاً بعد الأرشفة + `grep -rn 'schemadb\|engine/tooling' SHAMEL/` = 0.

---

## 4) الطبقة 3 — orchestrator (G6): توحيد الـ fork ثم الربط بالحوكمة

**القرار: يُدمج.** «fork مزدوج نشط في نفس اليوم» — أي تفعيل قبل الدمج يرسّخ الانقسام (AUTOMATION §1.3-N3). خريطة المصادر المعتمدة ملزمة (AUTOMATION §3.1): `translator_gateway` نسخة MAIN (455) · `state_db` نسخة WT (356 — جدول history فقط، يُدمج في taskq) · `ceo_agent.py` المنقَذ من MAIN · `agent_invoker` الحالي (MOCK/live) · الأدوات الـ 22 برموز v6.

**خطوات الترحيل الآمنة:**
1. **الإنقاذ أولاً (Phase 0.2 — تم):** فرع `rescue/g6-main` يحفظ الحصريات untracked (ceo_agent + translator الأغنى + orchestrator.db).
2. فرع دمج `merge/g6-unified` في Lorka: جمع النسخ المعتمدة من الجدول أعلاه — كل اختيار نسخة يُذكر في رسالة الـ commit (أي fork، أي ملف، لماذا).
3. إعادة التجذير: النسخة الموحّدة → `SHAMEL/engine/shamel_tools/pipeline/` (Phase 3.8) مع: توحيد رموز الغرف على v6 (`bck` لا `bkd_05`) · حذف كل جدول غرف/routes مضمّن · `nexus-binding.yaml` (scope: gate 4 + budgets).
4. استيراد تاريخ `orchestrator.db` الحي إلى `taskq.db:history` بسكربت idempotent، ثم يُرفَق ملف الـ db الأصلي بالأرشيف (لا يُحذف).
5. **بار القبول قبل أي طي:** MOCK run كامل حتى COMPLETED يقرأ `core/nexus/*.yaml` حصراً (Phase 9.4) + فحص doctor `rooms ⊆ registry`.
6. طي fork MAIN (إخراجه من مساره إلى الأرشيف) — فقط بعد الخطوة 5 خضراء (Phase 10.4).

**نقطة اللاعودة:** طي fork MAIN — وبعده الاسترداد يبقى ممكناً عبر `rescue/g6-main` (فرع دائم لا يُحذف).
**Rollback:** `git checkout rescue/g6-main -- <path>` لأي ملف؛ فرع الدمج نفسه قابل للهجر قبل اعتماده.
**التحقق:** `grep -rn 'bkd_05\|uxr_02\|ROOM_CODES' SHAMEL/engine/shamel_tools/pipeline/` = 0 · MOCK COMPLETED مسجَّل في run log · `pgrep` بعد الانتهاء = 0 (flat topology).

---

## 5) الطبقة 4 — engine القديم (G2 v5): التقاط الجوهر ثم الدفن

**القرار: يُتقاعد+يُؤرشف** بعد التقاط ثلاثة أصول فقط (مصفوفة §3 بندا 14/15): (أ) منطق intake-orchestration (wear-the-hierarchy، leaf-spawn one hop) → **المادة 11** بصياغة تحسم تناقض «no slash-commands» نصاً (FR-20)؛ (ب) الماسحات feature_scan/sofi_scan/sofi_verify — النسخة الأحدث بعد فك الازدواج البايتي؛ (ج) الأسطر الفريدة من `engine/EVOLUTION.md` (تباعدت 60 سطراً عن نسخة org — BRAIN §6-6).

**خطوات الترحيل الآمنة:**
1. tag `pre-shamel/g2-engine`.
2. تعيين النسخة الأحدث من كل ماسح: `md5sum engine/agents/*.py company/os/agents/*.py` — المتطابق بايتياً يثبت الأصل المشترك، والمتفرّع يُعتمد الأحدث (بشهادة `git log`)؛ القرار يُدوَّن.
3. صياغة المادة 11 من `engine/protocols/02-intake-orchestration.md` + مراجعة عدائية لها (فاحص غير الكاتب) قبل الاعتماد.
4. diff يدوي لـ EVOLUTION والتقاط الفريد إلى `brain/org/EVOLUTION.md`؛ برهان تطابق HANDOFFS/PERSONAS البايتي يُلصق في MANIFEST قبل الدفن.
5. `git mv engine/ archive/g2-engine-v5/` + MANIFEST + tag `archive/g2-engine-v5` + سطر ADR — commit واحد.
6. ملاحظة تزامن: dashboard (الطبقة 9) يقرأ `engine/routing` — دفن G2 لا يسبق قرار dashboard (يُدفنان في نفس دفعة Phase 10 كي لا يكسر أحدهما الآخر بصمت).

**نقطة اللاعودة:** commit النقل إلى الأرشيف (خطوة 5).
**Rollback:** `git revert <sha>` لذلك الـ commit — يعيد `engine/` لمكانه كاملاً (نقل git لا حذف).
**التحقق:** `test -f archive/g2-engine-v5/MANIFEST.md` · المادة 11 موجودة وتذكر شرعية الـ skills · `diff` برهان التطابق مؤرشف.

---

## 6) الطبقة 5 — .opencode (G1): الانتشال قبل كل شيء، ثم الدفن الأثقل

**القرار: انتشال ثم يُتقاعد+يُؤرشف.** الخطر الأعلى: الكنز (114 سكربت + browser-eyes + checklists) موجود **فقط على القرص خارج أي git** (GAP-03)، والجثة 69M (منها 63M node_modules) تلوّث كل grep (GAP-14).

**خطوات الترحيل الآمنة:**
1. **الانتشال (Phase 0.3 — تم):** فرع `rescue/g1-assets` يلتزم: `tools/` الـ 114 (بعد `bash -n` جماعي — 104/105 pass موروث) + browser-eyes **بعد نزع اعتمادات admin من السطرين 13–14 إلى env** (شرط FR-70 قبل أول add — قاعدة §0-8) + gate checklists 0–8.
2. التوزيع في SHAMEL (Phase 4.6/4.8): الأدوات على `core/rooms/*/tools/` بغرفها، والـ checklists إلى `core/gates/checklists/`.
3. snapshot الجثة: `tar --exclude='node_modules' --exclude='.sofi-run'` لكامل `.opencode` + sha256 على وسيط ثانٍ + برهان ما-قبل-الحذف للذاكرة الصفرية (`find .opencode/memory -size +0c` فارغ — BRAIN §6-7).
4. **المرحلة الحذفية الوحيدة في الخطة كلها (Phase 10.1):** حذف `node_modules/` (63M) و`.sofi-run/` وملفات memory الصفرية — كلها قابلة الاسترداد: node_modules بـ `npm ci` من الـ lockfile المؤرشف أو من الـ tar؛ `.sofi-run` وmemory أصفار موثَّقة البصمة.
5. أرشفة الباقي (68 وكيلاً — منها 14 ملوثة CJK بموديل ميت، السجلات الثلاثة المتناقضة) في `archive/g1-opencode/` بـ MANIFEST يذكر: ما انتُشل (البنود 10–13 في المصفوفة §3)، التلوث، وسجلات dangling الـ 100%.

**نقطة اللاعودة:** خطوة الحذف 4 — مشروطة ببصمة snapshot متحققة (`sha256sum -c`).
**Rollback:** فك الـ tar يعيد كل شيء؛ الذهب مستقل عنه في `rescue/g1-assets` وفي SHAMEL.
**التحقق:** `git ls-files core/rooms/*/tools | wc -l` ≥ 110 في SHAMEL · `grep -rn 'ADMIN_PASSWORD\|admin@' <browser-eyes>` = 0 · `du -sh .opencode` < 6M بعد الدفعة.

---

## 7) الطبقة 6 — org-rooms (G4): طبقة تُدمج، لا كون يبقى

**القرار: يُدمج** — «يُرحَّل كطبقة، لا ككون» (PRD §7.2). ما يُلتقط: الحوكمة السداسية per-person (سلطة/مال/فيتو/تصعيد/اعتماديات — لا نظير لها في أي جيل) + الكانون العربي-السوري للأسماء (Q4) + الملفات الـ 100 كـ HR profiles. ما يسقط: الخريطة العشرية (تخسر أمام الـ 15 — Q3) ودلالة GTW-06 الخارجية (تُعاد توزيعاً — FR-05-ج).

**خطوات الترحيل الآمنة:**
1. tag `pre-shamel/g4-org-rooms`.
2. بناء `nexus/personas.yaml` (Phase 4.3): 100 صف ربط + personas جديدة لفجوات fnt/qa/obs/brd بنفس القالب السداسي؛ ازدواج الأسماء الثلاثي (Priya Nair/عمّار خضّور/كريم فاروق) يُحل: الكانون العربي canonical والباقي aliases.
3. صب حقول `authority:` في frontmatter الملفات القانونية (Phase 4.2) — نسخ بالتقطير لا بالاستنساخ (قاتل نمط bytes المتباعدة — BRAIN §7.1).
4. فحص NFR-10 (محارف دخيلة) على كل نص مستورد.
5. برهان التغطية قبل الأرشفة: doctor يتحقق أن كل agent-id له `persona:` يحلّ في الجدول، وكل persona أصلية إمّا مربوطة أو مذكورة في MANIFEST كغير-مستعملة-عمداً.
6. أرشفة `org-rooms/` الأصل مع دفعة Phase 10 (`archive/g4-org-rooms` + MANIFEST).

**نقطة اللاعودة:** commit أرشفة الأصل (بعد برهان الخطوة 5).
**Rollback:** الأصل tracked في WT — `git revert` يعيده؛ personas.yaml يبقى صالحاً بذاته.
**التحقق:** `grep -c 'PER-' nexus/personas.yaml` ≥ 105 · `grep -L 'authority:' core/rooms/*/agents/*.md` = فارغ · صفر أسماء بشرية حرّة في frontmatter (FR-04).

---

## 8) الطبقة 7 — projects: النمط يُعاد بناؤه، والمحتوى يُرحَّل كما هو

**القرار المزدوج:** (أ) **نمط** إدارة المشاريع **يُعاد بناؤه** — يُلغى نهائياً نمط «فرع `prj/<ID>` في ريبو الإطار الذي يتجاهل projects/» (الفرع الذي لا يستطيع حمل المشروع المسمّى باسمه — PROJECT-STRUCTURE §2.1)، ويحل محله المصنع بقانون يوم-صفر (Phase 7)؛ (ب) **محتوى** PRJ-SAKK (كود + دماغ) **يُرحَّل كما هو** — لا إعادة كتابة (PRD §4.2-1) — إلى ريبو git خاص.

**خطوات الترحيل الآمنة (ترتيبها ملزم — الأسرار قبل التاريخ):**
1. **الإنقاذ (Phase 0.1 — تم):** التسلسل الحرفي من PROJECT-STRUCTURE §2.3: tar خارج الشجرة → تطهير اعتمادات browser-eyes.sh → gitleaks نظيف → `.gitignore` القياسي → `git init -b main` → مراجعة staged → commit إنقاذ → remote/mirror.
2. التبنّي (Phase 8.2): الريبو تحت `SHAMEL/projects/PRJ-SAKK/` — نقل مجلد يحمل `.git` خاصه؛ لا عملية git عابرة للسلالات.
3. مواءمة الشكل القانوني + `.github/shamel/` standalone + توصيل hooks (Phase 8.3، 7.4).
4. الدماغ الصادق: `shamel facts` يولّد الأرقام · تصحيح روايات الـ stack بـ ADR · إضافة LESSONS/FOUNDATIONS/LOCKS · أول `shamel checkpoint` يملأ branch/head_sha (Phase 8.4).
5. إعادة التصنيف gate 6 → 4/5 + وسم `UNVERIFIED-LEGACY` لما لا دليل عليه — يُمنع اختراع artifacts بأثر رجعي (Phase 8.5).
6. تسجيل `IMPORTED.md` + ADR الاستيراد؛ خسارتا xo-game وheart-clinic توثَّقان فيه كسابقتين غير قابلتين للاسترداد (سبب قانون يوم-صفر).
7. الحاوية القديمة `MAIN/projects/` تبقى متجاهَلة في Lorka وتُفرَّغ تدريجياً؛ `projects/README.md` المشير لمسار v5 يُصحَّح (GAP-19).

**نقطة اللاعودة:** أول `git push` لتاريخ SAKK إلى remote — ما دخل التاريخ المنشور يبقى؛ لذلك الخطوة 1 تجعل التطهير سابقاً لأول add بلا استثناء.
**Rollback:** الـ tar المبصوم خارج الشجرة (خطوة 0 من §2.3) لأي كارثة؛ وكل خطوة بعد الولادة commit عادي قابل `git revert`.
**التحقق:** `shamel projects --verify` PASS · gitleaks = 0 · STATE بـ gate ≤5 وfacts مولَّدة · CI أخضر (معايير Phase 8).

---

## 9) الطبقات الملحقة

### 9.1 جيل الـ port (`MAIN/.claude/`) — يُتقاعد+يُؤرشف
- **الذهب الوحيد:** ≤15 أمراً من الـ 54 (gate-check/deploy/parallel-build/security-sweep…) بعد فحص مراجع آلي — درس dangling الـ 100% (FR-82، Phase 6.6). الـ 105 stubs (بـ `model: inherit` بلا tools — GAP-10) والـ 107 skills المرآة لا يُنسخ منها شيء.
- **خطوات:** tag (مشمول بـ `pre-shamel/main-head`) → غربلة الأوامر إلى SHAMEL بفحص أن كل أمر يحلّ مراجعه → أرشفة الباقي في دفعة Phase 10.
- **نقطة اللاعودة:** commit الأرشفة. **Rollback:** `git revert` / الـ tag.
- **تحقق:** `ls SHAMEL/.claude/commands | wc -l` ≤ 15 وكلها بلا مرجع ميت.

### 9.2 dashboard v5 + index.html — يُتقاعد+يُؤرشف
- يعرضان عالم «30 وكيلاً» المنقرض ويقرآن `engine/routing` (GAP-14). لا انتشال — البديل مشروع لاحق خارج النطاق (PRD §4.2-3).
- **خطوات:** أرشفة متزامنة مع G2 (الاعتماد المتبادل — §5 خطوة 6). **Rollback:** `git revert`.

### 9.3 الذاكرات المتوازية — يُدمج وفق جدول BRAIN §6 (استيراد لا استنساخ)
| المصدر | الإجراء | الحماية |
|--------|---------|----------|
| `WT/MEMORY.md` | الأساس المعتمد → `SHAMEL/MEMORY.md` بمسارات محدَّثة، <200 سطر | الأصل باقٍ في WT |
| `MAIN/MEMORY.md` | يُقتل — أرشفة بشاهد قبر، **لا دمج** (خرائطه تشير لموتى) | tag `pre-shamel/main-head` |
| `MAIN/sessions.jsonl` (47 جلسة) | **استيراد** إلى brain.db (`source='legacy-sessions'`) ثم أرشفة الملف | العدّ 47 = برهان القبول |
| `WT/sessions.jsonl` (7 أسطر test) | حذف بسطر ADR (بيانات اختبار معلنة) | مذكور في ADR الهجرة |
| `WT/brain.db` (صف واحد) | يُنقل نواةً للقاعدة الوحيدة | قاعدة النمو الأسبوعي في doctor |
| ملفات `engine/` الجذرية | دفن بعد **برهان التطابق البايتي** مع نسخة org (diff يُلصق في MANIFEST)؛ فرائد EVOLUTION تُلتقط | §5 خطوة 4 |
| `stash@{0}` (teardown، 3368 ملفاً) | مؤمَّن فرعاً منذ Phase 0.4 (`git branch rescue/stash-teardown stash@{0}` — غير مدمّر)؛ `stash drop` فقط في Phase 10.7 بموجب ADR الموثَّق في Phase 1.5 | الفرع دائم لا يُحذف |
| Harness memory + claude-mem | يبقى خارجياً — حدود تكامل معلنة بسطري pointer في MEMORY.md؛ لا يُعدّ نظام ذاكرة داخلياً | BRAIN §6-8 |

**نقطة اللاعودة:** `stash drop` (آخر فعل في السلسلة كلها). **Rollback:** الفرع `rescue/stash-teardown` يحمل نفس الـ commit.

---

## 10) التسلسل الزمني الجامع (طبقة × Phase)

```
Phase 0   ██ إنقاذ: SAKK→git · rescue/g6-main · rescue/g1-assets · stash→فرع · tags
Phase 1   ██ مصالحة السلالات + قتل MEMORY-MAIN وsession_start-MAIN (قرارات، التنفيذ الأرشيفي لاحقاً)
Phase 2-3 ██ G3 (دستور/nexus) + G5 (substrate) + G6 (pipeline المدموج) → SHAMEL   [نسخ، الأصول قراءة-فقط]
Phase 4   ██ G3 (rooms/agents) + G4 (يُدمج طبقةً) + ذهب G1 (tools/checklists) → SHAMEL
Phase 5   ██ الذاكرات: org brain + memdb + استيراد sessions الـ 47
Phase 6   ██ hooks/skills + غربلة أوامر جيل الـ port
Phase 7-8 ██ المصنع + تبنّي SAKK وإصلاح دماغه وإعادة تصنيفه
Phase 9   ██ برهان MOCK/live → يفتح باب طي fork G6
Phase 10  ██ الدفن الجماعي: g1 (بحذف node_modules المشروط) · g2+dashboard · port · fork ·
             ذاكرات الجثث · stash drop (ADR) · archive/INDEX.md كامل
Phase 11  ██ الإعلان التشغيلي = نقطة اللاعودة الوحيدة للطبقة 1 (G3) — وبعدها Lorka أرشيف مرجعي
```

**قاعدة الختام:** اكتمال الترحيل يُقاس بأمر واحد لا بتقرير: `shamel doctor --strict` = PASS (لا ازدواج، لا ملف حي في مسار متقاعد، لا untracked ذهبي، archive/INDEX يغطي كل جيل) + جدول قبول Phase 11 أخضر — وأي طبقة لم يثبت دفنها بالثلاثية (MANIFEST + tag + ADR) تبقى قانونياً «حية مُدارة» يفحصها doctor، لا منطقة رمادية.
