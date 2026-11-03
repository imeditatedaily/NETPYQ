"""Builds data/questions/yoga-practice-set13.json: practice set 18, Yoga Units 6, 8, 9 and 10.

Each entry lists the correct option FIRST; the script moves it to a rotating
position (1-4) so answers are spread evenly. Assertion-Reason options keep
NTA's fixed order, so those give the answer number directly.
"""

import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "data" / "questions" / "yoga-practice-set13.json"
NOTE = ("Practice set 18 (Therapeutic yoga, applications of yoga, practical yoga and allied sciences). "
        "Written fresh for this app in NTA's pattern from standard references; not taken from any book or quiz sheet.")

U6 = "Yoga Unit 6: Allied Sciences: Psychology, Human Biology, Diet and Nutrition"
U8 = "Yoga Unit 8: Therapeutic Yoga"
U9 = "Yoga Unit 9: Applications of Yoga"
U10 = "Yoga Unit 10: Practical Yoga: Shatkarma, Asana, Pranayama, Mudra, Bandha, Dhyana"

AR = ["Both (A) and (R) are true and (R) is the correct explanation of (A)",
      "Both (A) and (R) are true but (R) is NOT the correct explanation of (A)",
      "(A) is true but (R) is false",
      "(A) is false but (R) is true"]
PROMPT = "Choose the correct answer from the options given below:"

Q = []


def mcq(unit, topic, text, options, why):
    Q.append(dict(unit=unit, topic=topic, type="mcq", text=text, options=options, why=why))


def statements(unit, topic, text, items, options, why):
    Q.append(dict(unit=unit, topic=topic, type="statements", text=text, items=items, options=options, why=why))


def sequence(unit, topic, text, items, options, why):
    Q.append(dict(unit=unit, topic=topic, type="sequence", text=text, items=items, options=options, why=why))


def match(unit, topic, text, l1, l2, options, why, t1="List I", t2="List II"):
    Q.append(dict(unit=unit, topic=topic, type="match", text=text, l1=l1, l2=l2, t1=t1, t2=t2, options=options, why=why))


def ar(unit, topic, a, r, answer, why):
    Q.append(dict(unit=unit, topic=topic, type="assertion_reason", a=a, r=r, answer=answer, why=why))


# --- Unit 8: Therapeutic yoga -----------------------------------------------------------

mcq(U8, "Evidence-based integrated yoga therapy",
    "The Integrated Approach of Yoga Therapy (IAYT) was developed at which institution?",
    ["S-VYASA (Swami Vivekananda Yoga Anusandhana Samsthana), Bengaluru", "Kaivalyadhama, Lonavala",
     "Bihar School of Yoga, Munger", "Krishnamacharya Yoga Mandiram, Chennai"],
    "IAYT was developed by H. R. Nagendra and R. Nagarathna at Vivekananda Kendra's yoga research wing, which became "
    "S-VYASA in Bengaluru. It treats the whole person through all five koshas rather than prescribing single asanas.")

mcq(U8, "Evidence-based integrated yoga therapy",
    "The Integrated Approach of Yoga Therapy plans practices for a patient on which framework?",
    ["Pancha kosha (five sheaths of the Taittiriya Upanishad)", "Tridosha of Ayurveda", "Triguna of Samkhya",
     "The eight limbs of the Yoga Sutra"],
    "IAYT maps practices onto the five koshas of the Taittiriya Upanishad: annamaya, pranamaya, manomaya, "
    "vijnanamaya and anandamaya, so that body, breath, mind, understanding and joy are all addressed.")

match(U8, "Evidence-based integrated yoga therapy",
      "Match each kosha with the IAYT practices aimed at it.",
      ["Annamaya kosha", "Pranamaya kosha", "Manomaya kosha", "Vijnanamaya kosha"],
      ["Pranayama and kriyas", "Asanas, loosening practices and diet", "Notional correction through self-study and counselling",
       "Meditation and dharana"],
      ["A-ii, B-i, C-iv, D-iii", "A-i, B-ii, C-iv, D-iii", "A-ii, B-iv, C-i, D-iii", "A-iii, B-i, C-ii, D-iv"],
      "Annamaya (body) → asanas and diet; pranamaya (vital energy) → pranayama and kriyas; manomaya (mind) → "
      "meditation and dharana; vijnanamaya (intellect) → jnana yoga, i.e. notional correction by self-study and counselling.")

mcq(U8, "Yoga therapy: hypertension",
    "Which practice is usually avoided in uncontrolled hypertension?",
    ["Kapalabhati", "Shavasana", "Nadi shodhana pranayama", "Bhramari pranayama"],
    "Kapalabhati's forceful, rapid exhalations raise intra-abdominal and intrathoracic pressure and stimulate the "
    "sympathetic system, so it is avoided in uncontrolled hypertension, as are inversions and breath retention.")

statements(U8, "Yoga therapy: hypertension",
           "Which of the following practices are commonly recommended for people with hypertension?",
           ["Shavasana", "Bhramari pranayama", "Shirshasana", "Nadi shodhana without breath retention", "Bhastrika"],
           ["Only (A), (B) and (D)", "Only (A), (C) and (E)", "Only (B), (C) and (D)", "Only (A), (D) and (E)"],
           "Relaxation (shavasana), humming breath (bhramari) and slow alternate-nostril breathing calm the sympathetic "
           "system and lower blood pressure. Shirshasana (an inversion) and bhastrika (vigorous breathing) are avoided.")

ar(U8, "Yoga therapy: respiratory disorders",
   "Breathing practices with prolonged exhalation are useful in bronchial asthma.",
   "Slow, prolonged exhalation reduces air trapping and calms the over-active stress response that narrows the airways.",
   1,
   "Both are true, and (R) is why (A) works: lengthening exhalation empties the lungs more completely, and slow "
   "breathing shifts the balance towards the parasympathetic system, easing bronchospasm triggered by anxiety.")

mcq(U8, "Yoga therapy: respiratory disorders",
    "Which kriya is used in yoga therapy for bronchial asthma to clear mucus and give reflex relief of bronchospasm?",
    ["Vamana dhauti (kunjal)", "Nauli", "Basti", "Trataka"],
    "In vamana dhauti (kunjal) the practitioner drinks lukewarm saline water and vomits it out. It clears mucus and, "
    "through a vagal reflex, helps relax the bronchi, so it is part of the IAYT module for asthma.")

mcq(U8, "Yoga therapy: musculoskeletal disorders",
    "In the acute stage of lumbar disc prolapse, which group of asanas is avoided?",
    ["Forward bends such as paschimottanasana", "Gentle back bends such as bhujangasana", "Prone relaxation in makarasana",
     "Supine relaxation in shavasana"],
    "Forward flexion squeezes the front of the disc and pushes the nucleus further backwards onto the nerve roots. "
    "Gentle extension (bhujangasana, makarasana) and relaxation are preferred.")

mcq(U8, "Yoga therapy: musculoskeletal disorders",
    "Which asana is contraindicated in cervical spondylosis?",
    ["Halasana", "Bhujangasana", "Makarasana", "Shavasana"],
    "Halasana (like sarvangasana) puts the neck in strong flexion under body weight, which strains the cervical discs "
    "and joints. Neck-friendly extension and relaxation postures are used instead.")

mcq(U8, "Yoga therapy: endocrine and metabolic disorders",
    "Which asana is commonly included in yoga modules for type 2 diabetes for its twisting action on the abdomen?",
    ["Ardha matsyendrasana", "Shirshasana", "Tadasana", "Shavasana"],
    "Twists such as ardha matsyendrasana compress and massage the abdominal organs, including the pancreas region. "
    "Diabetes modules also use mandukasana, dhanurasana, kapalabhati and relaxation.")

mcq(U8, "Yoga therapy: endocrine and metabolic disorders",
    "Which asana is traditionally recommended for the health of the thyroid gland?",
    ["Sarvangasana", "Vrikshasana", "Tadasana", "Vajrasana"],
    "Sarvangasana (shoulder stand) presses the chin towards the chest, compressing the front of the neck where the "
    "thyroid lies; yoga texts and teachers therefore traditionally prescribe it for thyroid health.")

ar(U8, "Yoga therapy: psychiatric disorders",
   "In depression, energising practices such as surya namaskar and kapalabhati are usually given before relaxation.",
   "Depression involves low arousal and psychomotor slowing.",
   1,
   "Both are true, and (R) explains (A): a person with depression is under-aroused, so the session first raises energy "
   "with dynamic practices and only then moves to relaxation. In anxiety the order is the reverse.")

mcq(U8, "Yoga therapy: gynaecological and urinary disorders",
    "Which practice is generally avoided during menstruation?",
    ["Sarvangasana", "Baddha konasana", "Shavasana", "Supta baddha konasana"],
    "Inversions such as sarvangasana and shirshasana are traditionally avoided during menstruation; gentle hip-opening "
    "postures and relaxation are recommended instead.")

statements(U8, "Yoga therapy: gynaecological and urinary disorders",
           "Which of the following are avoided during pregnancy?",
           ["Kapalabhati", "Nauli", "Bhramari pranayama", "Closed twists that compress the abdomen", "Lying on the left side for relaxation"],
           ["Only (A), (B) and (D)", "Only (A), (C) and (E)", "Only (B), (C) and (D)", "Only (C), (D) and (E)"],
           "Kapalabhati and nauli put strong pressure on the abdomen, and closed twists compress the uterus, so all three "
           "are avoided. Bhramari and side-lying (left) relaxation are safe and often recommended.")

# --- Unit 9: Applications of yoga ----------------------------------------------------------

mcq(U9, "Methods of teaching yoga",
    "In the whole-part-whole method of teaching an asana, what does the teacher do first?",
    ["Demonstrates the complete asana", "Teaches each step separately without showing the whole",
     "Asks students to try it without instruction", "Explains the theory of the asana only"],
    "The teacher first shows the whole posture, then breaks it into parts that are practised one by one, and finally "
    "has students perform the whole asana again.")

sequence(U9, "Yoga classroom and lesson plan",
         "Arrange the parts of a yoga session in the order of the Common Yoga Protocol.",
         ["Pranayama", "Prayer", "Asanas", "Dhyana", "Loosening practices (chalana kriya)"],
         ["(B), (E), (C), (A), (D)", "(B), (C), (E), (A), (D)", "(E), (B), (C), (D), (A)", "(B), (E), (A), (C), (D)"],
         "The Common Yoga Protocol runs: prayer → loosening practices → asanas → kapalabhati and pranayama → dhyana → "
         "sankalpa → shanti path.")

mcq(U9, "Contemporary yogic practices",
    "How long is the Common Yoga Protocol of the Ministry of AYUSH, used for the International Day of Yoga?",
    ["45 minutes", "30 minutes", "60 minutes", "90 minutes"],
    "The Common Yoga Protocol is a 45-minute sequence of prayer, loosening practices, asanas, kapalabhati, pranayama, "
    "dhyana, sankalpa and shanti path.")

mcq(U9, "Contemporary yogic practices",
    "In which year did the UN General Assembly declare 21 June the International Day of Yoga?",
    ["2014", "2015", "2013", "2016"],
    "The UN General Assembly adopted resolution 69/131 on 11 December 2014. The first International Day of Yoga was "
    "celebrated on 21 June 2015.")

mcq(U9, "Scientific study of meditation",
    "Who coined the term 'relaxation response'?",
    ["Herbert Benson", "Jon Kabat-Zinn", "Hans Selye", "Robert Keith Wallace"],
    "Herbert Benson of Harvard described the relaxation response (1975): a fall in heart rate, breathing rate, oxygen "
    "use and blood pressure, the physiological opposite of the fight-or-flight response.")

match(U9, "Scientific study of meditation",
      "Match the researcher with the work they are known for.",
      ["Jon Kabat-Zinn", "Herbert Benson", "Hans Selye", "Robert Keith Wallace"],
      ["General adaptation syndrome", "Physiological effects of Transcendental Meditation (1970)",
       "Mindfulness-Based Stress Reduction (MBSR)", "The relaxation response"],
      ["A-iii, B-iv, C-i, D-ii", "A-iv, B-iii, C-i, D-ii", "A-iii, B-i, C-iv, D-ii", "A-ii, B-iv, C-iii, D-i"],
      "Kabat-Zinn founded MBSR (1979); Benson described the relaxation response; Selye described the general "
      "adaptation syndrome of stress; Wallace published the first physiological study of TM in Science (1970).")

mcq(U9, "Scientific study of meditation",
    "Lutz and colleagues (2004) reported high-amplitude gamma synchrony in long-term practitioners of which meditation?",
    ["Compassion meditation of Tibetan Buddhist monks", "Transcendental Meditation", "Zen sitting (zazen)", "Mantra japa"],
    "Lutz, Davidson and colleagues found unusually strong gamma-band synchrony in EEG of Tibetan Buddhist monks during "
    "non-referential compassion meditation (PNAS, 2004).")

mcq(U9, "Contemporary yogic practices",
    "Cyclic meditation, which alternates stimulating and calming practices, was developed at:",
    ["S-VYASA, Bengaluru", "Bihar School of Yoga", "Kaivalyadhama", "Patanjali Yogpeeth"],
    "Cyclic meditation was developed by H. R. Nagendra at S-VYASA from a Mandukya Karika idea: alternate stimulation "
    "and calming lead to deep rest.")

mcq(U9, "Contemporary yogic practices",
    "Who developed the modern practice of Yoga Nidra?",
    ["Swami Satyananda Saraswati", "Swami Kuvalayananda", "Swami Sivananda", "B. K. S. Iyengar"],
    "Swami Satyananda Saraswati of the Bihar School of Yoga systematised Yoga Nidra in the 1960s from tantric nyasa "
    "practices; it has stages such as sankalpa, rotation of consciousness and visualisation.")

match(U9, "Contemporary yogic practices",
      "Match the institution with its founder.",
      ["Kaivalyadhama, Lonavala", "The Yoga Institute, Santacruz", "Bihar School of Yoga, Munger",
       "Krishnamacharya Yoga Mandiram, Chennai"],
      ["T. K. V. Desikachar", "Shri Yogendra", "Swami Kuvalayananda", "Swami Satyananda Saraswati"],
      ["A-iii, B-ii, C-iv, D-i", "A-ii, B-iii, C-iv, D-i", "A-iii, B-iv, C-ii, D-i", "A-iv, B-ii, C-iii, D-i"],
      "Kuvalayananda founded Kaivalyadhama (1924); Shri Yogendra the Yoga Institute (1918), the oldest organised yoga "
      "centre; Satyananda the Bihar School (1960s); Desikachar the KYM (1976) in his father's name.")

mcq(U9, "Yoga in education",
    "Integral education, built on developing the physical, vital, mental, psychic and spiritual being, was proposed by:",
    ["Sri Aurobindo and the Mother", "Swami Vivekananda", "Mahatma Gandhi", "Rabindranath Tagore"],
    "Sri Aurobindo and the Mother proposed integral education with five aspects (physical, vital, mental, psychic and "
    "spiritual), put into practice at the Sri Aurobindo International Centre of Education, Puducherry.")

match(U9, "Yoga in education",
      "Match the thinker with his idea of education.",
      ["Swami Vivekananda", "Sri Aurobindo", "Mahatma Gandhi", "Rabindranath Tagore"],
      ["Nai Talim (basic education through productive craft)", "Visva-Bharati and learning in harmony with nature",
       "'Education is the manifestation of the perfection already in man'", "Integral education"],
      ["A-iii, B-iv, C-i, D-ii", "A-iv, B-iii, C-i, D-ii", "A-iii, B-iv, C-ii, D-i", "A-i, B-iv, C-iii, D-ii"],
      "Vivekananda: education manifests the perfection already in man; Aurobindo: integral education; Gandhi: Nai Talim "
      "(Wardha scheme, 1937); Tagore: Shantiniketan and Visva-Bharati.")

mcq(U9, "Methods of teaching yoga",
    "Learning to perform an asana correctly belongs mainly to which domain of Bloom's taxonomy?",
    ["Psychomotor", "Cognitive", "Affective", "Conative"],
    "Bloom's taxonomy has three domains: cognitive (knowing), affective (feeling and values) and psychomotor (physical "
    "skills). Performing an asana correctly is a psychomotor skill.")

mcq(U9, "Methods of teaching yoga",
    "Which of the following is a projected teaching aid?",
    ["Overhead projector", "Chart", "Model", "Blackboard"],
    "Projected aids throw an image on a screen (overhead projector, slide projector, LCD projector). Charts, models and "
    "the blackboard are non-projected aids.")

# --- Unit 10: Practical yoga -------------------------------------------------------------

mcq(U10, "Asanas: classification and effects",
    "In Swami Kuvalayananda's classification, makarasana belongs to which group?",
    ["Relaxative asanas", "Meditative asanas", "Cultural asanas", "Balancing asanas"],
    "Kuvalayananda grouped asanas as meditative, cultural and relaxative. Makarasana and shavasana are relaxative.")

statements(U10, "Asanas: classification and effects",
           "Which of the following are meditative asanas?",
           ["Padmasana", "Siddhasana", "Swastikasana", "Dhanurasana", "Bhujangasana"],
           ["Only (A), (B) and (C)", "Only (A), (D) and (E)", "Only (B), (C) and (E)", "Only (C), (D) and (E)"],
           "Padmasana, siddhasana and swastikasana are seated postures that keep the spine erect and the body still for "
           "long periods. Dhanurasana and bhujangasana are cultural (body-conditioning) asanas.")

mcq(U10, "Shatkarma: practice and benefits",
    "Sutra neti is done with:",
    ["A rubber catheter or a waxed cotton thread", "A strip of cloth fifteen hastas long", "Lukewarm water poured through the mouth",
     "Ghee poured into the nostrils"],
    "In sutra neti a soft rubber catheter (traditionally a waxed cotton thread) is passed through a nostril and drawn "
    "out of the mouth. Jala neti uses lukewarm saline water.")

mcq(U10, "Shatkarma: practice and benefits",
    "According to the Hatha Pradipika, how long is the cloth used for vastra dhauti?",
    ["Fifteen hastas", "Ten hastas", "Twenty hastas", "Twenty-five hastas"],
    "HP 2.24: a moist cloth four fingers wide and fifteen hastas long (catur-aṅgula-vistāraṁ hasta-pañcadaśāyatam) is "
    "slowly swallowed and drawn out.")

ar(U10, "Shatkarma: practice and benefits",
   "Uddiyana bandha should be mastered before learning nauli.",
   "Nauli isolates the rectus abdominis muscles while the abdomen is held in uddiyana with the breath held out.",
   1,
   "Both are true, and (R) explains (A): nauli starts from the uddiyana position (exhaled, abdomen drawn in and up), "
   "then contracts the rectus abdominis in the centre (madhyama) or to one side (vama, dakshina).")

mcq(U10, "Shatkarma: practice and benefits",
    "In kapalabhati:",
    ["Exhalation is active and forceful; inhalation is passive", "Inhalation is active; exhalation is passive",
     "Both inhalation and exhalation are slow and active", "The breath is held after each inhalation"],
    "Kapalabhati is a series of quick, forceful exhalations by the abdominal muscles; inhalation follows passively as "
    "the muscles relax.")

mcq(U10, "Shatkarma: practice and benefits",
    "According to the Hatha Pradipika, trataka removes:",
    ["Eye diseases and sloth (tandra)", "Diseases of the stomach", "Disorders of kapha in the throat", "Diseases of the anus"],
    "HP 2.32: trataka frees one from eye diseases and shuts the door on sloth and the like (mocanaṁ netra-rogāṇāṁ "
    "tandrādīnāṁ kapāṭakam).")

match(U10, "Mudras and bandhas: practice and benefits",
      "Match each bandha with how it is done.",
      ["Mula bandha", "Uddiyana bandha", "Jalandhara bandha", "Jihva bandha"],
      ["The chin is pressed against the chest", "The tongue is pressed against the palate",
       "The perineum and anal sphincter are contracted", "The abdomen is drawn in and up with the breath held out"],
      ["A-iii, B-iv, C-i, D-ii", "A-iv, B-iii, C-i, D-ii", "A-iii, B-i, C-iv, D-ii", "A-ii, B-iv, C-iii, D-i"],
      "Mula bandha contracts the perineum; uddiyana draws the abdomen in and up after exhalation; jalandhara presses "
      "the chin to the chest; jihva bandha presses the tongue against the palate.")

match(U10, "Mudras and bandhas: practice and benefits",
      "Match the mudra with its practice.",
      ["Shambhavi mudra", "Agochari (nasikagra drishti)", "Khechari mudra", "Jnana mudra"],
      ["Gazing at the tip of the nose", "Tip of the index finger touching the tip of the thumb",
       "Gazing at the eyebrow centre", "Tongue turned back into the cavity above the palate"],
      ["A-iii, B-i, C-iv, D-ii", "A-i, B-iii, C-iv, D-ii", "A-iii, B-iv, C-i, D-ii", "A-iii, B-i, C-ii, D-iv"],
      "Shambhavi: gaze at the eyebrow centre; agochari: gaze at the nose tip; khechari: tongue rolled back into the "
      "nasal cavity; jnana mudra: index fingertip touching the thumb tip.")

sequence(U10, "Asanas: classification and effects",
         "Arrange the first four positions of surya namaskar (Bihar School sequence) in order.",
         ["Padahastasana", "Pranamasana", "Ashwa sanchalanasana", "Hasta uttanasana"],
         ["(B), (D), (A), (C)", "(B), (A), (D), (C)", "(D), (B), (A), (C)", "(B), (D), (C), (A)"],
         "Surya namaskar begins: pranamasana (prayer pose) → hasta uttanasana (raised arms) → padahastasana (hand to "
         "foot) → ashwa sanchalanasana (equestrian pose).")

# --- Unit 6: Allied sciences -------------------------------------------------------------

ar(U6, "Human biology: endocrine system and stress",
   "Cortisol, the main stress hormone, is secreted by the adrenal medulla.",
   "The adrenal medulla secretes adrenaline and noradrenaline.",
   4,
   "(A) is false: cortisol comes from the adrenal cortex (zona fasciculata). (R) is true: the medulla secretes the "
   "catecholamines adrenaline and noradrenaline.")

sequence(U6, "Human biology: endocrine system and stress",
         "Arrange the steps of the stress (HPA axis) response in order.",
         ["The pituitary releases ACTH", "Cortisol is released into the blood", "The hypothalamus releases CRH",
          "The adrenal cortex is stimulated"],
         ["(C), (A), (D), (B)", "(A), (C), (D), (B)", "(C), (D), (A), (B)", "(D), (C), (A), (B)"],
         "Hypothalamus → CRH → anterior pituitary → ACTH → adrenal cortex → cortisol.")

ar(U6, "Human biology: nervous system",
   "Slow breathing lowers the heart rate.",
   "Slow breathing increases vagal (parasympathetic) activity.",
   1,
   "Both are true, and (R) explains (A): slow breathing raises vagal tone, and the vagus nerve slows the heart's "
   "pacemaker (SA node).")

mcq(U6, "Human biology: respiratory system",
    "The tidal volume of a healthy adult at rest is about:",
    ["500 mL", "150 mL", "1,200 mL", "3,000 mL"],
    "Tidal volume, the air moved in one quiet breath, is about 500 mL; about 150 mL of it stays in the dead space of the "
    "airways. Residual volume is about 1,200 mL.")

mcq(U6, "Human biology: digestive system",
    "Bile is produced by the:",
    ["Liver", "Gall bladder", "Pancreas", "Duodenum"],
    "The liver produces bile; the gall bladder only stores and concentrates it and releases it into the duodenum.")

sequence(U6, "Psychology: personality theories",
         "Arrange the needs in Maslow's hierarchy from the lowest to the highest.",
         ["Esteem", "Physiological", "Self-actualisation", "Safety", "Love and belonging"],
         ["(B), (D), (E), (A), (C)", "(B), (E), (D), (A), (C)", "(D), (B), (E), (A), (C)", "(B), (D), (A), (E), (C)"],
         "Maslow's hierarchy: physiological → safety → love and belonging → esteem → self-actualisation.")

mcq(U6, "Psychology: memory and cognition",
    "The multi-store model of memory (sensory, short-term and long-term stores) was proposed by:",
    ["Atkinson and Shiffrin", "Baddeley and Hitch", "Craik and Lockhart", "Hermann Ebbinghaus"],
    "Atkinson and Shiffrin (1968). Baddeley and Hitch proposed working memory; Craik and Lockhart levels of processing; "
    "Ebbinghaus the forgetting curve.")

match(U6, "Psychology: personality theories",
      "Match the psychologist with his concept.",
      ["Carl Jung", "Hans Eysenck", "Sigmund Freud", "Gordon Allport"],
      ["Cardinal, central and secondary traits", "Id, ego and superego", "Introversion and extraversion as attitudes",
       "Extraversion, neuroticism and psychoticism"],
      ["A-iii, B-iv, C-ii, D-i", "A-iv, B-iii, C-ii, D-i", "A-iii, B-ii, C-iv, D-i", "A-iii, B-iv, C-i, D-ii"],
      "Jung: introversion/extraversion; Eysenck: E, N and P dimensions; Freud: id, ego and superego; Allport: cardinal, "
      "central and secondary traits.")

match(U6, "Nutrition: vitamins and deficiencies",
      "Match the vitamin with the disease its deficiency causes.",
      ["Vitamin B1 (thiamine)", "Vitamin C", "Vitamin B12", "Vitamin D"],
      ["Pernicious anaemia", "Rickets", "Beriberi", "Scurvy"],
      ["A-iii, B-iv, C-i, D-ii", "A-iv, B-iii, C-i, D-ii", "A-iii, B-i, C-iv, D-ii", "A-i, B-iv, C-iii, D-ii"],
      "Thiamine → beriberi; vitamin C → scurvy; B12 → pernicious anaemia; vitamin D → rickets (osteomalacia in adults).")

mcq(U6, "Nutrition: energy and metabolism",
    "About how much energy does 1 g of fat provide?",
    ["9 kcal", "4 kcal", "7 kcal", "17 kcal"],
    "Fat gives about 9 kcal per gram; carbohydrate and protein about 4 kcal per gram; alcohol about 7 kcal per gram.")


def build() -> list[dict]:
    out, pos = [], 0
    for n, q in enumerate(Q, start=1):
        base = {"id": f"YOGA-PRAC13-{n:03d}", "subject": "yoga", "paper": "Paper 2", "question_no": n,
                "source": {"type": "practice", "note": NOTE}, "answer_source": "unverified",
                "macro_unit": q["unit"], "micro_topic": q["topic"], "question_type": q["type"]}
        if q["type"] == "assertion_reason":
            base.update(question_text="Given below are two statements: one is labelled as Assertion (A) and the other "
                                      "is labelled as Reason (R).",
                        assertion=q["a"], reason=q["r"],
                        prompt="In the light of the above statements, choose the correct answer from the options given below:",
                        options=AR, correct_answer=q["answer"])
            label = AR[q["answer"] - 1]
        else:
            opts = list(q["options"])
            correct = opts[0]
            target = pos % 4
            pos += 1
            rest = opts[1:]
            opts = rest[:target] + [correct] + rest[target:]
            base.update(question_text=q["text"], options=opts, correct_answer=target + 1)
            label = correct
            if q["type"] in ("statements", "sequence"):
                base.update(items=q["items"], prompt=PROMPT)
            if q["type"] == "match":
                base.update(lists={"list_i": {"title": q["t1"], "items": q["l1"]},
                                   "list_ii": {"title": q["t2"], "style": "roman", "items": q["l2"]}},
                            prompt=PROMPT)
        base["detailed_explanation"] = f"**Answer: ({base['correct_answer']}) {label}.**\n\n{q['why']}"
        out.append(base)
    return out


if __name__ == "__main__":
    qs = build()
    OUT.write_text(json.dumps(qs, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(len(qs), "questions written")
