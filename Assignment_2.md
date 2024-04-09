* Actual source code must have 4 $ even though example only has 3

```
[* this is comment for this sample code for assignment 3 *]
$
$
integer i, max, sum; [* declarations *]
$
sum = 0;
i = 1;
scan (max);
while (i < max) {
sum = sum + i;
i = i + 1;
}
endwhile
print (sum + max);
$
```

* Regular stack module: memory, registers, ALU

* In our case (Virtual Stack Machine):
  * Memory starts at location 5000
  * ALU
  * Instead of registers, we have a stack

Using inctructions

1. PUSHI 1005		<-- Puch 1005 to top of stack
2. PUSHM 5000		<-- Pushes value at memory location 5000 to top of stack
3. POPM 5007		<-- Pops top of stack and stores in memory location 5007
4. SOUT 		<-- Same as printf
5. SIN			<-- Ex: if standard input is keyboard, typing would add what you type to top of stack
6. A			<-- STACK: [25, -15]   CALL A   STACK: [10]
7. S			<-- STACK: [-15, -5]   CALL B   STACK: [-10]

EX:

```
// Copy value at location 5005 to location 7
PUSHM 5005
POPM 5007
```

* scan is like cin or input


FOLLOW EXAMPLE CODE

SYMBOL TABLE:

Identifier 	MemoryLocation 	Type
i 		5000 		integer
max 		5001 		integer
sum 		5002 		integer

sum = 0;

```
1 PUSHI 0
2 POPM 5002
```

i = 1;

```
PUSHI 1
POPM 5000
```

scan (max);

```
SIN
POPM 5001
```

* Note: Label is like a point that you can jump to later

while

```
LABEL
```

(i < max) {

```
PUSHM 5000
PUSHM 5001
LES
JUMP0 21
```

sum = sum + i;

```
PUSHM 5002
PUSHM 5000
A
POPM 5002
```

i = i + 1;

```
PUSHM 5000
PUSHI 1
A
POPM 5000
```

}

```
JUMP 7
```

(sum + max)

```
PUSHM 5002
PUSHM 5001
A
```

print

```
SOUT
```

;

* For assignment 3, print out assembly instructions and then symbol table

