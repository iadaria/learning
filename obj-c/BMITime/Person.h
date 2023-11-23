//
//  Person.h
//  BMITime
//
//  Created by Daria on 29.10.2023.
//

#import <Foundation/Foundation.h>

NS_ASSUME_NONNULL_BEGIN

@interface Person : NSObject {
    float heightInMeters;
    int weightInKilos;
}
@property float heightInMeters;
//- (float) heightInMeters;
//- (void) setHeightInMeters: (float)h;
@property int weightInKilos;
//- (int) weightInKilos;
//- (void) setWeightInKilos: (int)w;
- (float) bodyMassIndex;
- (void) addYourselfToArray: (NSMutableArray *)theArray;
@end

NS_ASSUME_NONNULL_END
