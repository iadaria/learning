//
//  main.m
//  Stocks
//
//  Created by Daria on 31.10.2023.
//

#import <Foundation/Foundation.h>
#import "StockHolding.h"
#import "ForeignStockHolding.h"

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        NSMutableArray *stocks = [NSMutableArray array];
        
        StockHolding *stock1 = [[StockHolding alloc] init];
        [stock1 init:2.30 withCurrentPrice:4.50 withNumber:40];
        [stock1 addToArray:stocks];
        
        StockHolding *stock2 = [[StockHolding alloc] init];
        [stock2 init:12.18 withCurrentPrice:10.56 withNumber:90];
        [stock2 addToArray:stocks];
        
        StockHolding *stock3 = [[StockHolding alloc] init];
        [stock3 init:2.30 withCurrentPrice:4.50 withNumber:40];
        [stock3 addToArray:stocks];
        
        ForeignStockHolding *stock4 = [[ForeignStockHolding alloc] init];
        [stock4 init:2.30 withCurrentPrice:4.50 withNumber:40];
        [stock4 setConversionRate:0.011];
        [stock4 addToArray:stocks];

        
        for (StockHolding *stock in stocks) {
            NSLog(@"Stock: purchase = %f, current = %f, number = %d, costIn$ = %f $, valueIn$ = %f $", [stock purchaseSharePrice], [stock currentSharePrice], [stock numberOfShares], [stock costInDollars], [stock valueInDollars]);
        }
        
    }
    return 0;
}
