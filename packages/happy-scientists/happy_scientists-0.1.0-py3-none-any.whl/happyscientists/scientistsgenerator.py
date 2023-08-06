import random


class ScientistsGenerator:

    # based on google search
    adjetives = [
        "adaptable",
        "adventurous",
        "affectionate",
        "ambitious",
        "amiable",
        "friendly",
        "courageous",
        "compassionate",
        "considerate",
        "courageous",
        "courteous",
        "diligent",
        "empathetic",
        "exuberant",
        "frank",
        "generous",
        "gregarious",
        "impartial",
        "intuitive",
        "inventive",
        "passionate",
        "persistent",
        "philosophical",
        "practical",
        "rational",
        "reliable",
        "resourceful",
        "sensible",
        "sincere",
        "sympathetic",
        "unassuming",
        "witty",
        "funny"
    ]
    scientists = [
        "Curie",
        "Turing",
        "Bohr",
        "Darwin",
        "daVinci",
        "Galilei",
        "Tesla",
        "Einstein",
        "Newton",
        "Hawking",
        "Faraday",
        "Pasteur",
        "Edison",
        "Maxwell"
    ]

    mathematicians = [
        "deFermat",
        "Gauss",
        "Euler",
        "Euclides",
        "Leibniz",
        "Riemann",
        "Ramanujan",
        "Arquimedes",
        "Hilbert",
        "Poincare"

    ]

    philosophers = [
        "Platon",
        "Socrates",
        "Aristoteles",
        "Kant",
        "Nietzsche",
        "Descartes",
        "Hume",
        "Wittgenstein",
        "Confucio",
        "Marx",
        "Locke",
        "Seneca",
        "Epicuro",
        "Hobbes",
        "deBeauvoir"
    ]

    people = scientists + mathematicians + philosophers

    @staticmethod
    def __combine(adjetive, name):
        return "{}_{}".format(adjetive, name)
    
    @staticmethod
    def generate_name():
        adjetive = random.choice(ScientistsGenerator.adjetives)
        name = random.choice(ScientistsGenerator.people)
        return ScientistsGenerator.__combine(adjetive, name)

    @staticmethod
    def generate_scientist():
        adjetive = random.choice(ScientistsGenerator.adjetives)
        name = random.choice(ScientistsGenerator.scientists)
        return ScientistsGenerator.__combine(adjetive, name)

    @staticmethod
    def generate_mathematician():
        adjetive = random.choice(ScientistsGenerator.adjetives)
        name = random.choice(ScientistsGenerator.mathematicians)
        return ScientistsGenerator.__combine(adjetive, name)

    @staticmethod
    def generate_philosopher():
        adjetive = random.choice(ScientistsGenerator.adjetives)
        name = random.choice(ScientistsGenerator.philosophers)
        return ScientistsGenerator.__combine(adjetive, name)