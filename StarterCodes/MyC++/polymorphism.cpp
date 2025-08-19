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

class Cat : public Animal{
    void speak() override {
        cout << "Cat meows" << endl;
    }
};


int main() {
    Animal *a = new Animal();
    Animal *b = new Dog();
    Animal *c = new Cat();

    a->speak();
    b->speak();
    c->speak();
}