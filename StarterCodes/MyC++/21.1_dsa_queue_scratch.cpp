#include <iostream>

using namespace std;

/*
How to build a queue from scratch in C++ (using a linked list):

1. Define a Node struct:
   - Each node will store the data (e.g., int) and a pointer to the next node.
   - For a queue, you typically need a 'next' pointer (not 'front' and 'back' in the node itself).
   - Example:
        struct Node {
            int data;
            Node* next;
        };

2. Define a Queue class:
   - The class should have two pointers:
        - Node* front; // points to the front node (where elements are dequeued)
        - Node* back;  // points to the back node (where elements are enqueued)
   - Public methods to implement:
        - Constructor: Initialize front and back to nullptr.
        - Destructor: Free all nodes to avoid memory leaks.
        - void enqueue(int value): Add a new node at the back.
        - void dequeue(): Remove the node from the front.
        - int getFront(): Return the value at the front without removing it.
        - int getBack(): Return the value at the back without removing it.
        - bool isEmpty(): Check if the queue is empty (front == nullptr).
        - int size(): (Optional) Return the number of elements in the queue.

3. Enqueue operation:
   - Create a new node with the given value.
   - If the queue is empty, set both front and back to the new node.
   - Otherwise, set back->next to the new node and update back to the new node.

4. Dequeue operation:
   - If the queue is empty, do nothing or print an error.
   - Otherwise, remove the node at the front, update front to front->next.
   - If after removal the queue becomes empty, set back to nullptr.

5. The queue follows FIFO (First-In, First-Out) principle.

Summary:
- Use a singly linked list for dynamic memory allocation (no fixed size).
- Maintain both front and back pointers for efficient O(1) enqueue and dequeue.
- The Queue class manages the linked list and provides queue operations.
*/


struct Node{
    int data;
    Node* next;
};

class Queue{
    private:
        Node* front; // They both (front and back) are the pointer of type struct Node
        Node* back;
        // front gives the oldest element and back gives the latest element

    public:
        Queue(){ // constructor, which initialize an empty queue
            front = nullptr;
            back = nullptr;
        }
        ~Queue(){ // destructor, which frees all nodes to avoid memory leaks
            while(front != nullptr){
                dequeue();
            }
        }
        
        void enqueue(int value){ // element is added from the back, because added element is the latest element
            Node* newNode = new Node; // create a new node
            newNode->data = value; // set the data of the new created node
            newNode->next = nullptr; // means that next pointer of newNode is null

            if(front == nullptr){ // if the queue is empty
                front = newNode;
                back = newNode;
            }
            else{
                back->next = newNode; // next pointer of back is pointing to the newNode
                back = newNode;
            }
            cout << "Enqueued: " << value << endl;
        }

        void dequeue(){
            if(front == nullptr){
                cout << "Queue is empty" << endl;
                return;
            }
            else{
                Node* temp = front;
                front = front->next;
                cout << "Dequeued: " << temp->data << endl;

                if(front == nullptr){// means queue is empty, so it is necessary to set back to nullptr too
                    back = nullptr;
                }
                delete temp;

            }
        }
        int getFront(){ // returns the oldest element without removing it
            if(front == nullptr){
                cout << "Queue is empty" << endl;
                return -1;
            }
            else{
                return front->data;
            }
        }

        int getBack(){
            if(back == nullptr){
                cout << "Queue is empty" << endl;
                return -1;
            }
            else{
                return back->data;
            }
        }

        bool isEmpty(){
            return (front == nullptr);
        }
};

int main(){
    Queue q;
    cout << "Is queue empty: " << q.isEmpty() << endl;
    q.enqueue(10);
    q.enqueue(20);
    q.enqueue(30);

    cout << "Front element(oldest): " << q.getFront() << endl;
    cout << "Back element(latest): " << q.getBack() << endl;

    q.dequeue();
    cout << "Front element(oldest): " << q.getFront() << endl;
    cout << "Back element(latest): " << q.getBack() << endl;

    return 0;
}

/*
Queue (linked list) with 1 element (front = back):

Suppose the address of the node is 0x1000.

   +---------+
   |  data   |   = 42
   +---------+
   |  next   |---> NULL
   +---------+
   (0x1000)
      ^   ^
      |   |
   front  back

- Only one Node exists in the queue.
- 'data' holds the value (e.g., 42).
- 'next' is NULL (no other elements).
- Both 'front' and 'back' pointers point to this single Node.
*/

/*
Queue (linked list) with 2 elements (front != back):

Suppose the addresses of the nodes are:
- Node1 (front, data=10): 0x1000
- Node2 (back,  data=20): 0x2000

   +---------+      +---------+
   |  data   |      |  data   |
   |   10    |      |   20    |
   +---------+      +---------+
   |  next   |----->|  next   |
   | 0x2000  |      |  NULL   |
   +---------+      +---------+
   (0x1000)         (0x2000)
      ^                ^
      |                |
    front             back

- The 'front' pointer points to the first node (address 0x1000, data=10).
- The 'back' pointer points to the last node (address 0x2000, data=20).
- The 'next' of the front node points to the back node.
- The 'next' of the back node is NULL (end of queue).
*/

/*
Queue (linked list) with 3 elements (front != back):

Suppose the addresses of the nodes are:
- Node1 (front, data=5):   0x1000
- Node2 (middle, data=15): 0x2000
- Node3 (back, data=25):   0x3000

   +---------+      +---------+      +---------+
   |  data   |      |  data   |      |  data   |
   |   5     |      |   15    |      |   25    |
   +---------+      +---------+      +---------+
   |  next   |----->|  next   |----->|  next   |
   | 0x2000  |      | 0x3000  |      |  NULL   |
   +---------+      +---------+      +---------+
   (0x1000)         (0x2000)         (0x3000)
      ^                                ^
      |                                |
    front                             back

- The 'front' pointer points to the first node (address 0x1000, data=5).
- The 'back' pointer points to the last node (address 0x3000, data=25).
- Each node's 'next' points to the next node in the queue.
- The 'next' of the back node is NULL (end of queue).
*/
