# FunnyLang
Took insperation from [Porth](https://gitlab.com/tsoding/porth) but mine is way worse.

you can include stuff like this
```
"./Librairies(or wherever)/std.funny(or whatever)" attach
```

this is a simple hello world
```
"./Libraries/std.funny" attach

func main
  "Hello, World!" print
end
```

you make functions with

```
func (name)
  code
end
```

its all basically stack based so for conditional blocks you do this

```
(condition) (while/if)
  code
end
```

if statements also support else statements

```
"1 or 0" print input
if
  1 while
    1 print
  end
else
  0 print
end
```

you can do if else staements like this if you want

```
2 2 + 5 = if
  code yapping
else 2 1 1 + = if
  more yapping
end
```

you can also make variables

```
var (varname)
```

Here is a little program that asks for a name and sets a variable to it

```
"./Libraries/std.funny" attach
var Name

func main
	"What is your name?" print input
	"Name" set
	Name print
end
```

I'm to lazy to do the rest so look at the code yourself, bye!
