REFACTOR_PROMPT = """
Provide a refactored version of the code so that cyclomatic complexity is reduced if possible. Adhere to this response template provided below without any deviations.
{
    "cyclomatic_complexity": <Cyclomatic complexity of the refactored code:int>,
    "refactored_code": <Refactored code:text>,
    "comment": <Any natrual language text shoud be placed here: text>
}

"""


COGNITIVE_CHAIN_OF_THOUGHT_PROMPT= """
While considering the prompt below return the response in the following format with no exceptions.
{
    "complexity": <Your answer:int>,
    "reasoning": <Your explanation of the result>

}

Cognitive Complexity score is assessed according to
three basic rules:
1. Ignore structures that allow multiple statements to
be readably shorthanded into one
2. Increment (add one) for each break in the linear
flow of the code
3. Increment when flow-breaking structures are nested
Additionally, a complexity score is made up of four
different types of increments: A. Nesting - assessed
for nesting control flow structures inside each other
B. Structural - assessed on control flow structures that
are subject to a nesting increment, and that increase the
nesting count C. Fundamental - assessed on statements
not subject to a nesting increment D. Hybrid - assessed
on control flow structures that are not subject to a
nesting increment, but which do increase the nesting
count.

Consider the example below where the cognitive complexity is 7.
public String countVowels(String word) {
    int count = 0;
    for (String c : word.split("")) { 
        for(String v: vowels) {
            if(c.equalsIgnoreCase(v)) {
                count++;
            }
        }
    }
    if(count == 0) {
        return "does not contain vowels";
    }
    return "contains %s vowels".formatted(count);
} 

Determine the cognitive complexity of the code below,
"""

COGNITIVE_EXAMPLE_PROMPT = """
While considering the prompt below return the response in this format with no exceptions.
{
    "complexity": <Your answer:int>
}

Consider the example below where the cognitive complexity is 7.
public String countVowels(String word) {
    int count = 0;
    for (String c : word.split("")) { 
        for(String v: vowels) { 
            if(c.equalsIgnoreCase(v)) {
                count++;
            }
        }
    }
    if(count == 0) {
        return "does not contain vowels";
    }
    return "contains %s vowels".formatted(count);
}

Determine the cognitive complexity of the code below,
"""

COGNITIVE_STANDARD_PROMPT = """
While considering the prompt below return the response in this format with no exceptions.
{
    "complexity": <Your answer:int>
}

Determine the cognitive complexity of the code below,

"""

COGNITIVE_WITH_DEFINITION_PROMPT = """
While considering the prompt below return the response in this format with no exceptions.
{
    "complexity": <Your answer:int>
}

Consider the following definition for cognitive complexity:
Software cognitive complexity refers to how demanding the mental process of performing tasks such as coding, testing, debugging, or modifying source code is.
A Cognitive Complexity score is assessed according to three basic rules:
1. Ignore structures that allow multiple statements to be readably shorthanded into one
2. Increment (add one) for each break in the linear flow of the code
3. Increment when flow-breaking structures are nested


Determine the cognitive complexity of the code below,

"""

CYCLOMATIC_STANDARD_PROMPT = """"
While considering the prompt below return the response in this format with no exceptions.
{
    "complexity": <Your answer:int>
}

Determine the cyclomatic complexity of the code below,

"""

CYCLOMATIC_WITH_DEFINITION_PROMPT = """
While considering the prompt below return the response in this format with no exceptions.
{
    "complexity": <Your answer:int>
}

Consider the following definition for cyclomatic complexity:
The cyclomatic complexity of a section of source code is the number of linearly independent paths within it—a set of paths being linearly dependent if there is a subset of one or more paths where the symmetric difference of their edge sets is empty. 

Determine the cyclomatic complexity of the code below,

"""

CYCLOMATIC_EXAMPLE_PROMPT = """
While considering the prompt below return the response in this format with no exceptions.
{
    "complexity": <Your answer:int>
}

Consider the example below where the cyclomatic complexity is 5.
public String countVowels(String word) {
    int count = 0;
    for (String c : word.split("")) { 
        for(String v: vowels) {
            if(c.equalsIgnoreCase(v)) {
                count++;
            }
        }
    }
    if(count == 0) { 
        return "does not contain vowels";
    }
    return "contains %s vowels".formatted(count);
}

Determine the cyclomatic complexity of the code below,
"""

CYCLOMATIC_CHAIN_OF_THOUGHT_PROMPT= """
While considering the prompt below return the response in the following format with no exceptions.
{
    "complexity": <Your answer:int>,
    "reasoning": <Your explanation of the result>
}

Cyclomatic Complexity score is assessed by perform-
ing the following steps:
1. construct a flowchart or a graph diagram with nodes
and edges from the code.
2. Identify how many independent paths are there in
the graph.
3. Then calculate the cyclomatic complexity using the
following formula, M = E –N +2P, where E is the
number of edges of the graph, N is the number of
nodes in the graph, and P is the number of connected
components.
Consider the example below where the cyclomatic
complexity is 5.

Consider the example below where the cyclomatic complexity is 5.
public String countVowels(String word) {
    int count = 0;
    for (String c : word.split("")) {
        for(String v: vowels) {  (nesting level = 1)
            if(c.equalsIgnoreCase(v)) {  (nesting level = 2)
                count++;
            }
        }
    }
    if(count == 0) {
        return "does not contain vowels";
    }
    return "contains %s vowels".formatted(count);
} 

Determine the cyclomatic complexity of the code below,

"""