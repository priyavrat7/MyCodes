#include <iostream>
 using namespace std;

 class Person{
    string name;
    int age;
 public:
    Person(const string& n, int a) : name(n), age(a){
        cout << "Person(" << name << ", " << age << ") constructed\n";
    }
    Person& operator=(const Person& copy){ // assignment operator overloading to copy
        cout << "Assignment operator _=_ is called by: " << this << endl;
        if (this != &copy){
            name = copy.name;
            age = copy.age;
        }
        return *this;
    }

    // making the print function const so that it can be called on const and non-const objects
    void print() const {
        cout << "My Name is: " << name << ", and Age: " << age << ", memory address: " << this << endl;
    }
 };

 int main(){
    Person p1("Prit", 24);
    p1.print();

    // Copy constructor: called when a new object is created from another (e.g., Book b2 = b1;)
    Person p2(p1); //copy constructor
    p2.print();
    Person p3 = p1; //copy constructor in another way
    p3.print();



    Person p4temp("Temp", 0);
    p4temp.print();
    Person p5("P5", 25);
    p5.print();

    // Assignment operator: called when an existing object is assigned a new value (e.g., b3 = b1;)
    p4temp = p5; //assignment operator

    Person test_print("Test", 100); // It will work even if the print function is not const
    test_print.print();

    const Person test_print_const("Test_Const", 100); // It will not work if the print function is not const
    test_print_const.print();

    return 0;
 }