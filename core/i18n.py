"""
Internationalization (i18n) Module for JomiGuard.
Primary Language: Bengali (bn)
Secondary Language: English (en)
"""

from typing import Any, Union


# English to Bengali digit mapping
_EN_TO_BN_DIGITS = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")
_BN_TO_EN_DIGITS = str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789")


def to_bn_digits(value: Union[str, int, float]) -> str:
    """Convert western numerals to Bengali numerals."""
    if value is None:
        return ""
    return str(value).translate(_EN_TO_BN_DIGITS)


def to_en_digits(value: Union[str, int, float]) -> str:
    """Convert Bengali numerals to western numerals."""
    if value is None:
        return ""
    return str(value).translate(_BN_TO_EN_DIGITS)


def fmt_num(val: Union[int, float, str], lang: str = "bn", decimals: int = 2) -> str:
    """Format numbers according to selected language."""
    if val is None or val == "":
        return "—"
    try:
        num = float(val)
        if num.is_integer():
            s = f"{int(num):,}"
        else:
            s = f"{num:,.{decimals}f}"
        return to_bn_digits(s) if lang == "bn" else s
    except (ValueError, TypeError):
        return str(val)


TRANSLATIONS = {
    # -------------------------------------------------------------------------
    # GLOBAL & NAVBAR
    # -------------------------------------------------------------------------
    "brand_name": {
        "bn": "জমিগার্ড",
        "en": "JomiGuard"
    },
    "brand_tagline": {
        "bn": "ভূমি স্বত্ব ও দ্বৈত বিক্রয় প্রতিরোধ প্ল্যাটফর্ম",
        "en": "Land Title & Double-Selling Prevention Platform"
    },
    "nav_home": {
        "bn": "হোমপেজ",
        "en": "Home"
    },
    "nav_how_it_works": {
        "bn": "কীভাবে কাজ করে",
        "en": "How It Works"
    },
    "nav_modules": {
        "bn": "মূল মডিউলসমূহ",
        "en": "Core Modules"
    },
    "nav_roadmap": {
        "bn": "রোডম্যাপ",
        "en": "Roadmap"
    },
    "nav_faq": {
        "bn": "সাধারণ জিজ্ঞাসা",
        "en": "FAQ"
    },
    "nav_demo": {
        "bn": "লাইভ ডেমো",
        "en": "Live Demo"
    },
    "nav_get_started": {
        "bn": "সিস্টেমে প্রবেশ করুন",
        "en": "Get Started"
    },
    "nav_back_to_home": {
        "bn": "← হোমপেজে ফিরুন",
        "en": "← Back to Home"
    },
    "lang_toggle_label": {
        "bn": "বাং / EN",
        "en": "EN / বাং"
    },
    "theme_auto": {
        "bn": "স্বয়ংক্রিয় (অটো)",
        "en": "Auto (System)"
    },
    "theme_light": {
        "bn": "লাইট মোড",
        "en": "Light Mode"
    },
    "theme_dark": {
        "bn": "ডার্ক মোড",
        "en": "Dark Mode"
    },

    # -------------------------------------------------------------------------
    # GOVERNANCE NOTICE (Strict Legal Wording)
    # -------------------------------------------------------------------------
    "governance_notice": {
        "bn": "ℹ️ সিদ্ধান্ত-সহায়ক নির্দেশিকা: এই সতর্কবার্তাটি তথ্যের সম্ভাব্য অসঙ্গতি নির্দেশ করে, প্রমাণিত জালিয়াতি নয়। একই দাগের পুনরাবৃত্তি বৈধ আংশিক বিক্রয়, ওয়ারিশসূত্রে মালিকানা বা নামজারি প্রক্রিয়াধীন থাকার কারণেও হতে পারে—যাচাইয়ের জন্য মানবিক পর্যালোচনা আবশ্যক।",
        "en": "ℹ️ Decision-Support Notice: An alert indicates a record inconsistency requiring human verification, not proven fraud. Repeated plot identifiers may reflect legitimate partial transfers, inheritance shares, or pending mutation updates."
    },

    # -------------------------------------------------------------------------
    # LANDING PAGE: HERO SECTION
    # -------------------------------------------------------------------------
    "hero_badge": {
        "bn": "✨ বাংলাদেশে প্রথম স্বয়ংক্রিয় ভূমি স্বত্ব ও দ্বৈত বিক্রয় প্রতিরোধ প্রযুক্তি",
        "en": "✨ Bangladesh's Premier Automated Land Title & Double-Selling Prevention Platform"
    },
    "hero_title": {
        "bn": "জমির মালিকানা যাচাই ও দ্বৈত বিক্রয় প্রতিরোধে জাতীয় প্ল্যাটফর্ম",
        "en": "National Platform for Land Title Verification & Double-Selling Prevention"
    },
    "hero_subtitle": {
        "bn": "সাব-রেজিস্ট্রি দলিল ও এসি ল্যান্ড নামজারির রিয়েল-টাইম ক্রস-ম্যাচিং, গাণিতিক জমি বণ্টন নিরীক্ষা এবং রুল-ভিত্তিক ফ্রড প্রিভেনশন। সাব-রেজিস্ট্রার, ব্যাংক কর্মকর্তা ও ক্রেতাদের জন্য প্রাতিষ্ঠানিক ঝুঁকি মূল্যায়ন ব্যবস্থা।",
        "en": "Real-time cross-matching of Sub-Registry deed registrations and AC Land e-mutations with mathematical parcel integrity verification. Institutional risk intelligence for registry officers, bank credit auditors, and property buyers."
    },
    "hero_cta_primary": {
        "bn": "🚀 সিস্টেমে প্রবেশ করুন (Get Started)",
        "en": "🚀 Enter JomiGuard System (Get Started)"
    },
    "hero_cta_secondary": {
        "bn": "🧪 লাইভ ডেমো পরীক্ষা করুন (Try Sandbox)",
        "en": "🧪 Explore Live Sandbox (Try Demo)"
    },
    "hero_trust_badge_1": {
        "bn": "🔒 ১০০% ব্যাখ্যামূলক ও নিরপেক্ষ রুল ইঞ্জিন",
        "en": "🔒 100% Explainable Rule-Based Logic"
    },
    "hero_trust_badge_2": {
        "bn": "⚡ <৫০ মিলি-সেকেন্ডে তাৎক্ষণিক স্ক্রিনিং",
        "en": "⚡ Instant Screening in <50ms"
    },
    "hero_trust_badge_3": {
        "bn": "🏛️ সাব-রেজিস্ট্রি ও এসি ল্যান্ড সামঞ্জস্যপূর্ণ",
        "en": "🏛️ Sub-Registry & AC Land Aligned"
    },

    # -------------------------------------------------------------------------
    # STATS TICKER
    # -------------------------------------------------------------------------
    "stat_screened_plots": {
        "bn": "নিরীক্ষিত দাগ ও খতিয়ান",
        "en": "Screened Parcels"
    },
    "stat_registered_deeds": {
        "bn": "রেজিস্ট্রিকৃত সাব-কবলা দলিল",
        "en": "Registered Deeds"
    },
    "stat_verified_mutations": {
        "bn": "অনুমোদিত নামজারি কেস",
        "en": "Verified e-Mutations"
    },
    "stat_detection_speed": {
        "bn": "অসঙ্গতি শনাক্তকরণ গতি",
        "en": "Detection Latency"
    },
    "stat_detection_speed_val": {
        "bn": "< ৫০ মি.সে.",
        "en": "< 50ms"
    },

    # -------------------------------------------------------------------------
    # LANDING PAGE: THE PROBLEM
    # -------------------------------------------------------------------------
    "problem_section_badge": {
        "bn": "প্রশাসনিক ও আইনি চ্যালেঞ্জ",
        "en": "Administrative & Legal Challenges"
    },
    "problem_section_title": {
        "bn": "বাংলাদেশের ভূমি ব্যবস্থাপনায় প্রধান ঝুঁকিসমূহ",
        "en": "Critical Risks in Bangladesh Land Administration"
    },
    "problem_section_subtitle": {
        "bn": "সাব-রেজিস্ট্রি এবং এসি ল্যান্ড অফিসের ডেটাবেজ পৃথক হওয়ায় প্রতারক চক্র একই জমি বারবার বিক্রয় ও খতিয়ানে অতিরিক্ত জমি ঢুকিয়ে কোটি টাকার জালিয়াতি করে থাকে।",
        "en": "Fragmented data silos between Sub-Registry deed archives and AC Land mutation offices enable duplicate sales, inflated decimal areas, and fraudulent title transfers."
    },
    "prob_1_title": {
        "bn": "একই দাগ একাধিকবার বিক্রয় (দ্বৈত বিক্রয়)",
        "en": "Duplicate Sales on Same Plot"
    },
    "prob_1_desc": {
        "bn": "পূর্বে জমি বিক্রি করে নামজারি হওয়ার পূর্ববর্তী অবকাশে অসৎ বিক্রেতা নতুন ক্রেতার নিকট একই দাগের জমি পুনরায় সাব-রেজিস্ট্রি করে অর্থ হাতিয়ে নেয়।",
        "en": "Dishonest sellers re-execute deeds for plots already conveyed, exploiting the communication gap before mutation records are finalized."
    },
    "prob_2_title": {
        "bn": "নামজারিতে জমির পরিমাণ বৃদ্ধি (Area Inflation)",
        "en": "Area Inflation in Mutations"
    },
    "prob_2_desc": {
        "bn": "দলিলে ১০ শতাংশ হস্তান্তর থাকলেও এসি ল্যান্ড অফিসে প্রভাব খাটিয়ে ১৫ শতাংশ জমির নামজারি অনুমোদন করিয়ে খতিয়ান সৃষ্টি করা হয়।",
        "en": "Mutating larger decimal areas than legally conveyed in the registered deed, creating fictitious land rights on record."
    },
    "prob_3_title": {
        "bn": "ভুয়া ক্রেতা ও আবেদনকারী প্রতিস্থাপন (Identity Theft)",
        "en": "Impostor Applicant Substitution"
    },
    "prob_3_desc": {
        "bn": "দলিলের প্রকৃত ক্রেতার পরিবর্তে ভিন্ন ব্যক্তির এনআইডি ও নাম ব্যবহার করে নামজারি সম্পন্ন করে প্রকৃত মালিককে উচ্ছেদ করার অপচেষ্টা।",
        "en": "Approving mutation khatians in the name of unauthorized impostors whose NIDs differ from the deed's genuine purchaser."
    },
    "prob_4_title": {
        "bn": "দলিলের পূর্বে নামজারি (Chronological Paradox)",
        "en": "Chronological Inversion Paradox"
    },
    "prob_4_desc": {
        "bn": "দলিল সাব-রেজিস্ট্রির তারিখের পূর্ববর্তী কোনো তারিখে নামজারি অনুমোদন দেখানো—যা আইনত ও গাণিতিকভাবে সম্পূর্ণ অসম্ভব।",
        "en": "Mutation case approvals predating the underlying deed registration date, exposing severe back-dated clerical manipulation."
    },
    "prob_5_title": {
        "bn": "অস্তিত্বহীন ও ভুয়া দলিলের উদ্ধৃতি (Phantom Deeds)",
        "en": "Phantom Deed Citations"
    },
    "prob_5_desc": {
        "bn": "সাব-রেজিস্ট্রি অফিসে কোনো অস্তিত্ব নেই এমন কাল্পনিক বা জাল দলিল নম্বর দেখিয়ে নামজারি ও জোত খতিয়ান তৈরির অপচেষ্টা।",
        "en": "Referencing non-existent or unindexed deed numbers to manufacture fraudulent mutation dakhilas."
    },
    "prob_6_title": {
        "bn": "মালিকানা ধারাবাহিকতা বিচ্ছিন্নতা (Broken Chain of Title)",
        "en": "Broken Chain of Title"
    },
    "prob_6_desc": {
        "bn": "রেকর্ডিয় মালিক বা বৈধ উত্তরাধিকারী ব্যতিরেকে অননুমোদিত ব্যক্তি কর্তৃক জমি বিক্রয়—যার ফলে ক্রেতা আইনি বিরোধে পতিত হন।",
        "en": "Sales executed by parties with no verifiable prior ownership or recorded acquisition, severing legitimate title lineage."
    },

    # -------------------------------------------------------------------------
    # LANDING PAGE: THE SOLUTION & CORE MODULES
    # -------------------------------------------------------------------------
    "modules_section_badge": {
        "bn": "স্বয়ংক্রিয় নিরীক্ষা প্রযুক্তি",
        "en": "Automated Audit Engine"
    },
    "modules_section_title": {
        "bn": "জমিগার্ডের স্বয়ংক্রিয় রুল-ভিত্তিক অ্যানোমালি ইঞ্জিন",
        "en": "JomiGuard's Deterministic Risk Screening Engine"
    },
    "modules_section_subtitle": {
        "bn": "শতভাগ ব্যাখ্যামূলক ৬টি প্রাতিষ্ঠানিক অ্যালগরিদম যা যেকোনো অসঙ্গতি তাৎক্ষণিকভাবে নথির দ্বিমুখী প্রমাণসহ উপস্থাপন করে।",
        "en": "Six deterministic verification rules providing transparent, explainable bilateral evidence comparison."
    },
    "rule_r1_title": {
        "bn": "রুল R1: দ্বৈত বিক্রয় ও ওভার-সেল প্রতিরোধ",
        "en": "Rule R1: Conflicting Double-Selling Detection"
    },
    "rule_r1_desc": {
        "bn": "একই বিক্রেতা কর্তৃক পূর্ববর্তী বিক্রয়ের পর্যাপ্ত মালিকানা অবশিষ্টাংশ ছাড়া দ্বিতীয় দলিলের উপস্থিতি শনাক্ত করে।",
        "en": "Catches secondary deed executions by the same seller without sufficient verifiable remaining ownership balance."
    },
    "rule_r2_title": {
        "bn": "রুল R2: দাগের মোট ধারণক্ষমতা ও অতিরিক্ত বিক্রয়",
        "en": "Rule R2: Plot Capacity & Area Over-Sale"
    },
    "rule_r2_desc": {
        "bn": "দাগের সিএস/এসএ/আরএস খতিয়ানের মোট ক্ষেত্রফলের চেয়ে মোট বিক্রিত শতাংশের যোগফল বেশি হলে তাৎক্ষণিক অ্যালার্ট দেয়।",
        "en": "Flags plots where cumulative transferred decimals exceed the total surveyed capacity of the parcel."
    },
    "rule_m1_title": {
        "bn": "রুল M1: দলিল বনাম নামজারি এরিয়া অডিট",
        "en": "Rule M1: Deed vs. Mutation Area Mismatch"
    },
    "rule_m1_desc": {
        "bn": "সাব-কবলা দলিলে উল্লেখিত আয়তনের তুলনায় নামজারি কেসে অনুমোদিত আয়তনে ০.০২ শতাংশের বেশি তারতম্য থাকলে তা চিহ্নিত করে।",
        "en": "Verifies that mutated decimal area accurately corresponds with the registered deed within a 0.02-decimal tolerance."
    },
    "rule_m2_title": {
        "bn": "রুল M2: ক্রেতা ও আবেদনকারী এনআইডি যাচাই",
        "en": "Rule M2: Purchaser vs. Applicant NID Audit"
    },
    "rule_m2_desc": {
        "bn": "দলিলের নিবন্ধিত ক্রেতার জাতীয় পরিচয়পত্র (NID) এবং নামজারির আবেদনকারীর NID-এর শতভাগ মিল নিশ্চিত করে।",
        "en": "Ensures complete mathematical congruence between the deed purchaser's NID and the mutation applicant's identity."
    },
    "rule_m3_title": {
        "bn": "রুল M3: কালানুক্রমিক অসঙ্গতি (Chronological Paradox)",
        "en": "Rule M3: Temporal / Chronological Paradox"
    },
    "rule_m3_desc": {
        "bn": "দলিল সাব-রেজিস্ট্রির তারিখের পূর্বেই যদি নামজারি অনুমোদনের রেকর্ড পাওয়া যায়, তবে তা তৎক্ষণাৎ ক্রুশিয়াল রিভিউ হিসেবে চিহ্নিত করে।",
        "en": "Detects impossible chronological sequencing where a mutation approval date precedes deed registration."
    },
    "rule_m4_title": {
        "bn": "রুল M4: মালিকানা শৃঙ্খল ও অবিক্রিত সত্যতা",
        "en": "Rule M4: Title Continuity & Ownership Chain"
    },
    "rule_m4_desc": {
        "bn": "মূল খতিয়ানের আদি মালিক থেকে শুরু করে প্রতিটি বিক্রয় ও নামজারির ধারাবাহিক ট্রানজেকশন হিস্টোরি অডিট করে।",
        "en": "Audits the complete ownership genealogy from initial survey settlement through successive deeds and mutations."
    },

    # -------------------------------------------------------------------------
    # LANDING PAGE: HOW IT WORKS
    # -------------------------------------------------------------------------
    "hiw_section_badge": {
        "bn": "কার্যপ্রণালী",
        "en": "Workflow"
    },
    "hiw_section_title": {
        "bn": "৪টি ধাপে স্বয়ংক্রিয় ভূমি সুরক্ষা নিশ্চিতকরণ",
        "en": "Four Seamless Steps to Land Integrity"
    },
    "hiw_section_subtitle": {
        "bn": "সাব-রেজিস্ট্রি এবং রাজস্ব প্রশাসনের দৈনন্দিন কার্যক্রমে সহজেই অন্তর্ভুক্তযোগ্য ডিজিটাল অডিট পাইপলাইন।",
        "en": "A zero-disruption digital audit pipeline easily embeddable into registry and revenue offices."
    },
    "step_1_title": {
        "bn": "১. দলিল ও খতিয়ান ডেটা ইনজেশন",
        "en": "1. Multi-Source Record Ingestion"
    },
    "step_1_desc": {
        "bn": "সাব-রেজিস্ট্রি অফিসের দলিল রেজিস্ট্রি এবং এসি ল্যান্ড অফিসের ই-নামজারি রেকর্ড সমন্বিত কেন্দ্রীয় তথ্যভাণ্ডারে সংগৃহীত হয়।",
        "en": "Deed registration ledgers and AC Land e-mutation records are consolidated into a unified structured data repository."
    },
    "step_2_title": {
        "bn": "২. দ্বিমুখী ক্রস-ম্যাচিং পাইপলাইন",
        "en": "2. Bilateral Cross-Verification"
    },
    "step_2_desc": {
        "bn": "প্রতিটি দলিল ও খতিয়ানের দাগ নম্বর, এনআইডি, হস্তান্তরিত আয়তন এবং তারিখ স্বয়ংক্রিয়ভাবে পরস্পর মেপে দেখা হয়।",
        "en": "Plot identifiers, 10/17-digit NIDs, decimal areas, and execution timestamps are matched pairwise across systems."
    },
    "step_3_title": {
        "bn": "৩. রুল-ভিত্তিক অ্যানোমালি ফিল্টারিং",
        "en": "3. Rule-Based Anomaly Screening"
    },
    "step_3_desc": {
        "bn": "৬টি মূল আইনি অ্যালগরিদম প্রতিটি লেনদেন যাচাই করে এবং কোনো বিচ্যুতি পেলে তাৎক্ষণিক ব্যাখ্যা ও প্রমাণসহ সতর্কবার্তা তৈরি করে।",
        "en": "Six deterministic legal algorithms evaluate each transfer, generating instant alerts with transparent evidence diffs."
    },
    "step_4_title": {
        "bn": "৪. প্রাতিষ্ঠানিক ট্রায়াজ ও অ্যাকশনযোগ্য রিপোর্ট",
        "en": "4. Institutional Triage & Official Reports"
    },
    "step_4_desc": {
        "bn": "রেজিস্ট্রার ও রাজস্ব কর্মকর্তাদের জন্য সুনির্দিষ্ট দ্বি-কলাম প্রমাণপত্র এবং সাইন-অফ উপযোগী ফরমাল রিপোর্ট প্রস্তুত হয়।",
        "en": "Two-column comparison dossiers and formal printable inspection reports are delivered for official review."
    },

    # -------------------------------------------------------------------------
    # LANDING PAGE: ROADMAP
    # -------------------------------------------------------------------------
    "roadmap_section_badge": {
        "bn": "ভবিষ্যৎ পরিকল্পনা",
        "en": "Strategic Roadmap"
    },
    "roadmap_section_title": {
        "bn": "জমিগার্ড প্রাতিষ্ঠানিক সম্প্রসারণ রোডম্যাপ",
        "en": "Institutional Expansion Roadmap"
    },
    "roadmap_section_subtitle": {
        "bn": "পাইলট প্রোটোটাইপ থেকে বাংলাদেশের জাতীয় ভূমি সেবা নেটওয়ার্কে পূর্ণাঙ্গ রূপান্তর।",
        "en": "From high-precision pilot prototype to nationwide institutional land risk infrastructure."
    },
    "phase_1_badge": {
        "bn": "সম্পন্ন (Live Engine)",
        "en": "Completed (Live)"
    },
    "phase_1_title": {
        "bn": "ফেজ ১: কোর ভ্যালিডেশন ও রুল-বেসড অ্যানোমালি ইঞ্জিন",
        "en": "Phase 1: Core Rule Engine & Bilateral Verification"
    },
    "phase_1_desc": {
        "bn": "দ্বৈত বিক্রয়, আয়তন বৃদ্ধি, এনআইডি অসঙ্গতি এবং টাইমলাইন প্যারাডক্স তাৎক্ষণিকভাবে শনাক্তকরণে SQLite/SQL-ভিত্তিক সক্ষমতা তৈরি।",
        "en": "Full deployment of deterministic anomaly detection, monospace evidence diffing, and sandbox simulation."
    },
    "phase_2_badge": {
        "bn": "চলমান (In Progress)",
        "en": "In Progress"
    },
    "phase_2_title": {
        "bn": "ফেজ ২: সাব-রেজিস্ট্রি ও এসি ল্যান্ড রিয়েল-টাইম এপিআই",
        "en": "Phase 2: Sub-Registry & AC Land Live API Integration"
    },
    "phase_2_desc": {
        "bn": "দলিল সম্পাদনের মুহূর্তেই সাব-রেজিস্ট্রারের ডেস্কে স্বয়ংক্রিয় হোল্ড অ্যালার্ট প্রদান ও খতিয়ান যাচাই এপিআই সংযোগ।",
        "en": "Real-time pre-registration screening API alerting sub-registrars directly at deed execution."
    },
    "phase_3_badge": {
        "bn": "পরবর্তী ধাপ (Q3 2026)",
        "en": "Upcoming (Q3 2026)"
    },
    "phase_3_title": {
        "bn": "ফেজ ৩: ব্যাংক বন্ধক ও ডেভেলপার টাইটেল ভেরিফিকেশন",
        "en": "Phase 3: Bank Collateral & Developer Title Verification"
    },
    "phase_3_desc": {
        "bn": "ব্যাংক ও আর্থিক প্রতিষ্ঠানের জন্য রিয়েল-টাইম মর্টগেজ স্ক্রিনিং—যাতে একই জমি একাধিক ব্যাংকে বন্ধক রাখা রোধ করা যায়।",
        "en": "B2B SaaS portal enabling financial institutions to audit land collateral and stop duplicate mortgaging."
    },
    "phase_4_badge": {
        "bn": "দীর্ঘমেয়াদী ভিশন (Q4 2026)",
        "en": "Long-Term Vision (Q4 2026)"
    },
    "phase_4_title": {
        "bn": "ফেজ ৪: জাতীয় ডিএলআরএস ও আদালত সাক্ষ্য প্ল্যাটফর্ম",
        "en": "Phase 4: National DLRS & Judicial Evidence Network"
    },
    "phase_4_desc": {
        "bn": "ভূমি জরিপ ও রেকর্ড পরিদপ্তরের মৌজা ম্যাপের সাথে জিপিএস ইন্টিগ্রেশন এবং আদালতে গ্রহণযোগ্য ডিজিটাল অডিট ট্রেইল।",
        "en": "DLRS cadastral map linkage and tamper-evident audit dossiers certified for judicial title disputes."
    },

    # -------------------------------------------------------------------------
    # LANDING PAGE: FAQ
    # -------------------------------------------------------------------------
    "faq_section_badge": {
        "bn": "সাধারণ জিজ্ঞাসা",
        "en": "Frequently Asked Questions"
    },
    "faq_section_title": {
        "bn": "জমিগার্ড সম্পর্কিত সাধারণ প্রশ্নোত্তর",
        "en": "Frequently Asked Questions"
    },
    "faq_section_subtitle": {
        "bn": "প্ল্যাটফর্মের কার্যপদ্ধতি, আইনি অবস্থান এবং ব্যবহারবিধি সম্পর্কিত উত্তর।",
        "en": "Key questions on legal status, data security, false positive mitigation, and deployment."
    },
    "faq_q1": {
        "bn": "জমিগার্ডের সতর্কবার্তা কি নিশ্চিত জালিয়াতি বা অপরাধ প্রমাণ করে?",
        "en": "Does a JomiGuard alert legally prove fraud or a crime?"
    },
    "faq_a1": {
        "bn": "না। জমিগার্ড একটি প্রাতিষ্ঠানিক সিদ্ধান্ত-সহায়ক প্ল্যাটফর্ম (Decision-Support System)। একটি অ্যালার্ট শুধুমাত্র তথ্যের অসঙ্গতি নির্দেশ করে—যা বৈধ আংশিক বণ্টন, ওয়ারিশসূত্রে পাওয়া অংশ বা নামজারি প্রক্রিয়াধীন থাকার কারণেও ঘটতে পারে। এটি নিশ্চিত জালিয়াতি নয় এবং চূড়ান্ত সিদ্ধান্তের জন্য রেজিস্ট্রি ও রাজস্ব কর্মকর্তার মানবিক পর্যালোচনা অপরিহার্য।",
        "en": "No. JomiGuard is strictly an institutional decision-support system. An alert flags a record inconsistency requiring human verification, not proven fraud. Repeated plot identifiers may reflect legitimate partial transfers, inheritance shares, or pending mutation updates."
    },
    "faq_q2": {
        "bn": "সাব-রেজিস্ট্রি ও এসি ল্যান্ড অফিসের সাথে জমিগার্ড কীভাবে কাজ করে?",
        "en": "How does JomiGuard integrate with Sub-Registry and AC Land offices?"
    },
    "faq_a2": {
        "bn": "জমিগার্ড সাব-রেজিস্ট্রি অফিসের দলিল রেজিস্ট্রি তথ্য এবং এসি ল্যান্ড অফিসের ই-নামজারি ডাটাবেজের মধ্যে একটি স্বাধীন নিরীক্ষা সেতু হিসেবে কাজ করে। প্রতিটি নতুন দলিল বা নামজারি যুক্ত হওয়ামাত্র উভয় সিস্টেমের তথ্য মিলিয়ে দেখে কোনো দাগের অতিরিক্ত অংশ হস্তান্তর হচ্ছে কি না তা নিশ্চিত করে।",
        "en": "JomiGuard serves as an analytical bridge between Sub-Registry sale records and AC Land e-mutation ledgers. As transactions occur, it matches plot numbers, NIDs, and decimals pairwise to catch discrepancies before titles become clouded."
    },
    "faq_q3": {
        "bn": "ব্যাংক এবং আর্থিক প্রতিষ্ঠান কীভাবে জমিগার্ড থেকে উপকৃত হতে পারে?",
        "en": "How do banks and financial institutions benefit from JomiGuard?"
    },
    "faq_a3": {
        "bn": "ব্যাংকগুলো ঋণ প্রদানের সময় প্রস্তাবিত জমির দাগ ও খতিয়ান নম্বর জমিগার্ডে সার্চ করে মুহূর্তেই দেখতে পারে উক্ত দাগের জমি অন্য কোনো ব্যাংকে বন্ধক বা পূর্বে বিক্রয় হয়ে গেছে কি না। এর ফলে মর্টগেজ ফ্রড শতভাগ প্রতিরোধ করা সম্ভব হয়।",
        "en": "Banks verifying loan collateral can instantly inspect the plot's full timeline, checking whether the land was previously encumbered, sold, or subject to conflicting title claims."
    },
    "faq_q4": {
        "bn": "এনআইডি ও ব্যক্তিগত তথ্যের নিরাপত্তা কীভাবে নিশ্চিত করা হয়?",
        "en": "How is privacy and sensitive NID information safeguarded?"
    },
    "faq_a4": {
        "bn": "জমিগার্ড জাতীয় পরিচয়পত্র এবং দলিল তথ্যের সর্বোচ্চ এনক্রিপশন ও গোপনীয়তা নিশ্চিত করে। সিস্টেমে কেবল অনুমোদিত প্রাতিষ্ঠানিক ব্যবহারকারীগণ অডিট ও ভেরিফিকেশন কাজের প্রয়োজনে তথ্য অ্যাক্সেস করতে পারেন।",
        "en": "JomiGuard enforces enterprise-grade security controls. Sensitive identifiers are accessed exclusively by authorized institutional officers during verification workflows."
    },
    "faq_q5": {
        "bn": "ভুলবশত অ্যালার্ট (False Positive) আসলে তা সমাধানের উপায় কী?",
        "en": "What happens if an alert is triggered due to a legitimate transfer?"
    },
    "faq_a5": {
        "bn": "প্রতিটি অ্যালার্টের সাথে একটি প্রাতিষ্ঠানিক ট্রায়াজ সিস্টেম রয়েছে। পর্যালোচনা কর্মকর্তা নথিপত্র পরীক্ষা করে অ্যালার্টের স্ট্যাটাস 'বৈধ ব্যাখ্যা প্রাপ্ত' (Marked Legitimate) হিসেবে মার্ক করতে পারেন এবং সাথে সাথে অফিসিয়াল নোট ও কারণ লিপিবদ্ধ করতে পারেন।",
        "en": "Every alert features a formal triage workflow. Reviewing officers can mark alerts as 'Marked Legitimate' and record verifiable explanations (e.g., family partition deeds or court settlement decrees)."
    },

    # -------------------------------------------------------------------------
    # LANDING PAGE: CTA BANNER
    # -------------------------------------------------------------------------
    "cta_banner_title": {
        "bn": "আপনার প্রতিষ্ঠানের ভূমি স্বত্ব যাচাই এখনই সুরক্ষিত করুন",
        "en": "Secure Your Institutional Land Risk Today"
    },
    "cta_banner_subtitle": {
        "bn": "সাব-রেজিস্ট্রি, ব্যাংক মর্টগেজ কিংবা নাগরিক জমি যাচাই—জমিগার্ডের সাথে শুরু করুন নির্ভুল ডিজিটাল স্ক্রিনিং।",
        "en": "Empower registry officers, bank credit auditors, and property buyers with zero-latency deterministic screening."
    },
    "cta_banner_btn": {
        "bn": "🚀 জমিগার্ডে প্রবেশ করুন (Launch App)",
        "en": "🚀 Launch JomiGuard App"
    },
    "footer_credits": {
        "bn": "জমিগার্ড • বাংলাদেশ ভূমি রেকর্ড ও স্বত্ব সুরক্ষা প্রযুক্তি • সর্বস্বত্ব সংরক্ষিত",
        "en": "JomiGuard • Bangladesh Land Record & Title Protection Technology • All Rights Reserved"
    },

    # -------------------------------------------------------------------------
    # MAIN APP: NAVIGATION & SIDEBAR
    # -------------------------------------------------------------------------
    "sidebar_brand": {
        "bn": "🛡️ জমিগার্ড",
        "en": "🛡️ JomiGuard"
    },
    "sidebar_tagline": {
        "bn": "ভূমি স্বত্ব ও দ্বৈত বিক্রয় প্রতিরোধ প্ল্যাটফর্ম",
        "en": "Land Fraud & Double-Selling Alert System"
    },
    "sidebar_sub": {
        "bn": "রুল-ভিত্তিক অসঙ্গতি শনাক্তকরণ ও ব্যাখ্যামূলক স্ক্রিনিং",
        "en": "Rule-based anomaly detection & explainable risk screening"
    },
    "nav_tab_dashboard": {
        "bn": "📊 ড্যাশবোর্ড ওভারভিউ",
        "en": "📊 Dashboard Overview"
    },
    "nav_tab_alerts": {
        "bn": "🚨 সতর্কতা ও ঝুঁকি অনুসন্ধান",
        "en": "🚨 Alerts & Risk Investigation"
    },
    "nav_tab_plots": {
        "bn": "🔍 দাগের ইতিহাস ও টাইমলাইন",
        "en": "🔍 Searchable Plot History"
    },
    "nav_tab_sandbox": {
        "bn": "🧪 ইন্টারঅ্যাকটিভ ডেমো ও স্যান্ডবক্স",
        "en": "🧪 Interactive Demo & Sandbox"
    },
    "nav_tab_reports": {
        "bn": "📑 ডাউনলোডযোগ্য অডিট রিপোর্ট",
        "en": "📑 Downloadable Reports"
    },
    "sidebar_quick_actions": {
        "bn": "⚙️ দ্রুত কার্যক্রম (Quick Actions)",
        "en": "⚙️ Quick Actions"
    },
    "btn_rescan": {
        "bn": "🔄 পুনরায় অসঙ্গতি স্ক্যান করুন",
        "en": "🔄 Re-run Anomaly Scan"
    },
    "btn_reset_db": {
        "bn": "🔁 বেঞ্চমার্ক ডেটা রিসেট করুন",
        "en": "🔁 Reset Benchmark Data"
    },
    "rescan_success": {
        "bn": "স্ক্যান সম্পন্ন হয়েছে! {count}টি সম্ভাব্য অসঙ্গতি চিহ্নিত করা হয়েছে।",
        "en": "Scan complete! {count} inconsistencies flagged."
    },
    "reset_success": {
        "bn": "ডাটাবেজ মূল বেঞ্চমার্ক ডেটায় সফলভাবে রিসেট করা হয়েছে।",
        "en": "Database reset to original clean benchmark seed."
    },
    "sidebar_theme_label": {
        "bn": "🎨 ডিসপ্লে থিম",
        "en": "🎨 Display Theme"
    },
    "sidebar_engine_caption": {
        "bn": "জমিগার্ড • সক্রিয় ডেটাবেজ ইঞ্জিন (SQLite)",
        "en": "JomiGuard • Active Database Engine (SQLite)"
    },

    # -------------------------------------------------------------------------
    # MAIN APP: VIEW 1 - DASHBOARD OVERVIEW
    # -------------------------------------------------------------------------
    "dash_title": {
        "bn": "🛡️ জমিগার্ড প্রাতিষ্ঠানিক ড্যাশবোর্ড ও নিরীক্ষা ওভারভিউ",
        "en": "🛡️ JomiGuard Operational Overview"
    },
    "dash_sub": {
        "bn": "সাব-রেজিস্ট্রি দলিল, নামজারি খতিয়ান ও দাগের পূর্ণাঙ্গ অখণ্ডতা স্ক্রিনিং",
        "en": "Automated screening of deed registrations, land mutations, and parcel integrity"
    },
    "kpi_total_plots": {
        "bn": "মোট নিরীক্ষিত দাগ (প্লট)",
        "en": "Total Plots Screened"
    },
    "kpi_total_plots_foot": {
        "bn": "সার্ভে খতিয়ান অনুযায়ী দাগ",
        "en": "Parcels under integrity review"
    },
    "kpi_total_deeds": {
        "bn": "নিবন্ধিত সাব-কবলা দলিল",
        "en": "Registered Deeds"
    },
    "kpi_total_deeds_foot": {
        "bn": "সাব-রেজিস্ট্রি রেকর্ড",
        "en": "Sub-Registry sale records"
    },
    "kpi_total_mutations": {
        "bn": "অনুমোদিত ই-নামজারি কেস",
        "en": "Approved Mutations"
    },
    "kpi_total_mutations_foot": {
        "bn": "এসি ল্যান্ড অফিসের নামজারি",
        "en": "AC Land revenue records"
    },
    "kpi_flagged_alerts": {
        "bn": "চিহ্নিত অসঙ্গতি (অ্যালার্ট)",
        "en": "Flagged Inconsistencies"
    },
    "kpi_flagged_alerts_foot": {
        "bn": "জরুরি পর্যালোচনা আবশ্যক ({crit}টি ক্রুশিয়াল)",
        "en": "Requires human review ({crit} critical)"
    },
    "dash_charts_title": {
        "bn": "📈 বিশ্লেষণ ও ঝুঁকি বিন্যাস",
        "en": "📈 Analytics & Risk Distribution"
    },
    "chart_severity_title": {
        "bn": "ঝুঁকির গুরুত্ব স্তর অনুযায়ী অ্যালার্ট (Severity)",
        "en": "Alerts by Severity Level"
    },
    "chart_rules_title": {
        "bn": "চিহ্নিত রুল অনুযায়ী অসঙ্গতি বিন্যাস (Rule Distribution)",
        "en": "Inconsistencies by Triggered Rule"
    },
    "chart_mouza_title": {
        "bn": "মৌজাভিত্তিক দাগ ও দলিলের সংখ্যা",
        "en": "Parcels and Deeds by Mouza"
    },
    "dash_recent_alerts_title": {
        "bn": "🚨 তাৎক্ষণিক পর্যালোচনার জন্য সাম্প্রতিক অ্যালার্টসমূহ",
        "en": "🚨 Recent Alerts Requiring Review"
    },

    # -------------------------------------------------------------------------
    # MAIN APP: VIEW 2 - ALERTS & RISK INVESTIGATION
    # -------------------------------------------------------------------------
    "alerts_view_title": {
        "bn": "🚨 জমির রেকর্ড অসঙ্গতি ও ঝুঁকি অনুসন্ধান",
        "en": "🚨 Alerts & Risk Investigation"
    },
    "alerts_view_sub": {
        "bn": "রুল-ভিত্তিক দ্বিমুখী তথ্য পর্যালোচনা, প্রমাণ তুলনা এবং প্রাতিষ্ঠানিক ট্রায়াজ",
        "en": "Bilateral record review, side-by-side evidence diffs, and institutional triage"
    },
    "filter_severity": {
        "bn": "ঝুঁকির মাত্রা (Severity)",
        "en": "Severity Level"
    },
    "filter_rule": {
        "bn": "রুল বা অসঙ্গতির ধরন",
        "en": "Rule / Anomaly Type"
    },
    "filter_status": {
        "bn": "ট্রায়াজ স্ট্যাটাস",
        "en": "Triage Status"
    },
    "filter_plot": {
        "bn": "নির্দিষ্ট দাগ (Plot ID)",
        "en": "Target Plot ID"
    },
    "all_option": {
        "bn": "সকল (All)",
        "en": "All"
    },
    "search_alerts_placeholder": {
        "bn": "অ্যালার্ট আইডি, দাগ নম্বর বা বিবরণ দিয়ে খুঁজুন...",
        "en": "Search by Alert ID, Plot ID, or keyword..."
    },
    "evidence_diff_title": {
        "bn": "দ্বিমুখী প্রমাণ তুলনা (Side-by-Side Evidence Diff)",
        "en": "Side-by-Side Evidence Diff"
    },
    "record_a_label": {
        "bn": "নথি ক (প্রথম রেকর্ড / সাব-রেজিস্ট্রি দলিল)",
        "en": "Record A (Prior Deed / Sub-Registry Record)"
    },
    "record_b_label": {
        "bn": "নথি খ (দ্বিতীয় রেকর্ড / নামজারি খতিয়ান)",
        "en": "Record B (Conflicting Deed / Mutation Record)"
    },
    "trigger_data_title": {
        "bn": "অসঙ্গতির মূল সূচকসমূহ (Trigger Indicators)",
        "en": "Trigger Indicators"
    },
    "triage_box_title": {
        "bn": "প্রাতিষ্ঠানিক ট্রায়াজ ও পর্যালোচনা সিদ্ধান্ত",
        "en": "Institutional Triage & Review Decision"
    },
    "current_status": {
        "bn": "বর্তমান স্ট্যাটাস:",
        "en": "Current Status:"
    },
    "btn_update_triage": {
        "bn": "সিদ্ধান্ত সংরক্ষণ করুন",
        "en": "Update Triage Decision"
    },
    "reviewer_notes_label": {
        "bn": "কর্মকর্তার পর্যালোচনা ও সন্তোষজনক ব্যাখ্যার নোট",
        "en": "Reviewer Notes / Verified Legal Explanation"
    },
    "triage_updated_msg": {
        "bn": "অ্যালার্টের ট্রায়াজ স্ট্যাটাস সফলভাবে আপডেট করা হয়েছে।",
        "en": "Triage decision successfully recorded."
    },
    "no_alerts_found": {
        "bn": "নির্বাচিত ফিল্টারে কোনো অসঙ্গতি বা অ্যালার্ট পাওয়া যায়নি।",
        "en": "No alerts found matching the selected filters."
    },

    # -------------------------------------------------------------------------
    # MAIN APP: VIEW 3 - PLOT HISTORY & TIMELINE
    # -------------------------------------------------------------------------
    "plot_view_title": {
        "bn": "🔍 দাগের ইতিহাস, ধারণক্ষমতা ও ক্রমানুসারিক টাইমলাইন",
        "en": "🔍 Searchable Plot History & Timeline"
    },
    "plot_view_sub": {
        "bn": "নির্দিষ্ট দাগের সার্বিক তথ্য, ধারণক্ষমতা অতিরিক্ত বিক্রয় অ্যানিমেশন এবং সকল দলিলের শৃঙ্খল",
        "en": "Comprehensive parcel dossier, capacity overflow tracker, and complete ownership timeline"
    },
    "select_plot_label": {
        "bn": "অনুসন্ধানের জন্য দাগ নির্বাচন করুন:",
        "en": "Select Target Plot for Review:"
    },
    "plot_meta_mouza": {
        "bn": "মৌজা ও জেএল:",
        "en": "Mouza & JL:"
    },
    "plot_meta_khatian": {
        "bn": "মূল খতিয়ান:",
        "en": "Survey Khatian:"
    },
    "plot_meta_dag": {
        "bn": "দাগ নম্বর:",
        "en": "Dag No:"
    },
    "plot_meta_area": {
        "bn": "দাগের মোট ক্ষেত্রফল:",
        "en": "Total Surveyed Area:"
    },
    "plot_meta_owner": {
        "bn": "রেকর্ডিয় আদি মালিক:",
        "en": "Initial Recorded Owner:"
    },
    "plot_meta_type": {
        "bn": "জমির শ্রেণি:",
        "en": "Land Classification:"
    },
    "capacity_overflow_title": {
        "bn": "📊 দাগের ক্ষেত্রফল ও বিক্রয় ধারণক্ষমতা মিটার",
        "en": "📊 Plot Capacity & Area Allocation Meter"
    },
    "capacity_normal_label": {
        "bn": "মোট বিক্রিত: {sold} / {total} শতাংশ ({pct}%) — ধারণক্ষমতার মধ্যে রয়েছে",
        "en": "Transferred: {sold} / {total} decimals ({pct}%) — Within Capacity"
    },
    "capacity_overflow_label": {
        "bn": "⚠️ ধারণক্ষমতা অতিক্রান্ত: +{excess} শতাংশ অতিরিক্ত বিক্রয় হয়েছে!",
        "en": "⚠️ OVER CAPACITY: +{excess} decimals sold beyond plot size!"
    },
    "timeline_section_title": {
        "bn": "⏳ দাগের ক্রমানুসারিক লেনদেন ইতিহাস (Chronological Timeline)",
        "en": "⏳ Chronological Transaction Timeline"
    },
    "timeline_chart_title": {
        "bn": "লেনদেন ও নামজারির ইন্টারঅ্যাকটিভ টাইমলাইন",
        "en": "Interactive Transfer & Mutation Timeline"
    },
    "table_deeds_title": {
        "bn": "📜 দাগে সম্পাদনকৃত সকল সাব-কবলা দলিল",
        "en": "📜 Registered Deeds on this Plot"
    },
    "table_mutations_title": {
        "bn": "📑 দাগের অনুমোদিত নামজারি খতিয়ানসমূহ",
        "en": "📑 Approved Mutations on this Plot"
    },
    "table_alerts_title": {
        "bn": "🚨 দাগে সক্রিয় অসঙ্গতি ও অ্যালার্টসমূহ",
        "en": "🚨 Active Alerts on this Plot"
    },

    # -------------------------------------------------------------------------
    # MAIN APP: VIEW 4 - INTERACTIVE DEMO & SANDBOX
    # -------------------------------------------------------------------------
    "sandbox_title": {
        "bn": "🧪 ইন্টারঅ্যাকটিভ অ্যানোমালি ইনজেকশন স্যান্ডবক্স",
        "en": "🧪 Interactive Anomaly Injection Sandbox"
    },
    "sandbox_sub": {
        "bn": "লাইভ ডেমো: ডাটাবেজে ইচ্ছাকৃত অসঙ্গতি যুক্ত করুন এবং রুল ইঞ্জিনের তাৎক্ষণিক শনাক্তকরণ পরীক্ষা করুন",
        "en": "Live demonstration: Inject conflicting land sales or record mismatches and observe instant detection"
    },
    "sandbox_instructions": {
        "bn": "💡 ডেমো নির্দেশিকা: নিচের যেকোনো একটি সিনারিও নির্বাচন করে একটি কাল্পনিক বা অসঙ্গতিপূর্ণ রেকর্ড ইনজেক্ট করুন। রুল ইঞ্জিন মুহূর্তেই (<৫০ মি.সে.) ত্রুটি শনাক্ত করবে এবং লাল রঙের পালস অ্যানিমেশনসহ অ্যালার্ট তৈরি করবে।",
        "en": "💡 Demonstration Workflow: Choose a scenario below to introduce a conflicting sale or record mismatch. The engine will instantly run anomaly detection, extract explainable trigger indicators, and display the resulting alert."
    },
    "tab_inj_duplicate": {
        "bn": "১. দ্বৈত বিক্রয় ইনজেকশন (Double Sale)",
        "en": "1. Duplicate Sale Injection"
    },
    "tab_inj_area": {
        "bn": "২. আয়তন বৃদ্ধি ইনজেকশন (Area Inflation)",
        "en": "2. Area Inflation Injection"
    },
    "tab_inj_identity": {
        "bn": "৩. ভুয়া আবেদনকারী (Identity Mismatch)",
        "en": "3. Identity Impostor Injection"
    },
    "tab_inj_paradox": {
        "bn": "৪. কালানুক্রমিক প্যারাডক্স (Temporal Paradox)",
        "en": "4. Chronological Paradox Injection"
    },
    "btn_inject_dup": {
        "bn": "🚨 দ্বৈত বিক্রয় দলিল ইনজেক্ট করুন",
        "en": "🚨 Inject Duplicate Sale Now"
    },
    "btn_inject_area": {
        "bn": "🚨 নামজারিতে অতিরিক্ত আয়তন ইনজেক্ট করুন",
        "en": "🚨 Inject Area Inflation Now"
    },
    "btn_inject_id": {
        "bn": "🚨 ভুয়া আবেদনকারী এনআইডি ইনজেক্ট করুন",
        "en": "🚨 Inject Identity Mismatch Now"
    },
    "btn_inject_time": {
        "bn": "🚨 পূর্ববর্তী তারিখের নামজারি ইনজেক্ট করুন",
        "en": "🚨 Inject Chronological Paradox Now"
    },

    # -------------------------------------------------------------------------
    # MAIN APP: VIEW 5 - DOWNLOADABLE REPORTS
    # -------------------------------------------------------------------------
    "reports_title": {
        "bn": "📑 প্রাতিষ্ঠানিক অডিট ও ঝুঁকি পরিদর্শন রিপোর্ট",
        "en": "📑 Formal Audit & Investigation Reports"
    },
    "reports_sub": {
        "bn": "দাপ্তরিক ব্যবহারের জন্য সিএসভি ও মার্কডাউন ফরম্যাটে পূর্ণাঙ্গ জমি তদন্ত প্রতিবেদন ডাউনলোড করুন",
        "en": "Export structured anomaly records and generate formal printable land inspection reports"
    },
    "card_csv_title": {
        "bn": "📥 অ্যালার্ট লেজার এক্সপোর্ট (CSV)",
        "en": "📥 Export Alerts Ledger (CSV)"
    },
    "card_csv_desc": {
        "bn": "সকল চিহ্নিত অ্যালার্ট, সেভিয়ারিটি ও ট্রায়াজ স্ট্যাটাস স্প্রেডশিটে বিশ্লেষণের উপযোগী সিএসভি ফরম্যাট।",
        "en": "Tabular export of all flagged alerts, severity scores, and triage notes."
    },
    "btn_download_csv": {
        "bn": "অ্যালার্ট লেজার ডাউনলোড করুন (CSV)",
        "en": "Download Alerts Ledger (CSV)"
    },
    "card_md_title": {
        "bn": "📄 পূর্ণাঙ্গ পরিদর্শন প্রতিবেদন (Markdown)",
        "en": "📄 Export Investigation Report (Markdown)"
    },
    "card_md_desc": {
        "bn": "নির্বাহী সারসংক্ষেপ, বিস্তারিত কেইস ডসিয়ার এবং অফিসিয়াল সাইন-অফ সহ পূর্ণাঙ্গ প্রাতিষ্ঠানিক রিপোর্ট।",
        "en": "Comprehensive formal inspection report including executive summary, case dossiers, and officer sign-off."
    },
    "btn_download_md": {
        "bn": "ফরমাল রিপোর্ট ডাউনলোড করুন (.md)",
        "en": "Download Formal Report (.md)"
    },
    "report_preview_title": {
        "bn": "👁️ প্রতিবেদনের নমুনা প্রিভিউ",
        "en": "👁️ Report Preview"
    },
}


def t(key: str, lang: str = "bn", **kwargs) -> str:
    """Lookup a localized string by key and language, formatting if kwargs are passed."""
    entry = TRANSLATIONS.get(key)
    if not entry:
        return key
    text = entry.get(lang) or entry.get("en") or key
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text
