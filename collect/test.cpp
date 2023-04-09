#include <iostream>


int main(){

std::string s;
int arr[3];

std::cin >> s;

for(int i=0; i<s.size(); i+= 2){
    if(s[i] == 1){
        arr[0] += 1;
    }
    else if(s[i] == 2){
        arr[1] += 1;
    }
    else{
        arr[2] += 1;
    }

return 0;
}}
