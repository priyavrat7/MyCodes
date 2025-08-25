#include <iostream>
#include <memory>
#include <string>
#include <cmath>
using namespace std;

const double PI = 3.14;

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

/*
UML Diagram for Factory Pattern Example (Shape Factory)

+-------------------+
|     <<abstract>>  |
|      Shape        |
+-------------------+
| +getShapeType()   |
| +area()           |
| +perimeter()      |
+-------------------+
        /_\
         |
   +-----+-----+------+
   |     |     |      |
+------+ +--------+ +---------+
|Circle| |Square  | |Triangle |
+------+ +--------+ +---------+
| -radius      | | -side     | | -base      |
|              | |           | | -height    |
+--------------+ +-----------+ +------------+
| +getShapeType()| +getShapeType()| +getShapeType()|
| +area()        | +area()        | +area()        |
| +perimeter()   | +perimeter()   | +perimeter()   |
+----------------+ +--------------+ +--------------+

Notes:
- Shape is an abstract base class (interface) with pure virtual functions.
- Circle, Square, and Triangle are concrete classes inheriting from Shape.
- A Factory (not shown here, but typically a class or function) would return a pointer (e.g., unique_ptr<Shape>) to one of these derived classes based on input.

Legend:
- + : public member
- - : private member
- /_\ : inheritance (arrow points to base)
- <<abstract>> : abstract class (interface)
*/

class Shape{ // Abstract base class with pure virtual functions behaves as an interface
    public:
        virtual void getShapeType() const = 0;
        virtual double area() const = 0;
        virtual double perimeter() const = 0;

        virtual ~Shape(){ cout << "Shape destructor called by " << this << endl; }
};

class Circle : public Shape{
    private:
        double radius;
    public:
        Circle(const double& radius) : radius(radius) {}
        void getShapeType() const override {
            cout << "Circle" << endl;
        }
        double area() const override{
            return PI * radius * radius;
        }
        double perimeter() const override{
            return 2 * PI * radius;
        }
};

class Square : public Shape{
    private:
        double side;
    public:
        Square(const double& side) : side(side) {}
        void getShapeType() const override{
            cout << "Square" << endl;
        }
        double area() const override{
            return side * side;
        }
        double perimeter() const override{
            return 4 * (side);
        }
};

class Triangle : public Shape{
    private:
        double base;
        double height;
    public:
        Triangle(const double& base, const double& height) : base(base), height(height) {}
        void getShapeType() const override{
            cout << "Triangle" << endl;
        }
        double area() const override{
            return 0.5 * base * height;
        }
        double perimeter() const override{
            return base + height + sqrt(base * base + height * height);
        }
};

class FactoryShape{
    public:
    // A function which takes a string and returns a pointer to the shape object
    static unique_ptr<Shape> createShape(const string& shapeType, const double& radius = 0, const double& side = 0, const double& base = 0, const double& height = 0){
        if(shapeType == "Circle"){
            cout << "Circle radius: " << radius << endl;
            unique_ptr<Shape> circle = make_unique<Circle>(radius);
            return circle;
        }
        if(shapeType == "Square"){
            cout << "Square side: " << side << endl;
            unique_ptr<Shape> square = make_unique<Square>(side);
            return square;
        }
        if(shapeType == "Triangle"){
            unique_ptr<Shape> triangle = make_unique<Triangle>(base, height);
            return triangle;
        }
        return nullptr;
    }
};

int main(){
    
    FactoryShape obj;
    auto s = obj.createShape("Circle", 10);
    s->getShapeType();
    cout << "Area: " << s->area() << endl;
    cout << "Perimeter: " << s->perimeter() << endl;

    //Since createShape is a static function, we can call it without creating the object of the class
    auto s2 = FactoryShape::createShape("Square", 0, 10);
    s2->getShapeType();
    cout << "Area: " << s2->area() << endl;
    cout << "Perimeter: " << s2->perimeter() << endl;

}