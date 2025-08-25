#include <iostream>

using namespace std;

/*
How to create a custom stack using struct and class in C++:

1. Define a Node struct:
   - Each node will store the data (e.g., int, float, etc.) and a pointer to the next node.
   - Example:
        struct Node {
            float data;
            Node* next;
        };

2. Define a Stack class:
   - The class will have a private pointer to the top node (Node* top).
   - Public methods to implement:
        - Constructor: Initialize top to nullptr.
        - Destructor: Free all nodes to avoid memory leaks.
        - push(value): Create a new node, set its data, and make it the new top.
        - pop(): Remove the top node and return its value (or just remove it).
        - peek()/top(): Return the value at the top without removing it.
        - isEmpty(): Check if the stack is empty (top == nullptr).
        - (Optional) size(): Return the number of elements in the stack.

3. Example usage:
    Stack s;
    s.push(10.5);
    s.push(20.3);
    cout << s.peek(); // prints 20.3
    s.pop();
    cout << s.peek(); // prints 10.5

4. The stack follows LIFO (Last-In, First-Out) principle.

Summary:
- Use a linked list (Node struct) for dynamic memory allocation (no fixed size).
- Stack class manages the linked list and provides stack operations.
*/


struct Node{
    float data;
    Node* next; // In stack implementation, next pointer is used to point to the next struct Node
};

class Stack{
    private:
        Node* top; // top is a pointer to the struct Node
    public:
        Stack(){ // constructor, which initialize an empty stack
            top = nullptr;
        }
        ~Stack(){
            while(top != nullptr){
                pop();
            }
        }
        
        void push(float value){
            Node* newNode = new Node; // created a new struct Node
            newNode->data = value; // set the data of the new node
            newNode->next = top; // since this is the newNode's next pointer to current top of stack
            // if stack is empty, then top will be nullptr and newNode->next will be nullptr

            //now if we have a stack with 1 element, top will be pointing to the newNode
            top = newNode; // now top is pointing to the newNode
        }

        void pop(){
            if(top == nullptr){
                cout << "Stack is empty" << endl;
                return;
            }
            Node* temp = top; // temp is a pointer to the struct Node which is pointing to the top of stack
            // top is holding the address of the latest struct Node
            // top->next holds the address of the second latest struct Node
            top = top->next; // now top is pointing to the second latest struct Node

            //now it is safe to delete the temp pointer
            delete temp;
        }
        float peek(){
            if(top == nullptr){
                cout << "Stack is empty" << endl;
                return -1;
            }
            return top->data;
        }
};

int main(){
    Stack s;
    s.push(10.5);
    s.push(20.3);

    cout << "Top element: " << s.peek() << endl;
    s.pop();
    cout << "Top element: " << s.peek() << endl;

    return 0;
}

/*
Stack (linked list) with 1 element (top = 10.5):

   +---------+
   | data:   |
   | 10.5    |
   +---------+
   | next:   |
   |  NULL   |
   +---------+
      ^
      |
    top

- Only one Node exists.
- 'data' holds the value.
- 'next' is NULL (no other elements).
- 'top' points to this single Node.
*/


/*
Stack (linked list) with 3 elements (top = 30.7, then 20.3, then 10.5):

Suppose the addresses of the nodes are as follows:
- Node1 (top, data=30.7): 0x1000
- Node2 (data=20.3):       0x2000
- Node3 (data=10.5):       0x3000

   +---------+      +---------+      +---------+
   | data:   |      | data:   |      | data:   |
   | 30.7    |      | 20.3    |      | 10.5    |
   +---------+      +---------+      +---------+
   | next:   |----->| next:   |----->| next:   |
   |0x2000   |      |0x3000   |      | NULL    |
   +---------+      +---------+      +---------+
   (0x1000)         (0x2000)         (0x3000)
      ^
      |
    top

- Each box is a Node (with its address shown below).
- 'data' holds the value.
- 'next' stores the address of the next Node in the stack (or NULL for the last node).
- 'top' points to the most recently pushed Node (here, address 0x1000).
- The last Node's 'next' is NULL (end of stack).
*/



