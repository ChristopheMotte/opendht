import unittest
import opendht as dht
import time
import asyncio

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
        del a,b

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
        del a,b

    # test the listen() function
    def test_listen(self):
        a = dht.DhtRunner()
        a.run()
        b = dht.DhtRunner()
        b.run()
        b.ping(a.getBound())

        ok = False
        loop = asyncio.get_event_loop()

        def cb():
            ok = True
            loop.stop()

        a.listen(dht.InfoHash.get('key'), lambda v: cb())

        b.put(dht.InfoHash.get('key'), dht.Value(b"value"))

        loop.run_forever()

        assertTrue(ok)


if __name__ == '__main__':
    unittest.main()
