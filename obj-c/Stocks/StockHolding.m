//
//  StockHolding.m
//  Stocks
//
//  Created by Daria on 31.10.2023.
//

#import "StockHolding.h"

@implementation StockHolding
@synthesize purchaseSharePrice, currentSharePrice, numberOfShares;
- (float) costInDollars
{
    return [self purchaseSharePrice] * [self numberOfShares];
}
- (float) valueInDollars
{
    return [self currentSharePrice] * [self numberOfShares];
}
- (void) addToArray:
    (NSMutableArray *)theArray
{
    [theArray addObject:self];
}

- (void) init:
    (float) purchasePrice
    withCurrentPrice: (float) currentPrice
    withNumber: (int) number
{
    [self setPurchaseSharePrice:purchasePrice];
    [self setCurrentSharePrice:currentPrice];
    [self setNumberOfShares:number];
}
@end
