# CORTEX — الذاكرة الدائمة (Long-Term Knowledge)
**المعرفة التي تبقى عبر الجلسات — يقرؤها كل وكيل عند بدء العمل**

```
CORTEX = ما تعلمناه وما قررناه وما بنيناه
     ↓
يدوم للأبد، يُحدث بعد كل قرار مهم أو تغيير في الهيكل
```

---

## | هيكل الفريق (Team Structure)

### غرف SHAMEL الـ 15

| الرمز | الغرفة | القائد | عدد الوكلاء | الاختصاص |
|-------|--------|--------|-------------|----------|
| 00 | boardroom | brd-ceo | 7 | القيادة العليا والحوكمة |
| 01 | strategy | str-lead | 7 | الاستراتيجية وتحليل السوق |
| 02 | research | res-lead | 7 | البحث وتجربة المستخدم |
| 03 | design | dsn-lead | 8 | التصميم والهوية البصرية |
| 04 | architecture | arc-lead | 7 | الهندسة المعمارية |
| 05 | backend | bck-lead | 8 | تطوير الباك إند |
| 06 | frontend | fnt-lead | 8 | تطوير الفرونت إند |
| 07 | mobile | mob-lead | 6 | تطوير الموبايل |
| 08 | data | dat-lead | 7 | البيانات والتحليلات |
| 09 | security | sec-lead | 8 | الأمن والامتثال |
| 10 | quality | qa-lead | 7 | الجودة والاختبارات |
| 11 | devops | ops-lead | 7 | العمليات والنشر |
| 12 | observability | obs-lead | 6 | المراقبة والموثوقية |
| 13 | knowledge | knw-lead | 6 | المعرفة والتوثيق |
| 14 | gateway | gtw-dispatcher | 6 | البوابة والتوجيه |

**الإجمالي:** 106 وكيل، 15 غرفة، 15 قائد غرفة

---

## | القرارات المعمارية (Architectural Decisions)

*آخر 10 قرارات مهمة — للقائمة الكاملة راجع `brain/org/DECISIONS.md`*

| # | العنوان | التاريخ | الحالة |
|---|---------|---------|--------|
| ADR-001 | فصل SHAMEL عن SOFI v6 | 2026-07-10 | نافذ |
| ADR-002 | اعتماد هيكل الغرف الـ 15 | 2026-07-10 | نافذ |
| ADR-003 | بروتوكول العزل (Room Isolation Law) | 2026-07-10 | نافذ |
| ADR-004 | نظام RCCF لأوامر العمل | 2026-07-10 | نافذ |
| ADR-005 | الذاكرة ثلاثية الأقسام (HPC/CORTEX/THL) | 2026-07-13 | نافذ |
| ADR-006 | وكلاء بشخصيات بشرية (Phase 5) | 2026-07-13 | نافذ |
| ADR-007 | MCP server للذاكرة | 2026-07-13 | نافذ |

---

## | الدروس المستفادة (Lessons Learned)

*للقائمة الكاملة راجع `brain/org/LESSONS.md`*

1. **التدفق الإجباري:** لا يمكن تخطي intake أو CEO — النظام يرفض
2. **العزل بين الغرف:** وكيل لا يخاطب غرفة أخرى مباشرة — عبر القائد فقط
3. **الأدلة قبل التسليم:** كل وكيل يقدم أدلة (ملف:سطر، exit code)
4. **النماذج البشرية:** الوكلاء بشخصيات — يحسن التعاون والتفاهم
5. **MCP للذاكرة:** brain_mcp.py يسمح للوكلاء بقراءة/كتابة الذاكرة مباشرة

---

## | الوكلاء حسب القدرات (Agent Capability Index)

### وكلاء مع Task tool (16):
brd-ceo, brd-chief-of-staff, str-lead, res-lead, dsn-lead, arc-lead, bck-lead, fnt-lead, mob-lead, dat-lead, sec-lead, qa-lead, ops-lead, obs-lead, knw-lead, gtw-dispatcher

### وكلاء مع WebSearch (23):
gtw-intake-reformer, gtw-external-reviewer, res-ux-researcher, res-competitor-analyst, res-data-researcher, res-fact-checker, res-web-scout, str-product-strategist, str-business-analyst, str-market-analyst, str-risk-analyst, dsn-content-strategist, dsn-ux-architect, dat-analytics-engineer, sec-threat-modeler, sec-pentester, obs-insights-analyst, knw-brain-query, knw-reflector, brd-cpo, brd-cso, brd-cto, brd-cqo

### وكلاء بصلاحيات الأمن (8):
sec-lead, sec-pentester, sec-appsec-engineer, sec-authn-engineer, sec-compliance-auditor, sec-incident-responder, sec-threat-modeler, sec-secrets-warden

---

## | قوانين النظام الثابتة (Immutable Rules)

1. **قانون العزل:** وكيل لا يخاطب غرفة أخرى مباشرة
2. **قانون التسليم:** أنجز ← سجل أدلة ← سلم لقائدك ← CEO ← مستخدم
3. **قانون الأداة:** كل وكيل له أدواته المحددة — لا يستخدم أداة غير مصرح بها
4. **قانون RCCF:** لا تنفيذ بدون أمر عمل رسمي
5. **قانون المجلس:** CEO يستشير المجلس (brd-*) عبر Task قبل القرارات المصيرية

---

## | تفاصيل المشروع (Project Details)

**المشروع الحالي:** PRJ-SAKK
**نوع المشروع:** Laravel + Blade + Caddy
**المستودع:** github.com/3rafat000-alt/SHAMEL
**الفرع الرئيسي:** main

*تم آخر تحديث في 2026-07-13*

*سجل الجلسات يُحتفظ به في HIPPOCAMPUS.md و brain/db/sessions.jsonl*

