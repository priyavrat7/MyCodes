// The <iostream> library is used to perform input and output operations in C++,
// such as printing to the console using std::cout or reading input with std::cin.
#include <iostream>


// The <typeinfo> library is used to enable runtime type identification (RTTI),
// allowing us to use the typeid operator to get information about the type of an object at runtime.
#include <typeinfo> 


// 'using namespace std;' is used to avoid having to prefix standard library names (like cout, endl) with 'std::'.
// It brings all the names in the std namespace into the global namespace for convenience.
using namespace std;

class Animal {
    public:
    virtual void speak() {
        cout << "Animal speaks" << endl;
    }
};

class Dog : public Animal {
    void speak() override {
        cout << "Dog barks" << endl;
    }
};

// Even if we do not write override in the Dog class, it will override the speak function from the Animal class in Dog class


// because the speak function is virtual in the Animal class
// and the Dog class is derived from the Animal class
// and the speak function is overridden in the Dog class

// If the base class is not virtual then using override in the derived class will not work
// because the compiler will not know which function to override
// So it is safe to write override in the Dog class too

class Cat : public Animal{
    void speak() override {
        cout << "Cat meows" << endl;
    }
};


int main() {
    Animal *a = new Animal();
    Animal *b = new Dog();
    Animal *c = new Cat();

    cout << "Type of pointer a: " << typeid(a).name() << endl;
    cout << "Type of pointer b: " << typeid(b).name() << endl;
    cout << "Type of pointer c: " << typeid(c).name() << endl;

    cout << "Type of object a: " << typeid(*a).name() << endl;
    cout << "Type of object b: " << typeid(*b).name() << endl;
    cout << "Type of object c: " << typeid(*c).name() << endl;

    cout << "Size of Animal: " << sizeof(Animal) << endl;
    cout << "Size of Dog: " << sizeof(Dog) << endl;
    cout << "Size of Cat: " << sizeof(Cat) << endl;
    // Size of Animal: 8, Size of Dog: 8, Size of Cat: 8
    // Because Animal is a virtual base class, it has a vptr pointer to the vtable
    // and the vtable is a pointer to the Animal class
    // and the Animal class has a speak function
    // and the speak function is a virtual function
    // and the speak function is overridden in the Dog and Cat classes
    // and the Dog and Cat classes have a bark and meow function
    // and the bark and meow function are not virtual functions




    a->speak();
    b->speak();
    c->speak();

    delete a;
    delete b;
    delete c;
}