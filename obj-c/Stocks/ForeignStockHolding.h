//
//  ForeignStockHolding.h
//  Stocks
//
//  Created by Daria on 06.11.2023.
//

#import <Foundation/Foundation.h>
#import "StockHolding.h"

NS_ASSUME_NONNULL_BEGIN

@interface ForeignStockHolding : StockHolding {
    float conversionRate;
}
@property float conversionRate;
@end

NS_ASSUME_NONNULL_END
