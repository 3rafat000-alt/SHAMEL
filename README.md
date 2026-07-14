# شامل / SHAMEL — النظام الموحّد الجديد

> **ما هذا؟** الوثائق التأسيسية الكاملة لنظام «شامل» — الخليفة الموحّد لكل أجيال SOFI AI المتراكمة.
> بُني بأوركسترا 30 وكيلاً: 7 مدقّقين متوازيين فحصوا كل جيل على القرص → مصفوفة مقارنة + تحليل فجوات →
> 7 وثائق تصميم → مراجعة عدائية لكل وثيقة (دحض + إصلاح) → فحص اتساق عابر للوثائق.
> كل ادعاء عن النظام القائم مُسند بدليل `file:line` أو أمر + ناتج.

**التاريخ:** 2026-07-10 · **المصدر المفحوص:** `~/Desktop/Lorka` (كل الأجيال) · **الحالة:** وثائق معتمدة بعد التحقق العدائي

---

## اقرأ بهذا الترتيب

| # | الوثيقة | ماذا تجيب |
|---|---------|-----------|
| 1 | [`archive/00-analysis/09-GAP-ANALYSIS.md`](archive/00-analysis/09-GAP-ANALYSIS.md) | **لماذا نظام جديد؟** — 20 فجوة (2 CRITICAL · 7 HIGH · 7 MEDIUM · 4 LOW) |
| 2 | [`archive/00-analysis/08-COMPARISON-MATRIX.md`](archive/00-analysis/08-COMPARISON-MATRIX.md) | **من يفوز بماذا؟** — 6 أجيال × 10 أبعاد + 21 مكوّناً ذهبياً يُرحَّل |
| 3 | [`archive/01-prd/PRD.md`](archive/01-prd/PRD.md) | **ماذا نبني؟** — 46 FR + 10 NFR، كلٌّ مُسند لفجوة أو مكوّن فائز، بمعايير قبول ميكانيكية |
| 4 | [`archive/02-architecture/ARCHITECTURE.md`](archive/02-architecture/ARCHITECTURE.md) | **كيف يُبنى؟** — الطبقات، شجرة المجلدات، 5 قرارات ADR (منها مصير كل جيل قديم) |
| 5 | [`archive/02-architecture/BRAIN.md`](archive/02-architecture/BRAIN.md) | **العقل والدماغ** — توحيد 8 أنظمة ذاكرة متوازية في 3 طبقات بمالك لكل ملف |
| 6 | [`archive/02-architecture/PROTOCOL.md`](archive/02-architecture/PROTOCOL.md) | **البروتوكول الشامل** — العقد التشغيلي الواحد: RCCF، 9 بوابات، تأريض/تحقق، اقتصاد، git |
| 7 | [`archive/02-architecture/AUTOMATION.md`](archive/02-architecture/AUTOMATION.md) | **المؤتمت** — الصادق: ما يعمل بلا بشر فعلاً، داخل Claude Code وخارجه |
| 8 | [`archive/04-projects-method/PROJECT-STRUCTURE.md`](archive/04-projects-method/PROJECT-STRUCTURE.md) | **طريقة بناء المشاريع** — الهيكل القانوني، قانون VCS (كل مشروع git خاص)، مصنع يوم-صفر |
| 9 | [`archive/03-plan/MASTER-PLAN.md`](archive/03-plan/MASTER-PLAN.md) | **الخطة الكبرى** — 12 مرحلة من الإنقاذ إلى التشغيل الكامل، قبول G-01..G-12 |
| 10 | [`archive/03-plan/MIGRATION.md`](archive/03-plan/MIGRATION.md) | **الترحيل** — قرار لكل طبقة قائمة: يُرحّل / يُدمج / يُعاد / يُتقاعد + rollback |

---

## الهيكل

```
SHAMEL/
├── README.md                     ← أنت هنا
├── archive/                      ← أرشيف أجيال SOFI السابقة
│   ├── 00-analysis/                  الفحص والمقارنة (الأدلة)
│   ├── 01-prd/PRD.md                 وثيقة متطلبات المنتج
│   ├── 02-architecture/              التصميم (4 وثائق)
│   ├── 03-plan/                      الخطة الكبرى + الترحيل
│   ├── 04-projects-method/           مصنع المشاريع
│   └── 05-review/                    سجل التحقق العدائي
├── shamel/                       ← SHAMEL النظام الموحد
│   ├── core/                     ← الدستور، البروتوكولات، العقود، البوابات
│   ├── engine/                   ← CLI، أدوات، ماسحات، اختبارات
│   ├── brain/                    ← الذاكرة (6 مناطق + قواعد بيانات)
│   ├── agents/                   ← 106 وكيل بشخصيات بشرية
│   └── skills/                   ← مهارات متخصصة (Stripe, CCPayment...)
├── projects/PRJ-SAKK/           ← المشروع النشط
├── CLAUDE.md                     ← عقد الجلسة
├── MEMORY.md                     ← خريطة التوجيه
└── opencode.json                 ← إعدادات OpenCode
```

---

## الخلاصة التنفيذية

**الأجيال الستة المفحوصة:** OpenCode (`.opencode`) · Engine القديم (`engine/`) · v6 Company of Rooms (`company/` + 105 وكيل) · org-rooms (100 persona) · الطبقة الحتمية (`.claude/engine/tooling`) · الإطار الخارجي (`orchestrator/` + `tools/`).

**الحكم:** v6 يفوز بـ 8/10 أبعاد (doctor PASS، دستور مُسلَّك كوداً) والطبقة الحتمية تفوز بالأدوات (selftest 6/6) — لكن التعايش بينها هو المرض: **8 نقاط دخول تنفيذية، 8 أنظمة ذاكرة متوازية، 5 جرود وكلاء، حتى 6 تطبيقات لطابور المهام وحده.**

**أخطر فجوتين (CRITICAL — Phase 0 في الخطة):**
1. **GAP-01:** كود PRJ-SAKK الفينتك + دماغه الحي خارج أي git — والخطر متحقق مرتين (xo-game وheart-clinic ضاعا نهائياً).
2. **GAP-02:** ثلاث سلالات git متباعدة والجذر الرئيسي راكب فرعاً بلا نواة v6 — كود حي untracked مهدَّد (منه fork نشط للـ orchestrator).

**جوهر شامل:** مصدر حقيقة واحد لكل concern — جرد وكلاء واحد (spec آلي + persona بشري)، موزّع واحد، عقل بثلاث طبقات بمالك لكل ملف، بروتوكول واحد مرقّم، أتمتة حقيقية مُتحقَّق منها عدائياً، وكل مشروع ريبو git خاص منذ اللحظة صفر.

---

## سجل الجودة

- كل وثائق التصميم الست خضعت لمراجع عدائي مستقل → كلها احتاجت إصلاحات CRITICAL → **أُصلحت كلها** (السجل في `archive/05-review/`).
- الخطة الكبرى: **PASS** من أول مراجعة (تغطية كاملة لكل GAP بخطورة CRITICAL/HIGH).
- فحص الاتساق النهائي عبر الوثائق العشر: 25 تناقضاً (2 CRITICAL أُصلحا مباشرة، والبقية موثّقة في `archive/05-review/10-CONSISTENCY.md`).
