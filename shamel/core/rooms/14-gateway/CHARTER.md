# البوابة — Gateway Room
**الغرفة:** 14-gateway
**الرمز:** gtw
**قائد الغرفة:** `gtw-dispatcher`

---

## | الهوية (Identity)

**الغرض:**
استقبال الطلبات، التوجيه، الميزانية، حل النزاعات
Request intake, routing, budget, conflict resolution

**عدد الوكلاء:** 7

---

## | قائمة الوكلاء (Agent Roster)

- `gtw-dispatcher` — dispatcher
- `gtw-router` — router
- `gtw-gatekeeper` — gatekeeper
- `gtw-budget-warden` — budget-warden
- `gtw-conflict-resolver` — conflict-resolver
- `gtw-external-reviewer` — external-reviewer
- `gtw-intake-reformer` — intake-reformer

---

## | إجراءات التشغيل القياسية (SOP)

1. gtw-intake-reformer يستقبل الطلب
2. gtw-dispatcher يوجه للغرفة المناسبة
3. gtw-gatekeeper يتحقق من الصلاحيات
4. gtw-budget-warden يدير الميزانية
5. gtw-conflict-resolver يحل النزاعات

---

## | الأدوات المسموحة (Permitted Tools)

WebSearch, WebFetch (للاستقبال), Task (للتوزيع)

---

## | الغرف المتصلة (Connected Rooms)

جميع الغرف + خارجي

---

## | بوابات المسؤولية (Gate Ownership)

G0 (استقبال)

---

## | بروتوكول التسليم (Handoff Protocol)

1. الوكيل ينهي مهمته ويسجل الأدلة
2. الوكيل يسلم لقائد الغرفة
3. قائد الغرفة يراجع ويوحد
4. قائد الغرفة يسلم لـ brd-ceo
5. brd-ceo يسلم للمستخدم

**ممنوع:**
- الوكيل يسلم للمستخدم مباشرة
- الوكيل يخاطب غرفة أخرى
- قائد الغرفة ينفذ بنفسه

---

## | قانون الغرفة (Room Law)

البوابة تعمل ضمن حدود الدستور (core/CONSTITUTION.md).
جميع القرارات تتوافق مع قانون العزل (Room Isolation Law).
التواصل مع الغرف الأخرى يتم عبر قائد الغرفة فقط.
