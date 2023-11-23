//
//  Person.m
//  BMITime
//
//  Created by Daria on 29.10.2023.
//

#import "Person.h"

@implementation Person
/*- (float) heightInMeters {
    return heightInMeters;
}
- (void) setHeightInMeters:(float)h {
    heightInMeters = h;
}
- (int) weightInKilos {
    return weightInKilos;
}
- (void) setWeightInKilos:(int)w {
    weightInKilos = w;
}*/
@synthesize heightInMeters, weightInKilos;
- (float) bodyMassIndex {
    float h = [self heightInMeters];
    return [self weightInKilos] / (h * h);
}
- (void) addYourselfToArray: (NSMutableArray *)theArray {
    [theArray addObject:self];
}
@end
