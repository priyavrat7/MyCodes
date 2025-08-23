#include <iostream>
#include <typeinfo>
#include <memory>

using namespace std;

class Foo{
    public:
    int val;
        Foo(int x) : val(x){
            cout << "Foo(" << val << ") is constructed" << endl;
        }

        ~Foo(){
            cout << "Foo(" << val << ") is destructed" << endl;
        }
};

int main(){
    auto p = new Foo(11); // heap object
    cout << "p->val = " << p->val << endl;
    delete p;

    unique_ptr<Foo> p1 = make_unique<Foo>(16);
    unique_ptr<Foo> p2(new Foo(10));
    auto p3 = make_unique<Foo>(19);
    // p1, p2, p3 are all stack objects


    shared_ptr<Foo> p4 = make_shared<Foo>(25);
    shared_ptr<Foo> p5 = p4; // p5 is a shared pointer to the same object as p4
    // p5 will increase the use count of p4 by 1
    cout << "use count of p4: " << p4.use_count() << endl;


    weak_ptr<Foo> wp = p4; // weak pointer will not increase the use count of p4
    cout << "use count of p4: " << p4.use_count() << endl;
    if (auto temp = wp.lock()){
        cout << "wp is not expired, its value is " << temp->val << endl;
    }

    size_t size = 5;

    for (size_t i = 0; i != size; ++i){
        auto temp_shared_ptr = p4; // it will increase the use count of p4 by 1
        cout << "use count of p4: " << p4.use_count() << endl;
    }
    // temp_shared_ptr is destroyed as it goes out of scope
    // hence, the use count of p4 will be decremented by 1
    cout << "use count of p4: " << p4.use_count() << endl;
    
}