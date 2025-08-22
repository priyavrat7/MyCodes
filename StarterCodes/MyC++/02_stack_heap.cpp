#include <iostream>
#include <memory>

using namespace std;

struct Point{
    int x{0}, y{0};
    int x, y; // if we do not give default values

    Point(int x, int y): x(x), y(y) {
        cout << "Point(" << x << ", " << y << ") constructed\n";
    }

    ~Point(){
        cout << "Point(" << x << ", " << y << ") destructed\n";
    }
};



int main(){
    // Stack allocation
    Point a(1, 2);

    // Heap allocation
    Point* b = new Point(3, 4);
    delete b; // must delete exactly once to avoid memory leak and double free

    // Smart pointers (RAII)
    auto c = make_unique<Point>(5, 6); // will be deleted automatically when c goes out of scope

    // Alternatively
    // unique_ptr<Point> c = std::make_unique<Point>(5, 6); // Here, make_unique<Point>(5, 6) returns a std::unique_ptr<Point>
}
/*
To do:
Explore more about smart pointers (unique_ptr, shared_ptr, weak_ptr)
Explore more about memory management function (make_unique, make_shared, allocator, uninitialized_copy, uninitialized_fill, uninitialized_default_construct, uninitialized_value_construct)
*/