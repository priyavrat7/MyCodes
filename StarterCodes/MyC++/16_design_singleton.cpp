#include <iostream>
#include <vector>

using namespace std;

/* Singleton Design Pattern:
    - It ensures that a class has only one instance
    - The class provides a single, globally accessible entry point, for example Singleton::getInstance()

*/

class Singleton{
    private:
        Singleton() {}; // private constructor

        Singleton(const Singleton&) = delete; // removing the copy constructor

        Singleton& operator=(const Singleton&) = delete; // removing the assignment operator

    public:
        int data;
        static Singleton& getInstance(){
            static Singleton instance; // static instance of Singleton class is created only once and it is destroyed only when the program ends, which is thread safe

            // Singleton instance; // NOT THREAD SAFE, not recommended
            
            return instance;
        }
        void showMessage(){
            cout << "Hello, I am a Singleton class" << endl;
        }
        ~Singleton(){
            cout << "Singleton destructor is called" << endl;
        }
};

int main(){
    Singleton& s1 = Singleton::getInstance();
    s1.data = 10;
    cout << "s1.data = " << s1.data << endl;

    //Create another instance
    Singleton& s2 = Singleton::getInstance();
    cout << "s2.data = " << s2.data << endl; // s2.data is also same as s1.data
    // Because s1 and s2 are the same instance

    /* Singleton copy_s1 = s1; // Trying to copy, using the copy constructor
    cout << "copy_s1.data = " << copy_s1.data << endl; // copy_s1.data is also same as s1.data 
    It will work if we do not remove copy constructor, because the copy constructor is defaulted in the class
    */
    

}