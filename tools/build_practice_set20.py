"""Practice set 20: the eight Yoga Upanishads of Unit 3.

Facts follow the texts and the Guru Parampara Yoga Sansthan comparison notes
"ALL 8 YOG UPNISHAD COMPERISION + DETAIL-2" in the Drive folder "notes UGC",
cross-checked against AWGP 108 Upanishad (Sadhana khand) and Aiyar's Thirty
Minor Upanishads (1914). Points where the notes and the texts disagreed were
left out.

    python tools/build_practice_set20.py
"""

from practice_builder import PracticeSet

U3 = "Yoga Unit 3: Yoga Texts II: Yoga Upanishads"
OV = "Yoga Upanishads: overview"
SV, YK, YC, TB = "Shvetashvatara Upanishad", "Yogakundali Upanishad", "Yogachudamani Upanishad", "Trishikhibrahmana Upanishad"
YT, DB, NB, YR = "Yogatattva Upanishad", "Dhyanabindu Upanishad", "Nadabindu Upanishad", "Yogaraja Upanishad"

s = PracticeSet("YOGA-PRAC15", "Practice set 20 (the eight Yoga Upanishads of Unit 3). Written fresh from the texts, "
                "checked against the Guru Parampara Yoga Sansthan comparison notes and the AWGP 108 Upanishad volume "
                "in the Drive folder.")

# --- overview ---------------------------------------------------------------------------

s.match(U3, OV, "Match the Yoga Upanishad with its Veda.",
        ["Yogachudamani Upanishad", "Trishikhibrahmana Upanishad", "Nadabindu Upanishad", "Dhyanabindu Upanishad"],
        ["Rigveda", "Krishna Yajurveda", "Samaveda", "Shukla Yajurveda"],
        ["A-iii, B-iv, C-i, D-ii", "A-iv, B-iii, C-i, D-ii", "A-iii, B-iv, C-ii, D-i", "A-iii, B-i, C-iv, D-ii"],
        "Yogachudamani → Samaveda; Trishikhibrahmana → Shukla Yajurveda; Nadabindu → Rigveda. Dhyanabindu, "
        "Yogatattva, Yogakundali and Shvetashvatara are Krishna Yajurveda. The Yogaraja is not attached to any Veda.")

s.statements(U3, OV, "Which of these Yoga Upanishads belong to the Krishna Yajurveda?",
             ["Yogatattva", "Dhyanabindu", "Yogakundali", "Nadabindu", "Yogachudamani"],
             ["Only (A), (B) and (C)", "Only (A), (D) and (E)", "Only (B), (C) and (D)", "Only (C), (D) and (E)"],
             "Yogatattva, Dhyanabindu and Yogakundali (with Shvetashvatara) are Krishna Yajurveda. Nadabindu is Rigveda, "
             "Yogachudamani Samaveda.")

s.match(U3, OV, "Match the Upanishad with the number of limbs of yoga it teaches.",
        ["Trishikhibrahmana Upanishad", "Yogachudamani Upanishad", "Yogaraja Upanishad"],
        ["Six limbs (shadanga)", "Four limbs (asana, pranasamrodha, dhyana, samadhi)", "Eight limbs (ashtanga)"],
        ["A-iii, B-i, C-ii", "A-i, B-iii, C-ii", "A-iii, B-ii, C-i", "A-ii, B-i, C-iii"],
        "Trishikhibrahmana and Yogatattva teach ashtanga yoga; Yogachudamani and Dhyanabindu teach shadanga yoga "
        "(no yama, niyama); the Yogaraja names four limbs.")

s.statements(U3, OV, "The four yogas — mantra, laya, hatha and raja — are described in which Upanishads?",
             ["Yogatattva", "Yogaraja", "Nadabindu", "Trishikhibrahmana"],
             ["Only (A) and (B)", "Only (A) and (D)", "Only (B) and (C)", "Only (C) and (D)"],
             "Both the Yogatattva and the Yogaraja describe the four yogas (mantra, laya, hatha, raja). The "
             "Trishikhibrahmana speaks of two paths, jnana yoga and karma yoga.")

# --- Shvetashvatara ---------------------------------------------------------------------

s.mcq(U3, SV, "According to the Shvetashvatara Upanishad (2.8), how should the meditator sit?",
      ["With the three upper parts — head, neck and chest — held erect (trirunnatam)",
       "With the gaze fixed on the tip of the nose", "In padmasana with the hands in jnana mudra",
       "Lying flat in shavasana"],
      "Shvetashvatara 2.8: *trir-unnataṃ sthāpya samaṃ śarīraṃ* — holding the body straight with the three upper "
      "parts erect, drawing the senses into the heart, the wise one crosses the fearful streams on the boat of Brahman (Om).")

s.statements(U3, SV, "According to the Shvetashvatara Upanishad (2.13), the first signs of progress in yoga include:",
             ["Lightness of the body", "Health", "Freedom from craving", "Long hair", "Loud voice"],
             ["Only (A), (B) and (C)", "Only (A), (D) and (E)", "Only (B), (C) and (D)", "Only (C), (D) and (E)"],
             "2.13: *laghutvam ārogyam alolupatvaṃ varṇa-prasādaṃ svara-sauṣṭhavaṃ ca, gandhaḥ śubho mūtra-purīṣam "
             "alpam* — lightness, health, freedom from craving, clear complexion, a pleasant voice, a sweet odour and "
             "scanty excretions.")

s.mcq(U3, SV, "'māyāṃ tu prakṛtiṃ vidyān māyinaṃ tu maheśvaram' (know maya as prakriti and the Great Lord as the "
              "wielder of maya) is from:",
      ["Shvetashvatara Upanishad 4.10", "Mundaka Upanishad 2.1.1", "Katha Upanishad 1.3.10", "Yogatattva Upanishad 1"],
      "Shvetashvatara 4.10 (asked in November 2021). The whole world is pervaded by beings that are parts of him.")

s.mcq(U3, SV, "According to the Shvetashvatara Upanishad (6.13), the Supreme cause is to be known through:",
      ["Samkhya and yoga", "Mantra and laya", "Karma and bhakti", "Hatha and raja"],
      "6.13: *tat kāraṇaṃ sāṃkhya-yogādhigamyaṃ, jñātvā devaṃ mucyate sarva-pāśaiḥ* — that cause, attained by Samkhya "
      "and yoga; knowing God one is freed from all fetters.")

s.mcq(U3, SV, "The Shvetashvatara Upanishad (5.9) describes the size of the individual self as:",
      ["A hundredth part of a hundredth part of the tip of a hair", "The size of a thumb only",
       "The size of a grain of barley", "As large as the body it lives in"],
      "5.9: imagine the tip of a hair divided a hundred times, and one part divided a hundred times again — that is "
      "the jiva, yet it is capable of infinity. (Elsewhere, 3.13 and 5.8, the purusha is 'thumb-sized'.)")

# --- Yogakundali ------------------------------------------------------------------------

s.mcq(U3, YK, "According to the Yogakundali Upanishad, the two causes of the mind's restlessness are:",
      ["Vasanas and vayu (prana)", "Rajas and tamas", "Raga and dvesha", "Avidya and asmita"],
      "Yogakundali 1.1: *hetu-dvayaṃ hi cittasya vāsanā ca samīraṇaḥ*. When one is destroyed both are, so one first "
      "masters prana.")

s.mcq(U3, YK, "According to the Yogakundali Upanishad, prana is mastered through:",
      ["Mitahara, asana and shakti-chalana", "Yama, niyama and asana", "Neti, dhauti and basti",
       "Japa, dhyana and samadhi"],
      "Yogakundali 1.2–3: the three means of mastering prana are moderate diet (mitahara), posture (asana) and "
      "rousing the shakti (shakti-chalana, i.e. kundalini).")

s.statements(U3, YK, "Which kumbhakas are described in the Yogakundali Upanishad?",
             ["Surya-bhedana", "Ujjayi", "Shitali", "Bhramari", "Murchha"],
             ["Only (A), (B) and (C)", "Only (A), (D) and (E)", "Only (B), (C) and (D)", "Only (C), (D) and (E)"],
             "The Yogakundali names four kumbhakas: surya-bhedana, ujjayi, shitali and bhastrika. Bhramari and murchha "
             "belong to the Hatha Pradipika's eight.")

s.mcq(U3, YK, "The second chapter of the Yogakundali Upanishad is devoted to:",
      ["Khechari vidya", "The ten nadis", "The eight limbs of yoga", "The four states of consciousness"],
      "Chapter 2 teaches khechari vidya, with its melana mantra and the gradual lengthening of the tongue; "
      "chapter 1 covers prana, kumbhakas and kundalini, chapter 3 the melana mantra and the state beyond.")

s.mcq(U3, YK, "Which two asanas does the Yogakundali Upanishad prescribe?",
      ["Padmasana and vajrasana", "Siddhasana and simhasana", "Bhadrasana and swastikasana", "Mayurasana and kukkutasana"],
      "Yogakundali 1.4–6: padmasana and vajrasana. (Yogachudamani has siddha and kamala/padma; Dhyanabindu and "
      "Yogatattva have four.)")

# --- Yogachudamani ----------------------------------------------------------------------

s.sequence(U3, YC, "Arrange the six limbs of yoga in the Yogachudamani Upanishad in order.",
           ["Pratyahara", "Asana", "Dhyana", "Pranayama", "Dharana", "Samadhi"],
           ["(B), (D), (A), (E), (C), (F)", "(B), (A), (D), (E), (C), (F)", "(D), (B), (A), (E), (C), (F)",
            "(B), (D), (A), (C), (E), (F)"],
           "Yogachudamani 2: *āsanaṃ prāṇa-saṃrodhaḥ pratyāhāraś ca dhāraṇā, dhyānaṃ samādhir etāni yogāṅgāni bhavanti "
           "ṣaṭ* — asana, pranayama, pratyahara, dharana, dhyana, samadhi.")

s.match(U3, YC, "According to the Yogachudamani Upanishad, match each limb with what it removes or brings.",
        ["Asana", "Pranayama", "Pratyahara", "Samadhi"],
        ["Mental disorders", "Release from good and bad karma, and liberation", "Disease", "Sin"],
        ["A-iii, B-iv, C-i, D-ii", "A-iv, B-iii, C-i, D-ii", "A-iii, B-i, C-iv, D-ii", "A-i, B-iv, C-iii, D-ii"],
        "Yogachudamani: *āsanena rujaṃ hanti prāṇāyāmena pātakam, vikāraṃ mānasaṃ yogī pratyāhāreṇa muñcati* — asana "
        "destroys disease, pranayama sin, pratyahara mental disorders; dharana gives firmness of mind, and in samadhi "
        "one leaves good and bad karma and attains liberation.")

s.match(U3, YC, "Match the nadi with its place, as given in the Yogachudamani (and Dhyanabindu) Upanishad.",
        ["Gandhari", "Hastijihva", "Pusha", "Kuhu"],
        ["Right eye", "Genitals", "Left eye", "Right ear"],
        ["A-iii, B-i, C-iv, D-ii", "A-i, B-iii, C-iv, D-ii", "A-iii, B-iv, C-i, D-ii", "A-iii, B-i, C-ii, D-iv"],
        "Gandhari — left eye; hastijihva — right eye; pusha — right ear; yashasvini — left ear; alambusha — mouth; "
        "kuhu — genitals; shankhini — anus. Ida, pingala and sushumna run left, right and centre.")

s.mcq(U3, YC, "How many times a day does the jiva repeat the hamsa mantra (ajapa gayatri), according to the "
              "Yogachudamani and Dhyanabindu Upanishads?",
      ["21,600", "72,000", "10,800", "1,008"],
      "The breath goes out with the sound 'ha' and in with 'sa'; the jiva repeats *haṃsa* 21,600 times in a day and "
      "night. This is the ajapa gayatri. (72,000 is the number of nadis.)")

s.match(U3, YC, "Match the chakra with the number of petals given in the Yogachudamani Upanishad.",
        ["Adhara (muladhara)", "Manipura (navel)", "Vishuddhi", "Bhrumadhya (between the brows)"],
        ["Sixteen", "Two", "Four", "Ten"],
        ["A-iii, B-iv, C-i, D-ii", "A-iv, B-iii, C-i, D-ii", "A-iii, B-i, C-iv, D-ii", "A-iii, B-iv, C-ii, D-i"],
        "Adhara 4, svadhishthana 6, manipura 10, heart lotus 12, vishuddhi 16, bhrumadhya 2, and the thousand-petalled "
        "lotus at the brahmarandhra.")

s.ar(U3, YC, "The Yogachudamani Upanishad says that one who practises pranayama wrongly develops hiccups, asthma, "
             "cough and pains in the head, ears and eyes.",
     "Prana must be brought under control gradually, as a lion, elephant or tiger is tamed slowly.", 1,
     "Both are true and (R) explains (A): the text compares taming prana to taming wild animals step by step; forcing "
     "it disturbs the vayu and causes these diseases. (Hatha Pradipika 2.15–17 says the same.)")

# --- Trishikhibrahmana -----------------------------------------------------------------

s.mcq(U3, TB, "The Trishikhibrahmana Upanishad is a dialogue between the brahmana Trishikhi and:",
      ["Aditya (the sun god)", "Lord Vishnu", "Lord Shiva", "The sage Yajnavalkya"],
      "Trishikhi goes to the world of the sun and questions Aditya, who teaches him the body, the elements and "
      "ashtanga yoga. (In the Yogatattva it is Vishnu who teaches Brahma.)")

s.mcq(U3, TB, "How many yamas and niyamas does the Trishikhibrahmana Upanishad list?",
      ["Ten yamas and ten niyamas", "Five yamas and five niyamas", "Ten yamas and five niyamas",
       "Five yamas and ten niyamas"],
      "Ten each. Yamas: ahimsa, satya, asteya, brahmacharya, daya, arjava, kshama, dhriti, mitahara, shaucha. "
      "Niyamas: tapas, santosha, astikya, dana, worship of Ishvara, siddhanta-shravana, hri, mati, japa, vrata.")

s.statements(U3, TB, "Which of these are among the ten niyamas of the Trishikhibrahmana Upanishad?",
             ["Siddhanta-shravana (hearing the scriptures)", "Hri (modesty)", "Japa", "Mitahara", "Daya"],
             ["Only (A), (B) and (C)", "Only (A), (D) and (E)", "Only (B), (C) and (D)", "Only (C), (D) and (E)"],
             "Siddhanta-shravana, hri and japa are niyamas. Mitahara and daya are among the ten yamas.")

s.mcq(U3, TB, "How many asanas does the Trishikhibrahmana Upanishad describe?",
      ["Seventeen", "Four", "Two", "Eighty-four"],
      "Seventeen, from swastika, gomukha and vira to padma, mayura, matsya, siddha, paschimottana and sukhasana — "
      "the most of any Yoga Upanishad in the syllabus.")

s.mcq(U3, TB, "According to the Trishikhibrahmana Upanishad, pratyahara is withdrawing the attention from one to "
              "another of the body's how many vital points (marma sthana)?",
      ["Eighteen", "Seven", "Twelve", "Ninety-six"],
      "The Trishikhibrahmana (like the Shandilya) defines one form of pratyahara as drawing prana and the mind from one "
      "to another of the eighteen marma sthanas. (96 angulas is the body's length in the same text.)")

s.mcq(U3, TB, "The Trishikhibrahmana Upanishad names two paths of yoga. They are:",
      ["Jnana yoga and karma yoga", "Hatha yoga and raja yoga", "Mantra yoga and laya yoga", "Bhakti yoga and karma yoga"],
      "Jnana yoga is keeping the mind always on the highest good; karma yoga is keeping it bound to prescribed duties. "
      "Practising both without attachment leads quickly to liberation.")

# --- Yogatattva -------------------------------------------------------------------------

s.mcq(U3, YT, "In the Yogatattva Upanishad, who teaches yoga to whom?",
      ["Vishnu teaches Brahma", "Brahma teaches Vishnu", "Shiva teaches Parvati", "Aditya teaches Trishikhi"],
      "Brahma (Pitamaha) asks Vishnu (Hrishikesha) to teach him yoga with its eight limbs, and Vishnu explains its "
      "subtle principles.")

s.sequence(U3, YT, "Arrange the four stages (avastha) of yoga in the Yogatattva Upanishad in order.",
           ["Ghata", "Nishpatti", "Arambha", "Parichaya"],
           ["(C), (A), (D), (B)", "(C), (D), (A), (B)", "(A), (C), (D), (B)", "(C), (A), (B), (D)"],
           "Arambha (beginning), ghata, parichaya, nishpatti (consummation). The Hatha Pradipika (4.69) uses the same four "
           "stages for nadanusandhana.")

s.match(U3, YT, "Match the four yogas of the Yogatattva Upanishad with their description.",
        ["Mantra yoga", "Laya yoga", "Hatha yoga", "Raja yoga"],
        ["Absorption of the mind in the Supreme while walking, sitting, eating", "Repeating a mantra for twelve years; "
         "for those of small intellect", "Perfected through vajroli and amaroli", "Yoga with eight limbs"],
        ["A-ii, B-i, C-iv, D-iii", "A-i, B-ii, C-iv, D-iii", "A-ii, B-iv, C-i, D-iii", "A-iii, B-i, C-iv, D-ii"],
        "Mantra yoga brings anima and the like after twelve years of japa but suits the dull; laya is constant absorption "
        "of the mind in the Supreme; hatha is yoga with eight limbs; raja yoga is attained by one who has mastered "
        "vajroli and amaroli.")

s.mcq(U3, YT, "In the Yogatattva Upanishad, what is called the chief yama and what the chief niyama?",
      ["Light food (mitahara) and ahimsa", "Ahimsa and santosha", "Satya and tapas", "Brahmacharya and Ishvara pranidhana"],
      "Yogatattva: among the yamas the chief is light, moderate food (*laghv-āhāra*); among the niyamas the chief is "
      "ahimsa.")

s.mcq(U3, YT, "What ratio of puraka, kumbhaka and rechaka (in matras) do the Yogatattva and Trishikhibrahmana "
              "Upanishads give?",
      ["16 : 64 : 32", "12 : 16 : 10", "1 : 2 : 2", "4 : 16 : 8"],
      "Inhale for 16 matras, hold for 64, exhale for 32 — practised four times a day (dawn, noon, evening, midnight) "
      "and gradually raised to 80 kumbhakas. A matra is the time to circle the knee with the hand and snap the fingers.")

s.sequence(U3, YT, "According to the Yogatattva Upanishad, arrange the signs that appear as pranayama advances.",
           ["The body rises from the ground", "Sweating", "Hopping like a frog (dardura)", "Trembling"],
           ["(B), (D), (C), (A)", "(B), (C), (D), (A)", "(D), (B), (C), (A)", "(B), (D), (A), (C)"],
           "First sweat (to be rubbed into the body), then trembling, then hopping like a frog, then rising from the "
           "ground (bhuchari siddhi).")

s.ar(U3, YT, "The Yogatattva Upanishad advises the accomplished yogi to behave in public like a dull, foolish or "
             "deaf person.",
     "Siddhis displayed to others become obstacles that draw the yogi away from the goal.", 1,
     "Both are true and (R) explains (A): the text treats siddhis as obstacles and tells the yogi to hide them and "
     "appear ordinary.")

# --- Dhyanabindu ------------------------------------------------------------------------

s.mcq(U3, DB, "The Dhyanabindu Upanishad opens by saying that even a heap of sins as large as a mountain is destroyed "
              "by:",
      ["Dhyana yoga", "Pranayama", "Pilgrimage", "Charity"],
      "Dhyanabindu 1: *yadi śaila-samaṃ pāpaṃ vistīrṇaṃ bahu-yojanam, bhidyate dhyāna-yogena nānyo bhedaḥ kadācana*.")

s.match(U3, DB, "According to the Dhyanabindu Upanishad, match each letter of Om with its colour.",
        ["A-kara", "U-kara", "M-kara"],
        ["Black (krishna)", "Yellow (pita)", "White (shveta)"],
        ["A-ii, B-iii, C-i", "A-iii, B-ii, C-i", "A-ii, B-i, C-iii", "A-i, B-iii, C-ii"],
        "A: yellow, rajas, Brahma; U: white, sattva, Vishnu; M: black, tamas, Rudra/Maheshvara. In each, the earth, "
        "mid-region and heaven, and the three Vedas, are dissolved in turn.")

s.mcq(U3, DB, "The Dhyanabindu Upanishad names how many principal asanas?",
      ["Four: siddha, bhadra, simha and padma", "Two: siddha and padma", "Seventeen", "Eighty-four lakh"],
      "It says there are as many asanas as living beings, but four are chief: siddha, bhadra, simha and padma. "
      "The Yogatattva gives the same four.")

s.match(U3, DB, "In the Dhyanabindu Upanishad, match each phase of pranayama with the deity meditated on.",
        ["Puraka (inhalation)", "Kumbhaka (retention)", "Rechaka (exhalation)"],
        ["Shiva at the forehead", "Four-armed Vishnu at the navel", "Four-faced Brahma in the heart"],
        ["A-ii, B-iii, C-i", "A-iii, B-ii, C-i", "A-ii, B-i, C-iii", "A-i, B-iii, C-ii"],
        "Puraka: Vishnu, the colour of the atasi flower, at the navel; kumbhaka: Brahma, red-gold, in the heart lotus; "
        "rechaka: three-eyed Shiva, white as crystal, at the forehead.")

s.ar(U3, DB, "The Dhyanabindu Upanishad calls uddiyana bandha 'the lion to the elephant of death'.",
     "Uddiyana drives prana up through the sushumna.", 1,
     "Both are true, and (R) is why: uddiyana makes the great bird of prana fly up the sushumna, so death is overcome. "
     "The Yogachudamani has the same image.")

# --- Nadabindu --------------------------------------------------------------------------

s.match(U3, NB, "In the Nadabindu Upanishad Om is a bird (hamsa). Match each part of Om with the part of the bird.",
        ["A-kara", "U-kara", "M-kara", "Ardhamatra"],
        ["Tail", "Head", "Right wing", "Left wing"],
        ["A-iii, B-iv, C-i, D-ii", "A-iv, B-iii, C-i, D-ii", "A-iii, B-i, C-iv, D-ii", "A-i, B-iv, C-iii, D-ii"],
        "Nadabindu 1: A is the right wing, U the left, M the tail, and the half-measure the head. Its feet are the "
        "gunas and its body truth.")

s.match(U3, NB, "Match each matra of Om with its presiding deity in the Nadabindu Upanishad.",
        ["First matra (A)", "Second matra (U)", "Third matra (M)", "Ardhamatra"],
        ["Varuna", "Vayu", "Agni", "The sun (surya)"],
        ["A-iii, B-ii, C-iv, D-i", "A-ii, B-iii, C-iv, D-i", "A-iii, B-iv, C-ii, D-i", "A-iv, B-ii, C-iii, D-i"],
        "Nadabindu 6–7: the first matra belongs to Agni, the second to Vayu, the third shines like the orb of the sun, "
        "and the highest, the ardhamatra, the wise know as Varuni.")

s.sequence(U3, NB, "According to the Nadabindu Upanishad, arrange the sounds heard in nadanusandhana from the first "
                   "stage to the last.",
           ["Bell (ghanta)", "Ocean (jaladhi)", "Vina"],
           ["(B), (A), (C)", "(A), (B), (C)", "(C), (A), (B)", "(B), (C), (A)"],
           "First come loud sounds like the ocean, clouds, the kettledrum and waterfalls; in the middle the mardala, bell "
           "and horn; at the end tinkling bells, flute, vina and bees. Attention moves from the gross to the subtle.")

s.ar(U3, NB, "According to the Nadabindu Upanishad, when nada ends the mind becomes 'amanas' (no-mind).",
     "The mind exists only as long as there is sound.", 1,
     "Both are true and (R) explains (A): *yāvan nādo 'sti tāvan manaḥ, nādānte tu manonmanī* — the mind lasts as long "
     "as the sound; at its end the mind is dissolved and the yogi rests in turiya.")

# --- Yogaraja ---------------------------------------------------------------------------

s.mcq(U3, YR, "How many mantras does the Yogaraja Upanishad have?",
      ["21", "18", "64", "108"],
      "The Yogaraja is a short text of 21 mantras. (18 is the Isha, 64 the Mundaka.)")

s.sequence(U3, YR, "Arrange these chakras of the Yogaraja Upanishad from the lowest to the highest.",
           ["Kantha chakra", "Nabhi chakra", "Talu chakra", "Hridaya chakra", "Bhru chakra"],
           ["(B), (D), (A), (C), (E)", "(B), (A), (D), (C), (E)", "(D), (B), (A), (C), (E)", "(B), (D), (C), (A), (E)"],
           "The nine chakras: brahma, svadhishthana, nabhi, hridaya, kantha, talu, bhru, brahmarandhra and vyoma. "
           "The talu chakra is sixth (asked in June 2019).")

s.mcq(U3, YR, "In the Yogaraja Upanishad, meditation on the nine chakras is the method of which yoga?",
      ["Laya yoga", "Mantra yoga", "Hatha yoga", "Raja yoga"],
      "By dissolving the mind in the nine chakras in turn the great ones attain laya yoga. Mantra yoga was perfected "
      "by Vatsaraja and others; laya by Krishna Dvaipayana (Vyasa) and others.")

if __name__ == "__main__":
    s.write("yoga-practice-set15.json")
