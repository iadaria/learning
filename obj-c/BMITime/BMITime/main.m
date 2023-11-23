//
//  main.m
//  BMITime
//
//  Created by Daria on 29.10.2023.
//
#import "Person.h"
#import "Employee.h"
#import <Foundation/Foundation.h>

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        Person *person = [[Person alloc] init];
        [person setWeightInKilos:67];
        [person setHeightInMeters:1.73];

        float bmi = [person bodyMassIndex];
        NSLog(@"person (%d, %f) has a BMI of %f",[person weightInKilos], [person heightInMeters], bmi);
        
        Employee *person2 = [[Employee alloc] init];
        [person2 setWeightInKilos:67];
        [person2 setHeightInMeters:1.73];
        [person2 setEmployeeID:111];

        bmi = [person2 bodyMassIndex];
        NSLog(@"person (%d, %f) has a BMI of %f",[person2 weightInKilos], [person2 heightInMeters], bmi);
    }
    
    return 0;
}
