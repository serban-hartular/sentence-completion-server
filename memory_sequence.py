
# export type MemorySequenceSceneData = {
#   prompt: string;
#   items: MemorySequenceItem[];
#   cardSize?: number;
#   studyButtonLabel?: string;
# };

from sequences import QuestionSequenceFactory
import random

random.seed()

class MemorySequence(QuestionSequenceFactory):
    CLASS_NAME = 'MEM: Secvente'
    SCREEN_KIND = 'memory-sequence'
    COLOR = '#AA00AA'

    SHAPES = {"square", "circle", "triangle", "ellipse", "diamond"};
    SHAPE_COLORS = {"#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF"}

    def __init__(self, **kwargs) -> None:
        self.num_shapes = kwargs.get('num_shapes')
        if not self.num_shapes:
            self.num_shapes = 3
        self.num_q = 2
        self.count = -1

    def get_next_question(self, previous_was_good: bool = True) -> dict | None:
        if previous_was_good:
            self.count += 1
        if self.count >= self.num_q:
            return None
        
        shapes = list(MemorySequence.SHAPES)
        colors = list(MemorySequence.SHAPE_COLORS)
        for l in (shapes, colors):
            random.shuffle(l)
        

        return dict(prompt="Rearanjeaza in ordine:",
                    studyButtonLabel="Am memorat",
                    items=[{'type':'shape', 'shape':sh, 'color':c}
                           for sh,c in list(zip(shapes, colors))[:self.num_shapes]],
                    reshuffleDelaySeconds=3,
                    waitingMessage= "Asteapta putin...",

                    )