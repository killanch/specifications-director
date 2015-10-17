@import <Foundation/Foundation.j>
@import <RESTCappuccino/NURESTAbstractUser.j>

@class SDRepositoriesFetcher


@implementation SDAuth : NURESTAbstractUser
{
    CPString                _username       @accessors(property=username);

    SDRepositoriesFetcher   _repositories   @accessors(property=repositories);

}


#pragma mark -
#pragma mark Initialization

+ (CPString)RESTName
{
    return @"auth";
}

- (id)init
{
    if (self = [super init])
    {
        [self exposeLocalKeyPathToREST:@"username"];
        [self exposeLocalKeyPathToREST:@"password"];

        _role = @"NURESTUserRoleCSPRoot";
        _repositories = [SDRepositoriesFetcher fetcherWithParentObject:self];
    }

    return self;
}

- (void)setRole:(CPString)aRole
{
    _role = @"NURESTUserRoleCSPRoot";
}

- (CPString)role
{
    return @"NURESTUserRoleCSPRoot";
}

@end
