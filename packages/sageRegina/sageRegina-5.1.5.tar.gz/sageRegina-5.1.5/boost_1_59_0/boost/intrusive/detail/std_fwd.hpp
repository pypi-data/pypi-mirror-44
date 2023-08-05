//////////////////////////////////////////////////////////////////////////////
//
// (C) Copyright Ion Gaztanaga 2014-2014. Distributed under the Boost
// Software License, Version 1.0. (See accompanying file
// LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
//
// See http://www.boost.org/libs/container for documentation.
//
//////////////////////////////////////////////////////////////////////////////

#ifndef BOOST_INTRUSIVE_DETAIL_STD_FWD_HPP
#define BOOST_INTRUSIVE_DETAIL_STD_FWD_HPP

#ifndef BOOST_CONFIG_HPP
#  include <boost/config.hpp>
#endif

#if defined(BOOST_HAS_PRAGMA_ONCE)
#  pragma once
#endif

//////////////////////////////////////////////////////////////////////////////
//                        Standard predeclarations
//////////////////////////////////////////////////////////////////////////////

#if defined(_LIBCPP_VERSION)
   #define BOOST_INTRUSIVE_CLANG_INLINE_STD_NS
   #pragma GCC diagnostic push
   #if defined(__clang__)
      #pragma GCC diagnostic ignored "-Wc++11-extensions"
   #endif
   #define BOOST_INTRUSIVE_STD_NS_BEG _LIBCPP_BEGIN_NAMESPACE_STD
   #define BOOST_INTRUSIVE_STD_NS_END _LIBCPP_END_NAMESPACE_STD
#elif defined(BOOST_GNU_STDLIB) && defined(_GLIBCXX_BEGIN_NAMESPACE_VERSION)  //GCC >= 4.6
   #define BOOST_INTRUSIVE_STD_NS_BEG namespace std _GLIBCXX_VISIBILITY(default) { _GLIBCXX_BEGIN_NAMESPACE_VERSION 
   #define BOOST_INTRUSIVE_STD_NS_END _GLIBCXX_END_NAMESPACE_VERSION  } // namespace
#elif defined(BOOST_GNU_STDLIB) && defined(_GLIBCXX_BEGIN_NAMESPACE)  //GCC >= 4.2
   #define BOOST_INTRUSIVE_STD_NS_BEG _GLIBCXX_BEGIN_NAMESPACE(std)
   #define BOOST_INTRUSIVE_STD_NS_END _GLIBCXX_END_NAMESPACE
#else
   #define BOOST_INTRUSIVE_STD_NS_BEG namespace std{
   #define BOOST_INTRUSIVE_STD_NS_END }
#endif

BOOST_INTRUSIVE_STD_NS_BEG

template<class T>
struct less;

template<class T>
struct equal_to;

struct input_iterator_tag;
struct forward_iterator_tag;
struct bidirectional_iterator_tag;
struct random_access_iterator_tag;

BOOST_INTRUSIVE_STD_NS_END

#ifdef BOOST_INTRUSIVE_CLANG_INLINE_STD_NS
   #pragma GCC diagnostic pop
   #undef BOOST_INTRUSIVE_CLANG_INLINE_STD_NS
#endif   //BOOST_INTRUSIVE_CLANG_INLINE_STD_NS

#endif //#ifndef BOOST_INTRUSIVE_DETAIL_STD_FWD_HPP
