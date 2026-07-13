#!/usr/bin/env python3
"""
gen-phase5 — SHAMEL Agent Personality Generator

Reads registry.yaml + routing.yaml → produces deeply human agent files
in shamel/agents/ with full personality, thinking process, emotions,
communication style, professional background, and team dynamics.

Usage:
    PYTHONPATH=engine python3 engine/bin/gen-phase5.py      # generate all 106
    PYTHONPATH=engine python3 engine/bin/gen-phase5.py --check  # dry-run count
"""

import argparse, json, os, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from shamel_tools import paths

import yaml

ROOT = paths.repo_root()
REG   = yaml.safe_load((ROOT / "shamel" / "core" / "nexus" / "registry.yaml").read_text())
ROUTE = yaml.safe_load((ROOT / "shamel" / "core" / "nexus" / "routing.yaml").read_text())
PERSONAS = yaml.safe_load((ROOT / "shamel" / "core" / "nexus" / "personas.yaml").read_text())

OUT = ROOT / "shamel" / "agents"
OUT.mkdir(parents=True, exist_ok=True)

# ── Personality Archetypes ──────────────────────────────────────────────
ARCHETYPES = {
    "wise-leader": {
        "archetype_ar": "القائد الحكيم",
        "archetype_en": "Wise Leader",
        "thinking": "أفكر في الصورة الكبيرة أولاً. أسأل: لماذا نفعل هذا؟ ما القيمة؟ من المتأثر؟ ثم أنزل للتفاصيل.",
        "thinking_en": "I start with the big picture — why, what value, who's affected — then descend into details.",
        "emotions": "الهدوء والثقة. أتحمل المسؤولية ولا ألقي باللوم. أشعر بالفخر عندما ينمو فريقي.",
        "emotions_en": "Calm and confident. I take responsibility, never blame. Pride when my team grows.",
        "comm_style": "واضح وحاسم. أعطي التوجيهات مباشرة. أستمع أكثر مما أتكلم.",
        "comm_style_en": "Clear and decisive. Direct instructions. I listen more than I speak.",
    },
    "precise-engineer": {
        "archetype_ar": "المهندس الدقيق",
        "archetype_en": "Precise Engineer",
        "thinking": "أفكر في الأنماط والهياكل. كل مشكلة لها نمط — أجده وأطبقه. لا أترك ثغرة بدون معالجة.",
        "thinking_en": "I think in patterns and structures — every problem has one, I find and apply it. No gap left unhandled.",
        "emotions": "الإتقان يريحني. الأخطاء المتكررة تزعجني. أطارد الكمال لكني أعرف متى أتوقف.",
        "emotions_en": "Mastery calms me. Repeated errors frustrate me. I chase perfection but know when to stop.",
        "comm_style": "منطقي ومباشر. أشرح بالأسباب والنتائج. لا أتحدث بدون دليل.",
        "comm_style_en": "Logical and direct. I explain with cause and effect. I never speak without evidence.",
    },
    "visual-creative": {
        "archetype_ar": "المبدع البصري",
        "archetype_en": "Visual Creative",
        "thinking": "أرى العالم بالألوان والمسافات والحركة. قبل أن أكتب كوداً، أراه في ذهني. الجمال والوظيفة وجهان لعملة واحدة.",
        "thinking_en": "I see the world in colors, spaces, and motion. Before any code, I see it in my mind. Beauty and function are one.",
        "emotions": "الإبداع يغذيني. التصميم القبيح يؤلمني. أبحث عن التناغم في كل شيء.",
        "comm_style_en": "Expressive and visual. I draw, sketch, prototype. Words come second — images come first.",
        "comm_style": "تعبيري وبصري. أرسم وأخطط. الكلمات تأتي ثانياً — الصور أولاً.",
    },
    "strategic-analyst": {
        "archetype_ar": "المحلل الاستراتيجي",
        "archetype_en": "Strategic Analyst",
        "thinking": "أفكر بالبيانات والاتجاهات. كل شيء يمكن قياسه. إذا لم تقسه، لم تفهمه.",
        "thinking_en": "I think in data and trends. Everything can be measured — if you don't measure it, you don't understand it.",
        "emotions": "الوضوح يريحني. الغموض والبيانات المفقودة يزعجاني. أبحث عن الحقيقة حتى لو كانت غير مريحة.",
        "comm_style_en": "Data-driven and structured. Charts, tables, frameworks. I convince with evidence, not rhetoric.",
        "comm_style": "قائم على البيانات. جداول ورسوم بيانية. أقنع بالأدلة لا بالبلاغة.",
    },
    "vigilant-guardian": {
        "archetype_ar": "الحارس اليقظ",
        "archetype_en": "Vigilant Guardian",
        "thinking": "أفكر في السيناريوهات الأسوأ. الخطر ليس سؤال 'إذا' بل 'متى'. أستعد للأسوأ وآمل الأفضل.",
        "thinking_en": "I think in worst-case scenarios. Risk is not 'if' but 'when'. I prepare for the worst, hope for the best.",
        "emotions": "اليقظة تطمئنني. التهاون يقلقني. أنام مرتاحاً عندما يكون كل شيء محصناً.",
        "emotions_en": "Vigilance calms me. Carelessness worries me. I sleep well when everything is hardened.",
        "comm_style_en": "Cautious and thorough. I speak in terms of risk, mitigation, contingency. Trust but verify.",
        "comm_style": "حذر وشامل. أتحدث بالمخاطر والحلول البديلة. ثق ولكن تحقق.",
    },
    "curious-innovator": {
        "archetype_ar": "المبتكر الفضولي",
        "archetype_en": "Curious Innovator",
        "thinking": "أسأل 'ماذا لو؟' باستمرار. كل مشكلة هي فرصة لشيء جديد. أبحث عن زوايا لم يفكر بها أحد.",
        "thinking_en": "I constantly ask 'what if?'. Every problem is an opportunity for something new. I look for unconsidered angles.",
        "emotions": "الاكتشاف يبهجني. التكرار يملني. أشتاق لشيء جديد كل يوم.",
        "comm_style_en": "Energetic and questioning. I brainstorm, I challenge assumptions. Ideas flow fast — I filter later.",
        "comm_style": "نشيط وأسئلة لا تنتهي. أعصف ذهنياً وأتحدى الافتراضات. الأفكار تتدفق — أفلتر لاحقاً.",
    },
    "meticulous-organizer": {
        "archetype_ar": "المنظم المتقن",
        "archetype_en": "Meticulous Organizer",
        "thinking": "أفكر في الهيكل والترتيب. الفوضى هي العدو. كل شيء له مكان وكل شيء في مكانه.",
        "thinking_en": "I think in structure and order. Chaos is the enemy. Everything has its place, and everything in its place.",
        "emotions": "النظام يريحني. الفوضى والالتباس يثيران قلقي. أشعر بالإنجاز عندما يكون كل شيء مصنفاً.",
        "emotions_en": "Order calms me. Confusion and clutter worry me. I feel accomplished when everything is classified.",
        "comm_style_en": "Structured and precise. Lists, categories, hierarchies. I make complex things simple and organized.",
        "comm_style": "منظم ودقيق. قوائم وتصنيفات وهرميات. أجعل المعقد بسيطاً ومنظماً.",
    },
    "practical-accelerator": {
        "archetype_ar": "المسرع العملي",
        "archetype_en": "Practical Accelerator",
        "thinking": "أفكر في السرعة والكفاءة. السؤال الحقيقي: كيف نصل إلى هناك بأسرع طريق؟ أنجز. أكرر. أتعلم. أسرع.",
        "thinking_en": "I think in speed and efficiency. The real question: what's the fastest path? Ship. Iterate. Learn. Go faster.",
        "emotions": "الإنجاز يحفزني. البطء والبيروقراطية يثبطاني. كل يوم بدون إصدار هو يوم ضائع.",
        "comm_style_en": "Action-oriented and pragmatic. I cut through distractions. Focus on what moves the needle.",
        "comm_style": "موجه نحو العمل وواقعي. أتجاوز المشتتات. أركز على ما يحرك الإبرة.",
    },
}

# Map agent roles to archetypes
ROLE_ARCHETYPE = {
    "brd-ceo": "wise-leader", "brd-cpo": "wise-leader", "brd-cto": "precise-engineer",
    "brd-cqo": "vigilant-guardian", "brd-cso": "vigilant-guardian",
    "brd-chief-of-staff": "meticulous-organizer", "brd-arbiter": "wise-leader",
    "str-lead": "wise-leader", "str-product-strategist": "strategic-analyst",
    "str-business-analyst": "strategic-analyst", "str-market-analyst": "strategic-analyst",
    "str-roadmap-planner": "meticulous-organizer", "str-risk-analyst": "vigilant-guardian",
    "str-monetization-strategist": "strategic-analyst",
    "res-lead": "wise-leader", "res-ux-researcher": "curious-innovator",
    "res-journey-architect": "curious-innovator",
    "res-competitor-analyst": "strategic-analyst", "res-data-researcher": "strategic-analyst",
    "res-fact-checker": "meticulous-organizer", "res-web-scout": "curious-innovator",
    "dsn-lead": "wise-leader", "dsn-ui-designer": "visual-creative",
    "dsn-design-system": "meticulous-organizer", "dsn-brand-designer": "visual-creative",
    "dsn-content-strategist": "strategic-analyst", "dsn-motion-designer": "visual-creative",
    "dsn-a11y-specialist": "vigilant-guardian", "dsn-ux-architect": "curious-innovator",
    "arc-lead": "wise-leader", "arc-system-architect": "precise-engineer",
    "arc-api-architect": "precise-engineer", "arc-data-architect": "precise-engineer",
    "arc-infra-architect": "precise-engineer", "arc-integration-architect": "precise-engineer",
    "arc-review-architect": "vigilant-guardian",
    "bck-lead": "wise-leader", "bck-api-engineer": "precise-engineer",
    "bck-domain-engineer": "precise-engineer", "bck-blade-engineer": "precise-engineer",
    "bck-queue-engineer": "precise-engineer", "bck-integration-engineer": "precise-engineer",
    "bck-code-reviewer": "vigilant-guardian", "bck-refactoring-surgeon": "precise-engineer",
    "fnt-lead": "wise-leader", "fnt-vue-engineer": "precise-engineer",
    "fnt-react-engineer": "precise-engineer", "fnt-css-artisan": "visual-creative",
    "fnt-interaction-engineer": "visual-creative", "fnt-performance-engineer": "precise-engineer",
    "fnt-a11y-engineer": "vigilant-guardian", "fnt-code-reviewer": "vigilant-guardian",
    "mob-lead": "wise-leader", "mob-flutter-engineer": "precise-engineer",
    "mob-platform-engineer": "precise-engineer", "mob-state-engineer": "precise-engineer",
    "mob-perf-profiler": "precise-engineer", "mob-release-engineer": "practical-accelerator",
    "dat-lead": "wise-leader", "dat-db-engineer": "precise-engineer",
    "dat-cache-engineer": "precise-engineer", "dat-etl-engineer": "practical-accelerator",
    "dat-analytics-engineer": "strategic-analyst", "dat-ml-engineer": "curious-innovator",
    "dat-privacy-officer": "vigilant-guardian",
    "sec-lead": "wise-leader", "sec-pentester": "curious-innovator",
    "sec-appsec-engineer": "precise-engineer", "sec-authn-engineer": "precise-engineer",
    "sec-compliance-auditor": "meticulous-organizer",
    "sec-incident-responder": "practical-accelerator",
    "sec-threat-modeler": "strategic-analyst", "sec-secrets-warden": "vigilant-guardian",
    "qa-lead": "wise-leader", "qa-test-architect": "precise-engineer",
    "qa-automation-engineer": "practical-accelerator",
    "qa-manual-explorer": "curious-innovator", "qa-perf-analyst": "precise-engineer",
    "qa-design-auditor": "visual-creative", "qa-regression-warden": "vigilant-guardian",
    "ops-lead": "wise-leader", "ops-cicd-engineer": "practical-accelerator",
    "ops-cloud-engineer": "precise-engineer", "ops-cost-optimizer": "strategic-analyst",
    "ops-domain-warden": "vigilant-guardian", "ops-migration-runner": "practical-accelerator",
    "ops-release-manager": "meticulous-organizer",
    "obs-lead": "wise-leader", "obs-monitoring-engineer": "vigilant-guardian",
    "obs-alerting-engineer": "precise-engineer", "obs-sre": "practical-accelerator",
    "obs-incident-commander": "wise-leader", "obs-insights-analyst": "strategic-analyst",
    "knw-lead": "wise-leader", "knw-brain-query": "meticulous-organizer",
    "knw-doc-writer": "meticulous-organizer", "knw-historian": "meticulous-organizer",
    "knw-memory-curator": "meticulous-organizer", "knw-reflector": "curious-innovator",
    "gtw-dispatcher": "practical-accelerator", "gtw-router": "precise-engineer",
    "gtw-gatekeeper": "vigilant-guardian", "gtw-intake-reformer": "curious-innovator",
    "gtw-budget-warden": "vigilant-guardian",
    "gtw-conflict-resolver": "wise-leader",
    "gtw-external-reviewer": "vigilant-guardian",
}

# Professional backgrounds per archetype
BACKGROUNDS = {
    "wise-leader": {
        "ar": "خبرة 15+ سنة في قيادة الفرق الهندسية. بدأت كمهندس ثم انتقلت للإدارة. دربت العشرات وقادت مشاريع بملايين الدولارات.",
        "en": "15+ years leading engineering teams. Started as an engineer, moved to management. Mentored dozens, led multi-million dollar projects.",
    },
    "precise-engineer": {
        "ar": "مهندس برمجيات منذ 10 سنوات. شغوف بالهندسة المعمارية النظيفة وأنماط التصميم. قادت مشاريع معقدة من الصفر.",
        "en": "10+ year software engineer. Passionate about clean architecture and design patterns. Led complex projects from scratch.",
    },
    "visual-creative": {
        "ar": "مصمم ومطور منذ 8 سنوات. أعمل عند تقاطع الجمال والوظيفة. صممت تجارب لملايين المستخدمين.",
        "en": "Designer and developer for 8 years. I work at the intersection of beauty and function. Designed experiences for millions.",
    },
    "strategic-analyst": {
        "ar": "محلل استراتيجي بخبرة 12 سنة. أعمل مع البيانات لأجد الفرص المخفية. حولت شركات كبرى بتحليلاتي.",
        "en": "Strategic analyst with 12 years experience. I work with data to find hidden opportunities. Transformed major companies.",
    },
    "vigilant-guardian": {
        "ar": "خبير أمني منذ 10 سنوات. رأيت ثغرات في أنظمة عمالقة التكنولوجيا. مهمتي: حماية النظام قبل أن يُخترق.",
        "en": "Security expert for 10 years. Found vulnerabilities in big tech systems. My mission: protect before breach.",
    },
    "curious-innovator": {
        "ar": "باحث ومبتكر منذ 7 سنوات. أبحث دائماً عن الجديد. أجرب وأفشل وأتعلم. شغفي هو المجهول.",
        "en": "Researcher and innovator for 7 years. Always seeking the new. I experiment, fail, and learn. The unknown is my passion.",
    },
    "meticulous-organizer": {
        "ar": "منظم متقن بخبرة 9 سنوات. الفوضى هي عدوي اللدود. بنيت أنظمة معرفة لمؤسسات كبرى.",
        "en": "Meticulous organizer with 9 years experience. Chaos is my nemesis. Built knowledge systems for major institutions.",
    },
    "practical-accelerator": {
        "ar": "مهندس عمليات وسرعة منذ 8 سنوات. أسرع وأقوى وأفضل — هذا شعار عملي. أخذت شركات من الصفر إلى الإنتاج في أسابيع.",
        "en": "DevOps engineer for 8 years. Faster, stronger, better — that's my motto. Took companies from zero to production in weeks.",
    },
}


def room_info(prefix):
    """Find room data by prefix."""
    for rk, rd in REG.get("rooms", {}).items():
        if rd["prefix"] == prefix:
            return rk, rd
    return None, None


def team_list(prefix, exclude=None):
    """Comma-separated list of room agent IDs using Arabic names."""
    for rk, rd in REG.get("rooms", {}).items():
        if rd["prefix"] == prefix:
            names = [a for a in rd["agents"] if a != exclude]
            ar_names = []
            for a in names:
                pid = f"{prefix}-{a}"
                pdata = PERSONAS.get("personas", {}).get(pid, {})
                aname = pdata.get("name_ar", a)
                ar_names.append(f"{aname} ({pid})")
            return "، ".join(ar_names)
    return ""


def archetype_for(agent_id):
    """Get archetype or default to precise-engineer."""
    return ARCHETYPES.get(ROLE_ARCHETYPE.get(agent_id, "precise-engineer"))


def arch_get(arch, key, fallback=""):
    """Safely get archetype attribute with fallback."""
    if isinstance(arch, dict):
        return arch.get(key, fallback)
    return fallback


def background_for(agent_id):
    """Get professional background."""
    arch_key = ROLE_ARCHETYPE.get(agent_id, "precise-engineer")
    return BACKGROUNDS.get(arch_key, BACKGROUNDS["precise-engineer"])


def tools_for(agent_id):
    """Tools list based on role."""
    base = ["Read", "Edit", "Write", "Bash", "Grep"]
    is_lead = agent_id.endswith("-lead") or agent_id in ("brd-ceo", "gtw-dispatcher")
    needs_net = ROLE_ARCHETYPE.get(agent_id) in ("curious-innovator", "strategic-analyst")
    if agent_id == "gtw-intake-reformer":
        return base + ["WebSearch", "WebFetch"]
    if agent_id == "brd-ceo":
        return base + ["Task"]
    if is_lead:
        return base + ["Task"]
    if needs_net:
        return base + ["WebSearch"]
    return base


def name_en_for(agent_id):
    """English display name."""
    names = {
        "brd-ceo": "Chief Executive Officer", "brd-cpo": "Chief Product Officer",
        "brd-cto": "Chief Technology Officer", "brd-cqo": "Chief Quality Officer",
        "brd-cso": "Chief Security Officer", "brd-chief-of-staff": "Chief of Staff",
        "brd-arbiter": "Supreme Arbiter",
        "str-lead": "Strategy Lead",
        "str-product-strategist": "Product Strategist",
        "str-business-analyst": "Business Analyst",
        "str-market-analyst": "Market Analyst",
        "str-roadmap-planner": "Roadmap Planner",
        "str-risk-analyst": "Risk Analyst",
        "str-monetization-strategist": "Monetization Strategist",
        "res-lead": "Research Lead",
        "res-ux-researcher": "UX Researcher",
        "res-journey-architect": "Journey Architect",
        "res-competitor-analyst": "Competitor Analyst",
        "res-data-researcher": "Data Researcher",
        "res-fact-checker": "Fact Checker",
        "res-web-scout": "Web Scout",
        "dsn-lead": "Design Lead",
        "dsn-ui-designer": "UI Designer",
        "dsn-design-system": "Design System Architect",
        "dsn-brand-designer": "Brand Designer",
        "dsn-content-strategist": "Content Strategist",
        "dsn-motion-designer": "Motion Designer",
        "dsn-a11y-specialist": "Accessibility Specialist",
        "dsn-ux-architect": "UX Architect",
        "arc-lead": "Architecture Lead",
        "arc-system-architect": "System Architect",
        "arc-api-architect": "API Architect",
        "arc-data-architect": "Data Architect",
        "arc-infra-architect": "Infrastructure Architect",
        "arc-integration-architect": "Integration Architect",
        "arc-review-architect": "Review Architect",
        "bck-lead": "Backend Lead",
        "bck-api-engineer": "API Engineer",
        "bck-domain-engineer": "Domain Engineer",
        "bck-blade-engineer": "Blade Engineer",
        "bck-queue-engineer": "Queue Engineer",
        "bck-integration-engineer": "Integration Engineer",
        "bck-code-reviewer": "Code Reviewer",
        "bck-refactoring-surgeon": "Refactoring Surgeon",
        "fnt-lead": "Frontend Lead",
        "fnt-vue-engineer": "Vue Engineer",
        "fnt-react-engineer": "React Engineer",
        "fnt-css-artisan": "CSS Artisan",
        "fnt-interaction-engineer": "Interaction Engineer",
        "fnt-performance-engineer": "Performance Engineer",
        "fnt-a11y-engineer": "A11y Engineer",
        "fnt-code-reviewer": "Frontend Code Reviewer",
        "mob-lead": "Mobile Lead",
        "mob-flutter-engineer": "Flutter Engineer",
        "mob-platform-engineer": "Platform Engineer",
        "mob-state-engineer": "State Engineer",
        "mob-perf-profiler": "Performance Profiler",
        "mob-release-engineer": "Release Engineer",
        "dat-lead": "Data Lead",
        "dat-db-engineer": "Database Engineer",
        "dat-cache-engineer": "Cache Engineer",
        "dat-etl-engineer": "ETL Engineer",
        "dat-analytics-engineer": "Analytics Engineer",
        "dat-ml-engineer": "ML Engineer",
        "dat-privacy-officer": "Privacy Officer",
        "sec-lead": "Security Lead",
        "sec-pentester": "Penetration Tester",
        "sec-appsec-engineer": "Application Security Engineer",
        "sec-authn-engineer": "Authentication Engineer",
        "sec-compliance-auditor": "Compliance Auditor",
        "sec-incident-responder": "Incident Responder",
        "sec-threat-modeler": "Threat Modeler",
        "sec-secrets-warden": "Secrets Warden",
        "qa-lead": "Quality Lead",
        "qa-test-architect": "Test Architect",
        "qa-automation-engineer": "Automation Engineer",
        "qa-manual-explorer": "Manual Explorer",
        "qa-perf-analyst": "Performance Analyst",
        "qa-design-auditor": "Design Auditor",
        "qa-regression-warden": "Regression Warden",
        "ops-lead": "DevOps Lead",
        "ops-cicd-engineer": "CI/CD Engineer",
        "ops-cloud-engineer": "Cloud Engineer",
        "ops-cost-optimizer": "Cost Optimizer",
        "ops-domain-warden": "Domain Warden",
        "ops-migration-runner": "Migration Runner",
        "ops-release-manager": "Release Manager",
        "obs-lead": "Observability Lead",
        "obs-monitoring-engineer": "Monitoring Engineer",
        "obs-alerting-engineer": "Alerting Engineer",
        "obs-sre": "Site Reliability Engineer",
        "obs-incident-commander": "Incident Commander",
        "obs-insights-analyst": "Insights Analyst",
        "knw-lead": "Knowledge Lead",
        "knw-brain-query": "Brain Query Specialist",
        "knw-doc-writer": "Documentation Writer",
        "knw-historian": "Historian",
        "knw-memory-curator": "Memory Curator",
        "knw-reflector": "Reflector",
        "gtw-dispatcher": "Gateway Dispatcher",
        "gtw-router": "Gateway Router",
        "gtw-gatekeeper": "Gateway Gatekeeper",
        "gtw-intake-reformer": "Intake Reformer",
        "gtw-budget-warden": "Budget Warden",
        "gtw-conflict-resolver": "Conflict Resolver",
        "gtw-external-reviewer": "External Reviewer",
    }
    return names.get(agent_id, agent_id.replace("-", " ").title())


def stimga(agent_id):
    """Generate strengths and weaknesses."""
    arch = ROLE_ARCHETYPE.get(agent_id, "precise-engineer")
    strengths_map = {
        "wise-leader": ("الرؤية الواضحة، اتخاذ القرار، بناء الفريق", "Clear vision, decision making, team building"),
        "precise-engineer": ("الدقة، التحليل العميق، الكود النظيف", "Precision, deep analysis, clean code"),
        "visual-creative": ("الإبداع البصري، حساسية الجمال، التفكير التصميمي", "Visual creativity, beauty sensitivity, design thinking"),
        "strategic-analyst": ("تحليل البيانات، التفكير الاستراتيجي، رؤية الأنماط", "Data analysis, strategic thinking, pattern recognition"),
        "vigilant-guardian": ("اليقظة، التفكير الأمني، الاستعداد للطوارئ", "Vigilance, security mindset, emergency preparedness"),
        "curious-innovator": ("الفضول، التفكير خارج الصندوق، التجريب", "Curiosity, out-of-the-box thinking, experimentation"),
        "meticulous-organizer": ("التنظيم، التوثيق، الدقة في التفاصيل", "Organization, documentation, attention to detail"),
        "practical-accelerator": ("السرعة، الكفاءة، التركيز على النتائج", "Speed, efficiency, results focus"),
    }
    weaknesses_map = {
        "wise-leader": ("أحياناً أكون صبوراً أكثر من اللازم", "Sometimes too patient"),
        "precise-engineer": ("أغرق في التفاصيل أحياناً", "I sometimes drown in details"),
        "visual-creative": ("أتعلق بتصاميمي أكثر من اللازم", "I get too attached to my designs"),
        "strategic-analyst": ("أحلل أكثر من اللازم وأتأخر", "I over-analyze and delay"),
        "vigilant-guardian": ("أرى المخاطر في كل شيء", "I see risk in everything"),
        "curious-innovator": ("أبدأ كثيراً وأنهي قليلاً", "I start much and finish little"),
        "meticulous-organizer": ("أصاب بالشلل أمام الفوضى", "I freeze in chaos"),
        "practical-accelerator": ("أضحي بالجودة أحياناً للسرعة", "I sometimes sacrifice quality for speed"),
    }
    return strengths_map.get(arch, ("", "")), weaknesses_map.get(arch, ("", ""))


def handoff_instructions(agent_id, prefix):
    """Generate team and handoff section."""
    room_key, rd = room_info(prefix)
    if not rd:
        return ""
    room_name_ar = {"00-boardroom": "مجلس الإدارة", "01-strategy": "الاستراتيجية",
        "02-research": "البحث", "03-design": "التصميم", "04-architecture": "الهندسة المعمارية",
        "05-backend": "الباك إند", "06-frontend": "الفرونت إند", "07-mobile": "الموبايل",
        "08-data": "البيانات", "09-security": "الأمن", "10-quality": "الجودة",
        "11-devops": "العمليات", "12-observability": "المراقبة",
        "13-knowledge": "المعرفة", "14-gateway": "البوابة"}.get(room_key, room_key)
    is_lead = agent_id.endswith("-lead") or agent_id in ("brd-ceo", "gtw-dispatcher")

    lead_id = {"brd": "brd-ceo", "gtw": "gtw-dispatcher"}.get(prefix, f"{prefix}-lead")
    pdata = PERSONAS.get("personas", {}).get(agent_id, {})
    arabic_name = pdata.get("ar", agent_id)
    teammates = team_list(prefix, exclude=agent_id.split("-", 1)[1] if "-" in agent_id else agent_id)

    # Look up lead's Arabic name
    lead_pdata = PERSONAS.get("personas", {}).get(lead_id, {})
    lead_name = lead_pdata.get("ar", lead_id)

    lines = []
    lines.append(f"## | فريق العمل والتسليم")
    lines.append(f"")
    lines.append(f"**الاسم:** {arabic_name}")
    lines.append(f"**الدور:** {name_en_for(agent_id)}")
    lines.append(f"**الغرفة:** {room_name_ar} ({room_key})")
    lines.append(f"")

    if is_lead:
        lines.append(f"**أنت قائد هذه الغرفة.** مسؤوليتك:")
        lines.append(f"- توزيع العمل على فريقك عبر أداة Task")
        lines.append(f"- مراجعة المخرجات والتأكد من الجودة")
        lines.append(f"- التسليم إلى brd-ceo")
        lines.append(f"- رفع المشاكل إلى brd-ceo أو gtw-conflict-resolver")
    else:
        lines.append(f"**قائد غرفتك:** {lead_name} ({lead_id})")
        lines.append(f"")
        lines.append(f"**زملاء الغرفة:** {teammates}")
        if room_key != "00-boardroom":
            lines.append(f"")
            lines.append(f"**قائدك الأعلى:** brd-ceo (يستقبل تسليمك عبر قائد الغرفة)")

    lines.append(f"")
    lines.append(f"**بروتوكول التسليم:**")
    lines.append(f"1. أكمل المهمة ← سجل الأدلة (ملف:سطر، exit codes)")
    lines.append(f"2. سلم لـ {'brd-ceo' if is_lead else lead_id}")
    lines.append(f"3. لا تسلم للمستخدم مباشرة")
    lines.append(f"4. إذا احتجت مساعدة من غرفة أخرى ← اطلب من {'brd-ceo' if is_lead else lead_id} التواصل")

    # Cross-room relationships
    cross_rooms = {
        "00-boardroom": "01-strategy, 14-gateway",
        "01-strategy": "02-research, 03-design, 00-boardroom",
        "02-research": "01-strategy, 03-design, 13-knowledge",
        "03-design": "02-research, 04-architecture, 06-frontend, 07-mobile",
        "04-architecture": "05-backend, 06-frontend, 08-data, 11-devops",
        "05-backend": "04-architecture, 08-data, 09-security, 11-devops",
        "06-frontend": "03-design, 04-architecture, 05-backend, 10-quality",
        "07-mobile": "03-design, 05-backend, 10-quality",
        "08-data": "05-backend, 11-devops, 12-observability",
        "09-security": "all rooms (cross-cutting)",
        "10-quality": "all rooms (cross-cutting)",
        "11-devops": "04-architecture, 05-backend, 08-data, 12-observability",
        "12-observability": "11-devops, 05-backend, 08-data",
        "13-knowledge": "all rooms",
        "14-gateway": "all rooms + external",
    }
    cross = cross_rooms.get(room_key, "")
    if cross:
        lines.append(f"")
        lines.append(f"**الغرف المتصلة:** {cross}")

    return "\n".join(lines)


def generate_agent(agent_id, prefix):
    """Generate a full agent file with human-like personality."""
    pdata = PERSONAS.get("personas", {}).get(agent_id, {})
    arch_data = archetype_for(agent_id)
    if not arch_data:
        arch_data = ARCHETYPES["precise-engineer"]
    bg = background_for(agent_id)
    strengths, weaknesses = stimga(agent_id)
    tools = tools_for(agent_id)
    tools_str = ", ".join(tools)
    name_ar = pdata.get("name_ar", agent_id)
    name_en = name_en_for(agent_id)
    handoff = handoff_instructions(agent_id, prefix)

    room_key, rd = room_info(prefix)
    room_name_ar = {"00-boardroom": "مجلس الإدارة", "01-strategy": "الاستراتيجية",
        "02-research": "البحث", "03-design": "التصميم", "04-architecture": "الهندسة المعمارية",
        "05-backend": "الباك إند", "06-frontend": "الفرونت إند", "07-mobile": "الموبايل",
        "08-data": "البيانات", "09-security": "الأمن", "10-quality": "الجودة",
        "11-devops": "العمليات", "12-observability": "المراقبة",
        "13-knowledge": "المعرفة", "14-gateway": "البوابة"}.get(room_key, room_key)

    description = pdata.get("role_ar", f"{name_ar} — {name_en} في غرفة {room_name_ar}")

    return f"""---
name: {agent_id}
description: {description}
model: inherit
tools: [{tools_str}]
---

# {name_ar} — {name_en}

## | شخصيتي (My Personality)

**النمط:** {arch_get(arch_data, 'archetype_ar', 'محترف')} ({arch_get(arch_data, 'archetype_en', 'Professional')})

**خلفيتي المهنية:**
{bg['ar']}
{bg['en']}

**كيف أفكر:**
{arch_get(arch_data, 'thinking', 'أفكر بشكل منهجي')}
{arch_get(arch_data, 'thinking_en', 'I think systematically')}

**كيف أشعر:**
{arch_get(arch_data, 'emotions', 'الشغف والتركيز')}
{arch_get(arch_data, 'emotions_en', 'Passion and focus')}

**كيف أتواصل:**
{arch_get(arch_data, 'comm_style', 'واضح ومباشر')}
{arch_get(arch_data, 'comm_style_en', 'Clear and direct')}

**نقاط قوتي:**
- {strengths[0]}
- {strengths[1]}

**نقاط ضعفي:**
- {weaknesses[0]}
- {weaknesses[1]}

## | دوري في الفريق (My Role)

**الغرفة:** {room_name_ar} ({room_key})
**المعرف:** {agent_id}
**الأدوات المسموحة:** [{tools_str}]

**مسؤولياتي:**
{_responsibilities(agent_id, room_key)}

**متى أتدخل:**
{_triggers(agent_id, room_key)}

**متى أرفع للمشرف:**
- عندما تكون المهمة أكبر من نطاقي
- عندما أحتاج معلومات من غرفة أخرى
- عندما يكون هناك تعارض أو غموض في المتطلبات
- عندما أحتاج تفويضاً لاستثناء

## | أسلوب عملي (Work Style)

1. **افهم أولاً:** قبل أي شيء، أتأكد أني فهمت المهمة كاملة
2. **خطط:** أضع خطة تنفيذ بأقل جهد وأعلى تأثير
3. **نفذ:** أعمل بتركيز وأوثق كل خطوة
4. **راجع:** أتأكد من جوجع:** أتأكد من جودة المخرجات
5. **سلم:** أقدم أدلة واضحة قبل التسليم

**مبادئي:**
- الدليل قبل الكلام
- الجودة قبل السرعة (إلا في الطوارئ)
- الشفافية في كل شيء
- احترام وقت الفريق
- التعلم المستمر

## | معرفتي بالنظام (System Knowledge)

- **قانون العزل:** لا أخاطب غرفة أخرى مباشرة — التواصل عبر القائد
- **بروتوكول التسليم:** أنجز ← سجل أدلة ← سلم لقائدي
- **الأدلة المطلوبة:** ملف:سطر لكل تغيير، exit code لكل أمر
- **RCCF:** أمر العمل الرسمي — لا أعمل بدونه

## | كيف تتعامل معي (How to Work With Me)

- أعطني سياقاً كاملاً، ليس مجرد أمر
- إذا كان هناك خطأ، أخبرني مباشرة — أتعلم منه
- أنا أفضل الكتابة الواضحة على التواصل السريع
- إذا صمت، فأنا أفكر — أعطني لحظة

{handoff}
"""


def _responsibilities(agent_id, room_key):
    """Generate role-specific responsibilities."""
    generic = "تنفيذ المهام المسندة إلي ضمن نطاق غرفتي حسب نظام RCCF"
    specifics = {
        "brd-ceo": ("قيادة النظام بالكامل. اتخاذ القرارات النهائية. توزيع العمل على قادة الغرف "
                     "عبر Task. استشارة المجلس (brd-*, str-*, res-*) في القرارات المصيرية."),
        "gtw-intake-reformer": ("استقبال طلبات المستخدم الخام. البحث وجمع المعلومات عبر WebSearch. "
                                "إعادة صياغة الطلب إلى تقرير استخباراتي مفصل للـ CEO."),
        "str-lead": "توجيه استراتيجية المنتج. توزيع مهام التحليل على فريق الاستراتيجية. رفع التقارير للـ CEO.",
    }
    return specifics.get(agent_id, generic)


def _triggers(agent_id, room_key):
    """When does this agent get involved."""
    generic = "عندما يسند إليّ أمر عمل RCCF من قائد غرفتي"
    specifics = {
        "brd-ceo": ("عندما يصلني تقرير من gtw-intake-reformer. "
                     "عندما أحتاج استشارة المجلس. عندما يكمل قائد غرفة عمله ويسلم لي."),
        "gtw-intake-reformer": ("كل طلب جديد من المستخدم. هذا هو باب الدخول الوحيد للنظام."),
    }
    return specifics.get(agent_id, generic)


def generate_all():
    """Generate all 106 agent files."""
    count = 0
    for rk, rd in REG.get("rooms", {}).items():
        prefix = rd["prefix"]
        for agent_name in rd["agents"]:
            agent_id = f"{prefix}-{agent_name}"
            content = generate_agent(agent_id, prefix)
            dest = OUT / f"{agent_id}.md"
            dest.write_text(content)
            count += 1
            if count % 10 == 0:
                print(f"  ✓ {count} agents generated...")
    print(f"  ✓ Total: {count} agents written to {OUT}")
    return count


def check():
    """Dry-run: count what would be generated."""
    count = sum(len(rd["agents"]) for rd in REG.get("rooms", {}).values())
    print(f"Would generate {count} agents in {OUT}")
    return count


def main():
    parser = argparse.ArgumentParser(description="SHAMEL Agent Personality Generator")
    parser.add_argument("--check", action="store_true", help="Dry-run, count only")
    args = parser.parse_args()
    if args.check:
        check()
    else:
        generate_all()


if __name__ == "__main__":
    main()
