from abc import ABC


class Circuit(ABC):
    def __init__(self, name):
        self.name = name

    def process(self):
        raise NotImplementedError
        # can not call process(), it's an abstract method


class And(Circuit):
    def __init__(self, name, num_inputs=2):
        super().__init__(name)
        self.inputs = [None]*num_inputs
        self.output = None

    def process(self):
        # TODO: no evident when we have multiple gates and components
        #  in a circuit because we have to the propagate output
        pass


class Or(Circuit):
    def __init__(self, name, num_inputs=2):
        super().__init__(name)
        self.inputs = [None]*num_inputs
        self.output = None

    def process(self):
        # TODO
        pass


class Not(Circuit):
    def __init__(self, name):
        super().__init__(name)
        self.input = None
        self.output = None

    def process(self):
        # TODO
        pass


class Component(Circuit):
    def __init__(self, name, num_inputs, num_outputs):
        super().__init__(name)
        self.inputs = [None] * num_inputs
        self.output = [None] * num_outputs
        self.circuits = []

    def addCircuit(self, circuit):
        self.circuits.append(circuit)


xor = Component("xor", 2, 1)
or1 = Or("or1")
and1 = And("and1")
not1 = Not("not1")
and2 = And("and2")
# the order of adds will matter to simulation
xor.addCircuit(or1) # more readable than xor.circuits.append(or)
xor.addCircuit(and1)
xor.addCircuit(not1)
xor.addCircuit(and2)