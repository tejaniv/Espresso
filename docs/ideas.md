# Ideas

## While loop replacement
Instead of conventional while loops like:

```
while (x <= y){
    do_blah();
    x += 1;
}
```

Consider the inverse:

```
until (x > y){
    do_blah();
    x += 1;
}
```
This would essentially be an inverted while loop. The equivalent while loops would be:

```
while (!(x > y)){
    do_blah();
    x += 1;
}
```

## Function definitions
Rather than the boring function definitions like ```def``` or ```void```, we should spice things up and use the following syntax:

```
exp <func name> (parameters): 
    do_blah();
resso
``` 
because "expresso" kinda means "fast" and functions speed up code writing.
It doesn't have to be exactly like this, its just an idea. I feel like this formatting is quite ugly (i'm not super set on anything). 

## Variable declaration
Use the key word `coffee` or `coffe` or some variation of that to define variables:
```
coffee x = 15;
```
or
```
coffe y = 15;
```
If you want, you can use separate keywords for different types (like ```int```, ```char```, ```float``` and so on).

## Other words to consider including 
Consider implementing the words Coffee, Creamer, Beans, Shots, Foam, Milk and other coffee related lingo. 
This doesn't mean these terms have to be included, its just a suggestion

## Design a basic language 
As of now, include things like variables, different data types, functions, different kinds of loops, conditionals and maybe classes if you get to it. Classes may be something we put off until we get the rest of those things working but its never to early to plan and design.
I think it is important to note, there doesn't need to be a specific syntax for this language. it can look similar to Ada, Java or Python. Lines can end in a new line or with a semi-colon, or maybe even something new if you so choose. All of them will come with their pain in the ass moments and the entire point is to have fun do whatever you desire
