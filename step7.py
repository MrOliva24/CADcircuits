from abc import ABC

class Circuit(ABC):
    def __init__(self, name, num_inputs, num_outputs):
        self.name = name
        self.inputs = [Pin('input {} of {}'.format(i + 1, name)) for i in
                       range(num_inputs)]
        self.outputs = [Pin('output {} of {}'.format(i + 1, name)) for i in
                        range(num_outputs)]
        self.connections = []

    def process(self):
        raise NotImplementedError
        # can not call process(), it's an abstract method

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
        if observer in observers:
            self.observers.remove(observer)
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
        self.wire = [pin_from, pin_to]



def binaryToDecimal(n, bits):
    decimal = 0
    for i in range(bits):
        if n[i]:
            decimal += 2**i
    return decimal



def decimalToBinary(n):
    return int(bin(n).replace("0b", ""))

def bin_to_dec(bin, digitos):
    sum = 0
    for i,bool in enumerate(bin):
        if bool:
            sum += 2**(digitos -i-1)

    return sum

xor1 = Component('xor1', 2, 1)
or1 = Or('or1')
and1 = And('and1')
not1 = Not('not1')
and2 = And('and2')
# the order of adds will matter to simulation
xor1.add_circuit(or1)  # more readable than xor.circuits.append(or)
xor1.add_circuit(and1)
xor1.add_circuit(not1)
xor1.add_circuit(and2)

Connection(xor1.inputs[0], and1.inputs[0])
Connection(xor1.inputs[0], or1.inputs[0])
Connection(xor1.inputs[1], and1.inputs[1])
Connection(xor1.inputs[1], or1.inputs[1])
Connection(or1.outputs[0], and2.inputs[0])
Connection(and1.outputs[0], not1.inputs[0])
Connection(not1.outputs[0], and2.inputs[1])
Connection(and2.outputs[0], xor1.outputs[0])

import copy

oneBitAdder = Component("OneBitAdder", 3, 2)
xor2 = copy.deepcopy(xor1)
xor2.name = 'xor2'
and3 = And('and3')
and4 = And('and4')  # or copy.deepcopy(and3) and rename
or2 = Or('or2');
# this order matters for the simulation
oneBitAdder.add_circuit(xor1)
oneBitAdder.add_circuit(xor2)
oneBitAdder.add_circuit(and3)
oneBitAdder.add_circuit(and4)
oneBitAdder.add_circuit(or2)

# connections "left to right"

A = oneBitAdder.inputs[0]
B = oneBitAdder.inputs[1]
Ci = oneBitAdder.inputs[2]
S = oneBitAdder.outputs[0]
Co = oneBitAdder.inputs[1]

input1Xor1 = xor1.inputs[0]
input2Xor1 = xor1.inputs[1]
outputXor1 = xor1.outputs[0]

input1Xor2 = xor2.inputs[0]
input2Xor2 = xor2.inputs[1]
outputXor2 = xor2.outputs[0]

input1And3 = and3.inputs[0]
input2And3 = and3.inputs[1]
outputAnd3 = and3.outputs[0]

input1And4 = and4.inputs[0]
input2And4 = and4.inputs[1]
outputAnd4 = and4.outputs[0]

input1Or2 = or2.inputs[0]
input2Or2 = or2.inputs[1]
outputOr2 = or2.outputs[0]

Connection(A, input1Xor1)
Connection(B, input2Xor1)
Connection(outputXor1, input1Xor2)
Connection(Ci, input2Xor2)
Connection(outputXor1, input1And3)
Connection(Ci, input2And3)
Connection(A, input1And4)
Connection(B, input2And4)
Connection(outputAnd3, input1Or2)
Connection(outputAnd4, input2Or2)
Connection(outputXor2, S)
Connection(outputOr2, Co)

print("\n ONE BIT ADDER \n")

inputs = []
for a in [False, True]:
    for b in [False, True]:
        for c in [False, True]:
            inputs.append([a, b, c])
expected_S = [False, True, True, False, True, False, False, True]
expected_Co = [False, False, False, True, False, True, True, True]

for (a, b, ci), exp_s, exp_co in zip(inputs, expected_S, expected_Co):
    A.set_state(a)
    B.set_state(b)
    Ci.set_state(ci)
    oneBitAdder.process()
    s = S.is_state()
    co = Co.is_state()
    print('{} + {} + {} = {}, {}'.format(a, b, ci, s, co))
    assert s == exp_s
    assert co == exp_co


#HERE STARTS OUR CODE MODIFICATION
one_bit_adder_0 = copy.deepcopy(oneBitAdder)
one_bit_adder_0.name = 'one_bit_adder_0'
one_bit_adder_1 = copy.deepcopy(oneBitAdder)
one_bit_adder_1.name = 'one_bit_adder_1'
one_bit_adder_2 = copy.deepcopy(oneBitAdder)
one_bit_adder_2.name = 'one_bit_adder_2'
one_bit_adder_3 = copy.deepcopy(oneBitAdder)
one_bit_adder_3.name = 'one_bit_adder_3'


fourBitAdder = Component("4bitsAdder", 9, 5)  #4As + 4Bs + 1Cin, 4S + 1Cout

#input and output of 4bitadder
InputA_0 = fourBitAdder.inputs[0]
InputB_0 = fourBitAdder.inputs[1]
OutputS_0 = fourBitAdder.outputs[0]
InputA_1 = fourBitAdder.inputs[2]
InputB_1 = fourBitAdder.inputs[3]
OutputS_1 = fourBitAdder.outputs[1]
InputA_2 = fourBitAdder.inputs[4]
InputB_2 = fourBitAdder.inputs[5]
OutputS_2 = fourBitAdder.outputs[2]
InputA_3 = fourBitAdder.inputs[6]
InputB_3 = fourBitAdder.inputs[7]
OutputS_3 = fourBitAdder.outputs[3]
CarryIn = fourBitAdder.inputs[8]
CarryOut = fourBitAdder.outputs[4]

#input and output of each one bit adder

#ONE BIT ADDER 0
A0 = one_bit_adder_0.inputs[0]
B0 = one_bit_adder_0.inputs[1]
Ci0 = one_bit_adder_0.inputs[2]
S0 = one_bit_adder_0.outputs[0]
Co0 = one_bit_adder_0.outputs[1]

#ONE BIT ADDER 1
A1 = one_bit_adder_1.inputs[0]
B1 = one_bit_adder_1.inputs[1]
Ci1 = one_bit_adder_1.inputs[2]
S1 = one_bit_adder_1.outputs[0]
Co1 = one_bit_adder_1.outputs[1]

#ONE BIT ADDER 2
A2 = one_bit_adder_2.inputs[0]
B2 = one_bit_adder_2.inputs[1]
Ci2 = one_bit_adder_2.inputs[2]
S2 = one_bit_adder_2.outputs[0]
Co2 = one_bit_adder_2.outputs[1]

#ONE BIT ADDER 3
A3 = one_bit_adder_3.inputs[0]
B3 = one_bit_adder_3.inputs[1]
Ci3 = one_bit_adder_3.inputs[2]
S3 = one_bit_adder_3.outputs[0]
Co3 = one_bit_adder_3.outputs[1]

#We make a big circuit (4 bit adder) composed by 4 sub-circuits (1 bit adders)
fourBitAdder.add_circuit(one_bit_adder_0)
fourBitAdder.add_circuit(one_bit_adder_1)
fourBitAdder.add_circuit(one_bit_adder_2)
fourBitAdder.add_circuit(one_bit_adder_3)

#We connect each one bit adder with the next adder and the first and last one bit adders with the bigger four bit adder

#First 1 Bit Adder
Connection(CarryIn, Ci0)
Connection(InputA_0, A0)
Connection(InputB_0, B0)
Connection(S0, OutputS_0)

#Second 1 Bit Adder
Connection(Co0, Ci1)
Connection(InputA_1, A1)
Connection(InputB_1, B1)
Connection(S1, OutputS_1)

#Third 1 Bit Adder
Connection(Co1, Ci2)
Connection(InputA_2, A2)
Connection(InputB_2, B2)
Connection(S2, OutputS_2)


#Fourth 1 bit adder
Connection(Co2, Ci3)
Connection(InputA_3, A3)
Connection(InputB_3, B3)
Connection(S3, OutputS_3)
Connection(Co3, CarryOut)

print("\n FOUR BIT ADDER \n")

inputs = []
for a in [False, True]:
    for b in [False, True]:
        for c in [False, True]:
            for d in [False,True]:
                for e in [False,True]:
                    for f in [False,True]:
                        for g in [False, True]:
                            for h in [False, True]:
                                for i in [False, True]:
                                    inputs.append([a, b, c, d, e, f, g, h, i])



for (a, b, c, d, e, f, g, h, ci), exp_s, exp_co in zip(inputs, expected_S, expected_Co):
    InputA_0.set_state(a)
    InputB_0.set_state(b)
    InputA_1.set_state(c)
    InputB_1.set_state(d)
    InputA_2.set_state(e)
    InputB_2.set_state(f)
    InputA_3.set_state(g)
    InputB_3.set_state(h)
    Ci.set_state(ci)
    oneBitAdder.process()
    OutputS_0 = S.is_state()
    co = Co.is_state()
    print('{} + {} + {} + {} + {} + {} + {} + {} = {}, {}'.format(a, b, c, d, e, f, g, h, ci, s, co))
    #print("{} + {} + C {} = {} + {}".format(binaryToDecimal([a,b,c,d],4), binaryToDecimal([e,f,g,h],4), binaryToDecimal([ci],4), binaryToDecimal([OutputS_0],4), binaryToDecimal([co],4)))



InputA_0 = fourBitAdder.inputs[0]
InputB_0 = fourBitAdder.inputs[1]
OutputS_0 = fourBitAdder.outputs[0]
InputA_1 = fourBitAdder.inputs[2]
InputB_1 = fourBitAdder.inputs[3]
OutputS_1 = fourBitAdder.outputs[1]
InputA_2 = fourBitAdder.inputs[4]
InputB_2 = fourBitAdder.inputs[5]
OutputS_2 = fourBitAdder.outputs[2]
InputA_3 = fourBitAdder.inputs[6]
InputB_3 = fourBitAdder.inputs[7]
OutputS_3 = fourBitAdder.outputs[3]
CarryIn = fourBitAdder.inputs[8]
CarryOut = fourBitAdder.outputs[4]
# WE CREATE THE EIGHT (8) BIT ADDERt_adder_0 = copy.deepcopy(oneBitAdder)
four_bit_adder_0 = copy.deepcopy(fourBitAdder)
four_bit_adder_0.name = 'four_bit_adder_0'
four_bit_adder_1 = copy.deepcopy(fourBitAdder)
four_bit_adder_1.name = 'four_bit_adder_1'


eightBitAdder = Component("8bitsAdder", 17, 9)  #8As + 8Bs + 1Cin, 8S + 1Cout

#input and output of 8bitadder
InputA_0 = eightBitAdder.inputs[0]
InputB_0 = eightBitAdder.inputs[1]
OutputS_0 = eightBitAdder.outputs[0]
InputA_1 = eightBitAdder.inputs[2]
InputB_1 = eightBitAdder.inputs[3]
OutputS_1 = eightBitAdder.outputs[1]
InputA_2 = eightBitAdder.inputs[4]
InputB_2 = eightBitAdder.inputs[5]
OutputS_2 = eightBitAdder.outputs[2]
InputA_3 = eightBitAdder.inputs[6]
InputB_3 = eightBitAdder.inputs[7]
OutputS_3 = eightBitAdder.outputs[3]
InputA_4 = eightBitAdder.inputs[8]
InputB_4 = eightBitAdder.inputs[9]
OutputS_4 = eightBitAdder.outputs[4]
InputA_5 = eightBitAdder.inputs[10]
InputB_5 = eightBitAdder.inputs[11]
OutputS_5 = eightBitAdder.outputs[5]
InputA_6 = eightBitAdder.inputs[12]
InputB_6 = eightBitAdder.inputs[13]
OutputS_6 = eightBitAdder.outputs[6]
InputA_7 = eightBitAdder.inputs[14]
InputB_7 = eightBitAdder.inputs[15]
OutputS_7 = eightBitAdder.outputs[7]
CarryIn = eightBitAdder.inputs[16]
CarryOut = eightBitAdder.outputs[8]

#input and output of each four bit adder

#FOUR BIT ADDER 0
A0 = four_bit_adder_0.inputs[0]
B0 = four_bit_adder_0.inputs[1]
A1 = four_bit_adder_0.inputs[2]
B1 = four_bit_adder_0.inputs[3]
A2 = four_bit_adder_0.inputs[4]
B2 = four_bit_adder_0.inputs[5]
A3 = four_bit_adder_0.inputs[6]
B3 = four_bit_adder_0.inputs[7]
Ci0 = four_bit_adder_0.inputs[8]
S0 = four_bit_adder_0.outputs[0]
S1 = four_bit_adder_0.outputs[1]
S2 = four_bit_adder_0.outputs[2]
S3 = four_bit_adder_0.outputs[3]
Co0 = four_bit_adder_0.outputs[4]

#FOUR BIT ADDER 1
A4 = four_bit_adder_1.inputs[0]
B4 = four_bit_adder_1.inputs[1]
A5 = four_bit_adder_1.inputs[2]
B5 = four_bit_adder_1.inputs[3]
A6 = four_bit_adder_1.inputs[4]
B6 = four_bit_adder_1.inputs[5]
A7 = four_bit_adder_1.inputs[6]
B7 = four_bit_adder_1.inputs[7]
Ci1 = four_bit_adder_1.inputs[8]
S4 = four_bit_adder_1.outputs[0]
S5 = four_bit_adder_1.outputs[1]
S6 = four_bit_adder_1.outputs[2]
S7 = four_bit_adder_1.outputs[3]
Co1 = four_bit_adder_1.outputs[4]

#We make a big circuit (8 bit adder) composed by 2 sub-circuits (4 bit adders)
eightBitAdder.add_circuit(four_bit_adder_0)
eightBitAdder.add_circuit(four_bit_adder_1)

#We connect each one bit adder with the next adder and the first and last one bit adders with the bigger four bit adder

#First 4 Bit Adder
Connection(CarryIn, Ci0)
Connection(InputA_0, A0)
Connection(InputA_1, A1)
Connection(InputA_2, A2)
Connection(InputA_3, A3)
Connection(InputB_0, B0)
Connection(InputB_1, B1)
Connection(InputB_2, B2)
Connection(InputB_3, B3)
Connection(S0, OutputS_0)
Connection(S1, OutputS_1)
Connection(S2, OutputS_2)
Connection(S3, OutputS_3)


#Second 4 Bit Adder
Connection(Co0, Ci1)
Connection(InputA_4, A4)
Connection(InputA_5, A5)
Connection(InputA_6, A6)
Connection(InputA_7, A7)
Connection(InputB_4, B4)
Connection(InputB_5, B5)
Connection(InputB_6, B6)
Connection(InputB_7, B7)
Connection(S4, OutputS_4)
Connection(S5, OutputS_5)
Connection(S6, OutputS_6)
Connection(S7, OutputS_7)
Connection(Co1,CarryOut)

#PRINTS DE TOTS ELS EIGHTBITADDERS
inputs = []
for a0 in [False, True]:
    for b0 in [False, True]:
        for a1 in [False, True]:
            for b1 in [False, True]:
                for a2 in [False, True]:
                    for b2 in [False, True]:
                        for a3 in [False, True]:
                            for b3 in [False, True]:
                                for a4 in [False, True]:
                                    for b4 in [False, True]:
                                        for a5 in [False, True]:
                                            for b5 in [False, True]:
                                                for a6 in [False, True]:
                                                    for b6 in [False, True]:
                                                        for a7 in [False, True]:
                                                            for b7 in [False, True]:
                                                                for c in [False, True]:
                                                                    inputs.append([a0, b0, a1, b1,a2,b2,a3,b3,a4,b4,a5,b5,a6,b6,a7,b7,c])

for (a0,b0,a1,b1,a2,b2,a3,b3,a4,b4,a5,b5,a6,b6,a7,b7,ci) in inputs:
    InputA_0.set_state(a0)
    InputB_0.set_state(b0)
    InputA_1.set_state(a1)
    InputB_1.set_state(b1)
    InputA_2.set_state(a2)
    InputB_2.set_state(b2)
    InputA_3.set_state(a3)
    InputB_3.set_state(b3)
    InputA_4.set_state(a4)
    InputB_4.set_state(b4)
    InputA_5.set_state(a5)
    InputB_5.set_state(b5)
    InputA_6.set_state(a6)
    InputB_6.set_state(b6)
    InputA_7.set_state(a7)
    InputB_7.set_state(b7)
    CarryIn.set_state(ci)
    eightBitAdder.process()
    OutputS_0 = S0.is_state()
    OutputS_1 = S1.is_state()
    OutputS_2 = S2.is_state()
    OutputS_3 = S3.is_state()
    OutputS_4 = S4.is_state()
    OutputS_5 = S5.is_state()
    OutputS_6 = S6.is_state()
    OutputS_7 = S7.is_state()
    CarryOut = Co.is_state()

    print('{} + {} + {} =  {} , {}'.format(bin_to_dec([a7,a6,a5,a4,a3,a2,a1,a0],8),bin_to_dec([b7,b6,b5,b4,b3,b2,b1,b0],8), ci, bin_to_dec([co,OutputS_7,OutputS_6,OutputS_5,OutputS_4,OutputS_3,OutputS_2,OutputS_1,OutputS_0],9),co))


