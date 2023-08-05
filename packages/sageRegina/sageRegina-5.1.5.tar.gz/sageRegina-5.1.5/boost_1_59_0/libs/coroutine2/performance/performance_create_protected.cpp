
//          Copyright Oliver Kowalke 2014.
// Distributed under the Boost Software License, Version 1.0.
//    (See accompanying file LICENSE_1_0.txt or copy at
//          http://www.boost.org/LICENSE_1_0.txt)

#include <cstdlib>
#include <iostream>
#include <stdexcept>

#include <boost/chrono.hpp>
#include <boost/coroutine2/all.hpp>
#include <boost/cstdint.hpp>
#include <boost/program_options.hpp>

#include "bind_processor.hpp"
#include "clock.hpp"
#include "cycle.hpp"

typedef boost::coroutines2::protected_fixedsize_stack   stack_allocator;
typedef boost::coroutines2::coroutine< void >           coro_type;

bool preserve = false;
boost::uint64_t jobs = 1000;

void fn( coro_type::pull_type & c)
{ while ( true) c(); }

duration_type measure_time( duration_type overhead)
{
    stack_allocator stack_alloc;

    time_point_type start( clock_type::now() );
    for ( std::size_t i = 0; i < jobs; ++i) {
        coro_type::push_type c( stack_alloc, fn, preserve);
    }
    duration_type total = clock_type::now() - start;
    total -= overhead_clock(); // overhead of measurement
    total /= jobs;  // loops

    return total;
}

# ifdef BOOST_CONTEXT_CYCLE
cycle_type measure_cycles( cycle_type overhead)
{
    stack_allocator stack_alloc;

    cycle_type start( cycles() );
    for ( std::size_t i = 0; i < jobs; ++i) {
        coro_type::push_type c( stack_alloc, fn, preserve);
    }
    cycle_type total = cycles() - start;
    total -= overhead; // overhead of measurement
    total /= jobs;  // loops

    return total;
}
# endif

int main( int argc, char * argv[])
{
    try
    {
        bool bind = false;
        boost::program_options::options_description desc("allowed options");
        desc.add_options()
            ("help", "help message")
            ("bind,b", boost::program_options::value< bool >( & bind), "bind thread to CPU")
            ("fpu,f", boost::program_options::value< bool >( & preserve), "preserve FPU registers")
            ("jobs,j", boost::program_options::value< boost::uint64_t >( & jobs), "jobs to run");

        boost::program_options::variables_map vm;
        boost::program_options::store(
                boost::program_options::parse_command_line(
                    argc,
                    argv,
                    desc),
                vm);
        boost::program_options::notify( vm);

        if ( vm.count("help") ) {
            std::cout << desc << std::endl;
            return EXIT_SUCCESS;
        }

        if ( bind) bind_to_processor( 0);

        duration_type overhead_c = overhead_clock();
        std::cout << "overhead " << overhead_c.count() << " nano seconds" << std::endl;
        boost::uint64_t res = measure_time( overhead_c).count();
        std::cout << "average of " << res << " nano seconds" << std::endl;
#ifdef BOOST_CONTEXT_CYCLE
        cycle_type overhead_y = overhead_cycle();
        std::cout << "overhead " << overhead_y << " cpu cycles" << std::endl;
        res = measure_cycles( overhead_y);
        std::cout << "average of " << res << " cpu cycles" << std::endl;
#endif

        return EXIT_SUCCESS;
    }
    catch ( std::exception const& e)
    { std::cerr << "exception: " << e.what() << std::endl; }
    catch (...)
    { std::cerr << "unhandled exception" << std::endl; }
    return EXIT_FAILURE;
}
