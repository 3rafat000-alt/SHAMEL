# BASAL-GANGLIA — الروتين والعادات (Routines & Habits)
**العمليات التلقائية — ما يحدث بدون تفكير، في كل جلسة، كل خطوة**

```
BASAL-GANGLIA = العادة — ينفذ الروتين بدون استهلاك طاقة ذهنية
     ↓
يسحب من THALAMUS (التوجيه) و CORTEX (المعرفة)
     ↓
يُغذّي HIPPOCAMPUS (تسجيل ما حدث)
     ↓
يُبلغ AMYGDALA إذا انحرف الروتين
```

---

## | روتين بدء التشغيل (Boot Routine)

يُشغّل في بداية كل جلسة — تلقائياً، بدون أمر:

```
الخطوة 1: shamel doctor
    ↓ (تحقق صحة النظام — إذا فشل → توقف)
الخطوة 2: قراءة CORTEX.md ← الذاكرة الدائمة
    ↓
الخطوة 3: قراءة THALAMUS.md ← التوجيه الحالي
    ↓
الخطوة 4: قراءة PREFRONTAL.md ← الخطط النشطة
    ↓
الخطوة 5: مسح HIPPOCAMPUS.md ← جلسة جديدة
    ↓
الخطوة 6: مسح WORKING.md ← توليد snapshot جديد
    ↓
الخطوة 7: كتابة WORKING.md ← التاريخ، الفرع، commit
    ↓
الخطوة 8: التحقق من AMYGDALA.md ← هل هناك تنبيهات مفتوحة؟
    ↓
الخطوة 9: قراءة CONSTITUTION.md ← تذكير بالقوانين
    ↓
الخطوة 10: ← انتظار طلب المستخدم
```

**المدة المتوقعة:** < 10 ثوان
**إذا فشل:** `shamel doctor` يحدد المشكلة، AMYGDALA يسجل تنبيهاً

---

## | الروتين اليومي (Daily Routines)

### R-001: التقاط سياق الجلسة
- **التوقيت:** عند بدء كل جلسة
- **المنفذ:** gtw-dispatcher تلقائياً
- **الإجراءات:**
  1. قراءة `git log --oneline -5`
  2. تسجيل التاريخ والفرع والـ SHA في WORKING.md
  3. التحقق من التغييرات غير الملتزمة
  4. تسجيل في `brain/db/sessions.jsonl`
- **المخرجات:** WORKING.md محدث

### R-002: تسجيل القرارات
- **التوقيت:** بعد كل قرار مستوى 🟡 أو أعلى
- **المنفذ:** الوكيل الذي اتخذ القرار
- **الإجراءات:**
  1. فتح قالب DECISIONS.md
  2. تعبئة: العنوان، السياق، الخيارات، القرار، السبب
  3. حفظ في `brain/org/DECISIONS.md` برقم ADR-NNN
  4. تحديث CORTEX.md (آخر 10 قرارات)
  5. ربط مع RCCF إن وجد
- **المخرجات:** ADR جديد في السجل

### R-003: تقطير الدروس
- **التوقيت:** نهاية كل جلسة أو بعد حادثة
- **المنفذ:** knw-reflector
- **الإجراءات:**
  1. مراجعة HIPPOCAMPUS للدروس المحتملة
  2. صياغة الدرس بصيغة: "ماذا حدث؟ ماذا تعلمنا؟ ماذا سنفعل مختلفاً؟"
  3. تسجيل في `brain/org/LESSONS.md` برقم LES-NNN
  4. تحديث PREFRONTAL.md (الدروس المطبّقة)
  5. إن كان الدرس عاجلاً → إشعار CEO
- **المخرجات:** LES جديد + تحديث PREFRONTAL

### R-004: فحص العلامات الحيوية
- **التوقيت:** كل 5 دقائق
- **المنفذ:** AMYGDALA تلقائياً
- **الإجراءات:**
  1. حساب معدل فشل الوكلاء
  2. قياس زمن استجابة MCP
  3. التحقق من انحرافات pipeline
  4. عد التنبيهات المفتوحة
  5. إذا تجاوز حد → إصدار تنبيه
- **المخرجات:** تحديث Alert Registry أو لا شيء

### R-005: التنظيف اليومي
- **التوقيت:** نهاية كل جلسة
- **المنفذ:** knw-memory-curator
- **الإجراءات:**
  1. نقل التنبيهات المغلقة > 7 أيام إلى LESSONS.md
  2. ضغط `brain/db/sessions.jsonl`
  3. التحقق من الروابط المقطوعة في BRAIN.md
  4. تحديث TEAM_STATUS.md
- **المخرجات:** تنظيف + تحديث

---

## | روتينات البوابات (Gate Routines)

### G0 — Inception (البداية)
| النوع | المحتوى |
|-------|---------|
| **دخول:** | فكرة من مستخدم |
| **مطلوب:** | Blueprint (نصف صفحة كحد أقصى) |
| **المالك:** | brd-ceo |
| **المدة المتوقعة:** | < 5 دقائق |
| **مخرج:** | Blueprint + RCCF إذا استمر |

### G1 — Discovery (الاكتشاف)
| النوع | المحتوى |
|-------|---------|
| **دخول:** | Blueprint من G0 |
| **مطلوب:** | Personas + Journey Map |
| **المالك:** | str-lead |
| **الأدوات:** | res-lead team |
| **مخرج:** | Personas, Journey Map, Research Report |

### G2 — Design (التصميم)
| النوع | المحتوى |
|-------|---------|
| **دخول:** | Personas + Journey Map |
| **مطلوب:** | Screen Specs + Wireframes |
| **المالك:** | dsn-lead |
| **مخرج:** | Screen Specs, Design System Updates |

### G3 — Architecture (الهندسة)
| النوع | المحتوى |
|-------|---------|
| **دخول:** | Screen Specs |
| **مطلوب:** | Schema + Threat Model |
| **المالك:** | arc-lead |
| **مخرج:** | ERD, API Contract, Threat Model |

### G4 — Build (البناء)
| النوع | المحتوى |
|-------|---------|
| **دخول:** | Schema + API Contract |
| **مطلوب:** | Code + Tests |
| **المالك:** | bck-lead / fnt-lead / mob-lead |
| **مخرج:** | Code, Unit Tests, Integration Tests |

### G5 — Quality (الجودة)
| النوع | المحتوى |
|-------|---------|
| **دخول:** | Code + Tests |
| **مطلوب:** | PASS من جميع الاختبارات |
| **المالك:** | qa-lead |
| **مخرج:** | Test Report, PASS/Fail |

### G6 — Staging (التجربة)
| النوع | المحتوى |
|-------|---------|
| **دخول:** | PASS من G5 |
| **مطلوب:** | UAT Sign-off |
| **المالك:** | ops-lead |
| **مخرج:** | UAT Report, Sign-off |

### G7 — Production (الإنتاج)
| النوع | المحتوى |
|-------|---------|
| **دخول:** | UAT Sign-off |
| **مطلوب:** | Deploy + Health Check |
| **المالك:** | ops-lead |
| **مخرج:** | Live URL, Health Check PASS |

### G8 — Observe (المراقبة)
| النوع | المحتوى |
|-------|---------|
| **دخول:** | Live |
| **مطلوب:** | SLOs (99.9% uptime, < 200ms latency) |
| **المالك:** | obs-lead |
| **مخرج:** | Dashboard, Alerts, SLO Report |

---

## | أتمتة الـ Pipeline (Pipeline Automation)

| النص/الأمر | متى يُشغّل | المالك | الوصف |
|-----------|-----------|--------|-------|
| `shamel doctor` | بداية كل جلسة | النظام | التحقق من صحة النظام |
| `shamel brain sync` | بعد كل gate | knw-memory-curator | مزامنة الذاكرة |
| `shamel gate check` | قبل كل gate | gtw-gatekeeper | التحقق من متطلبات الدخول |
| `shamel alert check` | كل 5 دقائق | AMYGDALA | فحص العلامات الحيوية |
| `shamel session save` | نهاية الجلسة | gtw-dispatcher | حفظ حالة الجلسة |
| `shamel log rotate` | يومياً (آخر جلسة) | النظام | ضغط وتنظيف السجلات |

**البرامج النصية في:** `engine/scripts/`

---

## | تراكم العادات (Habit Stacking)

الروتينات التي تعمل معاً كسلسلة:

```
[S-01] Boot Stack:
  shamel doctor → قراءة الذاكرة → مسح HIPPOCAMPUS → توليد WORKING

[S-02] Decision Stack:
  اكتشاف حاجة → تشاور → اتخاذ قرار → ADR → تسجيل في CORTEX

[S-03] Gate Stack:
  Gate In → shamel gate check → تنفيذ → Gate Out → shamel brain sync

[S-04] Incident Stack:
  AMYGDALA ينبه → CEO يقرر → sec-lead يعالج → Postmortem → LESSON

[S-05] Cleanup Stack:
  نهاية جلسة → R-005 تنظيف → تحديث WORKING → حفظ sessions.jsonl

[S-06] Planning Stack:
  مراجعة الأهداف → Risk Register → Trade-offs → خطط → RCCFs
```

**مبدأ الربط:** كل روتين له "خطاف" — شرط يبدأه. الخطاف يكون إما زمنياً (كل 5 دقائق) أو حدثياً (بعد Gate).

---

## | سجل الروتينات (Routine Registry)

| المعرف | الاسم | المشغّل | التكرار | المالك | آخر تشغيل |
|--------|------|---------|---------|--------|-----------|
| R-001 | التقاط سياق الجلسة | بدء الجلسة | كل جلسة | gtw-dispatcher | — |
| R-002 | تسجيل القرارات | قرار 🟡+ | عند الحاجة | الوكيل المقرر | — |
| R-003 | تقطير الدروس | نهاية جلسة/حادثة | يومياً | knw-reflector | — |
| R-004 | فحص العلامات الحيوية | مؤقت | كل 5 دقائق | AMYGDALA | — |
| R-005 | التنظيف اليومي | نهاية جلسة | يومياً | knw-memory-curator | — |
| R-010 | G0 Inception | طلب مستخدم | عند الحاجة | brd-ceo | — |
| R-011 | G1 Discovery | خروج من G0 | عند الحاجة | str-lead | — |
| R-012 | G2 Design | خروج من G1 | عند الحاجة | dsn-lead | — |
| R-013 | G3 Architecture | خروج من G2 | عند الحاجة | arc-lead | — |
| R-014 | G4 Build | خروج من G3 | عند الحاجة | bck-lead | — |
| R-015 | G5 Quality | خروج من G4 | عند الحاجة | qa-lead | — |
| R-016 | G6 Staging | خروج من G5 | عند الحاجة | ops-lead | — |
| R-017 | G7 Production | خروج من G6 | عند الحاجة | ops-lead | — |
| R-018 | G8 Observe | خروج من G7 | عند الحاجة | obs-lead | — |
| R-020 | shamel doctor | boot | كل جلسة | النظام | — |
| R-021 | shamel brain sync | بعد gate | عند الحاجة | knw-memory-curator | — |
| R-022 | shamel gate check | قبل gate | عند الحاجة | gtw-gatekeeper | — |

---

## | قواعد الروتين (Routine Rules)

1. **الروتين لا يُسأل** — ينفذ بدون تشاور. إذا احتجت قراراً، فأنت لست في BASAL-GANGLIA
2. **الفشل يصعّد** — إذا فشل روتين، AMYGDALA يسجل تنبيهاً تلقائياً
3. **لا توجد خطوة 11** — كل روتين له نهاية محددة. إذا استمر > دقيقتين → تحذير
4. **سجل كل شيء** — كل تشغيل روتين يُسجل في HIPPOCAMPUS
5. **الروتين يتطور** — إذا تكرر نمط يدوي 3 مرات → يصبح روتيناً رسمياً
6. **التغلب على الروتين** — CEO فقط يمكنه إيقاف روتين جارٍ (بأمر `shamel override`)

---

*آخر تحديث: 2026-07-13*
