
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

#import <Foundation/Foundation.h>

namespace CppUnit {
    class TestFailure;
}

@interface TestSuiteController : UIViewController

/**
 * Runs the test suite.
 * Must be called from the main thread.
 */
- (void)runTests;

/**
 * Called at the beginning of each test.
 * May be called from any thread.
 */
- (void)startTest:(NSString*)name;
/**
 * Called at the end of a test if that test succeeds.
 * May be called from any thread.
 */
- (void)success;
/**
 * Called at the end of a test if that test fails.
 * May be called from any thread.
 */
- (void)failure:(const CppUnit::TestFailure&)failure;
/**
 * Called after all tests are finished.
 * May be called from any thread.
 */
- (void)finished;

@end

@interface WelcomeViewController : UIViewController
@end
