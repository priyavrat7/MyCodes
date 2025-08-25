#include <iostream>
#include <memory>
#include <vector>
#include <string>
#include <typeinfo>

const double BASE = 100.0;

using namespace std;

/*
Strategy Pattern UML Diagram (as implemented in this file):

+-------------------+           +---------------------+
|   Payment         |<----------| CreditCardPayment   |
|-------------------|           +---------------------+
| +pay(amount):void |           | +pay(amount):void   |
|-------------------|           +---------------------+
| <<interface>>     |
+-------------------+           +---------------------+
        ^                       | DebitCardPayment    |
        |                       +---------------------+
        |                       | +pay(amount):void   |
        |                       +---------------------+
        |                       +---------------------+
        |                       | PayPalPayment       |
        |                       +---------------------+
        |                       | +pay(amount):void   |
        |                       +---------------------+
        |                       +---------------------+
        |                       | GiftCardPayment     |
        |                       +---------------------+
        |                       | +pay(amount):void   |
        |                       +---------------------+
        |
+----------------------+
|  PaymentProcessor    |
+----------------------+
| -payment: Payment*   |
+----------------------+
| +processPayment()    |
+----------------------+

Legend:
- Payment is the Strategy interface (abstract class with pure virtual function).
- CreditCardPayment, DebitCardPayment, PayPalPayment, GiftCardPayment are Concrete Strategies implementing Payment.
- PaymentProcessor is the Context, which uses a Payment strategy to process payments.

The context (PaymentProcessor) is configured with a Payment strategy at runtime and delegates the payment processing to the strategy object.
*/


class Payment{
    public:
        virtual void pay(const double& amount) const = 0;
        virtual ~Payment() {}
};

class CreditCardPayment : public Payment{
    void pay(const double& amount) const override{
        cout << "Processing credit card payment of " << amount << " dollars by Credit Card" << endl;
    }
};

class DebitCardPayment : public Payment{
    void pay(const double& amount) const override{
        cout << "Processing debit card payment of " << amount << " dollars by Debit Card" << endl;
    }
};

class PayPalPayment : public Payment{
    void pay(const double& amount) const override{
        cout << "Processing PayPal payment of " << amount << " dollars by PayPal" << endl;
    }
};

class GiftCardPayment : public Payment{
    void pay(const double& amount) const override{
        cout << "Processing gift card payment of " << amount << " dollars by Gift Card" << endl;
    }
};

class PaymentProcessor{
    private:
        unique_ptr<Payment> payment;

    public:
        PaymentProcessor(unique_ptr<Payment> p) : payment(std::move(p)){}

        void processPayment(const double& amount) const{
            payment->pay(amount);
        }
};

int main(){
    
    unique_ptr<CreditCardPayment> creditCardPayment = make_unique<CreditCardPayment>();
    auto debitCardPayment = make_unique<DebitCardPayment>();
    unique_ptr<PayPalPayment> payPalPayment = make_unique<PayPalPayment>();
    auto giftCardPayment = make_unique<GiftCardPayment>();
    //unique_ptr<Payment> payPalPayment = make_unique<Payment>(); // This is not allowed because Payment is an abstract class

    unique_ptr<Payment> payment; // This is allowed, but it is not a good practice


    vector<unique_ptr<Payment>> payments;
    payments.push_back(std::move(creditCardPayment));
    payments.push_back(std::move(debitCardPayment));
    payments.push_back(std::move(payPalPayment));
    payments.push_back(std::move(giftCardPayment));
    
    for(auto it = payments.begin(); it != payments.end(); ++it){
        cout << "it: " << *it << endl;
        (*it)->pay(BASE + (it - payments.begin()));
    }

    for(size_t i = 0; i < payments.size(); ++i){
        payments[i]->pay(BASE + i);
    }

}