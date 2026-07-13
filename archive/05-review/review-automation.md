# مراجعة عدائية — AUTOMATION.md (شامل)

**المراجِع:** adversarial reviewer · **التاريخ:** 2026-07-10 · **المنهج:** فحص حي لكل ادعاء قابل للفحص (ملفات/مسارات/أسطر/أوامر) + فحص التناقض الداخلي + مطابقة مبادئ شامل
**الحكم:** **FIX** — ثلاث مشاكل CRITICAL تستوجب تعديل الوثيقة قبل اعتمادها للـ PRD. الوثيقة عدا ذلك مُسندة جيداً: **15+ ادعاءً قابلاً للفحص ثبتت صحته حرفياً** (§D أدناه).

---

## A. CRITICAL — تستوجب تعديل الوثيقة

### C1 — ادعاء «تحقق حي» كاذب: crontab ليس فارغاً (§1.2 P1 + خلاصة §1)
**الادعاء:** «لا مجدوِل: `crontab -l` فارغ (تحقق حي اليوم)» (سطر 26) و«لا يوجد اليوم أي شيء يجري بلا جلسة مفتوحة أو أمر يدوي — الجدولة صفر» (سطر 42).
**الواقع (فُحص حياً 2026-07-10):** `crontab -l` يحوي **سطرين نشطين يعملان كل دقيقة**:
```
* * * * * cd /home/es3dlll/Desktop/Lorka/projects/PRJ-SAKK/backend && /usr/bin/php artisan schedule:run ...
* * * * * cd /home/es3dlll/Desktop/Lorka/projects/PRJ-SAAS-001/src/backend && /usr/bin/php artisan schedule:run ...
```
الأول يشير إلى مسار موجود (backend لمشروع PRJ-SAKK الحي على Gate 6)؛ الثاني dangling (PRJ-SAAS-001 غير موجود). جوهر P1 (لا مجدوِل لـ reflection ولا LESSONS.md) صحيح، لكن الدليل المستشهد به «تحقق حي» **خاطئ** — خرق مباشر لقانون G1/G3 (grounding/execution truth) الذي تتبناه الوثيقة نفسها كمبدأ حاكم.
**الإصلاح:** تصحيح P1 والخلاصة: crontab يحوي سطرين لمجدولات Laravel لمشروعين (أحدهما dangling)؛ «لا أتمتة SOFI/شامل مجدولة» هي الصياغة الصحيحة.

### C2 — أمر تركيب مدمّر: `crontab cron/shamel.crontab` يمحو crontab القائم (§2.3 سطر 111/114)
الوثيقة تنص: «التركيب بأمر واحد: `crontab cron/shamel.crontab`». أمر `crontab <file>` **يستبدل** crontab المستخدم بالكامل — تنفيذه كما هو مكتوب **يحذف بصمت** سطر مجدول Laravel الحي لمشروع PRJ-SAKK (منتج أموال/KYC على Gate 6). الخطأ نتيجة مباشرة لـ C1 (الافتراض الكاذب أن crontab فارغ). هذا بالضبط نمط «أتمتة تكذب/تدمّر» الذي تحاربه الوثيقة في §1.3.
**الإصلاح:** تغيير أمر التركيب إلى دمج غير مدمّر، مثلاً `crontab -l | cat - cron/shamel.crontab | crontab -` (مع حارس ضد التكرار)، أو ملف مستقل في `/etc/cron.d/`، مع ذكر السطور القائمة صراحة.

### C3 — ملف crontab المعياري غير قابل للتنفيذ كما هو مكتوب: PATH + أذونات headless (§2.3)
1. **PATH:** سطر reflect يستدعي `claude -p` عارياً. `claude` مثبت في `~/.local/bin/claude` (فُحص: `which claude`)، وcron يعمل بـ PATH افتراضي `/usr/bin:/bin` — الملف يعرّف `SHAMEL=` فقط بلا سطر `PATH=` → المهمة النموذجية الوحيدة تفشل بـ command-not-found من أول ليلة.
2. **أذونات headless:** `claude -p "/shamel-reflect"` في وضع non-interactive لا يستطيع منح أذونات أدوات تفاعلياً؛ كتابة `LESSONS.md` (مخرَج المرحلة 4 وبرهان خروجها) تتطلب استراتيجية أذونات معلنة (`--allowedTools` / `--permission-mode` / allowlist في settings) — الوثيقة لا تذكر أياً منها، لا هنا ولا في invoker §3.2 الذي يعتمد نفس الآلية. حلقة «التعلّم المغلقة» (سطر 178) — الادعاء المركزي للوثيقة — **غير قابلة للتشغيل بالمواصفة الحالية**، وهو خرق لمبدئها الحاكم «لا ادعاء أتمتة بلا إنفاذ آلي قابل للفحص».
**الإصلاح:** إضافة `PATH=` (أو مسار مطلق للـ binary) إلى crontab، وفقرة أذونات headless صريحة لكل استدعاء `claude -p` (cron §2.3 + invoker §3.2).

---

## B. HIGH

### H1 — الوثيقة تخرق قاعدتها الملزمة في ملفها المعياري نفسه (§2.3)
القاعدة الملزمة (سطر 122): «فشله يستدعي `shamel notify` — **لا مهمة مجدولة صامتة الفشل**». لكن ملف `cron/shamel.crontab` المعياري (سطور 116–119) يضع `|| shamel notify` على سطر doctor **فقط**؛ سطور memdb compact وreflect وbudget بلا أي notify — ثلاث من أربع مهام مجدولة **صامتة الفشل** بنص الوثيقة ذاتها. تناقض داخلي مباشر بين القاعدة والملف الذي يجسّدها.
**الإصلاح:** `|| shamel notify "<job> FAIL"` على كل سطر.

---

## C. MEDIUM

### M1 — جدول الدمج (§3.1) يترك سلالة `agent_invoker.py` غامضة
كل صف في جدول الدمج يسمّي الفرع المعتمد (MAIN/WT) عدا `agent_invoker.py` المسمّى «الحالي» — بينما النسختان متباعدتان مادياً (MAIN=624 سطراً، WT=450 سطراً، فُحص). استشهاد A5 بالأسطر 268-269 يطابق نسخة **WT** حصراً. في وثيقة غرضها المعلن حسم الـ fork (N3: «أي تفعيل قبل الدمج يرسّخ الانقسام»)، ترك مكوّن التنفيذ المركزي بلا سلالة مسماة عيب مواصفة.
**الإصلاح:** تسمية «WT (450 سطراً، MOCK/live)» صراحة في الجدول.

### M2 — تناقض «الوظيفة النموذجية الوحيدة» (§6.2 vs §2.3)
§6.2: «الوظيفة النموذجية **الوحيدة** الدورية (reflect) بسقف 15 turns أسبوعياً — التكلفة الدورية القصوى معروفة سلفاً». لكن جدول §2.3 يعرّف مهمة نموذجية دورية ثانية: «مراجعة oracle الدورية — نموذجي — أسبوعي» (`claude -p "/shamel-report weekly"`, المرحلة 7). بعد تفعيل المرحلة 7 تنكسر «الوحيدة» ويصبح سقف التكلفة الدورية المعلن خاطئاً.
**الإصلاح:** «الوحيدة حتى المرحلة 6» + تحديث سقف التكلفة عند المرحلة 7.

### M3 — قسم ناقص: لا آلية تنافُس/قفل بين الجلسة الحية والـ orchestrator الخارجي
§5 يعرض مسارين متوازيين لـ Gate 4 (أ: جلسة حية بـ worktrees، ب: cron→orchestrator) على نفس المشروع، والوثيقة لا تحدد أي استبعاد متبادل: تصادم على taskq (SQLite) وgit index وملفات الدماغ إذا تزامن run خارجي ليلي مع جلسة مفتوحة. الأدوات القائمة تملك أصلاً `sofi claim/release` (cli.py) — والوثيقة لا تذكرهما ولا بديلاً عنهما لطبقة الأتمتة.
**الإصلاح:** فقرة قفل صريحة (claim/release لكل PRJ قبل أي run خارجي؛ cron يتخطى مشروعاً مُطالَباً به).

---

## D. LOW

### L1 — تسمية متناقضة: «sofi gate-check» في خط شامل (§5، سطر 317)
§2.4 يقرر أن `os/bin/shamel` «يخلف ثنائي sofi»، وGAP-15 (الذي تعالجه الوثيقة) هو تحديداً تصادم تسمية sofi — ثم يستخدم §5 «sofi gate-check يرفض Gate 6». يجب `shamel gate-check`.

### L2 — استشهاد غير دقيق: «PASS 6/6 (04)» (§1.1 A2)
التقرير 04 لا يحوي «6/6»؛ نصّه «substrate selftest = **PASS شامل**». الجوهر صحيح (6 أدوات والموزّع يجمّع selftest الكل ويدعم `--json` — فُحص الكود) لكن الرقم منسوب لمصدر لا يذكره.

### L3 — عدد غير دقيق: «runbook يستشهد بأربعة ملفات معدومة» (§1.2 P4)
الفحص وجد **≥8 أسماء workflow وهمية متمايزة** في ملفات PRJ-SAKK (ci.yml، ci.yaml، tests.yml، test.yml، deploy.yml، continuous-integration.yml، run-tests.yml، run-coverage.yml). جوهر P4 مؤكد (المجلد `.github/workflows/` موجود وفارغ تماماً — فُحص)؛ العدد «أربعة» غير مسنود.

### L4 — شبه-placeholder: `shamel notify` بلا تصميم (§2.3/§6)
سطح الإنذار الذي تتكئ عليه كل الـ fail-safes مُعرَّف بجملة اعتراضية واحدة («notify-send محلياً أو webhook لاحقاً»): لا ضمان تسليم، لا dedup، وnotify-send من cron يتطلب DISPLAY/DBUS غير متاحين headless. أضعف حلقة في سلسلة «لا فشل صامت».

---

## E. عيّنة الادعاءات المفحوصة التي ثبتت صحتها (إنصافاً)

| # | الادعاء | نتيجة الفحص |
|---|---------|--------------|
| 1 | A1: الخمسة hooks مسلّكة في `settings.json` بنمط `$CLAUDE_PROJECT_DIR` | ✓ حرفياً (WT `.claude/settings.json`) |
| 2 | A1: سقف ~1000 توكن للحقن · لقاح learn_match/vaccine_for · التقاط `[LEARN]` · deadlock cap في stop.py | ✓ (`session_start.py:35` token_budget=1000؛ `user_prompt_submit.py:63,71,81`؛ `stop.py:33` `_REMINDER_CAP=5`) |
| 3 | A2: substrate الست + schemas + selftest.sh في `.claude/engine/tooling/` | ✓ كلها موجودة |
| 4 | A5: `agent_invoker.py:268-269` يستدعي `claude -p` | ✓ حرفياً (`subprocess.run(["claude", "-p", prompt]...`) — نسخة WT |
| 5 | A5: `MOCK_FAIL_THEN_PASS` ينجح في المحاولة 2 | ✓ (`agent_invoker.py:14,338,403`) |
| 6 | A6: docstring «deterministic DAG scheduler … zero tokens on coordination» | ✓ حرفياً (`company/os/sofi_tools/scheduler.py`) |
| 7 | A3: تكافؤ 105 spawnables + 109 routes | ✓ (`ls .claude/agents \| wc -l` = 105؛ routing.yaml routes = 109) |
| 8 | A4: `validate_evidence()` داخل gate-check | ✓ (`gates.py:201` + استدعاء `cli.py:221`) |
| 9 | P2: `brain.db` بصفّ observations واحد | ✓ (`SELECT COUNT(*)` = 1) |
| 10 | P3: `oracle status` يعيد exit 0 حتى عند الفشل | ✓ (`gemini_review.py:408-410` — `return 0` غير مشروط) |
| 11 | P4: `.github/workflows/` فارغ تماماً | ✓ (موجود وفارغ في PRJ-SAKK؛ معدوم في MAIN/WT) |
| 12 | P5: `paths.py` صامت من الـ worktree + `branch/head_sha` فارغان | ✓ (fallback إلى `WT/projects` المعدوم بلا خطأ؛ `STATE.md:9-10` فارغان) |
| 13 | P1 (الجوهر): لا `LESSONS.md` لأي مشروع | ✓ (find = صفر نتائج) |
| 14 | N1: MAIN `session_start.py` يحقن «no slash-commands» + `engine/tooling/` | ✓ (السطور 77، 83-84) |
| 15 | N2/N3: dashboard عالم 30 وكيلاً · fork مزدوج وMAIN untracked | ✓ (README «30 agents»؛ `git status` = `?? orchestrator/`) |
| 16 | §3.1: translator MAIN=455 سطراً · state_db WT=356 · `ceo_agent.py` MAIN فقط untracked 14.8KB | ✓ كلها بالضبط (14799 بايت) |
| 17 | «G6» تسمية الـ fork | ✓ تطابق التقرير 08 (G6 = الإطار الخارجي) |
| 18 | ترقيم GAP-01..20 ونسبة كل GAP لموضوعه | ✓ يطابق 09-GAP-ANALYSIS.md |

**مطابقة مبادئ شامل:** مصدر حقيقة واحد ✓ (taskq الوحيد، HANDOFFS مرآة مولَّدة) · flat topology بلا daemon داخلي ✓ (cron خارجي فقط، watchdog نبضي) · كل مشروع git خاص ✓ (§2.4، §6.3) · token economy ✓ (حتمي/نموذجي مفصولان، budgets وmax-turns في كل استدعاء). لا خرق مبدئي وُجد خارج الثغرات المذكورة أعلاه.

---

*نهاية المراجعة — review-automation.md*
