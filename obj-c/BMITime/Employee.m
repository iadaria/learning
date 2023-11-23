//
//  Employee.m
//  BMITime
//
//  Created by Daria on 05.11.2023.
//

#import "Employee.h"

@implementation Employee
@synthesize employeeID;
- (float) bodyMassIndex {
    float normalBMI = [super bodyMassIndex];
    return normalBMI * 0.9;
}
@end
