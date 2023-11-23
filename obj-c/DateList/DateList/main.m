//
//  main.m
//  DateList
//
//  Created by Daria on 24.10.2023.
//

#import <Foundation/Foundation.h>

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        NSDate *now = [NSDate date];
        NSDate *tomorrow = [now dateByAddingTimeInterval:24.0 * 60.0 * 60.0];
        NSDate *yesterday = [now dateByAddingTimeInterval:-24.0 * 60.0 * 60.0];
        
        NSArray *dateList = [NSArray arrayWithObjects:now, tomorrow, yesterday, nil];
        
        NSLog(@"There are %lu dates", [dateList count]);
        
        for (NSDate *date in dateList) {
            NSLog(@"Here is a date: %@", date);
        }
        
        NSMutableArray *dateMutableList = [NSMutableArray array];
        
        [dateMutableList addObject:now];
        [dateMutableList addObject:tomorrow];
        [dateMutableList insertObject:yesterday atIndex:0];
        
        for (NSDate *dateMutable in dateMutableList) {
            NSLog(@"Here is a date: %@", dateMutable);
        }
        
        [dateMutableList removeObjectAtIndex:0];
        NSLog(@"Now the first date is %@", [dateList objectAtIndex:0]);
    }
    return 0;
}
