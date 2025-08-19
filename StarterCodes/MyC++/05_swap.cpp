#include <iostream>

using namespace std;

void print(const int x, const int y){
    cout << "x = " << x << ", y = " << y << endl;
}

void swap_by_value(int a, int b){
    a = (a + b) - (b = a);
}

void swap_by_reference(int& a, int& b){
    a = (a + b) - (b = a);
}

void swap_by_pointer(int* a, int* b){
    if (!a || !b) return;
    *a = (*a + *b) - (*b = *a);
    //int tmp = *a; *a = *b; *b = tmp;
}

int main(){
    int x = 10, y = 20;
    swap_by_value(x, y); // x and y in main are still 10, 20 (no change)
    cout << "Swapped by value: x = " << x << ", y = " << y << endl; // Output: Swapped by value: x = 10, y = 20
    swap_by_pointer(&x, &y); // x and y in main are now 20, 10 (swapped)
    cout << "Swapped by pointer: x = " << x << ", y = " << y << endl; // Output: Swapped by pointer: x = 20, y = 10
    swap_by_reference(x, y); // x and y in main are now 10, 20 (swapped back)
    cout << "Swapped by reference: x = " << x << ", y = " << y << endl; // Output: Swapped by reference: x = 10, y = 20
}