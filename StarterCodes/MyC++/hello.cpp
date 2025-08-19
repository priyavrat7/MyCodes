#include <iostream>
#include <typeinfo>

using namespace std;



class Base {
    virtual void priv_func() {}
};

class Derived : public Base {};

class Base2 {
    void priv_func() {}
};

class Derived2 : public Base2{};

int main() {
    cout << "C++ OK\n";
    cout << "sizeof(int) = " << sizeof(int) << ", sizeof(double) = " << sizeof(double) << endl;

    Base *b = new Derived();
    cout << "Type of pointer b: " << typeid(b).name() << endl;
    cout << "Type of object b point to: " << typeid(*b).name() << endl;

    Base2 *b2 = new Derived2();
    cout << "Type of pointer b2: " << typeid(b2).name() << endl;
    cout << "Type of object b2 points to: " << typeid(*b2).name() << endl;


    return 0;
}