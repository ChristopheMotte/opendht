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

    def test_crypto(self):
        i = dht.Identity.generate("id")
        message = dht.InfoHash.getRandom().toString()
        encrypted = i.publickey.encrypt(message)
        decrypted = i.key.decrypt(encrypted)
        self.assertTrue(message == decrypted)

    def test_crypto_ec(self):
        key = dht.PrivateKey.generateEC()
        cert = dht.Certificate.generate(key, "CA", is_ca=True)
        ca_id = dht.Identity(key, cert)
        self.assertTrue(cert.getId() == key.getPublicKey().getId())
        key2 = dht.PrivateKey.generateEC()
        cert2 = dht.Certificate.generate(key2, "cert", ca_id)
        trust = dht.TrustList()
        trust.add(cert)
        self.assertTrue(trust.verify(cert2))

    def test_trust(self):
        main_id = dht.Identity.generate("id_1")
        sub_id1 = dht.Identity.generate("sid_1", main_id)
        sub_id2 = dht.Identity.generate("sid_2", main_id)
        main_id.certificate.revoke(main_id.key, sub_id2.certificate)
        main_id2 = dht.Identity.generate("id_2")
        trust = dht.TrustList()
        trust.add(main_id.certificate)
        self.assertTrue(trust.verify(main_id.certificate))
        self.assertTrue(trust.verify(sub_id1.certificate))
        self.assertFalse(trust.verify(sub_id2.certificate))
        self.assertFalse(trust.verify(main_id2.certificate))

    # tests a simple put and get between two nodes
    def test_simple_put_and_get(self):
        a = dht.DhtRunner()
        a.run()
        b = dht.DhtRunner()
        b.run()
        b.ping(a.getBound())

        key = dht.InfoHash.get('key')
        value = b'value'
        a.put(key, dht.Value(value))
        #time.sleep(0.0075)
        self.assertEqual(b.get(key)[0].data, value)
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
            self.assertTrue(True)

        a.listen(dht.InfoHash.get('key'), lambda v: cb())

        b.put(dht.InfoHash.get('key'), dht.Value(b"value"))
        #ToDo: add timer to make the test fail after some time. (to be determined)

if __name__ == '__main__':
    unittest.main()
