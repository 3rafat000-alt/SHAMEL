# BRAIN — Memory Architecture (Master Index)

SHAMEL brain = 6 regions + working state:

```
                      ┌─────────────────────┐
                      │     HIPPOCAMPUS     │  ← الذاكرة العاملة (هذه الجلسة)
                      │  brain/HIPPOCAMPUS  │     يكتبها الوكلاء أثناء العمل
                      └────────┬────────────┘
                               ↓ (المهم يُنقل)
                      ┌─────────────────────┐
                      │       CORTEX        │  ← الذاكرة الدائمة (كل الجلسات)
                      │   brain/CORTEX      │     القرارات، الهيكل، الدروس
                      └────────┬────────────┘
                               ↓ (يُقرأ للتوجيه)
                      ┌─────────────────────┐
                      │      THALAMUS       │  ← التوجيه والتنسيق
                      │   brain/THALAMUS    │     المسارات، البوابات، التصعيد
                      └────────┬────────────┘
                               ↓ (يُصعّد إليه)
                      ┌─────────────────────┐
                      │      AMYGDALA       │  ← التنبيهات والطوارئ
                      │   brain/AMYGDALA    │     الكشف، التصعيد، الحوادث
                      └────────┬────────────┘
                               ↓ (يخطط له)
                      ┌─────────────────────┐
                      │     PREFRONTAL      │  ← التخطيط واتخاذ القرارات
                      │  brain/PREFRONTAL   │     الأهداف، المخاطر، المفاضلات
                      └────────┬────────────┘
                               ↓ (ينفذ تلقائياً)
                      ┌─────────────────────┐
                      │    BASAL-GANGLIA    │  ← الروتين والعادات
                      │ brain/BASAL-GANGLIA │     السير الذاتية، الأتمتة
                      └─────────────────────┘

                      ┌─────────────────────┐
                      │      WORKING        │  ← حالة الجلسة الحالية
                      │   brain/WORKING     │     snapshot مؤقت
                      └─────────────────────┘
```

---

## | فهرس الدماغ الكامل (Complete Brain Index)

### Region 1 — HIPPOCAMPUS (Working Memory)
| الملف | الوصف | يكتبه |
|-------|-------|-------|
| `brain/HIPPOCAMPUS.md` | ذاكرة الجلسة الحالية — السياق، القرارات الحديثة، التذاكر النشطة | الوكلاء أثناء العمل |

### Region 2 — CORTEX (Long-Term Knowledge)
| الملف | الوصف | يكتبه |
|-------|-------|-------|
| `brain/CORTEX.md` | الذاكرة الدائمة — هيكل الفريق، القرارات، الدروس، قوانين النظام | knw-lead + CEO بعد القرارات المهمة |
| `brain/org/DECISIONS.md` | سجل القرارات المعمارية (ADRs) | CEO + knw-historian |
| `brain/org/LESSONS.md` | الدروس المستفادة (توقيع LES-NNN) | knw-memory-curator + agents |
| `brain/org/EVOLUTION.md` | تطور النظام عبر الأجيال | knw-historian |
| `brain/org/PERSONAS.md` | خريطة الشخصيات (وكيل ← شخصية) | knw-lead |
| `brain/org/HANDOFFS.md` | فهرس التسليم بين الغرف | النظام تلقائياً |
| `brain/org/TEAM_STATUS.md` | حالة الفريق (مُولد) | النظام تلقائياً |
| `brain/INSTINCTS.md` | طبقة تسجيل الثقة والترقية فوق CORTEX — غرائز project→global scoped | knw-lead + knw-memory-curator |

### Region 3 — THALAMUS (Routing)
| الملف | الوصف | يكتبه |
|-------|-------|-------|
| `brain/THALAMUS.md` | التوجيه — pipeline, gates, escalation, MCP, events | knw-lead + CEO |
| `core/nexus/routing.yaml` | مسارات التوجيه الفعلية (model, effort, caveman) | النظام |
| `core/nexus/gates.yaml` | تعريفات البوابات التسع | النظام |
| `core/nexus/registry.yaml` | سجل الغرف والوكلاء | النظام |

### Region 4 — AMYGDALA (Alerts & Emergency)
| الملف | الوصف | يكتبه |
|-------|-------|-------|
| `brain/AMYGDALA.md` | التنبيهات والطوارئ — المستويات، القواعد، التصعيد، postmortem | sec-lead + gtw-gatekeeper |

### Region 5 — PREFRONTAL (Planning & Decisions)
| الملف | الوصف | يكتبه |
|-------|-------|-------|
| `brain/PREFRONTAL.md` | التخطيط والقرارات — الأهداف، المخاطر، المفاضلات، إطار القرارات | brd-ceo + knw-lead |

### Region 6 — BASAL-GANGLIA (Routines & Habits)
| الملف | الوصف | يكتبه |
|-------|-------|-------|
| `brain/BASAL-GANGLIA.md` | الروتين والعادات — boot routine, gate routines, pipeline automation, habit stacking | gtw-dispatcher + knw-lead |

### Session State
| الملف | الوصف | يكتبه |
|-------|-------|-------|
| `brain/WORKING.md` | حالة الجلسة الحالية — snapshot مؤقت | النظام عند بدء الجلسة |
| `brain/db/brain.db` | SQLite FTS5 — ذاكرة الجلسة للبحث | hooks تلقائياً |
| `brain/db/sessions.jsonl` | سجل الجلسات | hooks تلقائياً |

---

## | قواعد الذاكرة (Memory Rules)

1. **HIPPOCAMPUS = مؤقت:** يمسح في بداية كل جلسة. المحتوى المهم يُنقل إلى CORTEX
2. **CORTEX = دائم:** كل قرار معماري أو درس يضاف هنا — لا يحذف أبداً. الغرائز عالية الثقة تُصنَّف عبر `brain/INSTINCTS.md`
3. **THALAMUS = ثابت:** يتغير فقط عندما يتغير هيكل التوجيه نفسه
4. **AMYGDALA = يقظ:** يراقب باستمرار، يُصعّد عند الخطر، يُنظف التنبيهات المغلقة بعد 7 أيام
5. **PREFRONTAL = استراتيجي:** يُراجع أسبوعياً، يُحدث مع كل قرار مهم أو درس جديد
6. **BASAL-GANGLIA = تلقائي:** ينفذ الروتين بدون تفكير، يتطور عندما يتكرر نمط ما
7. **WORKING = snapshot:** يُولد عند البداية، يُحدث بعد كل خطوة رئيسية
8. **MEMORY.md = مؤشرات فقط:** لا تخزن محتوى هنا، فقط روابط سريعة
9. **MCP port 8765:** brain_mcp.py يسمح للوكلاء بقراءة/كتابة الذاكرة عبر API

---

## | القوالب (Templates)

`brain/templates/`:
- `STATE.md` — branch, head_sha, gate, facts
- `CONTEXT.md` — session context
- `DECISIONS.md` — ADR template
- `HANDOFFS.md` — ticket queue
- `LESSONS.md` — procedural memory (sig format)
- `FOUNDATIONS.md` — design foundations
- `FOLDER-MAP.md` — directory map
- `LOCKS.md` — gate-lock tracking

---

## | المالكون (Owners)

راجع `brain/OWNERS.yaml` — لكل ملف مالك واحد محدد.
