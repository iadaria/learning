//
//  main.m
//  TimeAfterTime
//
//  Created by Daria on 21.09.2023.
//

#import <Foundation/Foundation.h>

@interface CalcSecondsClass:NSObject
- (int) max: (int) num1 andNum2:(int)num2;
- (void) calc;
- (void) calcTimeZone;
- (bool) isEqual: (NSString *) str1 compareWith: (NSString *) str2;
- (NSString *) getHostName;
@end

@implementation CalcSecondsClass
- (bool) isEqual:(NSString *)str1 compareWith:(NSString *)str2 {
    return [str1 isEqual:str2];
}
- (void) calcTimeZone {
    NSTimeZone *timeZone = [NSTimeZone systemTimeZone];
    bool isSummer = [timeZone isDaylightSavingTime];
    
    NSLog(@"Is the summer now? Answer: %@", isSummer ? @"YES" : @"NO" );
}
- (int)max:(int)num1 andNum2:(int)num2 {
    int result;
    if (num1 > num2) {
        result = num1;
    } else {
        result = num2;
    }
    return result;
}
- (void) calc {
    NSDateComponents *comps = [[NSDateComponents alloc] init];
    [comps setYear:1986];
    [comps setMonth:3];
    [comps setDay:23];
    NSCalendar *g = [[NSCalendar alloc] initWithCalendarIdentifier:NSCalendarIdentifierGregorian];
    
    NSDate *dateOfBirth = [g dateFromComponents:comps];
    //NSDate *now = [NSDate date];
    NSDate *now = [[NSDate alloc] init];
    double seconds = [now timeIntervalSinceDate:dateOfBirth];
    
    NSLog(@"Interval of my life is %f", seconds);
    
    NSCalendar *cal = [NSCalendar currentCalendar];
    NSUInteger day = [cal ordinalityOfUnit:NSCalendarUnitDay inUnit:NSCalendarUnitMonth forDate:now];
    NSLog(@"This is day %lu of the month", day);

}
- (NSString *) getHostName {
    NSHost *host = [NSHost currentHost];
    NSString *name = [host localizedName];
    
    return name;
}
@end

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        int a = 100;
        int b = 200;
        int ret;
        
        CalcSecondsClass *calcClass = [[CalcSecondsClass alloc] init];
        ret = [calcClass max:a andNum2:b];
        NSLog(@"Max value is : %d\n", ret);
        
        [calcClass calc];
        
        [calcClass calcTimeZone];
        
        NSLog(@"***\n");
        NSString *lament = @"Why me!?";
        NSString *x = [NSString stringWithFormat:@"The best number is %d", 5];
        NSUInteger charCount = [x length];
        NSLog(@"The length of 'x' is %lu", (unsigned long)charCount);
        if ([calcClass isEqual:lament compareWith:x])
            NSLog(@"'%@' and '%@' are equal", lament, x);
        else
            NSLog(@"'%@' and '%@' are not equla", lament, x);
        
        NSLog(@"***\n");
        NSString *hostName = [calcClass getHostName];
        NSLog(@"The name of local host is %@", hostName);
    }
    return 0;
}

