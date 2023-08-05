//////////////////////////////////////////////////////////////////////////////
//
// (C) Copyright Ion Gaztanaga 2007-2013. Distributed under the Boost
// Software License, Version 1.0. (See accompanying file
// LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
//
// See http://www.boost.org/libs/container for documentation.
//
//////////////////////////////////////////////////////////////////////////////

#ifdef _MSC_VER
#pragma warning (disable : 4512)
#endif

#include <boost/container/detail/alloc_lib_auto_link.hpp>

#define BOOST_INTERPROCESS_VECTOR_ALLOC_STATS

#include <iostream>  //std::cout, std::endl
#include <typeinfo>  //typeid

#include <boost/timer/timer.hpp>
using boost::timer::cpu_timer;
using boost::timer::cpu_times;
using boost::timer::nanosecond_type;

template <class POD>
void allocation_timing_test(unsigned int num_iterations, unsigned int num_elements)
{
   size_t capacity = 0;
   unsigned int numalloc = 0, numexpand = 0;

   std::cout
      << "    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   \n"
      << "  Iterations/Elements:       " << num_iterations << "/" << num_elements << '\n'
      << "    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   \n"
      << std::endl;


   allocation_type malloc_types[] = { BOOST_CONTAINER_EXPAND_BWD, BOOST_CONTAINER_EXPAND_FWD, BOOST_CONTAINER_ALLOCATE_NEW };
   const char *    malloc_names[] = { "Backwards expansion", "Forward expansion", "New allocation" };
   for(size_t i = 0; i < sizeof(malloc_types)/sizeof(allocation_type); ++i){
      numalloc = 0; numexpand = 0;
      const allocation_type m_mode = malloc_types[i];
      const char *malloc_name = malloc_names[i];

      cpu_timer timer;
      timer.resume();

      for(unsigned int r = 0; r != num_iterations; ++r){
         void *first_mem = 0;
         if(m_mode != BOOST_CONTAINER_EXPAND_FWD)
            first_mem = boost_cont_malloc(sizeof(POD)*num_elements*3/2);
         void *addr = boost_cont_malloc(1*sizeof(POD));
         if(m_mode == BOOST_CONTAINER_EXPAND_FWD)
            first_mem = boost_cont_malloc(sizeof(POD)*num_elements*3/2);
         capacity = boost_cont_size(addr)/sizeof(POD);
         boost_cont_free(first_mem);
         ++numalloc;

         try{
            boost_cont_command_ret_t ret;
            for(size_t e = capacity + 1; e < num_elements; ++e){
               size_t received_size;
               size_t min = (capacity+1)*sizeof(POD);
               size_t max = (capacity*3/2)*sizeof(POD);
               if(min > max)
                  max = min;
               ret = boost_cont_allocation_command
                  ( m_mode, sizeof(POD)
                  , min, max, &received_size, addr);
               if(!ret.first){
                  std::cout << "(!ret.first)!" << std::endl;
                  throw int(0);
               }
               if(!ret.second){
                  assert(m_mode == BOOST_CONTAINER_ALLOCATE_NEW);
                  if(m_mode != BOOST_CONTAINER_ALLOCATE_NEW){
                     std::cout << "m_mode != BOOST_CONTAINER_ALLOCATE_NEW!" << std::endl;
                     return;
                  }
                  boost_cont_free(addr);
                  addr = ret.first;
                  ++numalloc;
               }
               else{
                  assert(m_mode != BOOST_CONTAINER_ALLOCATE_NEW);
                  if(m_mode == BOOST_CONTAINER_ALLOCATE_NEW){
                     std::cout << "m_mode == BOOST_CONTAINER_ALLOCATE_NEW!" << std::endl;
                     return;
                  }
                  ++numexpand;
               }
               capacity = received_size/sizeof(POD);
               addr = ret.first;
               e = capacity + 1;
            }
            boost_cont_free(addr);
         }
         catch(...){
            boost_cont_free(addr);
            throw;
         }
      }

      assert( boost_cont_allocated_memory() == 0);
      if(boost_cont_allocated_memory()!= 0){
         std::cout << "Memory leak!" << std::endl;
         return;
      }

      timer.stop();
      nanosecond_type nseconds = timer.elapsed().wall;

      std::cout   << "  Malloc type:               " << malloc_name
                  << std::endl
                  << "  allocation ns:             "
                  << float(nseconds)/(num_iterations*num_elements)
                  << std::endl
                  << "  capacity  -  alloc calls (new/expand):  "
                     << (unsigned int)capacity << "  -  "
                     << (float(numalloc) + float(numexpand))/num_iterations
                     << "(" << float(numalloc)/num_iterations << "/" << float(numexpand)/num_iterations << ")"
                  << std::endl << std::endl;
      boost_cont_trim(0);
   }
}

template<unsigned N>
struct char_holder
{
   char ints_[N];
};

template<class POD>
int allocation_loop()
{
   std::cout   << std::endl
               << "-------------------------------------------\n"
               << "-------------------------------------------\n"
               << "  Type(sizeof):              " << typeid(POD).name() << " (" << sizeof(POD) << ")\n"
               << "-------------------------------------------\n"
               << "-------------------------------------------\n"
               << std::endl;

   #define SINGLE_TEST
   #ifndef SINGLE_TEST
      #ifdef NDEBUG
      unsigned int numrep [] = { /*10000, */100000, 1000000, 10000000 };
      #else
      unsigned int numrep [] = { /*10000, */10000, 100000, 1000000 };
      #endif
      unsigned int numele [] = { /*10000,  */1000,    100,      10 };
   #else
      #ifdef NDEBUG
      unsigned int numrep [] = { 500000 };
      #else
      unsigned int numrep [] = { 50000 };
      #endif
      unsigned int numele [] = { 100 };
   #endif

   for(unsigned int i = 0; i < sizeof(numele)/sizeof(numele[0]); ++i){
      allocation_timing_test<POD>(numrep[i], numele[i]);
   }

   return 0;
}

int main()
{
   boost_cont_mallopt( (-3)//M_MMAP_THRESHOLD
             , 100*10000000);
   //allocation_loop<char_holder<4> >();
   //allocation_loop<char_holder<6> >();
   allocation_loop<char_holder<8> >();
   allocation_loop<char_holder<12> >();
   //allocation_loop<char_holder<14> >();
   allocation_loop<char_holder<24> >();
   return 0;
}
