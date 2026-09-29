"""Four sample questions (2 Yoga, 2 IKS), one in each multi-part NTA format.

These are PYQ-pattern MODEL questions: written in NTA's formats and checked
against the primary texts, but not reproductions of a specific paper. They
carry no exam year and are never counted as exam appearances. Their
trend_analysis therefore describes how the micro-topic is framed and what
the examiner targets, without inventing session counts. Real papers go in
data/questions/*.json (see the README there), and the app then counts
frequencies from them exactly.
"""

from inspect import cleandoc as text

SAMPLE_QUESTIONS: list[dict] = [
    {
        "id": "YOGA-SAMPLE-01",
        "subject": "yoga",
        "exam_year": None,
        "exam_cycle": None,
        "source": {
            "type": "model",
            "note": "Written in NTA's Match List I with List II format. Not a verbatim paper question.",
        },
        "question_type": "match",
        "question_text": "Match List I (kleśa) with List II (how the Yoga Sūtra defines it).",
        "lists": {
            "list_i": {"title": "List I: Kleśa", "items": ["Avidyā", "Asmitā", "Rāga", "Abhiniveśa"]},
            "list_ii": {
                "title": "List II: Definition",
                "items": [
                    "Clinging to life, flowing by its own momentum, present even in the learned",
                    "Taking the impermanent, impure, painful and non-self to be permanent, pure, pleasant and the self",
                    "That which follows in the wake of pleasure",
                    "The power of the seer and the power of seeing appearing as a single self",
                ],
            },
        },
        "prompt": "Choose the correct answer from the options given below:",
        "options": [
            "A-IV, B-II, C-III, D-I",
            "A-II, B-III, C-IV, D-I",
            "A-II, B-IV, C-III, D-I",
            "A-I, B-IV, C-II, D-III",
        ],
        "correct_answer": 3,
        "detailed_explanation": text("""
            **Answer: (3) A-II, B-IV, C-III, D-I.**

            Patañjali names five kleśas in YS 2.3 (avidyā, asmitā, rāga, dveṣa and abhiniveśa) and then defines each in turn:

            - **Avidyā (2.5):** *anityāśuci-duḥkhānātmasu nitya-śuci-sukhātma-khyātiḥ*. Taking the impermanent, impure, painful and non-self to be permanent, pure, pleasant and the self. → II
            - **Asmitā (2.6):** *dṛg-darśana-śaktyor ekātmatā iva*. The power of the seer and the power of seeing (the instrument, buddhi) appearing as one. → IV
            - **Rāga (2.7):** *sukhānuśayī*. Attachment that follows in the wake of pleasure. → III
            - **Dveṣa (2.8):** *duḥkhānuśayī*. Aversion that follows pain. It is left out of List I here, a favourite way to build distractors.
            - **Abhiniveśa (2.9):** *svarasavāhī viduṣo 'pi …* The will to live that runs on its own momentum and grips even the learned. → I

            **Why the other options fail.** (1) swaps avidyā and asmitā. This is the classic confusion, since both describe a misidentification: avidyā is the general error, asmitā the specific fusion of seer and instrument. (2) gives asmitā the definition of rāga. (4) turns avidyā into clinging to life, which is abhiniveśa.

            **Context the examiner builds on.** YS 2.4 makes avidyā the field (kṣetra) of the other four, which may be dormant (prasupta), attenuated (tanu), interrupted (vicchinna) or active (udāra). Removal is graded: kriyā-yoga attenuates the kleśas (2.2), their subtle forms are dissolved by pratiprasava, a return into their cause (2.10), and their active modifications are removed by dhyāna (2.11). The kleśas are the root of the store of karma, the karmāśaya (2.12).
        """),
        "macro_unit": "Yoga Unit 4: Patanjala Yoga Sutra",
        "micro_topic": "Kleshas and their removal",
        "trend_analysis": text("""
            **Pattern.** The kleśa block (YS 2.2–2.13) is a closed, countable set: five kleśas, four states and three methods of removal. That is exactly the raw material of NTA's Match-the-List and Sequence formats, so expect it to be tested through those formats rather than as a one-line definition.

            **What the examiner targets.**

            - Kleśa ↔ defining sūtra (2.5–2.9), usually as a four-pair match with one kleśa left out
            - The order of the five in 2.3, as a sequence item
            - The four states in 2.4, often as "which is NOT a state of kleśa", with citta-bhūmis such as kṣipta and mūḍha as distractors
            - Which method removes what: kriyā-yoga attenuates (2.2), pratiprasava removes the subtle kleśas (2.10), dhyāna removes their vṛttis (2.11)
            - Vyāsa's commentary on 2.4: the burnt-seed (dagdha-bīja) state of kleśas in the accomplished yogī

            **Traps.** *sukhānuśayī* (rāga) vs *duḥkhānuśayī* (dveṣa). Asmitā as a kleśa (2.6) vs asmitā in samprajñāta samādhi (1.17). The four states of kleśa vs the five citta-bhūmis.

            **Prep move.** Learn 2.3–2.11 as one run with the Sanskrit key word of each sūtra. Most variants of this question can be answered from those words alone.
        """),
        "references": ["Yoga Sūtra 2.2–2.13 with Vyāsa's bhāṣya"],
        "source_ids": ["woods-1914-yoga-system", "vivekananda-1896-raja-yoga"],
    },
    {
        "id": "YOGA-SAMPLE-02",
        "subject": "yoga",
        "exam_year": None,
        "exam_cycle": None,
        "source": {
            "type": "model",
            "note": "Written in NTA's sequence-arrangement format. Not a verbatim paper question.",
        },
        "question_type": "sequence",
        "question_text": "Arrange the following ṣaṭkarmas in the order in which the Haṭha Pradīpikā lists them.",
        "items": ["Neti", "Dhauti", "Trāṭaka", "Nauli", "Basti"],
        "prompt": "Choose the correct answer from the options given below:",
        "options": ["B, E, A, D, C", "B, E, A, C, D", "A, B, E, C, D", "E, B, A, C, D"],
        "correct_answer": 2,
        "detailed_explanation": text("""
            **Answer: (2) B, E, A, C, D:** dhauti, basti, neti, trāṭaka, nauli. Kapālabhāti, the sixth karma, is not in the list.

            Haṭha Pradīpikā 2.22 reads: *dhautir bastis tathā netis trāṭakaṃ naulikaṃ tathā | kapālabhātiś caitāni ṣaṭkarmāṇi pracakṣate*.

            **Option (1) is the trap.** It is the Gheraṇḍa Saṃhitā order (GS 1.12: dhauti, basti, neti, laulikī, trāṭaka, kapālabhāti), where nauli, under the name laulikī, comes before trāṭaka. Options (3) and (4) break the dhauti → basti opening that both texts share.

            **What each karma is in HP 2.21–2.35:**

            - **Dhauti:** slowly swallowing a moist cloth four fingers wide and fifteen hastas (cubits) long, then drawing it out (2.24)
            - **Basti:** sitting navel-deep in water in utkaṭāsana with a tube in the anus, drawing water in and expelling it (2.26)
            - **Neti:** passing a smooth thread one span (vitasti) long into the nose and out through the mouth (2.29)
            - **Trāṭaka:** gazing without blinking at a small point until tears flow (2.31)
            - **Nauli:** rotating the abdomen to right and left with the shoulders bent forward (2.33)
            - **Kapālabhāti:** rapid exhalation and inhalation like a blacksmith's bellows (2.35)

            **Who should do them.** HP 2.21 prescribes the ṣaṭkarmas for someone with excess fat or phlegm (*medaḥ-śleṣmādhika*). Others, whose doṣas are balanced, need not do them. HP 2.37 records that some teachers hold prāṇāyāma alone to be enough, and 2.38 adds gaja-karaṇī as a related practice. Gheraṇḍa, by contrast, makes ṣaṭkarma the first limb (śodhana, purification) of his seven-limbed yoga.

            Verse numbers follow the common four-chapter edition of the Haṭha Pradīpikā; some editions are off by one or two.
        """),
        "macro_unit": "Yoga Unit 5: Hatha Yoga Texts",
        "micro_topic": "Shatkarma in Hatha Pradipika and Gheranda Samhita",
        "trend_analysis": text("""
            **Pattern.** Ṣaṭkarma sits where Unit 5 (Haṭha texts) meets Unit 10 (practical yoga), so it can be asked textually (order, verse, definition) or practically (technique, indication, contraindication). The textual form separates candidates, because the Haṭha Pradīpikā and the Gheraṇḍa Saṃhitā differ in small, testable details.

            **What the examiner targets.**

            - The listing order in HP 2.22 vs GS 1.12, as sequence items and "which text lists…" questions
            - Names that differ between texts: HP's nauli is GS's laulikī
            - The sub-types in GS: four main kinds of dhauti (antar-dhauti, danta-dhauti, hṛd-dhauti, mūla-śodhana), two of basti (jala and śuṣka), three of kapālabhāti (vātakrama, vyutkrama, śītkrama)
            - The indication in HP 2.21: only for excess of fat or phlegm
            - Where ṣaṭkarma sits in each scheme: inside the prāṇāyāma chapter in HP, the first of seven limbs in GS

            **Traps.** The GS order moves nauli (laulikī) ahead of trāṭaka. Gaja-karaṇī is described but is not one of the six. HP 2.37 reports the view that prāṇāyāma alone can purify.

            **Prep move.** Learn the two listing verses side by side. The only difference in order is where nauli and trāṭaka fall.
        """),
        "references": ["Haṭha Pradīpikā 2.21–2.38", "Gheraṇḍa Saṃhitā 1.12 onwards"],
        "source_ids": ["sinh-1914-hatha-yoga-pradipika", "vasu-1895-gheranda-samhita"],
    },
    {
        "id": "IKS-SAMPLE-01",
        "subject": "iks",
        "exam_year": None,
        "exam_cycle": None,
        "source": {
            "type": "model",
            "note": "Written in NTA's multiple-statement format. Not a verbatim paper question.",
        },
        "question_type": "statements",
        "question_text": "Consider the following statements about the Kerala school of astronomy and mathematics.",
        "items": [
            "Mādhava of Saṅgamagrāma is credited with the series π/4 = 1 − 1/3 + 1/5 − 1/7 + …, now often called the Mādhava–Leibniz series.",
            "Yuktibhāṣā, which sets out proofs (upapatti) of the Kerala series results, was written in Malayalam by Jyeṣṭhadeva.",
            "Tantrasaṅgraha (c. 1500 CE) was composed by Nīlakaṇṭha Somayājī.",
            "Mādhava's infinite series are known chiefly from his own surviving treatises, such as the Veṇvāroha.",
        ],
        "prompt": "Choose the correct answer from the options given below:",
        "options": ["A and B only", "B, C and D only", "A, B, C and D", "A, B and C only"],
        "correct_answer": 4,
        "detailed_explanation": text("""
            **Answer: (4) A, B and C only.**

            - **A is correct.** The π/4 series, and the arctangent and sine–cosine series behind it, are attributed to Mādhava (c. 1340–1425) of Saṅgamagrāma, near present-day Irinjalakuda. In Europe, Newton (1660s), Gregory (1671) and Leibniz (1673–74) reached the same series independently. Mādhava also gave correction terms that make the slowly converging π series usable, and a value of π correct to 11 decimal places (3.14159265359).
            - **B is correct.** Jyeṣṭhadeva's Yuktibhāṣā (c. 1530) is in Malayalam, unusual for a technical work of the period. It is valued because it gives derivations (upapatti), not just rules.
            - **C is correct.** Nīlakaṇṭha Somayājī (b. 1444) completed Tantrasaṅgraha around 1500 CE. There, and in his commentary on the Āryabhaṭīya, he revised the planetary model for Mercury and Venus.
            - **D is incorrect.** Mādhava's surviving works (the Veṇvāroha, for example, computes the Moon's true position) do not contain the series. They reach us through attributions in later texts: Nīlakaṇṭha, Jyeṣṭhadeva's Yuktibhāṣā, and Śaṅkara Vāriyar's commentaries Yuktidīpikā (on Tantrasaṅgraha) and Kriyākramakarī (on Bhāskara II's Līlāvatī).

            **The lineage worth memorising:** Mādhava → Parameśvara (Dṛggaṇita, 1431) → his son Dāmodara → Nīlakaṇṭha Somayājī and Jyeṣṭhadeva → Śaṅkara Vāriyar and Acyuta Piṣāraṭi.
        """),
        "macro_unit": "IKS Unit 6: Mathematics",
        "micro_topic": "Kerala School of Mathematics",
        "trend_analysis": text("""
            **Pattern.** The Kerala school is the IKS mathematics topic richest in names, dates and texts, which makes it natural material for statement-based and match-type items: mathematician ↔ text, text ↔ language, result ↔ later European name.

            **What the examiner targets.**

            - Attribution: which series (π/4, arctangent, sine and cosine) goes with Mādhava, and the European names later attached to them (Gregory, Leibniz, Newton)
            - Texts ↔ authors: Tantrasaṅgraha (Nīlakaṇṭha), Yuktibhāṣā (Jyeṣṭhadeva, in Malayalam), Yuktidīpikā and Kriyākramakarī (Śaṅkara Vāriyar), Dṛggaṇita (Parameśvara)
            - The upapatti tradition, and why Yuktibhāṣā matters (proofs, not just rules)
            - The chronology of the lineage, as a sequence item
            - Transmission to Europe, which is a hypothesis and not a settled fact. A statement asserting proven transmission is usually the false one.

            **Traps.** Crediting Āryabhaṭa or Bhāskara II with the infinite series. Calling Yuktibhāṣā a Sanskrit work. Assuming Mādhava's own surviving texts preserve the series.

            **Prep move.** Build a four-column table (mathematician, dates, key text, key result) for the six names in the lineage.
        """),
        "references": [
            "K. V. Sarma, A History of the Kerala School of Hindu Astronomy (1972)",
            "Yuktibhāṣā, ed. and tr. K. V. Sarma et al. (2008)",
        ],
        "source_ids": ["whish-1834-quadrature", "datta-singh-hindu-mathematics"],
    },
    {
        "id": "IKS-SAMPLE-02",
        "subject": "iks",
        "exam_year": None,
        "exam_cycle": None,
        "source": {
            "type": "model",
            "note": "Written in NTA's Assertion–Reason format. Not a verbatim paper question.",
        },
        "question_type": "assertion_reason",
        "question_text": "Given below are two statements: one is labelled as Assertion (A) and the other is labelled as Reason (R).",
        "assertion": "Āryabhaṭa held that the daily westward motion of the stars across the sky is only apparent.",
        "reason": "In the Āryabhaṭīya, the Earth rotates on its axis from west to east.",
        "prompt": "In the light of the above statements, choose the correct answer from the options given below:",
        "options": [
            "Both (A) and (R) are true and (R) is the correct explanation of (A)",
            "Both (A) and (R) are true but (R) is NOT the correct explanation of (A)",
            "(A) is true but (R) is false",
            "(A) is false but (R) is true",
        ],
        "correct_answer": 1,
        "detailed_explanation": text("""
            **Answer: (1).** Both statements are true, and the Earth's eastward rotation is exactly why the stars appear to move westward.

            **The text.** The Āryabhaṭīya (499 CE) has 121 verses in four pādas: Gītikā (13), Gaṇita (33), Kālakriyā (25) and Gola (50). Golapāda 9 gives the boat simile: just as a man in a boat moving forward sees the stationary objects on the bank moving backward, so the stationary stars are seen moving due west at Laṅkā, on the equator.

            A line in the Gītikāpāda states it outright: *prāṇenaiti kalāṃ bhūḥ*, "the Earth moves one minute of arc in one prāṇa". One prāṇa is 4 sidereal seconds, so 21,600 prāṇas give 21,600 minutes of arc: one full turn in one sidereal day. Āryabhaṭa's yuga figures agree: 1,582,237,500 rotations of the Earth against 1,577,917,500 civil days in 4,320,000 years. The difference is exactly the number of years.

            **Why (2) is wrong.** (R) is not an unrelated true fact; it is the cause of what (A) describes. **Why (3) and (4) are wrong.** Both statements are faithful to the text.

            **Reception.** Varāhamihira and later Brahmagupta rejected the rotating Earth, and some later followers reworked the verses to fit a stationary Earth. Who proposed the idea and who opposed it is itself good exam material.
        """),
        "macro_unit": "IKS Unit 3: Astronomy",
        "micro_topic": "Aryabhata and the Earth's rotation",
        "trend_analysis": text("""
            **Pattern.** Āryabhaṭa is the anchor figure of the IKS astronomy unit, and the rotating Earth is his most distinctive thesis. That suits Assertion–Reason items: two true statements whose causal link has to be judged.

            **What the examiner targets.**

            - The structure of the Āryabhaṭīya: four pādas, 121 verses, and what each pāda covers
            - Earth's rotation, the boat simile (Golapāda 9) and the prāṇa–kalā correspondence
            - Eclipses explained by the shadows of the Earth and Moon rather than Rāhu, and the Moon shining by reflected sunlight
            - The alphabetic numeral notation of the Gītikāpāda, π ≈ 3.1416 (Gaṇitapāda 10) and the sine table
            - Reception: Varāhamihira, Brahmagupta and Lalla as critics; Bhāskara I as commentator

            **Traps.** A–R items where both statements are true but unrelated: read (R) as "because…" and ask whether it really answers "why (A)?". Also, Āryabhaṭa's rotating Earth is not heliocentrism; his model stays geocentric.

            **Prep move.** For every A–R item, restate it as "(A) because (R)" and check that it makes sense before choosing between options (1) and (2).
        """),
        "references": [
            "Āryabhaṭīya, Gītikāpāda and Golapāda 9",
            "K. S. Shukla and K. V. Sarma (eds.), Āryabhaṭīya of Āryabhaṭa (INSA, 1976)",
        ],
        "source_ids": ["clark-1930-aryabhatiya", "burgess-1860-surya-siddhanta"],
    },
]
