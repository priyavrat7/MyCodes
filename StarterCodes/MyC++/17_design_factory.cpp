#include <iostream>
#include <memory>
#include <string>
using namespace std;

/*
Factory Design Pattern (Creational Pattern):

The Factory Design Pattern is used to create objects without specifying the exact class of object that will be created.
It provides an interface for creating objects in a superclass, but allows subclasses to alter the type of objects that will be created.

Requirements for implementing Factory Pattern:
1. Define a common interface or abstract base class for the objects to be created (e.g., Product, Shape, Animal, etc.).
2. Implement one or more concrete classes that inherit from this interface or base class.
3. Create a Factory class (or function) that contains a method for creating objects. This method takes some parameter(s) to decide which concrete class to instantiate and return.
4. The client code uses the Factory to get objects, rather than using 'new' directly.

Benefits:
- Decouples object creation from its usage.
- Makes code more flexible and extensible (easy to add new types).
- Promotes loose coupling and adheres to the Open/Closed Principle.

Example Use Cases:
- When the exact type of object to create is determined at runtime.
- When you want to centralize object creation logic.

*/

class Shape{ // Abstract base class
    public:
        virtual void getShapeType() = 0;

        virtual ~Shape(){ cout << "Shape destructor called by " << this << endl; }
};

class Circle : public Shape{
    public:
        void getShapeType() override {
            cout << "Circle" << endl;
        }
};

class Rectangle : public Shape{
    public:
        void getShapeType() override{
            cout << "Rectangle" << endl;
        }
};

class Triangle : public Shape{
    public:
        void getShapeType() override{
            cout << "Triangle" << endl;
        }
};

class FactoryShape{
    public:
    // A function which takes a string and returns a pointer to the shape object
    static unique_ptr<Shape> createShape(const string& shapeType){
        if(shapeType == "Circle"){
            unique_ptr<Shape> circle = make_unique<Circle>();
            return circle;
        }
        if(shapeType == "Rectangle"){
            unique_ptr<Shape> rectangle = make_unique<Rectangle>();
            return rectangle;
        }
        if(shapeType == "Triangle"){
            unique_ptr<Shape> triangle = make_unique<Triangle>();
            return triangle;
        }
        return nullptr;
    }
};

int main(){
    
    FactoryShape obj;
    auto s = obj.createShape("Circle");
    s->getShapeType();

    //Since createShape is a static function, we can call it without creating the object of the class
    auto s2 = FactoryShape::createShape("Rectangle");
    s2->getShapeType();

}