#include <iostream>
#include <string>

using namespace std;

int count_upper(const string& s){
    int cnt = 0;
    for (unsigned char ch : s){
        if (isupper(ch)) cnt++;
    }
    return cnt;
}

int main(){
    cout << count_upper("ABcDE") << endl;
}
// Why const std::string&? 
// Passing by const reference (const std::string&) avoids making a copy of the string, which is more efficient, especially for large strings. 
// The const qualifier guarantees that the function will not modify the original string, providing safety and clarity of intent.
// This is generally the preferred way to pass large objects that should not be modified.
 // Example:
 // int count_upper(const std::string& s)
 // Here, s is not copied and cannot be changed inside the function.
