// Stack Data Structure using STL
#include <iostream>
#include <stack>

using namespace std;

/*
How to create a stack in C++:

1. You can use the built-in STL stack:
   #include <stack>
   stack<int> s; // creates a stack of integers
   s.push(10);   // push element onto stack
   s.pop();      // remove top element
   s.top();      // access top element
   s.empty();    // check if stack is empty

2. Or, you can implement your own stack using an array or vector:
   - Define a class with an array/vector and a variable to track the top index.
   - Implement push(), pop(), top(), and empty() methods.

Example (using STL stack):
    #include <stack>
    stack<int> s;
    s.push(1);
    s.push(2);
    cout << s.top(); // prints 2
    s.pop();
    cout << s.top(); // prints 1

The stack follows LIFO (Last-In, First-Out) principle.
*/


int main(){
    stack<int> s;
    s.push(1);
    s.push(2);
    cout << s.top() << endl; // prints 2
    s.pop();
    cout << s.top() << endl; // prints 1

}