from abc import ABC


class Circuit(ABC):
    def __init__(self, name, num_inputs, num_outputs):
        self.name = name
        self.inputs = [Pin('input {} of {}'.format(i + 1, name)) for i in
                       range(num_inputs)]
        self.outputs = [Pin('output {} of {}'.format(i + 1, name)) for i in
                       range(num_outputs)]

    def process(self):
        raise NotImplementedError
        # can not call process(), it's an abstract method


class And(Circuit):
    def __init__(self, name, num_inputs=2):
        super().__init__(name, num_inputs, 1)

    def process(self):
        # TODO: not evident when we have multiple gates and components
        #  in a circuit because we have to the propagate output
        pass


class Or(Circuit):
    def __init__(self, name, num_inputs=2):
        super().__init__(name, num_inputs, 1)

    def process(self):
        # TODO
        pass


class Not(Circuit):
    def __init__(self, name):
        super().__init__(name, 1, 1)

    def process(self):
        # TODO
        pass


class Component(Circuit):
    def __init__(self, name, num_inputs, num_outputs):
        super().__init__(name, num_inputs, num_outputs)
        self.circuits = []

    def add_circuit(self, circuit):
        self.circuits.append(circuit)

    def process(self):
        # TODO
        pass


class Pin():
    def __init__(self, name):
        self.name = name
        self.state = None


xor = Component('xor', 2, 1)
or1 = Or('or1')
and1 = And('and1')
not1 = Not('not1')
and2 = And('and2')
# the order of adds will matter to simulation
xor.add_circuit(or1) # more readable than xor.circuits.append(or)
xor.add_circuit(and1)
xor.add_circuit(not1)
xor.add_csircuit(and2)