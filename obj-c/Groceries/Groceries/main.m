//
//  main.m
//  Groceries
//
//  Created by Daria on 24.10.2023.
//

#import <Foundation/Foundation.h>

@interface Chapter15:NSObject
- (void) groceries;
- (void) findNames;
@end

@implementation Chapter15
- (void) groceries {
    NSString *chocolate = @"Milko 5 goods";
    NSString *juice = [NSString stringWithFormat:@"Apple juices %d", 5];
    
    NSMutableArray *goods = [NSMutableArray array];
    
    [goods addObject:chocolate];
    [goods addObject:juice];
    
    for (NSString *good in goods) {
        NSLog(@"Here is %@", good);
    }
}
- (void) findNames {
    NSString *nameString = [NSString stringWithContentsOfFile:@"/Users/daria/Documents/temp/propernames" encoding:NSUTF8StringEncoding error:NULL];
    
    NSArray *names = [nameString componentsSeparatedByString:@"\n"];
    
    for(NSString *name in names) {
        NSRange r = [name rangeOfString:@"AA" options:NSCaseInsensitiveSearch];
        
        if (r.location != NSNotFound) {
            NSLog(@"%@", name);
        }
    }
}
@end

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        //[[[Chapter15 alloc] init] groceries];
        [[[Chapter15 alloc] init] findNames];
    }
    return 0;
}
