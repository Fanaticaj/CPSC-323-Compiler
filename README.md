# RAT24S Language Specification

## 1. Lexical Analysis

### 1.1 Comments

A comment starts with a ```[*``` and ends with a ```*]```. Comments are ignored by the lexical analyzer and syntax analyzer.

```txt
[* This is a one line comment *]

[* This is a multiline comment
that spans three rows. All three
rows will be ignored by the compiler. *]
```

### 1.2 Identifiers

An identifier is a sequence of letters (a - z), digits (0 - 9), and underscores ("_"). The first character in an identifier must be a letter. Case is insignificant, so the lexical analyzer must convert all uppercase letters to lowercase so that all tokens are lowercase.

### 1.2 Keywords

The following identifiers are keywords of the language and cannot be used for ordinary identifiers.

```txt
boolean		else		endif
false		function	if
integer		print		real
return		scan		true
while
```

### 1.4 Integers

Integers are unsigned decimal integers. They are a sequence of digits.

Examples of integers

```txt
7	153	1849375932
```

### 1.5 Reals

A real is an integer, followed by a dot ("."), followed by an integer. There must be an integer before the dot, and an integer after the dot, meaning that something like ```89.``` or ```.57``` would be invalid.

Examples of reals

```txt
3.14	22.5	0.99	25.0
```

### 1.6 Operators

The following tokens are operators.

```txt
+	-	*	/
==	!=	>	<
<=	>=	=
```

### 1.7 Separators

The following tokens are separators.

```txt
(	)	{	}
,	;	$
```

Space (' ') is also a separator used to separate tokens and symbols.
