"""UGC NET Paper II syllabus units for Yoga (subject code 100) and
Indian Knowledge System (subject code 103).

A question's ``macro_unit`` must be one of the labels built here, for
example "Yoga Unit 4: Patanjala Yoga Sutra" or "IKS Unit 3: Astronomy".
"""

from dataclasses import dataclass

SYLLABUS_NOTE = (
    "Unit titles follow the NTA syllabi for Yoga (code 100) and Indian Knowledge "
    "System (code 103) as published by exam portals. Check them against the "
    "official PDFs at ugcnet.nta.ac.in before relying on the exact wording."
)


@dataclass(frozen=True, slots=True)
class Subject:
    id: str
    name: str
    short: str
    code: str
    units: tuple[str, ...]  # the title of unit n is units[n - 1]

    def unit_label(self, no: int) -> str:
        return f"{self.short} Unit {no}: {self.units[no - 1]}"

    @property
    def unit_labels(self) -> tuple[str, ...]:
        return tuple(self.unit_label(n) for n in range(1, len(self.units) + 1))

    @property
    def display(self) -> str:
        return f"{self.name} ({self.code})"


YOGA = Subject(
    id="yoga",
    name="Yoga",
    short="Yoga",
    code="100",
    units=(
        "Fundamentals of Yoga",
        "Yoga Texts I: Principal Upanishads, Bhagavad Gita and Yoga Vasishtha",
        "Yoga Texts II: Yoga Upanishads",
        "Patanjala Yoga Sutra",
        "Hatha Yoga Texts",
        "Allied Sciences: Psychology, Human Biology, Diet and Nutrition",
        "Yoga and Health",
        "Therapeutic Yoga",
        "Applications of Yoga",
        "Practical Yoga: Shatkarma, Asana, Pranayama, Mudra, Bandha, Dhyana",
    ),
)

IKS = Subject(
    id="iks",
    name="Indian Knowledge System",
    short="IKS",
    code="103",
    units=(
        "Indian Philosophical Systems (Part A)",
        "Indian Philosophical Systems (Part B)",
        "Astronomy",
        "Health and Well-being",
        "Architecture",
        "Mathematics",
        "Chemistry and Metallurgy",
        "Life Sciences, Agriculture and Ecology",
        "Kala (Arts)",
        "Ancient India and World History",
    ),
)

SUBJECTS: dict[str, Subject] = {s.id: s for s in (YOGA, IKS)}

# "Yoga Unit 4: Patanjala Yoga Sutra" -> (YOGA, 4)
UNIT_INDEX: dict[str, tuple[Subject, int]] = {
    s.unit_label(n): (s, n) for s in SUBJECTS.values() for n in range(1, len(s.units) + 1)
}
