# Resistance-Optimizer
Finds the closest series/parallel desired equivalent resistance among a finite set of resistors.

## Motivation/Problem Statement
This electronics problem usually arises whenever you need a specific resistor value, but only have a small number of resistors at your disposal.  Here is the problem stated a little more formally:

If you have a total of T resistors (r1, r2, r3,…,rT), what is the best way to combine them in series and/or parallel (i.e. not considering connections in delta, wye etc. – for now) in order to create a new resistance that’s closest to some desired resistance R? Or, more generally, what is the optimal way to combine these resistors using at most M resistors?

## Example

Here’s a specific example for clarification: suppose you need a 15k resistor (all units in ohms) but all that you have to work with is four 22k, and four 51k resistors (i.e. T = 8). Let’s also suppose that you’re willing to go through the hassle of physically connecting at most five of these resistors to arrive at the closest match (i.e. M = 5). Here is the program’s solution to this problem:

```
O------<2.200E+04>--------------------
    |                                |
    ---<2.200E+04>------<5.100E+04>---
                     |               |
                     ---<5.100E+04>------O
                     
This resistance = 15035.97 ohms (desired = 15000.0 ohms), difference = 0.240%                      
```

Notice how the resistor values here are represented in scientific notation. Also notice how the program’s optimal solution uses four resistors, instead of the maximum five. This is simply because the best five-combination has a total resistance of 15,157.21 ohms, which is not the optimal solution in this case.

Now to get a feel for the diagram, let’s go around and check its physics/math. The two 51k resistors on the bottom-right are in parallel and thus their combined resistance is equal to 1/(1/51000 + 1/51000) = 25500 ohms. Also notice how this 25500 ohm composite resistance is in turn connected in series to a 22k ohm resistor, and thus, their new combined resistance is now 25500 + 22000 = 47500 ohms. Finally, notice how the new 47500 ohms is connected in parallel to another 22k resistor, and thus, the final/total composite resistance is equal to 1/(1/47500 + 1/22000) = 15035.97 ohms. Hence the math works out, and is in accordance with a real, physical/electrical connection.

## How to use this software
I’ll demonstrate how to use this software by showing a full running of the program as it appears in the console. I’ll then go over the few aspects of the program that aren’t already self-evident. Here is full running of our previous example as it appears in the console: 
```
Enter your disired resistance: 15000

Enter the maximum number of resistors that you're willing to use/combine: 5

Finally, enter a stopping percentage (the program will stop once it finds a resisitance within this range): 0


Finding best combination with 1 resistor...

O------<2.200E+04>------O
    
This resistance = 22000.00 ohms (desired = 15000.0 ohms), difference = 46.667% 



Finding best combination with 2 resistors...

O------<2.200E+04>---
    |               |
    ---<5.100E+04>------O
    
This resistance = 15369.86 ohms (desired = 15000.0 ohms), difference = 2.466% 



Finding best combination with 3 resistors...

O------<2.200E+04>--------------------
    |                                |
    ---<2.200E+04>------<2.200E+04>------O
    
This resistance = 14666.67 ohms (desired = 15000.0 ohms), difference = -2.222% 



Finding best combination with 4 resistors...

O------<2.200E+04>--------------------
    |                                |
    ---<2.200E+04>------<5.100E+04>---
                     |               |
                     ---<5.100E+04>------O
    
This resistance = 15035.97 ohms (desired = 15000.0 ohms), difference = 0.240% 



Finding best combination with 5 resistors...

O------<5.100E+04>--------------------
    |                                |
    ---<5.100E+04>--------------------
    |                                |
    ---<2.200E+04>------<2.200E+04>---
                     |               |
                     ---<5.100E+04>------O
    
This resistance = 15157.21 ohms (desired = 15000.0 ohms), difference = 1.048% 



Search complete. The closest match uses 4 resistor(s):

O------<2.200E+04>--------------------
    |                                |
    ---<2.200E+04>------<5.100E+04>---
                     |               |
                     ---<5.100E+04>------O
    
This resistance = 15035.97 ohms (desired = 15000.0 ohms), difference = 0.240% 
```
Now notice that the only new parameter that was introduced by the program was a “stopping percentage”. This is simply a difference percentage range (relative to the desired resistance) that the program looks for at every stage of the search. If a newly found resistance comes within this range, the program will automatically terminate and return that resistance. The reason for this feature is that, in practice, you’re usually satisfied with a resistance that merely comes close to the “optimal” resistance.  Moreover, if you’re using, say, 5% tolerance resistors (a common case), it renders the act of looking for a “perfect” resistance, as more or less an academic exercise.

Another thing to note is how the program prints out the optimal resistance at every level (i.e. at every resistor number) and only prints out the global optimum at the very end. The reason for this goes back to the whole “close enough” principle that I mentioned above. If you were really facing this problem/choice in real life, you’d probably want to consider the two-resistor combination (that comes within 2.5%), as your real/over-all optimal choice. Generally speaking, in electrical engineering (and in all engineering in general) the less components that you have, the better. Not only does less resistors free up more circuit real-estate, it simultaneously lowers cost and lowers the overall probability of something disconnecting and/or breaking. Thus, also having these other “non-optimal” options printed out into the console is a no-brainer.

The final thing to note about using this program is that your resistor values should be located in another file named “myResistors.txt”. You need to locate this file in the same directory as this program (unless of course, you want to change the code so it finds your file in a specific location). The formatting of that text file should (in every line) have the resistor value, followed by a comma, and then followed by the quantity of that resistor. So, as for our previous example above, the text file should be formatted like this:

```
22000,4
51000,4
```

## Capacitance

Notice that since equivalent capacitance is calculated in an analogous manner to equivalent resistance, the code in this program can be easily tweaked/accommodated to find a desired capacitance. 
