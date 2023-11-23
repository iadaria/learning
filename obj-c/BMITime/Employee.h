//
//  Employee.h
//  BMITime
//
//  Created by Daria on 05.11.2023.
//

#import <Foundation/Foundation.h>
#import "Person.h"

NS_ASSUME_NONNULL_BEGIN

@interface Employee : Person
{
    int employeeID;
}
@property int employeeID;
@end

NS_ASSUME_NONNULL_END
