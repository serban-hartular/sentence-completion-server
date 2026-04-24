from sequences import QuestionSequenceFactory


class RoAdjUnderline(QuestionSequenceFactory):
    CLASS_NAME = 'RO: Adjectivul: subliniază în text'
    SCREEN_KIND = "underline-from-text"
    COLOR = '#11aa11'

    def __init__(self):
        self.count = -1

    def get_next_question(self, previous_was_good : bool = True) -> dict|None:
        if previous_was_good:
            self.count += 1
        if self.count > 0:
            return None
        
        text = "Un băiat frumos s-a dus repede la marea cea rece .".split()
        adjs = ["frumos", 'rece']
        text_chunks = [{'kind':'markable', 'text':t, 'spaceAfter':True,
                         'markStyle':'underline'}
                       for t in text]

        return dict(
            prompt='Subliniați adjectivele din următorul text:',
            sourceText=text_chunks,
            correctMarkedWords=adjs,
        )
