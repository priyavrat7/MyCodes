#include <iostream>
#include <vector>
#include <algorithm>
#include <numeric>

using namespace std;

int main(){
    vector<float> v = {5.5, 3.3, 32.2, 1.1, 34.4};

    // sort algorithm complexity is O(nlogn)
    sort(v.begin(), v.end()); // sort the vector in ascending order
    for(auto it = v.begin(); it != v.end(); ++it){
        cout << *it << " ";
    }

    cout << endl;

    sort(v.begin(), v.end(), greater<float>()); // sort the vector in descending order
    for(auto i : v){
        cout << i << " ";
    }

    cout << endl;

    // find algorithm complexity is O(n)
    auto it = find(v.begin(), v.end(), 32.2f);
    if (it != v.end()){
        cout << "32.2 is found in the vector" << endl;
    }
    // if the element is not found, it returns v.end()
    else{
        cout << "32.2 is not found in the vector" << endl;
    }

    float sum = std::accumulate(v.begin(), v.end(), 0.0f);
    cout << "Sum of the vector is " << sum << endl;
    
}