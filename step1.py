# pag 7
class And():
    def __init__(self, name, num_inputs=2):
        self.name = name
        self.inputs = [None]*num_inputs
        self.output = None

    def set_input(self, num_input, state):
        self.inputs[num_input] = state

    def process(self):
        result = True;
        for inp in self.inputs:
            result = result and inp
        self.output = result
        # also :
        # from functools import reduce
        # self.output = reduce(lambda x,y: x and y, self.inputs)


and1 = And("my and")
input1 = True
input2 = False
and1.set_input(0, input1)
and1.set_input(1, input2)
and1.process()
print('{} : {} and {} = {}'.format(and1.name, input1, input2, and1.output))
