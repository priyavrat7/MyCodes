#include <iostream>
#include <vector>
#include <string>
#include <memory>
#include <typeinfo>
#include <algorithm>

using namespace std;

/*
Observer Design Pattern UML Diagram (as implemented in this file):

+-------------------+           +---------------------+
|    Subject        |<----------|      Channel        |
|-------------------|           +---------------------+
| +subscribe()      |           | -observers: vector  |
| +unsubscribe()    |           | -channelName: string|
| +notifyAll()      |           | +subscribe()        |
|-------------------|           | +unsubscribe()      |
| <<interface>>     |           | +notifyAll()        |
+-------------------+           +---------------------+
        ^
        |
        |
+-------------------+
|   Observer        |<----------+---------------------+
|-------------------|           |        User         |
| +update()         |           +---------------------+
| +getName()        |           | -username: string   |
|-------------------|           | +update()           |
| <<interface>>     |           | +getName()          |
+-------------------+           +---------------------+

Legend:
- Subject is the abstract base class (interface) for the "publisher" (Channel).
- Observer is the abstract base class (interface) for the "subscriber" (User).
- Channel is a concrete Subject, maintains a list of Observer pointers and notifies them.
- User is a concrete Observer, receives updates from Channel.
- The Channel "has a" collection of Observer pointers (subscribers).
*/


class Observer{ // abstract class
    public:
        virtual void update(const string& message) = 0;
        virtual const string& getName() const = 0;

        virtual ~Observer() {}
};

class Subject{ // abstract class
    public:
        virtual void subscribe(Observer* observer) = 0;
        virtual void unsubscribe(Observer* observer)  = 0;
        virtual void notifyAll(const string& message) = 0;
};

class User : public Observer{
    private:
        string username;
    public:
        User(const string& name) : username(name){}
        void update(const string& message) override{
            cout << username << ": " << message << endl;
        }
        const string& getName() const override { return username; }
};

class Channel : public Subject{
    private:
        vector<Observer*> observers;
        string channelName;
    public:
        Channel(const string& name) : channelName(name){}

        void subscribe(Observer* observer) override {
            observers.push_back(observer);
        }
        void unsubscribe(Observer* observer) override {
            auto flag = find(observers.begin(), observers.end(), observer);
            if(flag != observers.end()){
                cout << (*flag)->getName() << " unsubscribed from the channel: " << channelName << endl;
                observers.erase(flag);
            }
            else{
                cout << "Observer did not subscribe to the channel:" << channelName << endl;
            }
        }
        void notifyAll(const string& message) override{
            for(auto it = observers.begin(); it != observers.end(); ++it){
                (*it)->update(message);                
            }
        }
        void videoUpload(const string& title){

            notifyAll("New video uploaded: " + title);
        }
};

int main(){
    Channel channel("Its PRIV Channel"); // stack object

    User user1("Pritika"); // stack object(culprit)
    User user2("Lamha");   // hmmm
    User user3("Taniya");
    User user4("Ashish");
    User user5("Vishnu");
    User user6("Saniya");  // culprit
    User user7("Pushpendra");

    channel.subscribe(&user1);
    channel.subscribe(&user2);
    channel.subscribe(&user5);
    channel.videoUpload("Cricket");
    channel.unsubscribe(&user5);

}