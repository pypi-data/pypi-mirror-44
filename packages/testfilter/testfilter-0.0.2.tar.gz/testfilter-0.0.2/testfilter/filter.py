# -*- coding:utf-8 -*-  
# __auth__ = mocobk
# email: mailmzb@qq.com

TAG_META = '__tag__'
LEVEL_META = '__level__'


def tag(*tag_type):
    """
    指定测试用例环境标签，支持同时设定多个标签，默认Tag.ALL
    :param tag_type: Tag obj
    :return: function
    e.g.
        @tag(Tag.TEST, Tag.PROD)
        def test_method(self):
            pass
    """

    def wrap(func):
        if not hasattr(func, TAG_META):
            tags = {Tag.ALL}
            tags.update(tag_type)
            setattr(func, TAG_META, tags)
        else:
            getattr(func, TAG_META).update(tag_type)
        return func
    return wrap


def level(_level):
    """
    指定测试用例环境标签，支持同时设定多个标签，默认Tag.ALL
    :param _level: Level obj
    :return: function
    e.g.
        @level(Level.P1)
        def test_method(self):
            pass
    """

    def wrap(func):
        if not hasattr(func, LEVEL_META):
            setattr(func, LEVEL_META, _level)
        else:
            __level = getattr(func, LEVEL_META)
            setattr(func, LEVEL_META, min([_level, __level], lambda x: int(x)))
        return func
    return wrap


class NewTag:
    def __init__(self, desc=""):
        self.desc = desc


class NewLevel:
    def __init__(self, value, desc=""):
        self.value = value
        self.desc = desc

    def __int__(self):
        return self.value


class Tag:
    DEV = NewTag('Development')
    TEST = NewTag('Testing')
    UAT = NewTag('User Acceptance Test')
    SIM = NewTag('Simulation')
    PROD = NewTag('Production')
    ALL = NewTag("ALL")

    RUN_TAG = {ALL}
    DEFAULT = {ALL, DEV, TEST, UAT, SIM, PROD}

    @classmethod
    def set_run_tag(cls, *tag_type):
        cls.RUN_TAG = set(tag_type)


class Level:
    SMOKE = NewLevel(10, 'Case Level Smoke')
    P1 = NewLevel(10, 'Case Level P1')
    P2 = NewLevel(20, 'Case Level P2')
    P3 = NewLevel(30, 'Case Level P3')
    P4 = NewLevel(40, 'Case Level P4')

    RUN_LEVEL = P4
    DEFAULT = P1

    @classmethod
    def set_run_level(cls, _level):
        cls.RUN_LEVEL = _level


class Meta(type):
    def __new__(mcs, cls_name, bases, attr_dict: dict):
        items = list(attr_dict)
        run_tag = set(Tag.RUN_TAG)
        run_level = int(Level.RUN_LEVEL)
        skip_tag_reason = '\nThe case tags are not in setting'
        skip_level_reason = '\nThe case level is greater than setting'
        for item in items:
            if item.startswith('test_'):
                if not hasattr(attr_dict[item], TAG_META):
                    setattr(attr_dict[item], TAG_META, Tag.DEFAULT)
                if not getattr(attr_dict[item], TAG_META) & run_tag:
                    setattr(attr_dict[item], '__unittest_skip__', True)
                    skip_reason = getattr(attr_dict[item],
                                          '__unittest_skip_why__', '')
                    setattr(attr_dict[item],
                            '__unittest_skip_why__',
                            (skip_reason + skip_tag_reason).strip())

                if not hasattr(attr_dict[item], LEVEL_META):
                    setattr(attr_dict[item], LEVEL_META, Level.DEFAULT)
                if int(getattr(attr_dict[item], LEVEL_META)) > run_level:
                    setattr(attr_dict[item], '__unittest_skip__', True)
                    skip_reason = getattr(attr_dict[item],
                                          '__unittest_skip_why__', '')
                    setattr(attr_dict[item],
                            '__unittest_skip_why__',
                            (skip_reason + skip_level_reason).strip())

        return super(Meta, mcs).__new__(mcs, cls_name, bases, attr_dict)
