import pickle
import redis

from mysite.config import MyConfig

instanceRedis = redis.StrictRedis(host=MyConfig.Redis.HOST, port=MyConfig.Redis.PORT, db=0)

class KeyGroupName():
    ROOM = "app:qq:room:" # Strings型
    ANSERERS = "app:qq:answerers:" # Hash型 key名はroom_idをつける。

class KVS:

    @staticmethod
    def get_obj(key):
        """
            Python Objectをget
        """
        bin = instanceRedis.get(key)
        obj = None
        if bin is not None:
            obj = pickle.loads(bin)
        return obj
    
    @staticmethod
    def get_hash_obj(key):
        """
            Python ObjectのHashをget
        """
        bin_dict = instanceRedis.hgetall(key)
        obj_dict = {}
        for b_id, b_obj in bin_dict.items():
            obj_dict[b_id.decode()] = pickle.loads(b_obj)
        
        return dict(sorted(obj_dict.items(), key=lambda x:x[0]))
        
    
    @staticmethod
    def set_obj(key, obj):
        """
            Python Objectをset
        """
        bin = pickle.dumps(obj)
        instanceRedis.set(key, bin)
        return

    @staticmethod
    def set_sw_obj(keys, obj):
        """
            指定したキーのうち、どこか(somewhere)にsetする。
            setできたkeyを返す。
            setできなかったらNone返す。
        """
        bin = pickle.dumps(obj)

        for key in keys:
            is_ok = instanceRedis.setnx(key, bin)
            if is_ok:
                return key
        return None
    
    @staticmethod
    def set_hash_obj(key, hkey, obj):
        """
            Python ObjectをHashにset
        """
        bin = pickle.dumps(obj)
        instanceRedis.hset(key, hkey, bin)
        return

    @staticmethod
    def set_hash_sw_obj(key, hkeys, obj):
        """
            指定したHashキーのうち、どこか(somewhere)にsetする。
            setできたHashkeyを返す。
            setできなかったらNone返す。
        """
        bin = pickle.dumps(obj)

        for hkey in hkeys:
            is_ok = instanceRedis.hsetnx(key, hkey, bin)
            if is_ok:
                return hkey
        return None

