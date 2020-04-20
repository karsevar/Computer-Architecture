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

        # create a pc counter variable that will be initialized to
        # zero
        self.pc = 0

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

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
        print(f'value {value} has been stored at ram position {address}') 

    def ram_read(self, address):
        # This function will take in an address (either in binary or 
        # base 10) and return the value stored in the ram in that specific 
        # adress 

        return self.ram[address]

    def run(self):
        """Run the CPU."""
        self.trace()
