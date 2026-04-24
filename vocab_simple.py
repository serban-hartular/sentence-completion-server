
import dataclasses

from sequences import QuestionData, QuestionSequenceFactory
import random
from utils import getkwarg
import utils

@dataclasses.dataclass
class VocabEntry:
    word : str
    image : str
    pron : str = ''

ANIMALS_EN = ['turtle', 'budgie', 'dog', 'guinea pig', 'horse', 'mouse', 'parrot', 'rabbit',
           'tortoise', 'cat', 'goldfish', 'hamster']

ANIMALS_EN_VOCAB = [VocabEntry(word=w, image=f'/images/en/animals/{w.replace(' ', '_')}.png',
                               pron=f'/pron/en/{w.replace(' ', '_')}.m4a') for w in ANIMALS_EN]

FURNITURE_EN = ['bed', 'cupboard', 'fridge', 'mirror', 'sofa', 'cooker',
                'curtain', 'lamp', 'rug', 'wardrobe']

FURNITURE_EN_VOCAB = [VocabEntry(word=w,
                        image=f'/images/en/furniture/{w.replace(' ', '_')}.jpeg',
                        pron=f'/pron/en/{w.replace(' ', '_')}.m4a')
                            for w in FURNITURE_EN]

NOUNS_FR = ['fleur', 'soleil', 'stylo', 'élèves',
                      'crayon', 'étoile', 'rose', 'métro',]

def fr2nodiacritics(w : str) -> str:
    return w.replace(' ', '_').replace('é', 'e').replace('è', 'e')

NOUNS_FR_VOCAB = [VocabEntry(word=w,
                        image=f'/images/{fr2nodiacritics(w)}.png',
                        pron=f'/pron/fr/{fr2nodiacritics(w)}.m4a')
                            for w in NOUNS_FR]

VocabArgs = [dict(vocab=ANIMALS_EN_VOCAB, seq_name='EN: Animals Vocabulary', color=utils.ENGL_COLOR),
             dict(vocab=FURNITURE_EN_VOCAB, seq_name='EN: Furniture Vocabulary', color=utils.ENGL_COLOR),
             dict(vocab=NOUNS_FR_VOCAB, seq_name='FR: Vocabulaire Simple', color=utils.FR_COLOR),]

class VocabSimple(QuestionSequenceFactory):
    def __init__(self, **kwargs) -> None:
        self.vocab : list[VocabEntry] = list(getkwarg(kwargs, 'vocab', exception='No vocab provided!'))
        self.seq_name = getkwarg(kwargs, 'seq_name', exception='No name provided!')
        self.screen_kind = 'vocab'
        self.color = getkwarg(kwargs, 'color', default='#555555')

        self.fit = getkwarg(kwargs, 'per_screen', default=3, typecheck=int)
        random.shuffle(self.vocab)
        self.index = -self.fit

    def get_next_question(self, previous_was_good: bool = True) -> dict | None:
        if previous_was_good:
            self.index += self.fit
        if self.index >= len(self.vocab):
            return None
        current_vocab = [e.word for e in self.vocab[self.index:self.index+self.fit]]
        return dict(prompt='Potriviți cuvintele:',
                    slotCount=len(current_vocab),
                    targets=[{'imageId':w, 'slotIndex':i} for i, w in enumerate(current_vocab)],
                    bankWords=current_vocab,
                    correct=current_vocab,
                    pronunciations={rec.word:rec.pron for rec in self.vocab if rec.word in current_vocab},
                    images={rec.word:rec.image for rec in self.vocab if rec.word in current_vocab},
                )
    
    def get_screen_kind(self) -> str:
        return self.screen_kind
    def get_color(self) -> str:
        return self.color
    def get_sequence_name(self) -> str:
        return self.seq_name


class VocabAnimalsEn(QuestionSequenceFactory):
    CLASS_NAME = 'EN: Animals Vocabulary'
    SCREEN_KIND = 'vocab'
    COLOR = '#aa1111'

    def __init__(self, **kwargs) -> None:
        print('kwargs = ',  kwargs.get('vocab'))
        self.vocab : list[VocabEntry] = kwargs.get('vocab') if kwargs.get('vocab') else ANIMALS_EN_VOCAB
        self.fit = 3
        self.index = -self.fit
        self.pron =  {
            e.word : e.pron for e in self.vocab
        } if kwargs.get('pron') is None else kwargs.get('pron')
        self.images =  {
            e.word : e.image for e in self.vocab
        } if kwargs.get('images') is None else kwargs.get('images')

        random.shuffle(self.vocab)

    def get_next_question(self, previous_was_good: bool = True) -> dict | None:
        if previous_was_good:
            self.index += self.fit
        if self.index >= len(self.vocab):
            return None
        vocab = [e.word for e in self.vocab[self.index:self.index+self.fit]]
        return dict(prompt='Potriviți cuvintele:',
                    slotCount=len(vocab),
                    targets=[{'imageId':w, 'slotIndex':i} for i, w in enumerate(vocab)],
                    bankWords=vocab,
                    correct=vocab,
                    pronunciations={k:v for k,v in self.get_pronounciations().items() if k in vocab},
                    images={k:v for k,v in self.get_images().items() if k in vocab},
                )

    def get_pronounciations(self) -> dict:
        return self.pron
    def get_images(self) -> dict:
        return self.images


class VocabFurnitureEN(VocabAnimalsEn):
    CLASS_NAME = 'EN: Furniture Vocabulary'

    def __init__(self):
        super().__init__(vocab=FURNITURE_EN_VOCAB)
        print(self.vocab)


class VocabSimpleEN(QuestionSequenceFactory):
    CLASS_NAME = 'EN: Jobs Vocabulary'
    SCREEN_KIND = 'vocab'
    COLOR = '#aa1111'

    def __init__(self, **kwargs) -> None:
        self.vocab = ['lorry driver', 'plumber', 'builder', 'office worker', 'mechanic', 'electrician', 'police officer', 'journalist', 'doctor', 'pilot', 'shop assistant', 'teacher', 'hairdresser', 'chef', 'nurse', 'taxi driver', 'cleaner', 'dentist']
        self.fit = 3
        self.index = -self.fit
        random.shuffle(self.vocab)

    def get_next_question(self, previous_was_good: bool = True) -> dict | None:
        if previous_was_good:
            self.index += self.fit
        if self.index >= len(self.vocab):
            return None
        vocab = self.vocab[self.index:self.index+self.fit]
        return dict(prompt='Potriviți cuvintele:',
                    slotCount=len(vocab),
                    targets=[{'imageId':w, 'slotIndex':i} for i, w in enumerate(vocab)],
                    bankWords=vocab,
                    correct=vocab,
                )
    
    def get_pronounciations(self) -> dict:
        return {
            w : f'/pron/en/{w.replace(' ', '_')}.m4a' for w in self.vocab
        }
    def get_images(self) -> dict:
        return {
                w : f'/images/en/{w.replace(' ', '_')}.png' for w in self.vocab
        }


class VocabSimpleFR(QuestionSequenceFactory):
    CLASS_NAME = 'FR: Vocabulaire Simple'
    SCREEN_KIND = 'vocab'
    COLOR = '#1111aa'

    def __init__(self, **kwargs) -> None:
        self.vocab = ['fleur', 'soleil', 'stylo', 'élèves',
                      'crayon', 'étoile', 'rose', 'métro',]
        self.fit = 3
        self.index = -self.fit
        random.shuffle(self.vocab)

    def get_next_question(self, previous_was_good: bool = True) -> dict | None:
        if previous_was_good:
            self.index += self.fit
        if self.index >= len(self.vocab):
            return None
        vocab = self.vocab[self.index:self.index+self.fit]
        return dict(prompt='Potriviți cuvintele:',
                    slotCount=len(vocab),
                    targets=[{'imageId':w, 'slotIndex':i} for i, w in enumerate(vocab)],
                    bankWords=vocab,
                    correct=vocab,
                    pronunciations={rec.word:rec.pron for rec in NOUNS_FR_VOCAB if rec.word in vocab},
                    images={rec.word:rec.image for rec in NOUNS_FR_VOCAB if rec.word in vocab},
                )
    
    def get_pronounciations(self) -> dict:
        return {
                'fleur':'/pron/fr/fleur.m4a',
                'soleil':'/pron/fr/soleil.m4a',
                'crayon':'/pron/fr/crayon.m4a',
                'stylo':'/pron/fr/stylo.m4a',
                'étoile':'/pron/fr/etoile.m4a',
                'élèves':'/pron/fr/eleve.m4a',
                'rose':'/pron/fr/rose.m4a',
                'métro': '/pron/fr/metro.m4a',
        }
    def get_images(self) -> dict:
        return {
                'fleur':'/images/fleur.png',
                'soleil':'/images/soleil.png',
                'crayon':'/images/crayon.png',
                'stylo':'/images/stylo.png',
                'étoile':'/images/etoile.png',
                'élèves':'/images/eleves.png',
                'rose':'/images/rose.png',
                'métro': '/images/metro.png',
        }

