#include <iostream>

int main() {
    int numCount;
    cout <<"How many numbers do you want to average? ";
    cin >> numCount // Missing semicolon here

    int numbers[numCout]; // Need to dynamically allocate if numCount is not known at compile time
    int sum = 0;

    for (int i = 0, i < numCount; i++) { // Comma instead of semicolon in for loop initialization
        cout << "Enter number " << i + 1 << ": ";
        cin >> numbers[i];
        sum =+ numbers[i]; // += should be used for addition assignment
    }

    double average = sum / numCount; // Missing semicolon here
    cout >> "The average is: " << average << endl; // << should be used for output

    return 0;
}