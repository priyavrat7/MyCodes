#include <iostream>

using namespace std;

/*
Inheritance diagram (this file):

A      B
\    /
  C
  |
  D

C inherits from both A and B (multiple inheritance).
D inherits from C (multilevel). 
Together this is a hybrid pattern (multiple + multilevel).
Also present: single inheritance (D : C).
*/

class A{
    public:
        void print(){
            cout << "A constructor" << endl;
        }
        void A1(){
            cout << "A1 function" << endl;
        }
        void AB(){
            cout << "AB function from A" << endl;
        }

};

class B{
    public:
        void print(){
            cout << "B constructor" << endl;
        }
        void B1(){
            cout << "B1 function" << endl;
        }
        void AB(){
            cout << "AB function from B" << endl;
        }
};

class C : public A, public B{
    public:
        void print(){
            cout << "C (child of A and B) constructor" << endl;
        }
        void C1(){
            cout << "C1 function" << endl;
        }
};

class D : public C{
    public:
        using A::AB;
        void print(){
            cout << "D (child of C) constructor" << endl;
        }
        void D1(){
            cout << "D1 function" << endl;
        }
};

int main(){
    A a;
    B b;
    C c;
    D d;

    a.print();
    b.print();
    c.print();
    d.print();

    cout << "sizeof(A) = " << sizeof(A) << endl;
    cout << "sizeof(B) = " << sizeof(B) << endl;
    cout << "sizeof(C) = " << sizeof(C) << endl;
    cout << "sizeof(D) = " << sizeof(D) << endl;

    // Some fun experiments

    //a.B1(); // This will not work because B1 is not a member of A
    //b.A1(); // This will not work because A1 is a member of B

    c.A1(); // Class C inherits from A and B
    c.B1(); // Hence C can access A1 and B1

    

    // c.AB(); // It will throw an error because of ambiguity

    c.A::AB(); // This will work because A::AB is a member of A
    c.B::AB(); // This will work because B::AB is a member of B

    static_cast<A&>(c).AB(); //Static cast using reference to A

    static_cast<B*>(&c)->AB(); //Static cast using pointer to B

    d.AB(); //No ambiguity because D has specified which AB to use in the using statement


    

    return 0;

}

