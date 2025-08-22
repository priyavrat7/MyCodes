#include <iostream>
#include <string>

using namespace std;

const double PI = 3.14;


class Shape{
    public:
        virtual double area() const{
            cout << "Area of Shape will be defined in the derived classes" << endl;
            return 0.0;
        }
        virtual ~Shape(){
            cout << "Destructor of Shape is called by: " << this << endl;
        }
};

class Circle : public Shape{
    double radius;
    public:
        Circle(double r) : radius(r){
            cout << "Circle constructor is called by: " << this << endl;
        }

        double area() const override {
            return PI * radius * radius;
        }

        ~Circle(){
            cout << "Circle destructor is called by: " << this << endl;
        }
};


int main(){

    // These stack and heap object will now work since the class Shape does not have 
    //Shape s(7); // Stack object
    //Shape* s_ptr = new Shape(11); // Heap object


    Circle c(10); // Stack object
    Shape* s1_ptr = new Circle(10); // Heap object

    cout << "Area = " << s1_ptr->area() << endl;

    delete s1_ptr; // This will call the destructor of the Circle class first and then the destructor of the Shape class

    return 0;

}