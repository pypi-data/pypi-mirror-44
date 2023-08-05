
/**************************************************************************
 *                                                                        *
 *  Regina - A Normal Surface Theory Calculator                           *
 *  iOS User Interface                                                    *
 *                                                                        *
 *  Copyright (c) 1999-2018, Ben Burton                                   *
 *  For further details contact Ben Burton (bab@debian.org).              *
 *                                                                        *
 *  This program is free software; you can redistribute it and/or         *
 *  modify it under the terms of the GNU General Public License as        *
 *  published by the Free Software Foundation; either version 2 of the    *
 *  License, or (at your option) any later version.                       *
 *                                                                        *
 *  As an exception, when this program is distributed through (i) the     *
 *  App Store by Apple Inc.; (ii) the Mac App Store by Apple Inc.; or     *
 *  (iii) Google Play by Google Inc., then that store may impose any      *
 *  digital rights management, device limits and/or redistribution        *
 *  restrictions that are required by its terms of service.               *
 *                                                                        *
 *  This program is distributed in the hope that it will be useful, but   *
 *  WITHOUT ANY WARRANTY; without even the implied warranty of            *
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU     *
 *  General Public License for more details.                              *
 *                                                                        *
 *  You should have received a copy of the GNU General Public             *
 *  License along with this program; if not, write to the Free            *
 *  Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston,       *
 *  MA 02110-1301, USA.                                                   *
 *                                                                        *
 **************************************************************************/

#import "LinkViewController.h"
#import "LinkPolynomials.h"
#import "ReginaHelper.h"
#import "link/link.h"

#define MAX_LINK_AUTO_POLYNOMIALS 6
#define KEY_LINK_HOMFLY_TYPE @"LinkHomflyType"

@interface LinkPolynomials () <UITextFieldDelegate> {
    UILabel* copyFrom;
}
@property (weak, nonatomic) IBOutlet UILabel *header;

@property (weak, nonatomic) IBOutlet UILabel *jones;
@property (weak, nonatomic) IBOutlet UILabel *homfly;
@property (weak, nonatomic) IBOutlet UILabel *bracket;
@property (weak, nonatomic) IBOutlet UIButton *calculateJones;
@property (weak, nonatomic) IBOutlet UIButton *calculateHomfly;
@property (weak, nonatomic) IBOutlet UIButton *calculateBracket;
@property (weak, nonatomic) IBOutlet UISegmentedControl *homflyType;

@property (assign, nonatomic) regina::Link* packet;
@end

@implementation LinkPolynomials

- (void)viewDidLoad
{
    UILongPressGestureRecognizer *r = [[UILongPressGestureRecognizer alloc] initWithTarget:self action:@selector(longPress:)];
    [self.view addGestureRecognizer:r];
}

- (void)viewWillAppear:(BOOL)animated {
    [super viewWillAppear:animated];
    self.homflyType.selectedSegmentIndex = [[NSUserDefaults standardUserDefaults] integerForKey:KEY_LINK_HOMFLY_TYPE];
    
    self.packet = static_cast<regina::Link*>(static_cast<id<PacketViewer> >(self.parentViewController).packet);

    [self reloadPacket];
}

- (IBAction)longPress:(id)sender {
    UILongPressGestureRecognizer *press = static_cast<UILongPressGestureRecognizer*>(sender);
    if (press.state == UIGestureRecognizerStateBegan) {
        copyFrom = nil;
        CGPoint location = [press locationInView:self.view];
        if (self.packet->knowsJones() && CGRectContainsPoint(self.jones.frame, location))
            copyFrom = self.jones;
        else if (self.packet->knowsHomfly() && CGRectContainsPoint(self.homfly.frame, location))
            copyFrom = self.homfly;
        else if (self.packet->knowsBracket() && CGRectContainsPoint(self.bracket.frame, location))
            copyFrom = self.bracket;
        if (! copyFrom)
            return;
        
        [self becomeFirstResponder];
        
        UIMenuItem *menuItem = [[UIMenuItem alloc] initWithTitle:@"Copy Plain Text" action:@selector(copyPlain:)];
        UIMenuController *copyMenu = [UIMenuController sharedMenuController];
        CGRect textBounds = [copyFrom textRectForBounds:copyFrom.bounds limitedToNumberOfLines:copyFrom.numberOfLines];
        [copyMenu setTargetRect:textBounds inView:copyFrom];
        copyMenu.arrowDirection = UIMenuControllerArrowDefault;
        copyMenu.menuItems = [NSArray arrayWithObject:menuItem];
        [copyMenu setMenuVisible:YES animated:YES];
    }
}

- (void)reloadPacket
{
    [static_cast<LinkViewController*>(self.parentViewController) updateHeader:self.header];

    if (self.packet->knowsJones() || self.packet->size() <= MAX_LINK_AUTO_POLYNOMIALS) {
        self.calculateJones.hidden = YES;
        self.jones.text = @(self.packet->jones().utf8(regina::Link::jonesVar).c_str());
    } else {
        self.jones.text = @" ";
        self.calculateJones.hidden = NO;
        self.calculateJones.enabled = YES;
    }

    if (self.packet->knowsHomfly() || self.packet->size() <= MAX_LINK_AUTO_POLYNOMIALS) {
        self.calculateHomfly.hidden = YES;
        if (self.homflyType.selectedSegmentIndex == 0)
            self.homfly.text = @(self.packet->homflyAZ().utf8(regina::Link::homflyAZVarX, regina::Link::homflyAZVarY).c_str());
        else
            self.homfly.text = @(self.packet->homflyLM().utf8(regina::Link::homflyLMVarX, regina::Link::homflyLMVarY).c_str());
    } else {
        self.homfly.text = @" ";
        self.calculateHomfly.hidden = NO;
        self.calculateHomfly.enabled = YES;
    }

    if (self.packet->knowsBracket() || self.packet->size() <= MAX_LINK_AUTO_POLYNOMIALS) {
        self.calculateBracket.hidden = YES;
        self.bracket.text = @(self.packet->bracket().utf8("A").c_str());
    } else {
        self.bracket.text = @" ";
        self.calculateBracket.hidden = NO;
        self.calculateBracket.enabled = YES;
    }
    
    self.homflyType.enabled = YES;
}

- (IBAction)computeJones:(id)sender {
    self.calculateJones.enabled = NO;
    self.calculateHomfly.enabled = NO;
    self.calculateBracket.enabled = NO;
    self.homflyType.enabled = NO;
    [ReginaHelper runWithHUD:@"Calculating…"
                        code:^{
                            self.packet->jones();
                        }
                     cleanup:^{
                         [self reloadPacket];
                     }];
}

- (IBAction)computeHomfly:(id)sender {
    self.calculateHomfly.enabled = NO;
    self.calculateJones.enabled = NO;
    self.calculateBracket.enabled = NO;
    self.homflyType.enabled = NO;
    [ReginaHelper runWithHUD:@"Calculating…"
                        code:^{
                            self.packet->homfly();
                        }
                     cleanup:^{
                         [self reloadPacket];
                     }];
}

- (IBAction)computeBracket:(id)sender {
    self.calculateBracket.enabled = NO;
    self.calculateJones.enabled = NO;
    self.calculateHomfly.enabled = NO;
    self.homflyType.enabled = NO;
    [ReginaHelper runWithHUD:@"Calculating…"
                        code:^{
                            self.packet->bracket();
                        }
                     cleanup:^{
                         [self reloadPacket];
                     }];
}

- (IBAction)homflyTypeChanged:(id)sender {
    [[NSUserDefaults standardUserDefaults] setInteger:self.homflyType.selectedSegmentIndex forKey:KEY_LINK_HOMFLY_TYPE];
    if (self.packet->knowsHomfly())
        [self reloadPacket];
}

#pragma mark - UIResponder

- (BOOL)canBecomeFirstResponder
{
    return (copyFrom != nil);
}

- (BOOL)canPerformAction:(SEL)action withSender:(id)sender
{
    if (action == @selector(copy:) && copyFrom)
        return YES;
    else
        return [super canPerformAction:action withSender:sender];
}

- (void)copy:(id)sender
{
    if (copyFrom)
        [[UIPasteboard generalPasteboard] setString:copyFrom.text];
}

- (void)copyPlain:(id)sender
{
    // Copy the selected polynomial in plain ASCII only.
    if (copyFrom == self.jones) {
        if (self.packet->knowsJones())
            [[UIPasteboard generalPasteboard] setString:@(self.packet->jones().str("x").c_str())];
        else
            [[UIPasteboard generalPasteboard] setString:@""];
    } else if (copyFrom == self.homfly) {
        if (self.packet->knowsHomfly()) {
            if (self.homflyType.selectedSegmentIndex == 0)
                [[UIPasteboard generalPasteboard] setString:@(self.packet->homflyAZ().str("a", "z").c_str())];
            else
                [[UIPasteboard generalPasteboard] setString:@(self.packet->homflyLM().str("l", "m").c_str())];
        } else
            [[UIPasteboard generalPasteboard] setString:@""];
    } else if (copyFrom == self.bracket) {
        if (self.packet->knowsBracket())
            [[UIPasteboard generalPasteboard] setString:@(self.packet->bracket().str("A").c_str())];
        else
            [[UIPasteboard generalPasteboard] setString:@""];
    } else
        [[UIPasteboard generalPasteboard] setString:@""];
}

@end
