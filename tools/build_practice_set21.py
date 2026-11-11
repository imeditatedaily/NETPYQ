"""Practice set 21: Upanishad questions drawn from the user's own quiz sheets in Drive
(Yoga_Upanishad_Quiz, Taittereya_Upanishad_Quiz, Kath_Mundak_Prasna_Upanishad_Quiz).

The sheets give no items for many questions and several of their keys are wrong, so each question is written
in full here and every answer is checked against the Sanskrit on the Sanskrit Texts page (data/texts). Where a
sheet's key was wrong, the explanation says what the text actually reads.

    python tools/build_practice_set21.py
"""

from practice_builder import PracticeSet

U2 = "Yoga Unit 2: Yoga Texts I: Principal Upanishads, Bhagavad Gita and Yoga Vasishtha"
U3 = "Yoga Unit 3: Yoga Texts II: Yoga Upanishads"
TA, PR, MU, KA, KE, IS = ("Taittiriya Upanishad", "Prashna Upanishad", "Mundaka Upanishad", "Katha Upanishad",
                          "Kena Upanishad", "Isha Upanishad")
SV, YR, TB, YC = "Shvetashvatara Upanishad", "Yogaraja Upanishad", "Trishikhibrahmana Upanishad", "Yogachudamani Upanishad"

s = PracticeSet("YOGA-PRAC16", "Practice set 21 (Upanishads). Built from your own Upanishad quiz sheets, with every "
                "answer checked against the Sanskrit text; where a sheet's answer key was wrong, the corrected answer is used.")

# --- Yogaraja ---------------------------------------------------------------------------

s.mcq(U3, YR, "According to the Yogaraja Upanishad, yoga has four limbs. Which of these is NOT one of them?",
      ["Dharana", "Asana", "Pranasamrodha (restraint of breath)", "Samadhi"],
      "Mantra 2: *āsanaṃ prāṇasaṃrodho dhyānaṃ caiva samādhikaḥ* — posture, restraint of breath, meditation and "
      "samadhi. Dharana is not among them. (Restraint of breath is pranayama, so 'pranayama' is NOT the answer.)")

s.mcq(U3, YR, "In the Yogaraja Upanishad, what does the yogi do in the sixth chakra, the talu (palate) chakra?",
      ["Dissolves the mind in the void (shunya)", "Meditates on the hamsa as light", "Meditates on the pure light",
       "Meditates on the full shakti in the Purnagiri seat"],
      "Mantras 13–14: the talu chakra, the place of the uvula, is the way to the tenth door; *tatra śūnye layaṃ kṛtvā "
      "mukto bhavati niścitam* — dissolving the mind in the void there, one is surely freed. The hamsa is meditated on "
      "in the heart chakra (11), the pure light in the throat chakra (13), and the full shakti in the ninth, vyoma chakra (18).")

s.mcq(U3, YR, "How many petals does the vyoma chakra (the ninth chakra) have in the Yogaraja Upanishad?",
      ["16", "10", "12", "2"],
      "Mantra 17: *navamaṃ vyomacakraṃ syād aśraiḥ ṣoḍaśabhir yutam* — the ninth is the space chakra with sixteen petals.")

s.mcq(U3, YR, "'साध्यते मन्त्रयोगस्तु वत्सराजादिभिर्यथा' — this line is from which Upanishad?",
      ["Yogaraja", "Yogachudamani", "Yogakundali", "Shvetashvatara"],
      "Yogaraja Upanishad, mantra 4: mantra yoga was accomplished by Vatsaraja and others, laya yoga by Krishna "
      "Dvaipayana (Vyasa) and others.")

# --- Shvetashvatara ---------------------------------------------------------------------

s.statements(U3, SV, "According to the Shvetashvatara Upanishad (2.13), which of these are the first signs of progress in yoga?",
             ["Lightness of body", "Freedom from disease", "Clearness of complexion", "Visions of the gods", "Scanty urine and faeces"],
             ["(A), (B), (C) and (E) only", "(A), (B) and (D) only", "(B), (C), (D) and (E) only", "(A), (C) and (D) only"],
             "2.13: *laghutvam ārogyam alolupatvaṃ varṇaprasādaḥ svarasauṣṭhavaṃ ca, gandhaḥ śubho mūtrapurīṣam alpaṃ, "
             "yogapravṛttiṃ prathamāṃ vadanti* — lightness, health, steadiness (freedom from craving), clear complexion, "
             "a pleasant voice, a sweet smell and scanty excretions. Visions of gods are not in the list.")

s.sequence(U3, SV, "Arrange these forms that appear before the yogi in the order given by the Shvetashvatara Upanishad (2.11).",
           ["Mist (nihara)", "Wind (anila)", "Lightning (vidyut)", "Smoke (dhuma)", "Fire (anala)"],
           ["(A), (D), (B), (E), (C)", "(A), (D), (E), (B), (C)", "(A), (B), (D), (E), (C)", "(D), (A), (B), (E), (C)"],
           "2.11: *nīhāra-dhūmārkānilānalānāṃ khadyota-vidyut-sphaṭika-śaśīnām* — mist, smoke, sun, wind, fire, firefly, "
           "lightning, crystal, moon. So mist, smoke, wind, fire, lightning: (A), (D), (B), (E), (C).")

s.mcq(U3, SV, "'न तस्य रोगो न जरा न मृत्युः प्राप्तस्य योगाग्निमयं शरीरम्' (Shvetashvatara 2.12) — whose mastery gives this?",
      ["The five elements (earth, water, fire, air, space) arising as the qualities of yoga", "Hatha yoga",
       "The five tanmatras", "Ashtanga yoga"],
      "2.12: *pṛthivy-ap-tejo-'nila-khe samutthite pañcātmake yoga-guṇe pravṛtte* — when the fivefold quality of yoga "
      "made of earth, water, fire, air and space has arisen, there is no disease, old age or death for one who has a "
      "body made of the fire of yoga. The verse is about the five mahabhutas, not about hatha yoga.")

s.match(U3, SV, "Match the line with its place in the Shvetashvatara Upanishad.",
        ["शृण्वन्तु विश्वे अमृतस्य पुत्राः", "एको हि रुद्रो न द्वितीयाय तस्थुः", "समाने वृक्षे पुरुषो निमग्नः",
         "न तत्र सूर्यो भाति न चन्द्रतारकम्"],
        ["2.5", "3.2", "4.7", "6.14"],
        ["A-i, B-ii, C-iii, D-iv", "A-ii, B-i, C-iii, D-iv", "A-i, B-iii, C-ii, D-iv", "A-i, B-ii, C-iv, D-iii"],
        "*śṛṇvantu viśve amṛtasya putrāḥ* 2.5; *eko hi rudro na dvitīyāya tasthuḥ* 3.2; *samāne vṛkṣe puruṣo nimagnaḥ* "
        "4.7; *na tatra sūryo bhāti* 6.14 (the same verse is Katha 2.2.15 and Mundaka 2.2.10).")

# --- Trishikhibrahmana and Yogachudamani -------------------------------------------------

s.match(U3, TB, "Match the definition with what the Trishikhibrahmana Upanishad calls it.",
        ["बन्धनं मनसो नित्यं (in prescribed duties)", "यत्तु चित्तस्य सततमर्थे श्रेयसि बन्धनम्",
         "जगत्सर्वमिदं मिथ्याप्रतीतिः", "चित्तस्यान्तर्मुखीभावः"],
        ["Karma yoga", "Jnana yoga", "Pranasamyama (pranayama)", "Pratyahara"],
        ["A-i, B-ii, C-iii, D-iv", "A-ii, B-i, C-iii, D-iv", "A-i, B-ii, C-iv, D-iii", "A-iv, B-ii, C-iii, D-i"],
        "Mantra part 2.25–2.27: fixing the mind always on the prescribed duties is karma yoga; *yat tu cittasya satatam "
        "arthe śreyasi bandhanam, jñānayogaḥ sa vijñeyaḥ* — fixing the mind on the highest good is jnana yoga. 2.30: "
        "*jagat sarvam idaṃ mithyā-pratītiḥ prāṇa-saṃyamaḥ* — seeing the world as unreal is restraint of prana; *cittasya "
        "antarmukhī-bhāvaḥ pratyāhāraḥ* — turning the mind inward is pratyahara. (Some notes key the second line as "
        "raja yoga and the third as pratyahara; the text says otherwise.)")

s.statements(U3, TB, "Which of these asanas are described in the Trishikhibrahmana Upanishad?",
             ["Svastikasana", "Gomukhasana", "Virasana", "Yogasana", "Padmasana"],
             ["(A), (B), (C), (D) and (E)", "(A), (B) and (E) only", "(B), (C) and (D) only", "(A), (C), (D) and (E) only"],
             "2.34–2.40 describe svastika (2.35), gomukha (2.36), vira (2.37), yogasana (2.38: pressing the anus with the "
             "heels crossed over), padma (2.39) and baddhapadma (2.40), among others. All five are there.")

s.mcq(U3, TB, "In the Trishikhibrahmana Upanishad, which nadi runs down from the kanda to the big toes?",
      ["Kaushiki", "Alambusa", "Kuhu", "Yashasvini"],
      "2.74: *pādāṅguṣṭhāvadhiḥ kandād adhoyātā ca kauśikī* — the kaushiki goes down from the kanda to the big toes. "
      "So the kaushiki IS described in this Upanishad. Alambusa goes to the root of the anus (2.73).")

s.mcq(U3, YC, "'आसनेन रुजं हन्ति' — according to the Yogachudamani Upanishad, asana destroys disease. What does pranayama destroy?",
      ["Sin (pataka)", "Mental disturbance", "Ignorance", "Old age"],
      "Mantra 109: *āsanena rujaṃ hanti prāṇāyāmena pātakam, vikāraṃ mānasaṃ yogī pratyāhāreṇa muñcati* — asana "
      "destroys disease, pranayama destroys sin, and pratyahara frees the yogi from mental disturbance.")

s.mcq(U3, YC, "Which two asanas does the Yogachudamani Upanishad name at the start of its teaching (mantra 3)?",
      ["Siddhasana and kamalasana (padmasana)", "Siddhasana and bhadrasana", "Padmasana and simhasana",
       "Svastikasana and gomukhasana"],
      "Mantra 3: *ekaṃ siddhāsanaṃ proktaṃ dvitīyaṃ kamalāsanam* — the first is siddhasana, the second the lotus. "
      "The verse goes on: six chakras, sixteen supports, three lakshyas and five spaces.")

s.mcq(U3, YC, "In the Yogachudamani Upanishad's pranayama with Om (mantra 103), how many units is kumbhaka?",
      ["16", "12", "10", "64"],
      "Mantra 103: *pūrakaṃ dvādaśaṃ kuryāt kumbhakaṃ ṣoḍaśaṃ bhavet, recakaṃ daśa coṅkāraḥ* — inhalation 12, "
      "retention 16, exhalation 10 repetitions of Om.")

# --- Taittiriya -------------------------------------------------------------------------

s.match(U2, TA, "Match the vyahriti with what the Taittiriya Upanishad (1.5) identifies it with among the Vedas.",
        ["Bhuh", "Bhuvah", "Suvah", "Mahah"], ["Rik verses", "Saman chants", "Yajus formulas", "Brahman"],
        ["A-i, B-ii, C-iii, D-iv", "A-i, B-iii, C-ii, D-iv", "A-iii, B-ii, C-i, D-iv", "A-i, B-ii, C-iv, D-iii"],
        "1.5.2–3: *bhūr iti vā ṛcaḥ, bhuva iti sāmāni, suvar iti yajūṃṣi, maha iti brahma*. So the Samaveda goes with "
        "BHUVAH, not mahah — mahah is Brahman, by which all the Vedas are made great.")

s.mcq(U2, TA, "'स मेन्द्रो मेधया स्पृणोतु' — the prayer for intelligence — is in which anuvaka of the Taittiriya Upanishad?",
      ["1.4", "1.10", "1.12", "1.1"],
      "Shikshavalli, fourth anuvaka (1.4.1): *yaś chandasām ṛṣabho viśvarūpaḥ … sa mendro medhayā spṛṇotu*. The tenth "
      "anuvaka (1.10) is Trishanku's *ahaṃ vṛkṣasya rerivā*.")

s.mcq(U2, TA, "Which of these is NOT a way of giving taught in the Taittiriya Upanishad (1.11.3)?",
      ["प्रिया देयम्", "श्रिया देयम्", "ह्रिया देयम्", "भिया देयम्"],
      "1.11.3: *śraddhayā deyam, aśraddhayā adeyam, śriyā deyam, hriyā deyam, bhiyā deyam, saṃvidā deyam* — give with "
      "faith, with plenty, with modesty, with fear (of doing wrong), with understanding. 'Priyā' is not in the list.")

s.match(U2, TA, "Match the part of the vijnanamaya and anandamaya persons with what it is said to be (Taittiriya 2.4–2.5).",
        ["Head of the vijnanamaya", "Left (northern) wing of the vijnanamaya", "Right wing of the anandamaya",
         "Left wing of the anandamaya"],
        ["Shraddha (faith)", "Satya (truth)", "Moda (delight)", "Pramoda (great delight)"],
        ["A-i, B-ii, C-iii, D-iv", "A-ii, B-i, C-iii, D-iv", "A-i, B-ii, C-iv, D-iii", "A-iii, B-ii, C-i, D-iv"],
        "2.4: of the vijnanamaya, *śraddhā* is the head, *ṛta* the right wing, *satya* the left wing, *yoga* the body and "
        "*mahas* the tail. 2.5: of the anandamaya, *priya* is the head, *moda* the right wing, *pramoda* the left wing, "
        "*ānanda* the body and *brahman* the tail. (So the left wing of the anandamaya is pramoda, not satya.)")

s.mcq(U2, TA, "In the Taittiriya Upanishad's ladder of bliss (2.8), a hundred times the bliss of the devas is the bliss of —",
      ["Indra", "the human gandharvas", "Brihaspati", "Prajapati"],
      "2.8: man → human gandharvas → divine gandharvas → the fathers → the gods born so → the karma-devas → the devas "
      "→ **Indra** → Brihaspati → Prajapati → Brahman, each a hundred times the one before. *te ye śataṃ devānām "
      "ānandāḥ, sa eka indrasyānandaḥ.*")

s.match(U2, TA, "Match the vow about food in the Bhriguvalli with its pair of food and eater.",
        ["अन्नं न निन्द्यात् (3.7)", "अन्नं न परिचक्षीत (3.8)", "अन्नं बहु कुर्वीत (3.9)"],
        ["Prana is food, the body the eater", "Water is food, fire (jyotih) the eater", "Earth is food, space the eater"],
        ["A-i, B-ii, C-iii", "A-ii, B-i, C-iii", "A-i, B-iii, C-ii", "A-iii, B-ii, C-i"],
        "3.7: do not blame food — *prāṇo vā annam, śarīram annādam*; 3.8: do not reject food — *āpo vā annam, jyotir "
        "annādam*; 3.9: make food plentiful — *pṛthivī vā annam, ākāśo 'nnādaḥ*. So 'jyotih, apah' belong to 3.8.",
        t1="Vow", t2="Food and eater")

s.mcq(U2, TA, "By what does Varuna tell Bhrigu to seek Brahman, again and again, in the Bhriguvalli?",
      ["Tapas", "Pranayama", "Dhyana", "Samadhi"],
      "3.2–3.6: *tapasā brahma vijijñāsasva, tapo brahmeti* — 'seek to know Brahman by tapas; tapas is Brahman.' By "
      "tapas Bhrigu passes from food, prana, mind and understanding to bliss (*ānando brahmeti*).")

# --- Prashna, Mundaka, Katha, Kena, Isha --------------------------------------------------

s.mcq(U2, PR, "In the Prashna Upanishad, who asks Pippalada about the 'person of sixteen parts' (shodashakala purusha)?",
      ["Sukesha Bharadvaja", "Kabandhi Katyayana", "Sauryayani Gargya", "Shaibya Satyakama"],
      "6.1: *atha hainaṃ sukeśā bhāradvājaḥ papraccha* — Sukesha Bharadvaja asks the sixth question, about the person "
      "of sixteen parts. Kabandhi asks the first (where creatures come from), Gargya the fourth (sleep and dream), "
      "Satyakama the fifth (meditation on Om).")

s.mcq(U2, PR, "Which of these is NOT one of the sixteen kalas created from the purusha (Prashna 6.4)?",
      ["Dama (self-control)", "Manas (mind)", "Tapas (austerity)", "Mantras"],
      "6.4: prana, shraddha, space, air, light, water, earth, the senses, mind, food, vigour, tapas, **the mantras**, "
      "karma, the worlds and name. Mantras are in the list; dama is not.")

s.mcq(U2, PR, "According to Prashna 5.4, one who meditates on Om with two matras is led by the Yajus verses to —",
      ["the antariksha, the world of Soma", "the world of Brahma", "the earth, as a human", "the sun"],
      "5.4: *atha yadi dvimātreṇa manasi sampadyate so 'ntarikṣaṃ yajurbhir unnīyate somalokam* — the mid-space, the "
      "world of the moon, from which he returns. One matra brings him back to the human world (5.3); three matras "
      "lead him to the sun and the world of Brahma (5.5).")

s.mcq(U2, PR, "In the Prashna Upanishad (1.5), prana is identified with —",
      ["the sun (aditya)", "the moon", "the earth", "water"],
      "1.5: *ādityo ha vai prāṇo, rayir eva candramāḥ* — the sun is prana, the moon is rayi (matter).")

s.mcq(U2, MU, "What is the fifth of the seven tongues of fire in the Mundaka Upanishad (1.2.4)?",
      ["Sudhumravarna", "Manojava", "Sulohita", "Sphulingini"],
      "1.2.4: *kālī karālī ca manojavā ca sulohitā yā ca sudhūmravarṇā, sphuliṅginī viśvarucī ca devī* — kali, "
      "karali, manojava, sulohita, **sudhumravarna**, sphulingini, vishvaruchi. Manojava is the third.")

s.mcq(U2, MU, "Which of these is NOT aparā vidyā (the lower knowledge) in the Mundaka Upanishad (1.1.5)?",
      ["That by which the akshara is attained", "The Atharvaveda", "Kalpa", "Chandas"],
      "1.1.5: the four Vedas and the six Vedangas — shiksha, kalpa, vyakarana, nirukta, chandas, jyotisha — are aparā; "
      "*atha parā yayā tad akṣaram adhigamyate* — the higher is that by which the imperishable is reached.")

s.match(U2, MU, "Match the line with its source.",
        ["द्वा सुपर्णा सयुजा सखाया", "सत्यमेव जयते नानृतम्", "नायमात्मा बलहीनेन लभ्यः", "उत्तिष्ठत जाग्रत प्राप्य वरान्निबोधत"],
        ["Mundaka 3.1.1", "Mundaka 3.1.6", "Mundaka 3.2.4", "Katha 1.3.14"],
        ["A-i, B-ii, C-iii, D-iv", "A-ii, B-i, C-iii, D-iv", "A-i, B-iii, C-ii, D-iv", "A-iv, B-ii, C-iii, D-i"],
        "Two birds on one tree, Mundaka 3.1.1; *satyam eva jayate*, Mundaka 3.1.6; *nāyam ātmā balahīnena labhyaḥ*, "
        "Mundaka 3.2.4; *uttiṣṭhata jāgrata*, Katha 1.3.14.")

s.mcq(U2, KA, "How many nadis of the heart does the Katha Upanishad (2.3.16) speak of?",
      ["101", "100", "72,000", "350,000"],
      "2.3.16: *śataṃ caikā ca hṛdayasya nāḍyaḥ* — a hundred and one nadis of the heart; one of them goes up to the "
      "crown, and going up by it one reaches immortality.")

s.match(U2, KA, "Match the teaching with its place.",
        ["Yoga as the steady holding of the senses (sthiram indriyadharanam)", "हिरण्मयेन पात्रेण सत्यस्यापिहितं मुखम्",
         "नाहं मन्ये सुवेदेति", "यदा पञ्चावतिष्ठन्ते ज्ञानानि मनसा सह"],
        ["Katha 2.3.11", "Isha 15", "Kena 2.2", "Katha 2.3.10"],
        ["A-i, B-ii, C-iii, D-iv", "A-iv, B-ii, C-iii, D-i", "A-i, B-iii, C-ii, D-iv", "A-i, B-ii, C-iv, D-iii"],
        "*tāṃ yogam iti manyante sthirām indriya-dhāraṇām* Katha 2.3.11; the golden lid over the face of truth, Isha 15; "
        "'I do not think I know it well', Kena 2.2; 'when the five senses and the mind are still', Katha 2.3.10.")

if __name__ == "__main__":
    s.write("yoga-practice-set16.json")
