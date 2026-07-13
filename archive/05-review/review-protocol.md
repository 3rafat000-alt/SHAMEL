# مراجعة عدائية — `PROTOCOL.md` (شامل v1.0)

**المراجع:** gatekeeper (fresh-context، READ-ONLY) · **التاريخ:** 2026-07-10
**النطاق:** `_scratch/shamel/PROTOCOL.md` ضد: النظام القائم على القرص (Lorka worktree + main tree) + مجموعة التصميم الشقيقة (`ARCHITECTURE.md` · `AUTOMATION.md` · `BRAIN.md` · `PROJECT-STRUCTURE.md`).
**الحكم:** **FIX** — 5 نتائج CRITICAL تستوجب تعديل الوثيقة قبل اعتمادها. جوهر الوثيقة سليم (القواعد المرقّمة، الدمج G/V، الاقتصاد، git) لكنها تتناقض بنيوياً مع الـ Design Record الحاكم وتخرق مبدأ «مصدر واحد لكل concern» الذي تعِظ به.

---

## 1) فحص الادعاءات الواقعية — عيّنة 10 ادعاءات قابلة للفحص

| # | الادعاء في PROTOCOL.md | الحكم | الدليل |
|---|---|---|---|
| 1 | «21 ملفاً في `engine/protocols/`» (رأس الوثيقة) | ✅ صحيح | `~/Desktop/Lorka/engine/protocols/` = 21 ملفاً؛ والنسخة المؤرشفة `company/brain/org/archive-v5/protocols/` = 21 |
| 2 | route المثال §2.1: `workhorse · medium · ultra` لـ bck-blade-engineer | ✅ صحيح | `company/nexus/routing.yaml:85` — `{ model: workhorse, effort: medium, caveman: ultra }` |
| 3 | persona المثال §2.1: «أنت **أمينة رحمان** — bck-blade-engineer» | ❌ **خاطئ** | `company/rooms/05-backend/agents/bck-blade-engineer.md:3` — `persona_name: Aisha Rahman` (عائشة رحمان) |
| 4 | route مثال التذكرة §9.3: `workhorse · medium · full` لـ bck-code-reviewer | ❌ **خاطئ** | `company/nexus/routing.yaml:89` — `caveman: review` لا `full`؛ والوثيقة نفسها (W2 + مخطط bus) توجب النسخ **الحرفي** |
| 5 | فئات الجهد وميزانياتها §6.2 (1–3 · 3–10 · 2–5 وكلاء · 3–8 أبعاد · deep واحد) | ✅ صحيح | `company/nexus/routing.yaml:204-209` `effort_scaling` |
| 6 | قاطع الدائرة: سقف 3 محاولات، الفشل الرابع → crash-dump بالحقول المذكورة (بما فيها `last_oracle_command`) | ✅ صحيح | `routing.yaml:213` + `company/nexus/bus/escalation.md:45-48` |
| 7 | أدوات الإنفاذ المسمّاة: `validate_evidence()` · `validate_no_skip()` · `validate_room_boundary()` · `guard.assert_net_allowed` · `memdb.compress_session` | ✅ صحيح | `company/os/sofi_tools/gates.py:201,110,159` · `guard.py:98` · `memdb.py:332` |
| 8 | مخطط التذكرة §9.3 (الحقول، دورة `open→accepted→done|rejected`، `blocked→escalated` بـ `escalated_from:`، الأزواج المشروعة في I1) | ✅ صحيح | `company/nexus/bus/ticket-schema.md` §1–§4 — تطابق كامل |
| 9 | P1: حقن SessionStart بميزانية ≤1000 توكن | ✅ صحيح | `.claude/hooks/session_start.py:35` — `memdb.inject_digest(pid, token_budget=1000)` |
| 10 | P1/P3: «لقاح LESSONS» في SessionStart و«حقن التذكرة الحية» في UserPromptSubmit | ❌ **معكوس** | اللقاح في UserPromptSubmit (`user_prompt_submit.py:71` — `lessons_cache.vaccine_for`)، والتذكرة تُحقن في SessionStart (`session_start.py:88` — `next_ticket`)؛ ويؤكده جرد `AUTOMATION.md` A1 «فُحصت حيّة» |

**الخلاصة:** 7/10 صحيحة — الأساس الواقعي جيد؛ لكن الخطأين في **المثالين القانونيين** (persona مخترعة + route مخترع) فادحان لأن الوثيقة نفسها تجرّم الاختراع وتوجب الحرفية، وخطأ الـ hooks يقلب آلية موثّقة حيّاً.

---

## 2) النتائج مرقّمة بالخطورة

### CRITICAL

**C1 — صراع سيادة: بروتوكولٌ «وحيد» يتعايش مع دستورٍ يعيد التصميمُ الحاكم بناءه.**
PROTOCOL.md:5 «تخلف وتُلغي: دستور v6 + المواد 00–10 … **لا يوجد بروتوكول ثانٍ**؛ أي نص يخالفها في أي طبقة defect». لكن `ARCHITECTURE.md` (الـ Design Record الحاكم) يبني `core/CONSTITUTION.md` «**القانون الأعلى**» + المواد `core/constitution/00..11` («02/03 **يرحَّل حرفياً من v6**») — أي يُحيي حرفياً ما تلغيه PROTOCOL. والأدهى: **PROTOCOL.md لا موقع لها في شجرة ARCHITECTURE §2 إطلاقاً**، ولا وثيقة شقيقة واحدة تُشير إليها (grep على المجموعة كلها = صفر). مصدران أعليان لنفس الـ concern = خرق P1/GAP-06 الذي أُنشئ شامل لقتله، وخرق بند الوثيقة العاشر نفسه.
**العلاج:** بند تحكيم صريح + موقع في الشجرة: إمّا ADR يجعل PROTOCOL.md تحل محل `core/constitution/*` في ARCHITECTURE، أو تنزل PROTOCOL إلى «فهرس مُجمَّع non-normative» للدستور.

**C2 — نسخة gates.yaml كاملة مضمّنة وموصوفة بـ«النسخة المرجعية» = مصدرا حقيقة لدورة الحياة.**
PROTOCOL.md:7 + §3.1 يضمّنان الـ YAML كاملاً بعنوان «الجدول الآلي الواحد (النسخة المرجعية المضمّنة)» بينما السطر الأول فيه يقول إن `nexus/gates.yaml` هو «المصدر الآلي الوحيد». نسختان حيّتان لملف آلي واحد، مع غموض أيهما يحسم عند التعارض («توأمان؛ تعارضهما defect») — وآلية doctor المزعومة لمطابقة نصٍّ عربي بملف YAML **غير مصمَّمة في أي وثيقة** (doctor في ARCHITECTURE = parity وكلاء + pins فقط). خرق مباشر لمبدأ «concern واحد = مصدر واحد».
**العلاج:** حذف الـ YAML المضمّن أو وسمه صراحة «snapshot توضيحي غير مُلزِم — الملف هو المصدر الوحيد»، وحذف صفة «المرجعية».

**C3 — نظام مسارات وأدوات يناقض بقية المجموعة في كل نقطة حِمل.**
`bin/shamel` (PROTOCOL:11، §9.4) ↔ `engine/bin/shamel` (ARCHITECTURE §2/ADR-002) · `nexus/*` و`rooms/*` (U4، W2، §2.1) ↔ `core/nexus/*` و`core/rooms/*` (ARCHITECTURE) · D1 يجعل أداة إنفاذ قانون يوم-صفر `bin/new-project.sh` بينما `PROJECT-STRUCTURE.md:233` ينص «`shamel new` (**خليفة** new-project.sh)» وADR-002 «يموت نمط bash» — الوثيقة تُحيي bash ميتاً كأداة إنفاذ. في وثيقة توجب النسخ الحرفي للمسارات (W2/U4)، كل مسار حامل فيها خاطئ نسبةً للشجرة الحاكمة.
**العلاج:** مواءمة كل المسارات مع شجرة ARCHITECTURE §2 واستبدال `shamel new` بـ new-project.sh.

**C4 — §9.4 «crontab المعتمد» يزدوج مع ملف التفعيل الوحيد في AUTOMATION.md ويستدعي skill غير موجودة.**
AUTOMATION §2.3: «ملف التفعيل **الوحيد** — `cron/shamel.crontab`» بقواعد ملزمة (reflect **أسبوعي** بـ `--max-turns 15`، سجلات `.shamel/logs/`، فشل → `shamel notify`). PROTOCOL §9.4 يعلن crontab آخر «معتمداً»: reflect **يومي** 22:00 بلا سقف turns، سجلات `.claude/memory/`، بلا notify، وسطر `claude -p "/budget-audit"` — **skill لا وجود لها** في أي جرد (الـ 13 في ARCHITECTURE §5 لا تشملها)، فيسقط في قاعدته هو: «ما لا مشغّل له لا يُدّعى» (§9.4) و«ادعاء بلا مشغّل كذب» (بند 9). (وBRAIN.md §5 يعرض جدولة ثالثة مختلفة — الازدواج ثلاثي عبر المجموعة.)
**العلاج:** §9.4 يُشير إلى `cron/shamel.crontab` كمصدر وحيد ويستعمل أسماء skills الموجودة فعلاً؛ يُحذف الجدول المضمّن أو يوسم مثالاً غير مُلزِم.

**C5 — U13 المطلقة تجعل التزامات الوثيقة نفسها مستحيلة التنفيذ.**
U13: «اكتب الـ artifact داخل `projects/<PRJ>/` **حصراً** — لا خارج مشروعك أبداً» بإنفاذ PreToolUse fail-closed، والرأس: «ملزم لكل وكيل … **بلا استثناء**». لكن الوثيقة ذاتها توجب كتابات خارج projects/: تعديلها بـ ADR في `brain/org/DECISIONS.md` (السطر 9)، عقيدة على `main` «من يعدّل نظام شامل نفسه» (§8.1)، دروس reflection وLESSONS التنظيمية (§9.4). الحارس كما هو منصوص يحجب أمر العمل الدستوري نفسه.
**العلاج:** حصر U13 بعمل المشاريع + جدول استثناءات مسمّى (doctrine على main · brain/org لأدوار knw/boardroom · مخرجات reflection) بمالك لكل استثناء.

### HIGH

**H6 — المثال القانوني §2.1 يخترع persona.** «أمينة رحمان» غير موجودة؛ الملف القانوني يقول `Aisha Rahman` (`bck-blade-engineer.md:3`). أول block تعليمي في الوثيقة يخرق W2 (النسخ الحرفي من الـ spec) — بالضبط النمط الذي تسميه الوثيقة «وكيل يخمّن».

**H7 — مثال التذكرة §9.3 يخترع route.** `workhorse · medium · full` بينما `routing.yaml:89` = `caveman: review`. مخطط bus القائم ينص «copied **verbatim** … never invented».

**H8 — P1/P3 يعكسان حمولتي الـ hooks الموثّقتين حيّاً.** اللقاح في UserPromptSubmit والتذكرة في SessionStart (الأدلة في جدول §1 بند 10). وثيقة تدّعي أن «كل خطوة مربوطة بأداة أو hook محدد» تربط خطوتين بالـ hook الخطأ. (يُضاف: ARCHITECTURE لا يذكر hook `UserPromptSubmit` أصلاً — خُماسيته: pre_tool_use/session_start/post_tool_use/stop/hook_health — فإما نقص هناك أو ادعاء هنا؛ يُحسم بالتوحيد.)

**H9 — ادعاءات إنفاذ بلا مشغّل مسمّى، خرقاً لقاعدة الوثيقة نفسها.** L8: «تذكرة تلقائية» عند خرق SLO بإنفاذ «hook تذاكر» — لا hook كهذا في أي جرد خُماسي. G5: «فحص coherence في حلقة reflection» — المجموعة (ARCHITECTURE §3.4) تُسند فحص تعارض STATE↔code إلى **doctor** لا إلى reflection. E7: «نمط delegate-reads» بلا أداة. بند 9 من عهدها: «ادعاء بلا مشغّل كذب».

**H10 — قائمة التوائم الآلية ناقصة.** الرأس يسمّي 3 توائم (registry/routing/gates) ويُسقط `models.yaml` (طبقة alias — GAP-17، محورية في ARCHITECTURE §3.1) و`pins.json` (بصمات ADR-003)؛ §6 يقول «طبقة alias في ملف واحد» بلا تسمية الملف. concern اقتصادي حامل بلا توأم مسمّى.

### MEDIUM

**M11 — إلغاء بلا تغطية (أقسام ناقصة عن الـ brief).** الوثيقة تلغي دستور v6 + 21 بروتوكولاً ثم تُسقط بلا بديل ولا pointer: (أ) **القواعد الفولاذية السبع / بوابة spec-review الصلبة** (skill قائمة في الـ 13، صفر ذكر هنا)؛ (ب) **قانون الدومين المحلي** `<slug>.local` كخطوة بناء أولى — لا يظهر إلا عرضاً داخل entry بوابة 0؛ (ج) **قانون الذاكرة**: trigger «تذكّر» الوحيد للكتابة العقائدية + «MEMORY.md pointers فقط» (موجودان في BRAIN.md:175 — لكن وثيقةً تدّعي أنها «مصدر الحقيقة الواحد للسلوك» لا يجوز أن تُسقطهما بلا إحالة).

**M12 — نموذج الفروع §8.1 إرث v6 مشوّش في عالم repo-لكل-مشروع.** فرع `prj/<PRJ-ID>` داخل repo مخصص للمشروع أصلاً زائدة بلا تعريف لعلاقته بـ main **المشروع** (غير معرّف)؛ وD2 «لا تدمج فرع مشروع في main» تخلط main الإطار بـ mainline المشروع وهما في repo-ين مختلفين لا يلتقيان. وموطن worktrees غير محدد (ARCHITECTURE: `.worktrees/` بجذر الريبو).

**M13 — فضاء أسماء skills متضارب.** `/boot` `/gate` `/handoff` `/delegate` `/reflect` `/report` هنا ↔ `/shamel-boot` `/shamel-reflect`… في AUTOMATION.md. الاستدعاء الحرفي في cron يجعل الاسم حاملاً.

**M14 — مواطن حالة الـ runtime متضاربة.** §7 وP7 وD10: `.claude/memory/audit.jsonl` و`sessions.jsonl` ↔ ARCHITECTURE: `brain/db/sessions.jsonl` (وaudit.jsonl لا وجود له في الشجرة الحاكمة).

**M15 — I3 يستشهد بـ `shared-packages/` بلا موطن.** المسار غير موجود في شجرة ARCHITECTURE (وفي v6 كان `.claude/shared-packages`) — مسار حامل لقانون العزل بلا عنوان.

### LOW

**L16 — هنات صياغة:** §3.1 تعليق «يستهلكه gate-check/squad//gate» (شرطة مزدوجة/اسم مبتور) · E5 يستشهد بـ«قاعدة S8» لقانون عدم-ضغط-النص-الأمني بينما S8 = فيتو CSO (الإحالة الصحيحة: ديباجة §7) · الـ YAML المضمّن يستعمل `owner_room` وARCHITECTURE ينص الحقل `owner`.

---

## 3) ما صمد أمام الدحض (إنصافاً)

- **flat topology بلا daemon داخلي:** محفوظ بلا خرق — U11/W10 (leaf-spawn قفزة واحدة)، §9.4 cron+`claude -p` حصراً، P6/P7 hooks داخل الجلسة فقط. لا daemon متخفٍّ في أي بند.
- **repo خاص لكل مشروع:** D1 (يوم-صفر، الدماغ داخل repo المشروع) متسق مع ARCHITECTURE/PROJECT-STRUCTURE — التشويش في M12 فرعي (نموذج الفروع) لا جوهري.
- **token economy:** §6 أمين لـ routing.yaml القائم (سلّم، فئات، caveman، استثناء الأمن/الكود) — تحقق حرفي.
- **placeholders:** الوثيقة كثيفة بلا أقسام فارغة؛ العمومية محصورة في خلايا إنفاذ معدودة (H9/L16)، واصطلاح `—` للقواعد العقائدية مُعلَن سلفاً فمقبول.
- 7/10 من الادعاءات الواقعية المفحوصة دقيقة حتى مستوى `file:line`.

## 4) الحكم

**FIX.** الأخطاء ليست في روح القواعد بل في **موقع الوثيقة من المجموعة ومساراتها وأمثلتها**: C1–C5 تجعلها — كما هي — غير قابلة للتنفيذ الحرفي وتخرق أول مبادئها (مصدر واحد لكل concern). إصلاحها جراحي لا بنيوي.
