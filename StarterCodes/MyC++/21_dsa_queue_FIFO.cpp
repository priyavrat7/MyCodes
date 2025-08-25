#include <iostream>
#include <queue>

using namespace std;

int main(){
    queue<int> q;
    q.push(10);
    q.push(20);
    q.push(30);

    /*
    In std::queue, q.front() returns the oldest element (the one that was pushed first and will be removed next),
    and q.back() returns the latest element (the one that was pushed most recently).
    So, front shows the oldest element and back shows the latest element.
    */

    cout << "Front element: " << q.front() << endl; // 10 (oldest element)
    cout << "Back element: " << q.back() << endl; // 30 (latest element)
    cout << "Size of queue: " << q.size() << endl;
    cout << "Is queue empty: " << q.empty() << endl;
    q.pop(); // FIFO: 10 is removed
    cout << "Front element: " << q.front() << endl; // 20 (updated oldest element)
    cout << "Back element: " << q.back() << endl;
    cout << "Size of queue: " << q.size() << endl;
    cout << "Is queue empty: " << q.empty() << endl;


    q.pop();
    cout << "Front element: " << q.front() << endl;
    cout << "Back element: " << q.back() << endl;
    cout << "Size of queue: " << q.size() << endl;
    cout << "Is queue empty: " << q.empty() << endl;


    q.pop();
    cout << "Front element: " << q.front() << endl;
    cout << "Back element: " << q.back() << endl;
    cout << "Size of queue: " << q.size() << endl;
    cout << "Is queue empty: " << q.empty() << endl;

    //q.pop(); // this will throw an error because the queue is empty

    return 0;
}