from spacy.language import Language

class ComprehensionModel:

    def __init__(self, text: str, sem_model: Language,
            min_activation_score: float, max_active_concepts: int,
            max_dictionary_expansion: int) -> None:
        self.min_activation_score = min_activation_score
        self.max_active_concepts = max_active_concepts
        self.max_dictionary_expansion = max_dictionary_expansion


