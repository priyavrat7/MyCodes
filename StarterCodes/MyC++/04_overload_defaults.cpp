#include <iostream>
#include <string>

using namespace std;

// Function overloading:
void greet(const string& s){
    cout << "Hello, " << s << endl;
}

void greet(const string& s, int times){
    while(times--) cout << "Hello, " << s << endl;
}

int add(int a, int b = 11){
    return a + b;
}

int main(){
    greet("Priv");
    greet("Priv", 3);

    cout << add(19) << endl;
    cout << add(3, 7) << endl;
}