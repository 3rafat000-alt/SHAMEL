# تدقيق شامل — أنظمة الذاكرة/الدماغ/البروتوكولات عبر الأجيال + لغز git

**التاريخ:** 2026-07-10 · **النطاق:** MAIN=`/home/es3dlll/Desktop/Lorka` · WT=`/home/es3dlll/Desktop/Lorka/.claude/worktrees/org-rooms-100` · **الوضع:** READ-ONLY

---

## الجرد

### أنظمة الذاكرة المتوازية — العدّ الكامل: **8 أنظمة**

| # | النظام | الموقع | الحالة | الدليل |
|---|--------|--------|--------|--------|
| 1 | **MEMORY.md (خريطتا توجيه متعارضتان)** | `MAIN/MEMORY.md` (3322 B) vs `WT/MEMORY.md` (6339 B) | حيّان معاً — **متباينان** | `md5sum`: `43ad71…` vs `0fddaf…`؛ نسخة MAIN توجّه إلى `engine/protocols/*` و`engine/tooling/registry.yaml` (MEMORY.md:19-20,48)؛ نسخة WT توجّه إلى `company/constitution/*` و`company/nexus/registry.yaml` (WT/MEMORY.md:19,37) |
| 2 | **Project brain الحي** | `MAIN/projects/PRJ-SAKK/_context/` (STATE·CONTEXT·DECISIONS·HANDOFFS) | **حيّ** — آخر كتابة 2026-07-09 22:48 (STATE.md) | لكن **غير مُدار بأي git**: لا يوجد `.git` داخل PRJ-SAKK ولا داخل `backend/`؛ `git rev-parse --show-toplevel` من داخله = `/home/es3dlll/Desktop/Lorka`، و`projects/` مُتجاهَل في `.gitignore:20` (`/projects/`) |
| 3 | **company/brain (دماغ v6 المؤسسي)** | `WT/company/brain/` — BRAIN.md (3 طبقات) + `org/` (6 ملفات + archive-v5) + `templates/` (6 قوالب) | حيّ نظرياً — **مستنسَخ من engine** | `org/HANDOFFS.md` و`org/PERSONAS.md` **متطابقان بايت-بايت** مع `engine/{HANDOFFS,PERSONAS}.md` (diff=IDENTICAL)؛ DECISIONS يختلف بـ4 أسطر فقط |
| 4 | **Session breadcrumbs (jsonl)** | `MAIN/.claude/memory/sessions.jsonl` (47 سطراً) · `WT/.claude/memory/sessions.jsonl` (7 أسطر) | MAIN **حيّ فعلاً** (آخر سطر: `2026-07-09T21:04 head=483d355 uncommitted=7`)؛ WT شبه اختباري (آخر session_id=`"test"`) | gitignored (`.gitignore:39-40`) |
| 5 | **brain.db (memdb — v6.1)** | `WT/.claude/memory/brain.db` (SQLite: `observations` + FTS5 + `sections`) | مبنيّ لكن **وليد**: صف observations واحد فقط | فحص sqlite read-only: `obs rows: (1,)` |
| 6 | **ذاكرة جيل engine (AUTOPILOT/DOCTRINE)** | `MAIN/engine/{HANDOFFS,DECISIONS,EVOLUTION,PERSONAS,TEAM_STATUS}.md` | **ميّتة/مُتجاوَزة** — لقطة نُسخت إلى company/brain/org ثم تجمّدت | مطابقة HANDOFFS/PERSONAS أعلاه؛ EVOLUTION تباعد (60 سطراً مغيّراً) لأن نسخة v6 استمرت وحدها |
| 7 | **ذاكرة جيل .opencode** | `MAIN/.opencode/memory/` — 4 ملفات jsonl **كلها 0 بايت** | **ميّتة** | `ls -la`: audit.jsonl/edit-tracker.json/events.jsonl/sessions.jsonl جميعها size=0؛ `.opencode/` مُتجاهَل (`.gitignore:8`) |
| 8 | **Harness memory + claude-mem** | `~/.claude/projects/-home-es3dlll-Desktop-Lorka/memory/` (MEMORY.md + ملفان) و**20 مجلد مشروع harness** لنفس الشجرة (Lorka، 6 worktrees، PRJ-SAKK، backend…) | **حيّان** (آخر تحديث 2026-07-09 20:16) — البنية مؤكدة دون قراءة المحتوى | `ls ~/.claude/projects/` — 20 مدخلاً متعلقاً بالمساحة |

**أرشيف مجمّد (لا يُحسب نظاماً):** `WT/company/brain/org/archive-v5/` — DOCTRINE/ROSTER/RUNBOOK/protocols v5 كاملة، read-only.

**الخلاصة:** 8 أنظمة متوازية؛ الحي فعلاً: #2 (دماغ المشروع)، #4-MAIN (breadcrumbs)، #8 (harness/claude-mem)، وخريطتا MEMORY.md متعارضتان. **لا يوجد مصدر حقيقة واحد** — نفس السؤال ("أين العقيدة؟") يعطي جوابين مختلفين حسب الشجرة التي فُتحت فيها الجلسة.

### البروتوكولات — جيلان كاملان متوازيان

- `MAIN/engine/protocols/` = **21 ملفاً** · `WT/company/constitution/` = **11 مادة** (00–10).
- **8 مفاهيم جوهرية مكررة بصياغتين متباينتين** (diff ≠ 0 لكل زوج):

| المفهوم | engine (أسطر) | constitution (أسطر) |
|---|---|---|
| Operating System | `00-operating-system.md` (75) — «30 agents/5 tiers»، يخدم `engine/DOCTRINE.md` (6 teachings) | `00-operating-system.md` (84) — «105 agents/15 rooms»، يخدم `company/CONSTITUTION.md` (7 teachings) |
| Delegation/RCCF | `01-delegation-rccf.md` (215) | `01-work-order.md` (157) |
| Grounding | `grounding.md` (26) | `02-grounding.md` (30) |
| Verification | `verification.md` (30) | `03-verification.md` (45) |
| Reflection | `reflection.md` (22) | `04-reflection.md` (26) |
| Git | `git-discipline.md` (130) | `06-git-discipline.md` (120) |
| Handoff | `handoff-and-interconnection.md` (76) | `08-handoff-law.md` (56) |
| Research | `research-and-internet.md` (34) | `09-research-law.md` (48) |

- **حصري لـ engine (بلا مقابل دستوري):** `02-intake-orchestration.md`، `02-autonomous-gemini-loop.md`، `03-ooda-loop.md`، `server-plane.md`، `spec-review.md`، `context-and-memory.md`، `incident-response.md`، `tooling-matrix.md`، وغيرها.
- **تناقض عقائدي مباشر:** `engine/protocols/02-intake-orchestration.md:1-15` يشرّع «team works without slash-commands — no menu of / commands» (binding)، بينما v6 يبني الانضباط كله على 13 skill بصيغة `/sofi-*` (WT CLAUDE.md «Session lifecycle»). جيلان يأمران بعكس بعضهما.

### أيّ نسخة يستدعيها الـ hook فعلاً؟

- كلا `settings.json` يستخدم `$CLAUDE_PROJECT_DIR/.claude/hooks/*.py` (MAIN: settings.json:45,55,66,76 · WT: settings.json:48,58,68,79,89) → **كل شجرة تشغّل جيلها**، ولا مسارات معلّقة (dangling):
  - **MAIN** `session_start.py:78-86` يحقن حرفياً: «no slash-commands … `engine/protocols/02-intake-orchestration.md`» + «`engine/tooling/` … `python3 engine/tooling/agents/ceo/sofi_scan.py`» — والملفات **موجودة** (تحقق ls).
  - **WT** `session_start.py:94-100` يحقن: «palette (`company/constitution/00-operating-system.md`) … `/sofi-boot` … `/sofi-feature`» + digest من `memdb` عبر `company/os/sofi_tools` (session_start.py:32-35) — موجودة.
- فرق تغطية: WT يسجّل **UserPromptSubmit** (settings.json:63-72)؛ MAIN لديه `user_prompt_submit.py` على القرص (untracked) لكنه **غير مسجّل** في settings.json → كود ميّت.
- النتيجة: فتح Claude في MAIN يحقن عقيدة «فريق مباشر بلا أوامر»، وفتحه في WT يحقن عقيدة «الـ13 skill» — **انفصام دماغي بحسب مجلد الإقلاع**.

### Oracle desk (بوابة Gemini)

- `WT/company/os/oracle/` = **3 ملفات توثيق فقط** (GEMINI_IMPLEMENTATION_GUIDANCE, GEMINI_LOOP_ARCHITECTURE, TESTING_TEACHING_VII) — التنفيذ ليس هنا.
- التنفيذ الفعلي: `company/os/agents/ceo/gemini_review.py` (437 سطراً) + `gemini_bridge.py`؛ التعقيم موجود: `def sanitize(` (gemini_review.py:118) و`def condense(` (:177). الربط: `cli.py:581-587` (`sofi oracle` → gemini_review.py) والاسم القديم `sofi gemini` alias (:675).
- اختبار تشغيلي: `bash company/os/bin/sofi oracle status` → يعمل ويفشل بأناقة: «cannot attach to browser on CDP port 9222 — start it with --remote-debugging-port=9222» (exit=0). أي أن الآلية **browser-automation عبر CDP على جلسة Chrome/Gemini يدوية مثبتة** — ليست API. مكتملة كوداً، هشّة تشغيلياً (تتطلب متصفحاً يدوياً حياً)، و`status` يعيد exit 0 حتى عند الفشل (probe لا gate).

---

## الصحة

- **دماغ المشروع الحي (PRJ-SAKK/_context):** محدّث ومتّسق (Gate 6، STATE:8) — لكنه **صفر نسخ احتياطي**: خارج أي git (خرق مباشر لـ BRAIN.md:14 «committed in the project's OWN repo» ولـ CLAUDE.md «each PRJ-XXXX/ is its own git repo»). حذف مجلد = فقدان كل تاريخ المشروع.
- **STATE.md نفسه ناقص العقد:** `branch:` و`head_sha:` **فارغان** (STATE.md:9-10) رغم أن العقد الكوني يوجب تسجيلهما.
- **Stop hook (MAIN):** يعمل فعلاً — 47 سطراً حقيقياً، آخرها يرصد `uncommitted: 7`.
- **memdb/brain.db (v6.1):** بنية FTS كاملة لكن شبه فارغة (صف واحد) — أوتوماتيكية مكتوبة لم تعش بعد.
- **LESSONS:** لا يوجد `projects/PRJ-SAKK/_context/LESSONS.md` إطلاقاً (ls: No such file) — حلقة التعلّم لم تدُر ولا مرة على المشروع الوحيد الحي.
- **hooks كلها fail-open** (exit 0 دائماً) — صحّي للتشغيل، لكنه يعني أن فشل الذاكرة صامت.

---

## نقاط القوة

1. **تصميم الطبقات الثلاث في BRAIN.md ممتاز** (org / project / session بجدول أعمار وملكية صريح — BRAIN.md:10-15) — أفضل توصيف ذاكرة في كل الأجيال.
2. **الـ hooks حقيقية لا نظرية:** حقن التوجيه عند SessionStart مُثبت تشغيلياً، وbreadcrumbs الجلسات تتراكم فعلاً (47 جلسة).
3. **MEMORY.md كخريطة توجيه (pointers لا content)** مبدأ سليم ومطبّق في النسختين، مع سلّم بحث صريح (WT/MEMORY.md:7-12).
4. **Oracle desk بطبقة تعقيم مدمجة** (sanitize/condense قبل أي خروج للخارج) — التزام فعلي بقانون «sanitized only».
5. **الأتمتة المتدرجة في WT stop.py** (compress_session + gate-reminder متصاعد ومسقوف بـ`_REMINDER_CAP=5`، لا يحجب أبداً — stop.py:33,87-89) — هندسة ناضجة.
6. **archive-v5 مجمّد كتاريخ read-only** — نمط صحيح للتقاعد (على عكس engine/ و.opencode/ المتروكين بلا شاهد قبر).

## نقاط الضعف

1. **دماغ المشروع الحي غير مُصدَّر (unversioned)** — أخطر نقطة في التدقيق كله: العمود الفقري للذاكرة خارج git تماماً.
2. **خريطتا MEMORY.md متناقضتان** توجّهان لجيلين مختلفين من نفس الجذر — «مصدر الحقيقة» نفسه مزدوج.
3. **8 أنظمة ذاكرة متوازية، 3 منها جثث** (engine root files، .opencode/memory، WT sessions التجريبي) بلا أي علامة إهمال (deprecation marker).
4. **العقيدة مكررة بصياغتين متباعدتين** (8 أزواج diff≠0) + تناقض صريح (slash-commands محرَّمة في جيل ومقدَّسة في آخر).
5. **حلقة reflection نظرية:** `/sofi-reflect` موجودة في WT فقط (MAIN حذف الـskills في 9a439ce)، `crontab -l` فارغ، لا LESSONS.md لأي مشروع — «scheduled dreaming» بلا مجدوِل.
6. **Oracle معتمد على متصفح يدوي** (CDP :9222) — نقطة فشل تشغيلية واحدة بلا fallback API.
7. **MAIN user_prompt_submit.py غير مسجّل** — كود موجود لا يستدعيه أحد.

---

## التداخل مع الطبقات الأخرى

- **engine ↔ company/brain:** org brain في v6 وُلد نسخاً حرفياً من ملفات engine (HANDOFFS/PERSONAS متطابقان بايت-بايت) — أصل مشترك ثم تباعد صامت (EVOLUTION: 60 سطراً فرقاً).
- **engine/protocols ↔ company/constitution:** نفس القانون بصيغتين (الجدول أعلاه)؛ أي agent يقرأ حسب جذره يعيش تحت دستور مختلف.
- **MAIN/.claude (port .opencode: 105 agents + 107 skills بلا sofi-*) ↔ WT/.claude (v6: 105 agents + 13 sofi-* skills):** جيلان لواجهة `.claude` نفسها؛ MAIN/CLAUDE.md:4-6 يصرّح أنه «faithful port of the .opencode organisation» بينما WT/CLAUDE.md v6 يبني على company/.
- **claude-mem/harness ↔ ذاكرة SOFI:** طبقة رابعة خارجية (observations + auto-memory) تعمل فوق الكل ولا يشير إليها إلا سطر واحد في MEMORY.md (`mem-search`) — تكامل بالصدفة لا بالتصميم.
- **oracle:** موجود في الجيلين (`engine/tooling/agents/ceo/gemini_review.py` داخل الـstash أيضاً) — نفس الأداة منسوخة مرتين.

---

## لغز git — التحقيق والإغلاق

**الوقائع (كلها read-only):**
1. `git sparse-checkout list` → **`fatal: this worktree is not sparse`**؛ `ls-files -v | grep -c '^S'` → **0** skip-worktree. ⇒ لا sparse ولا skip.
2. `git ls-tree --name-only HEAD` (483d355) → 8 مداخل فقط: `.claude .claudeignore .gitignore CLAUDE.md MEMORY.md dashboard engine index.html`. **شجرة HEAD نفسها لا تحوي company/ ولا org-rooms/ أصلاً** — الشجرة العاملة مطابقة لـHEAD (status: تعديل واحد + 6 untracked)، فلا شيء «منزوعاً» نسبةً إلى HEAD.
3. النسب: `merge-base prj/PRJ-SAKK origin/main` = `10dcfbe` (2026-07-04)؛ الفرع **23 أمام / 8 خلف** origin/main. `origin/main@1bf6a30` هو الذي يحوي company/org-rooms/tools/orchestrator (وأسقط engine/ من شجرته). حتى `main` المحلي منفصل: **9 أمام / 8 خلف** origin/main، عالق عند حقبة n8n (`3d5f8ec`).
4. **الـstash:** `stash@{0}: On prj/PRJ-SAKK: teardown-backup before SOFI team activation 2026-07-09`، أبوه `9a439ce`. المحتوى: **3368 ملفاً، 505,927 حذفاً / 139 إضافة** — التفصيل بالمجلد (`diff --name-only stash^ stash`): engine/ **3265** ملفاً، .claude/ 93، dashboard/ 7، حذف CLAUDE.md وindex.html، وتعديل MEMORY.md. أي: في 2026-07-09 جُرّدت شجرة العمل من الجيل القديم بالكامل (engine + .claude القديم)، ثم **`git stash` حفظ ذلك الهدم كنسخة احتياطية وأعاد الملفات إلى مكانها**؛ بعدها هبط commit `4b4d9ed` (440 ملفاً: نقل .opencode → .claude native، الـ105 agents) ثم `483d355`.

**التفسير (إغلاق اللغز):** لا يوجد أي «نزع» تقني — إنها **مغالطة توقّع**: المراقِب يتوقع محتوى origin/main (company/, org-rooms/) في الجذر، لكن الجذر راكب فرع منتج (`prj/PRJ-SAKK`) تفرّع قبل دمج طبقة v6 ولم يلحقها قط. `git status` نظيف لأن status يقارن بـHEAD لا بـorigin/main. (وبالمناسبة: فرضية «.claude/agents=15» في خريطة المهمة غير دقيقة — الـ15 هي مجلدات الغرف؛ `find .claude/agents -name '*.md' | wc -l` = **105** في MAIN و105 في WT.)

**الخطر الحالي:**
- ثلاث سلالات عقيدة متباعدة في مستودع واحد (prj/PRJ-SAKK ×origin/main ×main المحلي) بعقود CLAUDE.md/hooks متناقضة — أي دمج مستقبلي سيكون تصادمياً (CLAUDE.md وMEMORY.md و.claude/ معدَّلة في الجهتين).
- الـstash عرضة للضياع بـ`stash drop/clear` عرَضي (وإن كان جوهر محتواه محفوظاً في تاريخ `9a439ce` لأنه يسجّل حذوفاً لملفات متتبَّعة — قيمته الفريدة: تعديل MEMORY.md والإضافات الـ139).
- `projects/` الحي خارج أي تتبع (النقطة الحمراء أعلاه) — أفدح من الـstash بكثير.

**التصحيح الآمن (لا يُنفَّذ الآن):** (1) قرار توحيد صريح: اعتماد origin/main مرجعاً ثم إعادة زرع حمولة prj/PRJ-SAKK الفريدة (4b4d9ed+483d355 أو ما يُنتقى منها) فوقه عبر merge/cherry-pick على فرع جديد، مع حسم تصادم CLAUDE.md/MEMORY.md يدوياً؛ (2) قبل أي شيء: `git init` داخل projects/PRJ-SAKK وcommit أولي لـ`_context/` والكود؛ (3) إبقاء الـstash حتى اكتمال المصالحة ثم توثيق قرار التخلص في ADR؛ (4) بعد التوحيد: دفن engine/ و.opencode/ في archive بنمط archive-v5 لا تركهما أحياء-أمواتاً.

---

## أتمتة الذاكرة — المؤتمت فعلاً vs النظري

| الآلية | الحالة | الدليل |
|---|---|---|
| SessionStart → حقن STATE + ticket | **مؤتمت ويعمل** (الجيلان) | كود الـhook + سجل تشغيل مُشاهد (orientation ظهر في جلسات سابقة) |
| Stop → sessions.jsonl | **مؤتمت ويعمل** في MAIN (47 سطراً حقيقياً) | آخر سطر `2026-07-09T21:04… uncommitted:7` |
| Stop → memdb.compress_session + gate-reminder | مؤتمت **في WT فقط**، وليد | stop.py:92-101,56-89؛ brain.db صف واحد |
| UserPromptSubmit → حقن ticket | WT: مسجّل ويعمل؛ MAIN: **الملف موجود وغير مسجّل** | مقارنة settings.json (WT:63-72 موجود، MAIN غائب) |
| PreToolUse guard / PostToolUse nudge | مؤتمتان (الجيلان) | settings.json + الملفات موجودة |
| claude-mem observations + harness memory | **مؤتمت خارجياً** (plugin) | ملاحظات محقونة أثناء هذا التدقيق نفسه |
| `/sofi-reflect` → LESSONS | **نظري**: skill في WT فقط، لا cron (`crontab -l` تعليقات فقط)، لا LESSONS.md لأي مشروع، «scheduled» بلا مجدوِل | ls skills + crontab |
| `knw-reflector` | **نظري**: spec/agent موجود (105 parity) لكنه spawn-on-demand، لا مشغّل تلقائي | `.claude/agents/knw/knw-reflector.md` موجود في الشجرتين |
| scheduler.py | **ليس مجدوِل زمن** — DAG walker لـ`sofi plan/run` (docstring:1-12)؛ لا علاقة له بالـreflection | scheduler.py head |

**الخلاصة:** الالتقاط (capture) مؤتمت جيداً؛ **التقطير (distillation) والتوحيد يدويان بالكامل** — الذاكرة تتراكم ولا تتعلّم.

---

## ما يُرحَّل لنظام شامل

1. **نموذج الطبقات الثلاث من BRAIN.md** (org/project/session بجدول ملكية وأعمار) — يُرحَّل كما هو كهيكل ذاكرة شامل الوحيد، مع **إنفاذ** بند «project brain في repo المشروع» الذي بقي حبراً.
2. **MEMORY.md كخريطة pointers واحدة** — نسخة WT (الأحدث والأشمل، بأقسام write-triggers) هي الأساس؛ تُقتل نسخة MAIN.
3. **company/constitution 00–10** كصياغة العقيدة الوحيدة؛ يُلتقط منها الجوهر الفريد في engine قبل الدفن: منطق **intake-orchestration** (wear-the-hierarchy، leaf-spawn one hop) قيّم ويستحق مادة دستورية بدل التناقض الحالي مع الـskills.
4. **الـhooks الأربعة + الخامس (UserPromptSubmit) بنسخة WT** (memdb digest + gate-reminder المسقوف) — أنضج نسخة موجودة.
5. **memdb/brain.db (FTS5)** كعمود فقري للذاكرة القابلة للاستعلام — يحتاج فقط من يملؤه (ربط claude-mem أو الـobservations به).
6. **Oracle desk**: gemini_review.py مع sanitize/condense — يُرحَّل بشرط إضافة مسار API fallback وإنهاء الاعتماد الحصري على CDP اليدوي.
7. **نمط archive-v5** كإجراء تقاعد معياري لأي جيل يُطوى (يُطبَّق فوراً على engine/ و.opencode/).
8. **سياسة الكتابة «تذكّر»/contract-driven** (WT/MEMORY.md:92-96) — أوضح فصل بين ذاكرة العقيدة وذاكرة المشروع في كل الأجيال.
9. **قرار git التوحيدي** (فرع مرجعي واحد فوق origin/main) شرط مسبق لأي «شامل» — لا نظام موحّداً فوق ثلاث سلالات.

---

## الحكم

**DEGRADED** — الذاكرة الحية تعمل (hooks حقيقية، دماغ مشروع محدّث، oracle مكتمل كوداً) لكن 8 أنظمة متوازية بلا مصدر حقيقة واحد، وخريطتا MEMORY.md وجيلا بروتوكولات يتناقضان حسب مجلد الإقلاع، ودماغ المشروع الوحيد الحي خارج أي git، وحلقة reflection نظرية بالكامل — البنية سليمة التصميم، مهترئة التوحيد.
