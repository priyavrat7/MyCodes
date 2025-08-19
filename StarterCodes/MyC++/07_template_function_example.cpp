#include <iostream>
#include <string>

using namespace std;

template <typename T>
void print(const vector<T>& v){
    cout << "[";
    for(size_t i = 0; i < v.size(); i++){
        cout << v[i];
        if (i + 1 < v.size()) cout << ", ";
    }
    cout << "]" << endl;
}

int main(){
    vector<int> vi {1, 2, 3, 4, 5};
    vector<string> vs {"Hello", "World", "C++", "Template", "Function"};

    print(vi);
    print(vs);

    return 0;
}