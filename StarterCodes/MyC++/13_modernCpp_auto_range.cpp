#include <iostream>
#include <vector>
#include <typeinfo>

using namespace std;

int main(){
    vector<int> v = {1, 2, 3, 4, 5, 6, 7};

    cout << "Type of v is: " << typeid(v).name() << endl;

    // for loop, this is not considered as modern C++
    // Traditional for loops with index are not recommended in modern C++ because:
    // 1. They are more error-prone (e.g., off-by-one errors, incorrect index types).
    // 2. They are less readable and more verbose compared to range-based for loops.
    // 3. They do not work directly with all container types (e.g., std::list).
    // 4. Range-based for loops and iterators are safer and more generic.
    for (size_t i = 0; i != v.size(); ++i){
        cout << "v[" << i << "] = " << v[i] << endl;
    }

    // Range-based for (clear, safe, generic)
    // This range-based for loop is preferred in modern C++ because:
    // 1. It is more concise and readable than traditional for loops.
    // 2. It reduces the risk of errors such as off-by-one mistakes.
    // 3. It works seamlessly with all standard containers (vector, list, set, etc.).
    // 4. It abstracts away iterator management, making code safer and easier to maintain.
    
    for (auto i : v){  // v is unchanged, i is a copy of the element
        cout << "Range-based: " << i << endl;
    }

    cout << endl;

    for (auto& i : v){ // v is changed, i is a reference to the element
        i = i*i;
        cout << i << " ";
    }

    cout << endl;

    for (const auto& i : v){ // no change in v, i is a const reference to the element, so READ-ONLY
        cout << i << " ";
    }




    

    // auto deduces vector<int>::iterator
    // Benefits of iterator-based loops:
    // 1. Iterators provide a generic way to traverse containers, regardless of their underlying implementation (vector, list, set, etc.).
    // 2. They allow access to elements in containers that do not support random access (e.g., std::list, std::set).
    // 3. Iterator-based loops can be used to modify elements in-place (using non-const iterators).
    // 4. They enable use of standard algorithms (like std::find, std::sort) which operate on iterator ranges.
    // 5. Iterators can be used to traverse only a subrange of a container, offering more flexibility.
    // 6. They make code more generic and reusable, as algorithms can be written for any container supporting iterators.
    for (auto it = v.begin(); it != v.end(); ++it){
        cout << *it << " ";
    } 

    cout << endl;

    // with auto keyword
    for (vector<int>::iterator it = v.begin(); it != v.end(); ++it){
        cout << *it << " ";
    }
    
    cout << endl;

    size_t index= 0;
    for (auto it = v.begin(); it != v.end(); ++it, ++index){
        cout << "v[" << index << "] = " << *it << endl;
    }
}