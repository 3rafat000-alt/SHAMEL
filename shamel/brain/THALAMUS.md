# THALAMUS — التوجيه والتنسيق (Routing & Coordination)
**كيف تتدفق الإشارات عبر النظام — من يدخل، من يخرج، ماذا يحدث بينهما**

```
THALAMUS = التوجيه — يقرر أين تذهب الإشارة بعد كل خطوة
```

---

## | التدفق الإجباري (Mandatory Pipeline)

```
User input
    ↓ [دائماً — لا يمكن تخطي]
gtw-intake-reformer → Intake Report
    ↓ [دائماً]
brd-ceo → استشارة المجلس (Task: brd-*, str-*, res-*)
    ↓ [دائماً]
brd-ceo → Task: room lead(s)
    ↓ [كل قائد غرفة]
room lead → Task: room agent(s)
    ↓ [الوكلاء ينفذون]
room agent → يسلم لقائد الغرفة
    ↓ [قائد الغرفة]
room lead → يسلم لـ brd-ceo
    ↓ [CEO]
brd-ceo → user
```

---

## | بوابات الحياة (Lifecycle Gates)

| البوابة | الاسم | المالك | المدخل | المخرج |
|---------|-------|--------|--------|--------|
| G0 | Inception | brd-ceo | فكرة | Blueprint |
| G1 | Discovery | str-lead | Blueprint | Personas + Journey |
| G2 | Design | dsn-lead | Personas | Screen Specs |
| G3 | Architecture | arc-lead | Screen Specs | Schema + Threat Model |
| G4 | Build | bck-lead/fnt-lead | Schema | Code |
| G5 | Quality | qa-lead | Code | PASS |
| G6 | Staging | ops-lead | PASS | UAT Sign-off |
| G7 | Production | ops-lead | Sign-off | Live |
| G8 | Observe | obs-lead | Live | SLOs |

**المسار السريع:** G0 → G2 → G4 → G7 (للتغييرات الصغيرة)
**التدقيق العميق:** G0 → G1 → G2 → G3 → G4 → G5 → G6 → G7 → G8 (للمشاريع الكبيرة)

---

## | مسارات التصعيد (Escalation Paths)

```
وكيل → قائد غرفة → gtw-conflict-resolver → brd-arbiter → brd-ceo
                                    ↓
                            brd-chief-of-staff (تنظيمي)
```

**متى نصعد:**
- خلاف بين غرفتين → gtw-conflict-resolver
- قرار مصيري → brd-arbiter
- مخالفة دستورية → brd-ceo مباشرة
- مشكلة تقنية معقدة → brd-cto

---

## | قواعد التوجيه (Routing Rules)

### من intake:

| الشرط | الوجهة |
|-------|--------|
| طلب جديد | brd-ceo |
| تقرير عن مشروع قائم | brd-ceo |
| سؤال عن النظام | brd-ceo → knw-brain-query |
| مخالفة أمنية | brd-ceo → sec-lead (طارئ) |

### من CEO:

| الشرط | الوجهة |
|-------|--------|
| استراتيجية/تحليل | str-lead |
| بحث/تجربة مستخدم | res-lead |
| تصميم/واجهات | dsn-lead |
| هندسة معمارية | arc-lead |
| تطوير باك إند | bck-lead |
| تطوير فرونت إند | fnt-lead |
| تطوير موبايل | mob-lead |
| بيانات/تحليلات | dat-lead |
| أمن | sec-lead |
| جودة/اختبارات | qa-lead |
| عمليات/نشر | ops-lead |
| مراقبة | obs-lead |
| معرفة/توثيق | knw-lead |
| متعدد الغرف | gtw-dispatcher |
| غير واضح | gtw-conflict-resolver |

---

## | بنية MCP (MCP Architecture)

**خادم الذاكرة:** `engine/mcp_servers/brain_mcp.py` (port 8765)

| الأداة | الوصف |
|--------|-------|
| brain_read | قراءة أي ملف في الدماغ |
| brain_search | بحث FTS5 عبر ملفات الدماغ |
| brain_write | كتابة/إلحاق في ملفات الدماغ |
| brain_record_decision | تسجيل قرار معماري |
| brain_remember | تخزين حقيقة في الذاكرة العاملة |
| brain_recall | استرجاع حقيقة من الذاكرة العاملة |
| agent_lookup | البحث عن معلومات وكيل |
| room_lookup | البحث عن معلومات غرفة |
| route_lookup | البحث عن مسار توجيه |

**المكتبة:** `engine/shamel_tools/brain_client.py` — `BrainClient` للوكلاء

---

## | قناة الأحداث (Event Bus)

الوكلاء يرسلون أحداثاً عبر `telemetry.py`:

| الحدث | المعنى | المستقبل |
|-------|--------|---------|
| agent.started | بدأ الوكيل العمل | runlog, brain |
| agent.completed | أكمل الوكيل المهمة | runlog, brain |
| agent.error | حدث خطأ | runlog, قائد الغرفة |
| handoff.sent | تم التسليم | runlog |
| handoff.received | تم الاستلام | runlog |
| gate.passed | اجتياز بوابة | brain, CEO |
| gate.failed | فشل في بوابة | brain, CEO, escalation |

---

## | قيود النظام (System Constraints)

1. **لا وكيل يتحدث لمستخدم مباشرة** — عبر CEO فقط
2. **لا وكيل يتخطى قائد غرفته** — التسليم للقائد دائماً
3. **CEO لا ينفذ كوداً** — يوزع فقط
4. **قائد الغرفة لا ينفذ بنفسه** — يفوض لفريقه
5. **المجلس استشاري** — CEO صاحب القرار النهائي
6. **الأدلة إجبارية** — كل تسليم يحتاج أدلة
7. **RCCF إجباري** — لا عمل بدون أمر عمل رسمي

---

*آخر تحديث: 2026-07-13*
