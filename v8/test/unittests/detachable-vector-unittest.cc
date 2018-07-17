// Copyright 2017 the V8 project authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

#include "src/detachable-vector.h"

#include "testing/gtest/include/gtest/gtest.h"

namespace v8 {
namespace internal {

TEST(DetachableVector, ConstructIsEmpty) {
  DetachableVector<int> v;

  size_t empty_size = 0;
  EXPECT_EQ(empty_size, v.size());
  EXPECT_TRUE(v.empty());
}

TEST(DetachableVector, PushAddsElement) {
  DetachableVector<int> v;

  v.push_back(1);

  EXPECT_EQ(1, v.front());
  EXPECT_EQ(1, v.back());
  EXPECT_EQ(1, v.at(0));
  size_t one_size = 1;
  EXPECT_EQ(one_size, v.size());
  EXPECT_FALSE(v.empty());
}

TEST(DetachableVector, AfterFreeIsEmpty) {
  DetachableVector<int> v;

  v.push_back(1);
  v.free();

  size_t empty_size = 0;
  EXPECT_EQ(empty_size, v.size());
  EXPECT_TRUE(v.empty());
}

// This test relies on ASAN to detect leaks and double-frees.
TEST(DetachableVector, DetachLeaksBackingStore) {
  DetachableVector<int> v;
  DetachableVector<int> v2;

  size_t one_size = 1;
  EXPECT_TRUE(v2.empty());

  // Force allocation of the backing store.
  v.push_back(1);
  // Bit-copy the data structure.
  memcpy(&v2, &v, sizeof(DetachableVector<int>));
  // The backing store should be leaked here - free was not called.
  v.detach();

  // We have transferred the backing store to the second vector.
  EXPECT_EQ(one_size, v2.size());
  EXPECT_TRUE(v.empty());

  // The destructor of v2 will release the backing store.
}

}  // namespace internal
}  // namespace v8
