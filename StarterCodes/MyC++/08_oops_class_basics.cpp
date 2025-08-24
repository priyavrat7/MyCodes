/*
This program uses the following C++ keywords:

- class: To define the Person class.
- public: To specify the access specifier for class members.
- private: (implicitly, as class members are private by default if not specified)
- string: (from the standard library, not a keyword, but a type)
- int: To declare integer variables.
- const: To declare constant reference parameters in the constructor.
- void: For the greet() function and main() return type.
- new: To allocate memory for an object on the heap.
- delete: To deallocate memory allocated with new.
- return: To return a value from main().
- using: For using namespace std.
- namespace: For using namespace std.
- #include: For including header files (preprocessor directive, not a keyword, but essential in C++ programs).

Other notes:
- The program also uses the member access operators (dot . and arrow ->), but these are operators, not keywords.
- The destructor uses the ~ symbol, which is part of the destructor syntax, not a keyword.
*/


#include <iostream>
#include <typeinfo>

using namespace std;

class Person{
    string name;
    int age;

public:
    // constructor
    Person(const string& n, int a): name(n), age(a){
        cout << "Person(" << name << ", " << age << ") constructed\n";
    }

    
    // destroctor
    ~Person(){
        cout << "Person(" << name << ", " << age << ") destructed\n";
    }
    void greet(){
        cout << "Hello, my name is " << name << " and I am " << age << " years old.\n";
    }
};



int main() {
    Person p1("Priv", 28); //stack object
    p1.greet(); //dot operator is used to access the members of the object

    Person* p2 = new Person("Prit", 24); //heap object
    p2->greet(); //arrow operator is used to access the members of the object
    delete p2; // MUST delete exactly once to avoid memory leak and double free
    
    /*
    Stack objects are generally better than heap objects in most cases because:
    - Stack allocation and deallocation are faster and automatic (no need to manually delete).
    - Stack objects have automatic lifetime management and are less prone to memory leaks.
    - Heap objects require manual memory management (using new/delete), which can lead to memory 
      leaks or dangling pointers if not handled properly.
    - Use heap objects only when you need the object to outlive the current scope or require 
      dynamic lifetime management.
    */
    return 0;
}
