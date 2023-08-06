# coding:utf-8

from tweb.license import License
import config

max_lic_text = 'app:11;;|member:1111;;|org:111111111;30;'


class Identity(License):
    profiles = {
        'org': {
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
        'member': {
            'switch': [
                "create",
                "read",
                "update",
                "remove"
            ]
        },
        'app': {
            'switch': [
                "create",
                "remove"
            ]
        }
    }

    display = {
        'zh': {
            'org': '组织管理',
            'org.switch': '权限开关',
            'org.switch.create': '创建',
            'org.switch.read': '读取',
            'org.switch.update': '更新',
            'org.switch.remove': '删除',
            'org.switch.submit': '提交',
            'org.switch.audit': '审核',
            'org.switch.reject': '驳回',
            'org.switch.activate': '激活',
            'org.switch.deactivate': '去激活',
            'org.number': '数量限制',
            'org.number.visible_level': '可见级别',
            'member': '成员管理',
            'member.switch': '权限开关',
            'member.switch.create': '添加',
            'member.switch.read': '读取',
            'member.switch.update': '更新',
            'member.switch.remove': '移除',
            'app': '应用管理',
            'app.switch': '权限开关',
            'app.switch.create': '创建',
            'app.switch.remove': '移除',
        },
        'en': {
            'org': 'Organization',
            'org.switch': 'Switches',
            'org.switch.create': 'Create',
            'org.switch.read': 'Read',
            'org.switch.update': 'Update',
            'org.switch.remove': 'Remove',
            'org.switch.submit': 'Submit',
            'org.switch.audit': 'Audit',
            'org.switch.reject': 'Rejecg',
            'org.switch.activate': 'Activate',
            'org.switch.deactivate': 'Deactivate',
            'org.number': 'Number Limit',
            'org.number.visible_level': 'Visible Lever',
            'member': 'Member Manage',
            'member.switch': 'Switches',
            'member.switch.create': 'Add',
            'member.switch.read': 'Read',
            'member.switch.update': 'Update',
            'member.switch.remove': 'Remove',
            'app': 'App Manage',
            'app.switch': 'Switches',
            'app.switch.create': 'Create',
            'app.switch.remove': 'Delete',
        }
    }

    def __init__(self):
        super(Identity, self).__init__(self.profiles, self.display,
                                       authority=config.PLATFORM, secret=config.TornadoSettings['cookie_secret'])
