# RAT24S Compiler

* [1. Compiler Usage](#1-compiler-usage)

* [2. Language Specification](#2-language-specification)
  * [2.1 Comments](#21-comments)
  * [2.2 Identifiers](#22-identifiers)
  * [2.4 Integers](#24-integers)
  * [2.5 Reals](#25-reals)
  * [2.6 Operators](#26-operators)
  * [2.7 Separators](#27-separators)

## 1. Compiler Usage

```bash
usage: compiler.py [-h] [-p] [-t] [-o OUTPUT] [SourceCodeFilePath]

positional arguments:
  SourceCodeFilePath    Path to the source code file that will be compiled

options:
  -h, --help            show this help message and exit
  -p, --print-all       print source code and tokens
  -t, --print-tokens    print tokens returned by lexer
  -o OUTPUT, --output OUTPUT
                        Specify output file
```

## 2. Language Specification

### 2.1 Comments

A comment starts with a ```[*``` and ends with a ```*]```. Comments are ignored by the lexical analyzer and syntax analyzer.

```txt
[* This is a one line comment *]

[* This is a multiline comment
that spans three rows. All three
rows will be ignored by the compiler. *]
```

### 2.2 Identifiers

An identifier is a sequence of letters (a - z), digits (0 - 9), and underscores ("_"). The first character in an identifier must be a letter. Case is insignificant, so the lexical analyzer must convert all uppercase letters to lowercase so that all tokens are lowercase.

### 2.2 Keywords

The following identifiers are keywords of the language and cannot be used for ordinary identifiers.

```txt
boolean		else		endif
false		function	if
integer		print		real
return		scan		true
while		endwhile
```

### 2.4 Integers

Integers are unsigned decimal integers. They are a sequence of digits.

Examples of integers

```txt
7	153	1849375932
```

### 2.5 Reals

A real is an integer, followed by a dot ("."), followed by an integer. There must be an integer before the dot, and an integer after the dot, meaning that something like ```89.``` or ```.57``` would be invalid.

Examples of reals

```txt
3.14	22.5	0.99	25.0
```

### 2.6 Operators

The following tokens are operators.

```txt
+	-	*	/
==	!=	>	<
<=	>=	=
```

### 2.7 Separators

The following tokens are separators.

```txt
(	)	{	}
,	;	$
```

Space (' ') is also a separator used to separate tokens and symbols.
