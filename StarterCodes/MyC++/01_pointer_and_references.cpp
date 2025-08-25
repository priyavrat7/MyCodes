#include <iostream>

using namespace std;

void inc_by_pointer(int *ptr){
    if(ptr != nullptr){
        (*ptr)++;
    }
}

void inc_by_reference(int &ref){
    ref++;
}
int main(){
    int x = 10;
    int* ptr = &x; // int* is a pointer to an int, &x gives the memory address of x
    int& ref = x; // int& is a reference to an int, reference is an alias of the variable x and 
    
    
    // not ref and x are the name of the same memory location, ref is not a new variable
    // any changes to ref will be made to x and vice versa
    // we can not make ref to refer to a different variable after initialization 
    // reference must be initialized at the time of declaration and it can not be null


    cout << "x = " << x << ", &x = " << &x << endl;         // It prints the value and the address of x
    cout << "ptr = " << ptr << ", *ptr = " << *ptr << endl; // ptr is the address of x and *ptr means, deferencing ptr to get what value it points to
    cout << "ref = " << ref << ", &ref = " << &ref << endl; // ref is the value of x  and &ref is the address of the reference ref

    inc_by_pointer(&x); // pass the address of x to the function
    inc_by_reference(x); // pass the value of x to the function

    cout << "x after increments = " << x << endl; // x is now 12
}