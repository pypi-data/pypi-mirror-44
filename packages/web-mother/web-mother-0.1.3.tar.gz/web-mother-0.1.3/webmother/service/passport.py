# coding:utf-8

from tweb.license import License
import config
from tweb.error_exception import ErrException, ERROR


class Passport(License):
    profiles = {
        'catalog': {
            'switch': [
                "create",
                "read",
                "update",
                "remove",
                "submit",
                "audit",
                "reject",
                "activate",
                "deactivate"
            ],
            'number': [
                "visible_level"  # 资源可见级别，越大表示可以看到status值更低的资源，取值范围为资源status取值范围，如0～40
            ],
        },
        'grant': {
            'switch': [
                "create",
                "read",
                "update",
                "remove"
            ]
        }
    }

    display = {
        'zh': {
            'catalog': '分类操作',
            'catalog.switch': '权限开关',
            'catalog.switch.create': '创建',
            'catalog.switch.read': '读取',
            'catalog.switch.update': '更新',
            'catalog.switch.remove': '删除',
            'catalog.switch.submit': '提交',
            'catalog.switch.audit': '审核',
            'catalog.switch.reject': '驳回',
            'catalog.switch.activate': '激活',
            'catalog.switch.deactivate': '去激活',
            'catalog.number': '数量限制',
            'catalog.number.visible_level': '可见级别',
            'grant': '授权操作',
            'grant.switch': '权限开关',
            'grant.switch.create': '添加',
            'grant.switch.read': '读取',
            'grant.switch.update': '更新',
            'grant.switch.remove': '移除',
        },
        'en': {
            'catalog': 'Catalog',
            'catalog.switch': 'Switches',
            'catalog.switch.create': 'Create',
            'catalog.switch.read': 'Read',
            'catalog.switch.update': 'Update',
            'catalog.switch.remove': 'Remove',
            'catalog.switch.submit': 'Submit',
            'catalog.switch.audit': 'Audit',
            'catalog.switch.reject': 'Reject',
            'catalog.switch.activate': 'Activate',
            'catalog.switch.deactivate': 'Deactivate',
            'catalog.number': 'Number Limit',
            'catalog.number.visible_level': 'Visible Lever',
            'grant': 'Grant',
            'grant.switch': 'Switches',
            'grant.switch.create': 'Add',
            'grant.switch.read': 'Read',
            'grant.switch.update': 'Update',
            'grant.switch.remove': 'Remove',
        }
    }

    def __init__(self):
        super(Passport, self).__init__(profiles=self.profiles,
                                       authority=config.PLATFORM,
                                       secret=config.TornadoSettings['cookie_secret'])

    @staticmethod
    def add_profile(domain, profile):
        """
        :param domain:
        :param profile: 示例如下

        'catalog': {
            'switches': [
                "sample_sw1",  # 0
                "sample_sw2"
            ],

            # 共6个数值域可用
            'numbers': [
                "sample_num1",
                "sample_num2"
            ],

            # 共4个范围域可用
            'ranges': [
                "sample_range1",
                "sample_range2"
            ]
        }
        :return:
        """
        if domain in Passport.profiles:
            raise ErrException(ERROR.E50000, extra='duplicated about license profile: %s' % domain)

        Passport.profiles[domain] = profile

    @staticmethod
    def add_display(display):
        """
        :param domain:
        :param profile: 示例如下

        'zh': {
            'a': '一',
            'a.b': '1',
        },
        'en': {
            'a': 'One',
            'a.b': 'I',
        }
        :return:
        """
        for k, v in display.items():
            if k not in Passport.display:
                Passport.display[k] = dict()
            for w, d in v.items():
                Passport.display[k][w] = d
