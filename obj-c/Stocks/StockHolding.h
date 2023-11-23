//
//  StockHolding.h
//  Stocks
//
//  Created by Daria on 31.10.2023.
//

#import <Foundation/Foundation.h>

NS_ASSUME_NONNULL_BEGIN

@interface StockHolding : NSObject {
    float purchaseSharePrice;
    float currentSharePrice;
    int numberOfShares;
}
@property float purchaseSharePrice; // в местной валюте = 200 руб
@property float currentSharePrice; // в местной валюте = 100 руб
@property int numberOfShares;
- (float) costInDollars;
- (float) valueInDollars;
- (void) addToArray: (NSMutableArray *)theArray;
- (void) init:
    (float) purchasePrice
    withCurrentPrice: (float) currentPrice
    withNumber: (int) number;

@end

NS_ASSUME_NONNULL_END
