#include <iostream>
#include <vector>
#include <typeinfo>

using namespace std;

int main(){
    vector<int> v = {1, 2, 3, 4, 5, 6, 7};

    cout << "Type of v is: " << typeid(v).name() << endl;

    // range based for loop
    for (auto i : v){
        cout << i*i << " ";
    }

    cout << endl;

    // auto deduces vector<int>::iterator
    for (auto it = v.begin(); it != v.end(); ++it){
        cout << *it << " ";
    } 
    
    cout << endl;

    size_t index= 0;
    for (auto it = v.begin(); it != v.end(); ++it, ++index){
        cout << "v[" << index << "] = " << *it << endl;
    }
}