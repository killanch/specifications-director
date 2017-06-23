/*
* Copyright (c) 2016, Alcatel-Lucent Inc
* All rights reserved.
*
* Redistribution and use in source and binary forms, with or without
* modification, are permitted provided that the following conditions are met:
*     * Redistributions of source code must retain the above copyright
*       notice, this list of conditions and the following disclaimer.
*     * Redistributions in binary form must reproduce the above copyright
*       notice, this list of conditions and the following disclaimer in the
*       documentation and/or other materials provided with the distribution.
*     * Neither the name of the copyright holder nor the names of its contributors
*       may be used to endorse or promote products derived from this software without
*       specific prior written permission.
*
* THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
* ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
* WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
* DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY
* DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
* (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
* LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
* ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
* (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
* SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

@import <Foundation/Foundation.j>
@import <NUKit/NUModuleSelfParent.j>
@import "../../Models/SDModels.j"

@global SDAttributeTypeBoolean

@implementation SDEditorAttributeSelfViewController : NUModuleSelfParent
{
    @outlet CPTableView tableViewEnumarationValues;
    @outlet CPView      viewEditorEnumConfig;
    @outlet CPView      viewEditorEnumFlags;
    @outlet CPView      viewEditorNumberConfig;
    @outlet CPView      viewEditorStringConfig;
}


#pragma mark -
#pragma mark Initialization

+ (CPString)moduleName
{
    return @"Attribute";
}

+ (CPString)moduleTabIconIdentifier
{
    return @"self";
}

- (void)viewDidLoad
{
    var textField = [[tableViewEnumarationValues tableColumns][0] dataView];
    [textField setPlaceholderString:@"Double click to enter the value"];
    [[tableViewEnumarationValues tableColumns][0] setDataView:nil];
    [[tableViewEnumarationValues tableColumns][0] setDataView:textField];

    [super viewDidLoad];
}

- (void)configureContexts
{
    var context = [[NUModuleContext alloc] initWithName:@"Attribute" identifier:[SDAttribute RESTName]];
    [context setButtonSave:buttonSave];
    [context setEditionView:[self view]];
    [context setSearchForTagsRecursively:YES];
    [context setAdditionalEditionViews:[viewEditionMain, viewEditorStringConfig, viewEditorNumberConfig, viewEditorEnumConfig, viewEditorEnumFlags]];
    [self registerContext:context forClass:SDAttribute];
}


#pragma mark -
#pragma mark NUModule API

- (void)moduleUpdateEditorInterface
{
    var conditionRepoHasPushPermission = [[SDRepository currentRepository] pushPermission],
        conditionCanEdit               = conditionRepoHasPushPermission;

    [_currentContext setBoundControlsEnabled:conditionCanEdit];
}


#pragma mark -
#pragma mark NUModuleSelfParent API

- (CPArray)moduleCurrentVisibleEditionViews
{
    var editionViews = [viewEditionMain],
        editedObject = [_currentContext editedObject];

    switch ([editedObject type])
    {
        case SDAttributeTypeInteger:
        case SDAttributeTypeFloat:
            [editionViews addObject:viewEditorNumberConfig]
            break;

        case SDAttributeTypeString:
            [editionViews addObject:viewEditorStringConfig];
            break;

        case SDAttributeTypeEnum:
            [editionViews addObject:viewEditorEnumConfig];
            break;
    }

    [editionViews addObject:viewEditorEnumFlags];

    return editionViews;
}

#pragma mark -
#pragma mark Action

- (IBAction)changeType:(id)aSender
{
    var editedObject = [_currentContext editedObject];
    if (editedObject._type == SDAttributeTypeBoolean && !editedObject._defaultValue)
    {
        editedObject._defaultValue = "false";
    }
    [self reloadStackView];
}

@end
