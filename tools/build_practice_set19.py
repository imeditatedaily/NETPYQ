"""Practice set 19: the principal Upanishads (Unit 2), with Kena, Mundaka and
Brihadaranyaka covered properly for the first time.

Facts follow the texts (mantra numbers given) and the Guru Parampara Yoga
Sansthan notes in the Drive folder "notes UGC" (ISHA VASYO UPNISHAD-1,
KEN UNPISHAD-2, MUNDAK UPNISHAD-5, BRIHDARNAYK UPNISHAD-10), cross-checked
against Gita Press ईशादि नौ उपनिषद्.

    python tools/build_practice_set19.py
"""

from practice_builder import PracticeSet

U2 = "Yoga Unit 2: Yoga Texts I: Principal Upanishads, Bhagavad Gita and Yoga Vasishtha"
KENA, MUND, BRIH, ISHA = "Kena Upanishad", "Mundaka Upanishad", "Brihadaranyaka Upanishad", "Isha Upanishad"

s = PracticeSet("YOGA-PRAC14", "Practice set 19 (Principal Upanishads: Kena, Mundaka, Brihadaranyaka, Isha). Written "
                "fresh from the Upanishad texts, checked against the Guru Parampara Yoga Sansthan notes and Gita Press "
                "Ishadi Nau Upanishad in the Drive folder; mantra numbers given in each explanation.")

# --- Kena -------------------------------------------------------------------------------

s.mcq(U2, KENA, "The Kena Upanishad belongs to which Veda?",
      ["Samaveda", "Rigveda", "Shukla Yajurveda", "Atharvaveda"],
      "The Kena is part of the Talavakara (Jaiminiya) Brahmana of the Samaveda, which is why it is also called the "
      "Talavakara or Jaiminiya Upanishad. Its name comes from its first word, *kena* (by whom?).")

s.mcq(U2, KENA, "The Kena Upanishad opens with a disciple's question. What does it ask?",
      ["By whom are the mind, prana, speech, eye and ear directed to their work?",
       "What is the origin of prana and how does it enter the body?",
       "Knowing what is everything else known?",
       "What happens to a man after death?"],
      "Kena 1.1: *keneṣitaṃ patati preṣitaṃ manaḥ…* By whom impelled does the mind go to its objects, prana move, "
      "speech speak, and eye and ear work? (Option 2 is Prashna's third question, option 3 Mundaka 1.1.3, option 4 "
      "Nachiketa's question in the Katha.)")

s.mcq(U2, KENA, "According to the Kena Upanishad, Brahman is:",
      ["The ear of the ear, the mind of the mind, the speech of speech", "That which the eye sees and the mind thinks",
       "The god whom people worship as 'this'", "The prana that moves in the body"],
      "Kena 1.2: *śrotrasya śrotraṃ manaso mano yad vāco ha vācam…* Brahman is what powers the senses; it is not "
      "what is seen or thought, and 'not this which people worship here' (*nedaṃ yad idam upāsate*, 1.4–8).")

s.mcq(U2, KENA, "'avijñātaṃ vijānatāṃ vijñātam avijānatām' (Kena 2.3) means that Brahman is:",
      ["Not known to those who think they know it, and known to those who know they do not",
       "Known only through the Vedas",
       "Known through perception and inference",
       "Unknowable by anyone at all"],
      "Kena 2.3: it is unknown to those who claim to know, and known to those who do not claim to know. "
      "The teacher has just warned that one who thinks 'I know Brahman well' knows very little (2.1).")

s.match(U2, KENA, "Match the deity in the Yaksha story of the Kena Upanishad with what happened.",
        ["Agni (Jatavedas)", "Vayu (Matarishvan)", "Indra", "Uma Haimavati"],
        ["Could not blow away a blade of grass", "Could not burn a blade of grass",
         "Revealed that the Yaksha was Brahman", "Went up to the Yaksha, which vanished"],
        ["A-ii, B-i, C-iv, D-iii", "A-i, B-ii, C-iv, D-iii", "A-ii, B-i, C-iii, D-iv", "A-iv, B-i, C-ii, D-iii"],
        "Kena 3–4: Agni (Jatavedas) could not burn the straw, Vayu (Matarishvan) could not blow it away; when "
        "Indra approached, the Yaksha vanished and Uma Haimavati appeared and told him it was Brahman, by whose "
        "power the gods had won.")

s.mcq(U2, KENA, "In the Kena Upanishad, which god is called the foremost, because he was the first to know Brahman?",
      ["Indra", "Agni", "Vayu", "Varuna"],
      "Kena 4.2–3: Agni, Vayu and Indra stand above the other gods because they came closest to Brahman, and Indra "
      "above them all because he was the first to know it as Brahman (from Uma).")

s.mcq(U2, KENA, "According to the Kena Upanishad (4.8), the supports (pratishtha) of this secret teaching are:",
      ["Tapas, dama and karma", "Shama, dama and titiksha", "Yama, niyama and asana", "Shravana, manana and nididhyasana"],
      "Kena 4.8: *tasyai tapo damaḥ karmeti pratiṣṭhā, vedāḥ sarvāṅgāni, satyam āyatanam* — austerity, "
      "self-control and action are its foundation, the Vedas its limbs, truth its abode.")

s.mcq(U2, KENA, "In the Kena Upanishad, Brahman is to be meditated on under which name?",
      ["Tadvanam (the one to be adored)", "Hiranyagarbha", "Vaishvanara", "Antaryamin"],
      "Kena 4.6: *tad dha tadvanaṃ nāma, tadvanam ity upāsitavyam* — it is known as Tadvanam, the adorable; one "
      "who meditates on it so becomes dear to all beings.")

s.ar(U2, KENA, "The Kena Upanishad says that Brahman's teaching about itself is like a flash of lightning and the "
               "blink of an eye.",
     "Brahman is grasped not as an object but in a sudden, momentary illumination.", 1,
     "Kena 4.4: *yad etad vidyuto vyadyutadā itī nyamīmiṣadā* — like lightning flashing and the eye blinking. Both "
     "statements are true and (R) explains the simile.")

# --- Mundaka ----------------------------------------------------------------------------

s.mcq(U2, MUND, "The Mundaka Upanishad belongs to:",
      ["The Shaunaka recension of the Atharvaveda", "The Kauthuma recension of the Samaveda",
       "The Kanva recension of the Shukla Yajurveda", "The Taittiriya recension of the Krishna Yajurveda"],
      "The Mundaka is an Atharvaveda Upanishad (Shaunaka shakha). It has 64 mantras in three mundakas of two "
      "khandas each.")

s.mcq(U2, MUND, "In the Mundaka Upanishad, Shaunaka asks: 'kasmin nu bhagavo vijñāte sarvam idaṃ vijñātaṃ bhavati?' "
                "Whom does he ask?",
      ["Angiras", "Yajnavalkya", "Pippalada", "Uddalaka Aruni"],
      "Mundaka 1.1.3: the great householder Shaunaka asks the sage Angiras, 'Knowing what, revered sir, does all "
      "this become known?' Angiras answers with the two vidyas.")

s.sequence(U2, MUND, "Arrange the line through which the knowledge of Brahman was handed down, according to the "
                     "Mundaka Upanishad (1.1.1–2).",
           ["Angiras", "Atharvan", "Brahma", "Satyavaha Bharadvaja", "Angir"],
           ["(C), (B), (E), (D), (A)", "(C), (B), (D), (E), (A)", "(B), (C), (E), (D), (A)", "(C), (E), (B), (D), (A)"],
           "Brahma taught it to his eldest son Atharvan; Atharvan to Angir; Angir to Satyavaha of the Bharadvaja line; "
           "Satyavaha to Angiras, who taught it to Shaunaka.")

s.mcq(U2, MUND, "According to the Mundaka Upanishad, which of these belongs to para vidya (the higher knowledge)?",
      ["That by which the imperishable (akshara) is known", "The Rigveda and Samaveda",
       "Shiksha, kalpa and vyakarana", "Nirukta, chhandas and jyotisha"],
      "Mundaka 1.1.4–5: apara vidya is the four Vedas and the six Vedangas; para vidya is that by which the "
      "imperishable is attained (*yayā tad akṣaram adhigamyate*).")

s.statements(U2, MUND, "According to the Mundaka Upanishad, which of these are part of apara vidya?",
             ["Rigveda", "Shiksha (phonetics)", "Knowledge of the akshara", "Nirukta (etymology)", "Brahma vidya"],
             ["Only (A), (B) and (D)", "Only (A), (C) and (E)", "Only (B), (C) and (D)", "Only (C), (D) and (E)"],
             "Apara vidya (1.1.5) is the four Vedas plus the six Vedangas: shiksha, kalpa, vyakarana, nirukta, chhandas "
             "and jyotisha. Knowledge of the akshara, i.e. brahma vidya, is para vidya.")

s.mcq(U2, MUND, "How many tongues of the sacrificial fire does the Mundaka Upanishad (1.2.4) name?",
      ["Seven", "Five", "Three", "Nine"],
      "Mundaka 1.2.4: Kali, Karali, Manojava, Sulohita, Sudhumravarna, Sphulingini and Vishvaruchi — the seven "
      "flickering tongues of fire.")

s.match(U2, MUND, "In the Mundaka Upanishad (2.2.4), match each element of the image with what it stands for.",
        ["Bow (dhanu)", "Arrow (shara)", "Target (lakshya)"],
        ["Brahman", "Pranava (Om)", "The Self (atma)"],
        ["A-ii, B-iii, C-i", "A-iii, B-ii, C-i", "A-ii, B-i, C-iii", "A-i, B-iii, C-ii"],
        "Mundaka 2.2.4: *praṇavo dhanuḥ śaro hy ātmā brahma tal lakṣyam ucyate* — Om is the bow, the Self the arrow, "
        "Brahman the target; it is to be hit by one who is not careless. (The Dhyanabindu Upanishad repeats the image.)")

s.mcq(U2, MUND, "India's national motto 'Satyameva Jayate' is taken from:",
      ["Mundaka Upanishad 3.1.6", "Katha Upanishad 1.3.14", "Mandukya Upanishad 7", "Brihadaranyaka Upanishad 1.3.28"],
      "Mundaka 3.1.6: *satyam eva jayate nānṛtaṃ, satyena panthā vitato devayānaḥ* — truth alone wins, not "
      "untruth; by truth is laid the path of the gods.")

s.mcq(U2, MUND, "'dvā suparṇā sayujā sakhāyā samānaṃ vṛkṣaṃ pariṣasvajāte' (two birds, companions, on the same "
                "tree) is found in the Mundaka Upanishad and also in:",
      ["Shvetashvatara Upanishad (4.6)", "Isha Upanishad", "Kena Upanishad", "Mandukya Upanishad"],
      "Mundaka 3.1.1–2 = Shvetashvatara 4.6–7 (originally Rigveda 1.164.20). One bird eats the sweet fruit (the jiva); "
      "the other watches without eating (the Supreme Self).")

s.mcq(U2, MUND, "'nāyam ātmā balahīnena labhyaḥ' (this Self is not attained by the weak) is from:",
      ["Mundaka Upanishad 3.2.4", "Katha Upanishad 1.2.23", "Kena Upanishad 2.4", "Shvetashvatara Upanishad 6.13"],
      "Mundaka 3.2.4. Asked in the February 2023 paper. The Katha has the related line *nāyam ātmā pravacanena "
      "labhyaḥ* (1.2.23), not attained by discourse — a classic distractor.")

s.mcq(U2, MUND, "According to the Mundaka Upanishad (3.1.5), the Self within the body is attained through:",
      ["Truth, tapas, right knowledge and brahmacharya", "Yajna, dana and tapas", "Mantra, japa and dhyana",
       "Asana, pranayama and pratyahara"],
      "Mundaka 3.1.5: *satyena labhyas tapasā hy eṣa ātmā samyag-jñānena brahmacaryeṇa nityam* — by truth, "
      "austerity, right knowledge and constant brahmacharya.")

s.ar(U2, MUND, "The Mundaka Upanishad calls sacrifices 'unsteady boats' (plavā hy ete adṛḍhāḥ).",
     "Rituals done for heavenly rewards bring only a passing heaven, after which one returns to birth and death.", 1,
     "Mundaka 1.2.7–10: the eighteen-membered sacrifices are unsteady boats; fools who think them the highest good "
     "fall again into old age and death when their merit runs out. (R) is the reason for (A).")

# --- Brihadaranyaka ---------------------------------------------------------------------

s.mcq(U2, BRIH, "The Brihadaranyaka Upanishad forms the end of which text?",
      ["The Shatapatha Brahmana of the Shukla Yajurveda", "The Taittiriya Brahmana of the Krishna Yajurveda",
       "The Aitareya Aranyaka of the Rigveda", "The Talavakara Brahmana of the Samaveda"],
      "The Brihadaranyaka is the last part (kanda 14) of the Shatapatha Brahmana, Shukla Yajurveda. It is the longest "
      "Upanishad, with 6 adhyayas, and is counted among the oldest.")

s.mcq(U2, BRIH, "'asato mā sad gamaya, tamaso mā jyotir gamaya, mṛtyor mā amṛtaṃ gamaya' is from:",
      ["Brihadaranyaka Upanishad (1.3.28)", "Chandogya Upanishad", "Taittiriya Upanishad", "Isha Upanishad"],
      "Brihadaranyaka 1.3.28, the pavamana prayer chanted before the Saman: lead me from the unreal to the real, "
      "from darkness to light, from death to immortality.")

s.mcq(U2, BRIH, "Which of these great sayings is NOT from the Brihadaranyaka Upanishad?",
      ["Tat tvam asi", "Aham brahmasmi", "Neti neti", "Asato ma sad gamaya"],
      "*Tat tvam asi* is Uddalaka's teaching to Shvetaketu in the Chandogya (6.8.7). *Aham brahmāsmi* (1.4.10), "
      "*neti neti* (2.3.6) and *asato mā* (1.3.28) are all Brihadaranyaka.")

s.mcq(U2, BRIH, "'ātmā vā are draṣṭavyaḥ śrotavyo mantavyo nididhyāsitavyaḥ' — Yajnavalkya says this to:",
      ["Maitreyi", "Gargi", "Katyayani", "King Janaka"],
      "Brihadaranyaka 2.4.5 (and 4.5.6): Maitreyi asks what use is wealth that cannot make her immortal, and "
      "Yajnavalkya teaches that the Self is to be seen, heard about, reflected on and meditated upon.")

s.match(U2, BRIH, "In the Brihadaranyaka (5.2), Prajapati says one syllable 'Da' to each group. Match each group with "
                  "what they understood.",
        ["Devas (gods)", "Manavas (humans)", "Asuras (demons)"],
        ["Datta — give", "Dayadhvam — be compassionate", "Damyata — control yourselves"],
        ["A-iii, B-i, C-ii", "A-i, B-iii, C-ii", "A-iii, B-ii, C-i", "A-ii, B-i, C-iii"],
        "Brihadaranyaka 5.2: the gods, unrestrained by nature, heard *damyata* (self-control); greedy humans heard "
        "*datta* (give); cruel asuras heard *dayadhvam* (compassion). The thunder repeats 'da da da'.")

s.match(U2, BRIH, "According to the Brihadaranyaka (1.5.16), match each world with the means of winning it.",
        ["Manushya loka (world of men)", "Pitri loka (world of the ancestors)", "Deva loka (world of the gods)"],
        ["By knowledge (vidya)", "By a son", "By rites (karma)"],
        ["A-ii, B-iii, C-i", "A-iii, B-ii, C-i", "A-ii, B-i, C-iii", "A-i, B-iii, C-ii"],
        "1.5.16: the human world is won through a son, the world of the fathers through rites, the world of the gods "
        "through knowledge — and the world of the gods is the best, so knowledge is praised.")

s.mcq(U2, BRIH, "In the Brihadaranyaka, 'neti neti' (not this, not this) describes:",
      ["The Self, which cannot be described by any positive attribute", "The world, which is unreal",
       "The senses, which cannot grasp objects", "The rituals, which are useless"],
      "2.3.6 and 4.2.4: *sa eṣa neti nety ātmā* — the Self is 'not this, not this'; ungraspable, indestructible, "
      "unattached, unbound.")

s.mcq(U2, BRIH, "Gargi, Ashvala, Uddalaka and Shakalya question Yajnavalkya at the court of which king?",
      ["Janaka of Videha", "Ajatashatru of Kashi", "Ashvapati Kaikeya", "Pravahana Jaivali"],
      "Brihadaranyaka adhyaya 3: at King Janaka's sacrifice, Yajnavalkya claims the thousand cows and is questioned "
      "by Ashvala, Artabhaga, Gargi, Uddalaka Aruni, Shakalya and others.")

s.mcq(U2, BRIH, "To explain how the individual self merges in the Supreme, Yajnavalkya uses the image of:",
      ["A lump of salt dissolving in water", "Sparks rising from a fire", "A spider spinning its web",
       "Rivers flowing into the sea"],
      "Brihadaranyaka 2.4.12: as a lump of salt thrown into water dissolves and cannot be taken out again, so this "
      "great being dissolves. (Sparks from fire and the spider are Mundaka 2.1.1 and 1.1.7; rivers into the sea is "
      "Mundaka 3.2.8.)")

# --- Isha -------------------------------------------------------------------------------

s.mcq(U2, ISHA, "The Isha Upanishad is the fortieth chapter of:",
      ["The Shukla Yajurveda (Vajasaneyi Samhita)", "The Krishna Yajurveda", "The Atharvaveda", "The Samaveda"],
      "The Isha (Ishavasya) Upanishad, 18 mantras, is chapter 40 of the Vajasaneyi Samhita of the Shukla "
      "Yajurveda — the only principal Upanishad that is part of a Samhita.")

s.mcq(U2, ISHA, "According to the Isha Upanishad (mantra 11), what does one cross through avidya?",
      ["Death (mrityu)", "Immortality (amrita)", "Ignorance", "Heaven"],
      "Isha 11: *avidyayā mṛtyuṃ tīrtvā vidyayāmṛtam aśnute* — through avidya (action) one crosses death, through "
      "vidya (knowledge) one attains immortality. The same pattern is given for asambhuti and sambhuti (14).")

s.statements(U2, ISHA, "Which of the following are taught in the Isha Upanishad?",
             ["Enjoy through renunciation (tena tyaktena bhuñjīthāḥ)", "Wish to live a hundred years doing karma",
              "Those who kill the Self go to the asurya worlds", "The two birds on one tree",
              "The seven tongues of fire"],
             ["Only (A), (B) and (C)", "Only (A), (D) and (E)", "Only (B), (C) and (D)", "Only (C), (D) and (E)"],
             "Isha 1 (enjoy by renouncing), 2 (*kurvann eveha karmāṇi jijīviṣec chataṃ samāḥ*) and 3 (*asuryā nāma te "
             "lokāḥ*). The two birds are Mundaka/Shvetashvatara; the seven tongues of fire are Mundaka 1.2.4.")

s.mcq(U2, ISHA, "'hiraṇmayena pātreṇa satyasyāpihitaṃ mukham' (the face of truth is covered by a golden lid) is a "
                "prayer from:",
      ["Isha Upanishad (15)", "Katha Upanishad", "Prashna Upanishad", "Taittiriya Upanishad"],
      "Isha 15: the dying seeker asks Pushan (the sun) to remove the golden lid so that he, devoted to truth, may "
      "see it. Mantras 15–18 are the closing prayers.")

if __name__ == "__main__":
    s.write("yoga-practice-set14.json")
