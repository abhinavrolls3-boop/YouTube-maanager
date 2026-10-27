"""Small curated fact library; works offline and does not call a model API."""
from dataclasses import dataclass
from .content import Fact, validate_fact

@dataclass(frozen=True)
class Topic:
    slug: str
    fact: Fact

TOPICS = (
    Topic("astronauts-float", Fact(
        "Why do astronauts look like they float?",
        "Astronauts appear to float because they and their spacecraft are falling around Earth together.",
        "Gravity is still acting in orbit. The spacecraft moves forward fast enough to keep falling around Earth instead of hitting the ground. Astronauts experience this continuous free fall as weightlessness.",
        ("space", "science", "facts", "astronauts", "education"),
        ("https://www.nasa.gov/learning-resources/for-kids-and-students/what-is-microgravity-grades-5-8/",))),
    Topic("octopus-hearts", Fact(
        "How many hearts does an octopus have?",
        "An octopus has three hearts, and two help move blood through its gills.",
        "Two hearts pump blood to the gills, where it picks up oxygen. A third heart sends oxygen-rich blood to the rest of the body. This is one of the unusual features of octopus biology.",
        ("animals", "octopus", "science", "facts", "education"),
        ("https://ocean.si.edu/ocean-life/invertebrates/octopuses-squids-and-relatives",))),
    Topic("venus-day", Fact(
        "Is a day on Venus longer than its year?",
        "Yes. Venus takes longer to rotate once than it takes to orbit the Sun.",
        "Venus rotates very slowly. One rotation takes about 243 Earth days, while one trip around the Sun takes about 225 Earth days. That makes its rotation period longer than its orbital period.",
        ("space", "venus", "astronomy", "facts", "science"),
        ("https://science.nasa.gov/venus/venus-facts/",))),
    Topic("sharks-older", Fact(
        "Were sharks around before trees?",
        "Sharks as a group are older than the first trees.",
        "Shark ancestors appeared in the fossil record hundreds of millions of years ago. The earliest known trees appeared later, so sharks predate trees in Earth's history. Scientists update these dates as new fossils are found.",
        ("sharks", "animals", "history", "science", "facts"),
        ("https://www.amnh.org/explore/ology/marine-biology/all-about-sharks",))),
    Topic("honey", Fact(
        "Why can honey last a very long time?",
        "Honey resists many microbes because it has little available water and is naturally acidic.",
        "Honey's low water availability, acidity, and other properties make it difficult for many microbes to grow. It can still become contaminated or change, so storage and food safety matter.",
        ("food", "science", "honey", "facts", "education"),
        ("https://pmp.ars.usda.gov/WaterActivity.aspx",))),
    Topic("moon-drifting", Fact(
        "Is the Moon slowly moving away from Earth?",
        "Yes. The Moon is gradually moving farther from Earth by about 3.8 centimeters each year.",
        "Measurements using laser reflections from equipment left on the Moon show that its average distance from Earth is increasing. Tides transfer a small amount of energy from Earth's rotation to the Moon's orbit. The change is tiny each year, but it adds up over long periods.",
        ("moon", "space", "astronomy", "science", "facts"),
        ("https://science.nasa.gov/moon/tidal-locking/", "https://www.jpl.nasa.gov/news/the-apollo-experiment-that-keeps-on-giving/"))),
    Topic("jupiter-red-spot", Fact(
        "What is Jupiter's Great Red Spot?",
        "Jupiter's Great Red Spot is a huge, long-lived storm in the planet's atmosphere.",
        "Astronomers have observed this enormous storm for centuries. NASA describes it as a giant rotating storm system, larger than Earth. Its appearance and size can change, so avoid treating older measurements as a permanent exact size.",
        ("jupiter", "space", "astronomy", "science", "facts"),
        ("https://science.nasa.gov/asset/hubble/the-great-red-spot-an-ancient-storm-in-jupiters-atmosphere/",))),
)

def all_topics():
    for topic in TOPICS:
        validate_fact(topic.fact)
    return TOPICS

def get_topic(slug: str) -> Topic:
    for topic in all_topics():
        if topic.slug == slug:
            return topic
    choices = ", ".join(t.slug for t in TOPICS)
    raise ValueError(f"Unknown topic '{slug}'. Available topics: {choices}")
