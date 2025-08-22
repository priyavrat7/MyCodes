/* 
Inheritance is an object-oriented programming concept where a class (called the derived or child class) 
acquires the properties and behaviors (data members and member functions) of another class (called the base or parent class).
It allows for code reusability and the creation of hierarchical relationships between classes.
In C++, inheritance is implemented using the ':' symbol. For example:
class Dog : public Animal { ... };
Here, Dog inherits publicly from Animal, meaning Dog has access to public and protected members of Animal.
 
Types of inheritance in C++ include:
1. Single Inheritance: A class inherits from one base class.
2. Multiple Inheritance: A class inherits from more than one base class.
3. Multilevel Inheritance: A class is derived from a class which is also derived from another class.
4. Hierarchical Inheritance: Multiple classes inherit from a single base class.
5. Hybrid Inheritance: Combination of two or more types of inheritance.



Hierarchy in this file:
Animal (base)
├── Dog (derived)
└── Cat (derived)
Which is a single inheritance and Hierarchical inheritance as well
 */


#include <iostream>
 
using namespace std;

class Animal{
    public:
        void speak(){
            cout << "Animal speaks" << endl;
        }
};

class Dog : public Animal{
    public:
        void speak() {
            cout << "Dog barks" << endl;
        }
};

class Cat : public Animal{
    public:
        void speak(){
            cout << "Cat meows" << endl;
        }
};


int main(){
    Animal a; // stack object
    a.speak();
    
    Dog d; // stack object
    d.speak();

    Cat c; // stack object  
    c.speak();

    cout << "sizeof(Animal) = " << sizeof(Animal) << endl;
    cout << "sizeof(Dog) = " << sizeof(Dog) << endl;
    cout << "sizeof(Cat) = " << sizeof(Cat) << endl;

    Animal *a_ptr = new Animal(); // heap object
    Dog *d_ptr = new Dog(); // heap object
    Cat *c_ptr = new Cat(); // heap object

    a_ptr->speak();
    d_ptr->speak();
    c_ptr->speak();

    delete a_ptr; // delete the heap object
    delete d_ptr; // delete the heap object
    delete c_ptr; // delete the heap object

    return 0;
}

/*
Inheritance support across languages

| Type                | C++ | Java           | Python |
|---------------------|-----|----------------|--------|
| Single              | Yes | Yes            | Yes    |
| Multiple (classes)  | Yes | No (interfaces)| Yes    |
| Multilevel (A->B->C)| Yes | Yes            | Yes    |
| Hierarchical        | Yes | Yes            | Yes    |
| Hybrid (combination)| Yes | Limited*       | Yes    |

*Java: single class inheritance; multiple interface inheritance only.
Notes:
- C++: true multiple inheritance; resolve diamonds with virtual inheritance.

- Java: class extends one class; may implement many interfaces (default methods require disambiguation).
- Python: true multiple inheritance; method resolution via MRO (C3 linearization).

 
 Inheritance enables polymorphism and code reuse, making programs easier to maintain and extend.
 */

 /*
 // The "diamond problem" is a classic issue in multiple inheritance, particularly in C++.
// It occurs when a class inherits from two classes that both inherit from a common base class.
// This creates a diamond-shaped inheritance diagram:
//
//      Animal
//      /    \
//   Dog    Cat
//      \    /
//     PetDogCat
//
// In this scenario, PetDogCat inherits from both Dog and Cat, which both inherit from Animal.
// The problem: PetDogCat ends up with two copies of Animal's members (one via Dog, one via Cat).
// This can lead to ambiguity and redundancy. For example, if Animal has a method or data member,
// which one does PetDogCat use? This is called the "diamond problem".
//
// C++ solves this with "virtual inheritance":
//   class Dog : virtual public Animal { ... };
//   class Cat : virtual public Animal { ... };
//   class PetDogCat : public Dog, public Cat { ... };
// With virtual inheritance, only one shared Animal subobject exists in PetDogCat, resolving ambiguity.
//
// Other languages handle this differently:
// - Java avoids the problem by not allowing multiple class inheritance (only interfaces).
// - Python uses a method resolution order (MRO) to determine which base class's method to use.

