//
//  main.m
//  BMITime
//
//  Created by Daria on 29.10.2023.
//
#import "Person.h"
#import <Foundation/Foundation.h>

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        Person *person = [[Person alloc] init];
        [person setWeightInKilos:67];
        [person setHeightInMeters:1.73];
        float bmi = [person bodyMassIndex];
        NSLog(@"person (%d, %f) has a BMI of %f",[person weightInKilos], [person heightInMeters], bmi);
    }
    return 0;
}
