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

    # added
    def set_input(self, num_input, state):
        self.inputs[num_input].set_state(state)


class And(Circuit):
    def __init__(self, name, num_inputs=2):
        super().__init__(name, num_inputs, 1)

    def process(self):
        result = True
        for pin_input in self.inputs:
            result = result and pin_input.is_state()
        self.outputs[0].set_state(result)


class Or(Circuit):
    def __init__(self, name, num_inputs=2):
        super().__init__(name, num_inputs, 1)

    def process(self):
        result = False
        for pin_input in self.inputs:
            result = result or pin_input.is_state()
        self.outputs[0].set_state(result)


class Not(Circuit):
    def __init__(self, name):
        super().__init__(name, 1, 1)

    def process(self):
        self.outputs[0].set_state(not self.inputs[0].is_state())


class Component(Circuit):
    def __init__(self, name, num_inputs, num_outputs):
        super().__init__(name, num_inputs, num_outputs)
        self.circuits = []

    def add_circuit(self, circuit):
        self.circuits.append(circuit)

    def process(self):
        for circuit in self.circuits:
            circuit.process()



class Observable(ABC):
    def __init__(self):
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        # TODO
        pass

    def notify_observers(self, an_object=None):
        for obs in self.observers:
            obs.update(self, an_object)
            # observable sends itself to each observer


class Observer(ABC):
    def update(self, observable, an_object):
        raise NotImplementedError
        # abstract method


class Pin(Observable, Observer):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.state = None

    def is_state(self):
        return self.state

    def set_state(self, new_state):
        self.state = new_state
        self.notify_observers(self)

    def update(self, observed_pin, an_object):
        self.set_state(observed_pin.is_state())


class Connection:
    def __init__(self, pin_from, pin_to):
        pin_from.add_observer(pin_to)


xor = Component('xor', 2, 1)
or1 = Or('or1')
and1 = And('and1')
not1 = Not('not1')
and2 = And('and2')
# the order of adds will matter to simulation
xor.add_circuit(or1) # more readable than xor.circuits.append(or)
xor.add_circuit(and1)
xor.add_circuit(not1)
xor.add_circuit(and2)

Connection(xor.inputs[0], and1.inputs[0])
Connection(xor.inputs[0], or1.inputs[0])
Connection(xor.inputs[1], and1.inputs[1])
Connection(xor.inputs[1], or1.inputs[1])
Connection(or1.outputs[0], and2.inputs[0])
Connection(and1.outputs[0], not1.inputs[0])
Connection(not1.outputs[0], and2.inputs[1])
Connection(and2.outputs[0], xor.outputs[0])


print('\nTest of And')
inputs = [[False, False], [False, True], [True, False], [True, True]]
expected_outputs = [False, False, False, True]

for (input1, input2), expected_output in zip(inputs, expected_outputs):
    and1.set_input(0, input1)
    and1.set_input(1, input2)
    and1.process()
    output = and1.outputs[0].is_state()
    print('{} AND {} = {}'.format(input1, input2, output))
    assert output == expected_output

print('\nTest of xor')
expected_outputs = [False, True, True, False]
for (input1, input2), expected_output in zip(inputs, expected_outputs):
    xor.set_input(0, input1)
    xor.set_input(1, input2)
    xor.process()
    output = xor.outputs[0].is_state()
    print('{} XOR {} = {}'.format(input1, input2, output))
    assert output == expected_output
