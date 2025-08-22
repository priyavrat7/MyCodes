#include <iostream>
#include <string>

#include <unistd.h>

using namespace std;

class Point{
    public:
        int x, y;
        string obj_type;
        Point(const int& x, const int& y, const string& obj_type) : x(x), y(y), obj_type(obj_type){
            cout << "Point(" << x << ", " << y << ") with memory address " << this << " constructed as " << obj_type << "\n";
        }

        Point operator+(const Point& p) const{
            return Point(x + p.x, y + p.y, obj_type);
        }

        void print() const{
            cout << "I am a Point(" << x << ", " << y << ") with memory address " << this << endl;
        }

        ~Point(){
            cout << "Point(" << x << ", " << y << ") with memory address " << this << " destructed as " << obj_type << "\n";
        }
        
};

int main(){
    cout << "pid: " << getpid() << endl;
    Point p1(1, 2, "stack"); // stack object

    Point* p2 = new Point(3, 4, "heap"); // heap object

    //Point p2(3, 4);

    Point p3 = p1 + *p2; // Adding two points using operator overloading 
    // where one is a heap object and one is a stack object

    cout << "p3.x = " << p3.x << ", p3.y = " << p3.y << endl;
    delete p2; // MUST delete exactly once to avoid memory leak and double free

    Point* p4 = new Point(p1 + *p2);
    p4->print();
    delete p4;

    return 0;
}