#include <iostream>
#include<string>
using namespace std;

void print_name(const string& name){
    cout << "Name: " << name << endl;
}

void append_exclaim(string& s){
    s.push_back('!');
}

void demo_pointer_to_const(){
    int v = 43;

    const int* ptr = &v; // ptr is a pointer of a const int type
    // We can not change v through *ptr
    // But we can change ptr to point to a different variable, for example: ptr = &x


    int* const ptr2 = &v; //ptr2 is fixed to the address of v, cant change ptr2 like this: ptr2 = &x
    *ptr2 = 7; //We can change the value of v through ptr2

    const int* const ptr3 = &v; // ptr3 is fixed to the address of v and the value of v
    // We can not change v through ptr3
    // We can not change ptr3 to point to a different variable, for example: ptr3 = &x
}

int main(){
    string s = "Priv";
    print_name(s);
    append_exclaim(s);
    print_name(s);
    demo_pointer_to_const();
}
