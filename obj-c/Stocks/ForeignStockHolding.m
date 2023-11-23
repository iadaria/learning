//
//  ForeignStockHolding.m
//  Stocks
//
//  Created by Daria on 06.11.2023.
//

#import "ForeignStockHolding.h"

@implementation ForeignStockHolding
@synthesize conversionRate;
- (float) costInDollars
{
    return [self purchaseSharePrice] * [self numberOfShares] * [self conversionRate];
}
- (float) valueInDollars
{
    return [self currentSharePrice] * [self numberOfShares] * [self conversionRate];
}
@end
