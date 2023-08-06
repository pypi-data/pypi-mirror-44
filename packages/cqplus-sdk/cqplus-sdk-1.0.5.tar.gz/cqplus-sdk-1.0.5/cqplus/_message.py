#!-*- coding:utf-8 -*-

import cqplus.six as six


class MessageBuilder(object):
    def __init__(self):
        self.items = list()

    def clear(self):
        self.items.clear()

    def __str__(self):
        ''.join(self.items)

    def __unicode__(self):
        u''.join(self.items)

    def to_str(self):
        return six.text_type(self)

    def append_text(self, s):
        assert isinstance(s, six.string_types)
        s = s.replace('&', '&amp;')
        s = s.replace('[', '&#91;')
        s = s.replace(']', '&#93;')
        self.items.append(s)

    def append_cq(self, name, **kw):
        assert isinstance(name, six.string_types)
        assert isinstance(kw, dict)
        p = list()
        p.append('CQ:{}'.format(name))
        for k, v in six.iteritems(kw):
            assert isinstance(k, six.string_types)
            if isinstance(v, six.string_types):
                v = v.replace('&', '&amp;')
                v = v.replace('[', '&#91;')
                v = v.replace(']', '&#93;')
                v = v.replace(',', '&#44;')
                p.append('{}={}'.format(k, v))
        item = '[{}]'.format(','.join(p))
        self.items.append(item)

    def append_face(self, id):
        assert isinstance(id, six.integer_types) and (0 <= id <= 170)
        self.append_cq('face', id=int(id))

    def append_emoji(self, id):
        self.append_cq('emoji', id=id)

    def append_bface(self, id):
        self.append_cq('bface', id=id)

    def append_sface(self, id):
        self.append_cq('sface', id=id)

    def append_image(self, file):
        self.append_cq('image', file=file)

    def append_record(self, file, magic=False):
        self.append_cq('record', file=file, magic=magic)

    def append_at(self, qq):
        self.append_cq('at', qq=qq)

    def append_at_all(self):
        self.append_at('all')

    def append_rps(self):
        self.append_cq('rps')

    def append_dice(self):
        self.append_cq('dice')

    def append_shake(self):
        self.append_cq('shake')

    def append_music(self, type, id):
        self.append_cq('music', type=type, id=id)

    def append_qq_music(self, id):
        self.append_music('qq', id=id)

    def append_163_music(self, id):
        self.append_music('163', id=id)

    def append_xiami_music(self, id):
        self.append_music('xiami', id=id)

    def append_custom_music(self, url, audio, title, content, image):
        self.append_cq('music', type='custom', url=url, audio=audio, title=title, content=content, image=image)

    def append_share(self, url, title, content, image):
        self.append_cq('share', url=url, title=title, content=content, image=image)
