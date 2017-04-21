import unittest
import opendht as dht
import time

class OpenDhtTester(unittest.TestCase):

    # test that DhtRunner can be instatiated and deleted without throwing
    def test_instance(self):
        for i in range(10):
            r = dht.DhtRunner()
            r.run()
            del r

    # test that bootstraping works (raw address)
    def test_bootstrap(self):
        a = dht.DhtRunner()
        a.run()
        b = dht.DhtRunner()
        b.run()
        self.assertTrue(b.ping(a.getBound()))

    # test a simple put and get between two nodes
    def test_simple_put_and_get(self):
        a = dht.DhtRunner()
        a.run()
        b = dht.DhtRunner()
        b.run()
        b.ping(a.getBound())
        a.put(dht.InfoHash.get('key'), dht.Value(b"value"))
        #time.sleep(0.0075)
        self.assertEqual(b"value", b.get(dht.InfoHash.get('key'))[0].data)


if __name__ == '__main__':
    unittest.main()
