# coding: utf-8
"""
Tests for the base Stores
"""
import os
import unittest
import numpy as np
import mongomock.collection
import pymongo.collection
import numpy.testing.utils as nptu
from maggma.stores import *

module_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
db_dir = os.path.abspath(os.path.join(module_dir, "..", "..", "test_files", "settings_files"))
test_dir = os.path.abspath(os.path.join(module_dir, "..", "..", "test_files", "test_set"))


class TestMongoStore(unittest.TestCase):
    def setUp(self):
        self.mongostore = MongoStore("maggma_test", "test")
        self.mongostore.connect()

    def test_connect(self):
        mongostore = MongoStore("maggma_test", "test")
        with self.assertRaises(Exception):
            mongostore.collection
        mongostore.connect()
        self.assertIsInstance(mongostore.collection, pymongo.collection.Collection)

    def test_query(self):
        self.mongostore.collection.insert({"a": 1, "b": 2, "c": 3})
        self.assertEqual(self.mongostore.query_one(properties=["a"])["a"], 1)
        self.assertEqual(self.mongostore.query_one(properties=["a"])['a'], 1)
        self.assertEqual(self.mongostore.query_one(properties=["b"])['b'], 2)
        self.assertEqual(self.mongostore.query_one(properties=["c"])['c'], 3)

    def test_distinct(self):
        self.mongostore.collection.insert({"a": 1, "b": 2, "c": 3})
        self.mongostore.collection.insert({"a": 4, "d": 5, "e": 6, "g": {"h": 1}})
        self.assertEqual(self.mongostore.distinct("a"), [1, 4])

        # Test list distinct functionality
        self.mongostore.collection.insert({"a": 4, "d": 6, "e": 7})
        self.mongostore.collection.insert({"a": 4, "d": 6, "g": {"h": 2}})
        ad_distinct = self.mongostore.distinct(["a", "d"])
        self.assertTrue(len(ad_distinct), 3)
        self.assertTrue({"a": 4, "d": 6} in ad_distinct)
        self.assertTrue({"a": 1} in ad_distinct)
        self.assertEqual(len(self.mongostore.distinct(["d", "e"], {"a": 4})), 3)
        all_exist = self.mongostore.distinct(["a", "b"], all_exist=True)
        self.assertEqual(len(all_exist), 1)
        all_exist2 = self.mongostore.distinct(["a", "e"], all_exist=True, criteria={"d": 6})
        self.assertEqual(len(all_exist2), 1)

        # Test distinct subdocument functionality
        ghs = self.mongostore.distinct("g.h")
        self.assertEqual(set(ghs), {1, 2})
        ghs_ds = self.mongostore.distinct(["d", "g.h"], all_exist=True)
        self.assertEqual({s['g']['h'] for s in ghs_ds}, {1, 2})
        self.assertEqual({s['d'] for s in ghs_ds}, {5, 6})

    def test_update(self):
        self.mongostore.update([{"e": 6, "d": 4}], key="e")
        self.assertEqual(self.mongostore.query(criteria={"d": {"$exists": 1}}, properties=["d"])[0]["d"], 4)

        self.mongostore.update([{"e": 7, "d": 8, "f": 9}], key=["d", "f"])
        self.assertEqual(self.mongostore.query_one(criteria={"d": 8, "f": 9}, properties=["e"])["e"], 7)
        self.mongostore.update([{"e": 11, "d": 8, "f": 9}], key=["d", "f"])
        self.assertEqual(self.mongostore.query_one(criteria={"d": 8, "f": 9}, properties=["e"])["e"], 11)

    def test_groupby(self):
        self.mongostore.collection.drop()
        self.mongostore.update([{
            "e": 7,
            "d": 9,
            "f": 9
        }, {
            "e": 7,
            "d": 9,
            "f": 10
        }, {
            "e": 8,
            "d": 9,
            "f": 11
        }, {
            "e": 9,
            "d": 10,
            "f": 12
        }],
                               key="f")
        data = list(self.mongostore.groupby("d"))
        self.assertEqual(len(data), 2)
        grouped_by_9 = [g['docs'] for g in data if g['_id']['d'] == 9][0]
        self.assertEqual(len(grouped_by_9), 3)
        grouped_by_10 = [g['docs'] for g in data if g['_id']['d'] == 10][0]
        self.assertEqual(len(grouped_by_10), 1)

        data = list(self.mongostore.groupby(["e", "d"]))
        self.assertEqual(len(data), 3)

    def test_from_db_file(self):
        ms = MongoStore.from_db_file(os.path.join(db_dir, "db.json"))
        self.assertEqual(ms.collection_name, "tmp")

    def test_from_collection(self):
        ms = MongoStore.from_db_file(os.path.join(db_dir, "db.json"))
        ms.connect()

        other_ms = MongoStore.from_collection(ms._collection)
        self.assertEqual(ms.collection_name, other_ms.collection_name)
        self.assertEqual(ms.database, other_ms.database)

    def test_last_updated(self):
        self.assertEqual(self.mongostore.last_updated, datetime.min)
        tic = datetime.now()
        self.mongostore.collection.insert_one({self.mongostore.key: 1, "a": 1})
        with self.assertRaises(StoreError) as cm:
            self.mongostore.last_updated
        self.assertIn(self.mongostore.lu_field, str(cm.exception))
        self.mongostore.update([{self.mongostore.key: 1, "a": 1}])
        self.assertGreaterEqual(self.mongostore.last_updated, tic)

    def test_updated_keys(self):
        target = MongoStore("maggma_test", "test_target")
        target.connect()

        docs = []
        for i in range(10):
            docs.append({self.mongostore.key: i})

        # Insert docs in source
        self.mongostore.update(docs)
        # Make copy in target
        update_docs = list(self.mongostore.query())
        for d in update_docs:
            del d["_id"]
        target.update(update_docs, update_lu=False)

        # Update docs in source
        self.mongostore.collection.drop()
        self.mongostore.update(docs)

        self.assertEqual(len(target.updated_keys(self.mongostore)), 10)
        self.assertEqual(len(self.mongostore.updated_keys(target)), 0)

        target.collection.drop()

    def tearDown(self):
        try:
            self.mongostore.collection.drop()
        except:
            pass


class TestMemoryStore(unittest.TestCase):
    def setUp(self):
        self.memstore = MemoryStore()

    def test(self):
        with self.assertRaises(Exception):
            self.memstore.collection
        self.memstore.connect()
        self.assertIsInstance(self.memstore.collection, mongomock.collection.Collection)

    def test_groupby(self):
        self.memstore.connect()
        self.memstore.update([{
            "e": 7,
            "d": 9,
            "f": 9
        }, {
            "e": 7,
            "d": 9,
            "f": 10
        }, {
            "e": 8,
            "d": 9,
            "f": 11
        }, {
            "e": 9,
            "d": 10,
            "f": 12
        }],
                             key="f")
        data = list(self.memstore.groupby("d"))
        self.assertEqual(len(data), 2)
        grouped_by_9 = [g['docs'] for g in data if g['_id']['d'] == 9][0]
        self.assertEqual(len(grouped_by_9), 3)
        grouped_by_10 = [g['docs'] for g in data if g['_id']['d'] == 10][0]
        self.assertEqual(len(grouped_by_10), 1)

        data = list(self.memstore.groupby(["e", "d"]))
        self.assertEqual(len(data), 3)


class TestJsonStore(unittest.TestCase):
    def test(self):
        files = []
        for f in ["a.json", "b.json"]:
            files.append(os.path.join(test_dir, f))

        jsonstore = JSONStore(files)
        jsonstore.connect()
        self.assertEqual(len(list(jsonstore.query())), 20)

        jsonstore = JSONStore(os.path.join(test_dir, "c.json.gz"))
        jsonstore.connect()
        self.assertEqual(len(list(jsonstore.query())), 20)


class TestGridFSStore(unittest.TestCase):
    def setUp(self):
        self.gStore = GridFSStore("maggma_test", "test", key="task_id")
        self.gStore.connect()

    def test_update(self):
        data1 = np.random.rand(256)
        data2 = np.random.rand(256)
        # Test metadata storage
        self.gStore.update([{"task_id": "mp-1", "data": data1}])
        self.assertTrue(self.gStore._files_collection.find_one({"metadata.task_id": "mp-1"}))

        # Test storing data
        self.gStore.update([{"task_id": "mp-1", "data": data2}])
        self.assertEqual(len(list(self.gStore.query({"task_id": "mp-1"}))), 1)
        self.assertTrue("task_id" in self.gStore.query_one({"task_id": "mp-1"}))
        nptu.assert_almost_equal(self.gStore.query_one({"task_id": "mp-1"})["data"], data2, 7)

        # Test storing compressed data
        self.gStore = GridFSStore("maggma_test", "test", key="task_id", compression=True)
        self.gStore.connect()
        self.gStore.update([{"task_id": "mp-1", "data": data1}])
        self.assertTrue(self.gStore._files_collection.find_one({"metadata.compression": "zlib"}))
        nptu.assert_almost_equal(self.gStore.query_one({"task_id": "mp-1"})["data"], data1, 7)

    def test_query(self):
        data1 = np.random.rand(256)
        data2 = np.random.rand(256)
        tic = datetime(2018, 4, 12, 16)
        self.gStore.update([{"task_id": "mp-1", "data": data1}])
        self.gStore.update([{"task_id": "mp-2", "data": data2, self.gStore.lu_field: tic}], update_lu=False)

        doc = self.gStore.query_one(criteria={"task_id": "mp-1"})
        nptu.assert_almost_equal(doc["data"], data1, 7)

        doc = self.gStore.query_one(criteria={"task_id": "mp-2"})
        nptu.assert_almost_equal(doc["data"], data2, 7)
        self.assertTrue(self.gStore.lu_field in doc)

        self.assertEqual(self.gStore.query_one(criteria={"task_id": "mp-3"}), None)

    @unittest.skip
    def test_distinct(self):
        # TODO
        pass

    def tearDown(self):
        if self.gStore.collection:
            self.gStore._files_collection.drop()
            self.gStore._chunks_collection.drop()


if __name__ == "__main__":
    unittest.main()
