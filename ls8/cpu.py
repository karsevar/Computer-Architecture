"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # create the ram array that will have a total of 256 
        # spaces because of the structure of the cpu in the spec 
        self.ram = [0] * 256 

        # create a register array that will carry all variables 
        # that need to be executed for every opcode instruction 
        self.reg = [0] * 8 

        # stack pointer starts at index position 243 of the ram 
        # pointer saved in reg[7]

        # modify self.reg at position 7 to store the stack pointer 
        # within self.ram.
        self.reg[7] = 243

        # create a pc counter variable that will be initialized to
        # zero
        self.pc = 0

        ## moving the run instruction logic to the constructor:
        # opicode designations of functionality currently built out.
        LDI = 0b10000010 # used to save a specific value into the register 
        PRN = 0b01000111 # used to print a specific value in the register 
        MUL = 0b10100010 # used to multply two values using the alu.
        POP = 0b01000110 # used to pop the value at the top of the stack
        PUSH = 0b01000101 # used to push the value at the top of the stack

        # initialize the instruction_branch dictionary that will hold all the 
        # opcode functions indexed by the specific opcode.
        self.instruction_table = {}

        # place the helper methods into the instruction_table using the opcode 
        # variable values as the keys.
        self.instruction_table[LDI] = self.handle_LDI
        self.instruction_table[PRN] = self.handle_PRN
        self.instruction_table[MUL] = self.handle_MUL
        self.instruction_table[POP] = self.handle_pop
        self.instruction_table[PUSH] = self.handle_push

    def handle_LDI(self):
        # write value in self.ram[self.pc + 2] into self.reg[self.pc + 1]
        # increment self.pc by three since command was three bytes.
        self.reg[self.ram[self.pc + 1]] = self.ram[self.pc + 2]
        # print('value from ram at pc + 1', self.ram[self.pc + 1])
        # print('value from ram at pc + 2', self.ram[self.pc + 2])
        # self.pc += 3

    def handle_PRN(self):
        # find value in position self.pc + 1 in the register 
        # print the value as a decimal.
        # increment self.pc by two since command was two bytes.
        execute_value = self.reg[self.ram[self.pc + 1]]
        print(execute_value)
        # self.pc += 2

    def handle_MUL(self):
        # call the alu function within the cpu class 
        # self.alu(instruction, self.reg[self.ram[self.pc+1]], self.reg[self.ram[self.pc+1]])
        # pass the alu() method the opcode MUL, and both of the values in the 
        # register you would like to multiply
        self.alu('MUL', self.ram[self.pc + 1], self.ram[self.pc + 2])
        # self.pc += 3

    def handle_pop(self):
        # pop the value at the top of the stack into the given register
        # check if the pointer is at the end of the stack (position 243)
            # if not
                # copy the value from the address pointed to by stack pointer to the
                # given register 
                # increment stack pointer 
            # if so:
                # print a message that says stack is empty
        if self.reg[7] != 243:
            stack_head = self.ram[self.reg[7]]
            self.reg[self.ram[self.pc + 1]] = stack_head 
            self.reg[7] += 1
        else:
            print('~~~~~Stack is empty~~~~~~')
        # self.pc += 2

    def handle_push(self):
        # Push the value in the given register on the stack 
            # Decrement the sp 
            # copy the value in the given register to the address pointed 
            # to by stack pointer 
        self.reg[7] -= 1
        self.ram[self.reg[7]] = self.reg[self.ram[self.pc + 1]]
        # print('ram after push', self.ram)
        # self.pc += 2

    def load(self, file_path):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1
        with open(file_path, 'r', newline=None) as f:
            commands = f.readlines()
            new_commands = []
            for instruction in commands:
                # print(instruction.rstrip('\n'))
                if instruction.startswith('0') or instruction.startswith('1'):
                    instruction_mod = instruction.split()
                    new_commands.append(instruction_mod[0])

        # add the new_commands array into the cpu's ram:
        for address in range(len(new_commands)):
            value = int(new_commands[address], 2)
            self.ram_write(value, address)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """
        # self.pc = 0

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_write(self, value, address):
        # this function accepts a value and an address to which the 
        # value will be stored in the ram array.

        # store the value into self.ram through self.ram[address] = value 

        # return a message that the insertion was a success

        self.ram[address] = value 
        # print(f'value {value} has been stored at ram position {address}') 

    def ram_read(self, address):
        # This function will take in an address (either in binary or 
        # base 10) and return the value stored in the ram in that specific 
        # adress 

        return self.ram[address]

    def run(self):
        """Run the CPU."""

        # specify the instruction variables (initial instructions LDI, HLT, PRN)
        HLT = 0b00000001 # used to stop the program 
        # create a while loop that will only terminate once the command 
        # HLT is read from the ram.
            # create an instruction variable (since the assumption is the 
            # first value in the ram is an instruction) initialize it to 
            # first index in ram.
            # create an instruction length variable that will be used to increment 
            # self.pc according to the first two values in the opcode.

            # if instruction is in the dictionary self.instruction_table:
                # run self.instruction_table[instruction]()
            # elif command is HLT:
                # terminate the while loop 
            # else:
                # print an error message

            # increment self.pc by instruction length

        while True:
            instruction = self.ram[self.pc] 
            instruction_length = ((instruction & 0b11000000) >> 6) + 1
            if instruction in self.instruction_table:
                self.instruction_table[instruction]()
            elif instruction == HLT:
                break
            else:
                print('~~~~~Invalid Instruction~~~~~')
                break
                
            self.pc += instruction_length
            
        self.trace()
